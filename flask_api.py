from flask import Flask, jsonify, request, redirect, render_template, g, url_for, send_file, Response
import json
import glob
from outils_recherche import  Outils_rech
import zipfile
from collections import OrderedDict


app = Flask(__name__)
outils=Outils_rech()
listeFic_cv = []
listeFic_cv_V2 = []



@app.route('/')
def index():
    return jsonify({'status': 'ok'})

@app.route('/cv', methods=['GET'])
def affCVs():

    # pathCv = glob.glob('./cv/*')
    pathCv ={'pathCv':glob.glob('./cv/*')}
    p = pathCv
    ## test fonction cv_toString avec path de glob.glob
    # text =outils.cv_toString(pathCv['pathCv'][0])
    # print(text)

    return render_template('pageCv.html',pathCv = p)


@app.route('/cv', methods=['POST'])
def testMotCles():
   motClef = request.form['motClef']

   tab_motClef = motClef.split()
   print(tab_motClef)
   return jsonify({'motClef':motClef,'tab':tab_motClef})

@app.route('/cv/test',methods=['POST'])
def rechercheDansCV():
    #avec formulaire
    motClef = request.form['motClef']
    #sans formulaire
    # motClef = request.args.get('motClef')
    tab_motClef = motClef.split()
    listeMot = outils.traitement_motClef(tab_motClef)
    pathCv = {'pathCv': glob.glob('./cv/*')}
    res = outils.rechercheDansCvs(listeMot,pathCv['pathCv'])

    return jsonify({'match':res})



@app.route('/cv/recherche',methods=['GET','POST'])
def affResult():
    global listeFic_cv
    listeFic_cv.clear()
    if request.method == 'GET':
       return render_template('rechercheCv.html',dl_display = False)
    else :
        # avec formulaire
        motClef = request.form['motClef']
        # sans formulaire
        # motClef = request.args.get('motClef')
        tab_motClef = motClef.split()
        listeMot = outils.traitement_motClef(tab_motClef)
        pathCv = {'pathCv': glob.glob('./cv/*')}

        res = outils.rechercheDansCvs(listeMot, pathCv['pathCv'])

        listeFic_cv = res
        print(listeFic_cv)

        return render_template('rechercheCv.html', dl_display=True, resultat = res )


@app.route('/cv/rechercheV2',methods=['GET','POST'])
def affResult2():
    global listeFic_cv_V2
    listeFic_cv_V2.clear()
    if request.method == 'GET':
       return render_template('rechercheCv2.html',dl_display = False,afficher_table = True)
    else :
        # avec formulaire
        motClef = request.form['motClef']
        # sans formulaire
        # motClef = request.args.get('motClef')
        tab_motClef = motClef.split()
        listeMot = outils.traitement_motClef(tab_motClef)
        pathCv = {'pathCv': glob.glob('./cv/*')}

        res = outils.rechercheDansCvs_v3(listeMot, pathCv['pathCv'])
        print(res)
        liste_cv=list(res.keys())
        listeFic_cv_V2 = liste_cv

        print(listeFic_cv_V2)

        res2= OrderedDict(sorted(res.items(),key = lambda t:len(t[1]),reverse=True))

        return render_template('rechercheCv2.html', dl_display=True, resultat = res2, afficher_table = True)

######################################################################  download ###########################

@app.route('/cv/dl',methods=['POST'])
def dl_cv():

    zipf = zipfile.ZipFile('Cv.zip', 'w', zipfile.ZIP_DEFLATED)

    for fic in listeFic_cv:
        zipf.write(fic)
        print(fic)

    zipf.close()

    return send_file('Cv.zip',
                     mimetype='zip',
                     attachment_filename='Cv.zip',
                     as_attachment=True)



@app.route('/cv/dl2',methods=['POST'])
def dl_cv_2():

    zipf = zipfile.ZipFile('Cv.zip', 'w', zipfile.ZIP_DEFLATED)

    for fic in listeFic_cv_V2:
        zipf.write(fic)
        print(fic)

    zipf.close()

    return send_file('Cv.zip',
                     mimetype='zip',
                     attachment_filename='Cv.zip',
                     as_attachment=True)


@app.route('/cv/dl_candidat',methods=['POST'])
def dl_cv_candidat():

    zipf = zipfile.ZipFile('Cv_candidat.zip', 'w', zipfile.ZIP_DEFLATED)

    fic=request.form['path']
    zipf.write(fic)
    print(fic)

    zipf.close()

    return send_file('Cv_candidat.zip',
                     mimetype='zip',
                     attachment_filename='Cv_candidat.zip',
                     as_attachment=True)




if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
