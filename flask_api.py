from flask import Flask, jsonify, request, redirect, render_template, g, url_for, send_file, Response
import json
import glob
from outils_recherche import  Outils_rech
import zipfile

app = Flask(__name__)
outils=Outils_rech()
listeFic_cv = []


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



@app.route('/cv/dl',methods=['POST'])
def dl_cv():

    zipf = zipfile.ZipFile('Name.zip', 'w', zipfile.ZIP_DEFLATED)

    for fic in listeFic_cv:
        zipf.write(fic)
        print(fic)

    zipf.close()

    return send_file('Name.zip',
                     mimetype='zip',
                     attachment_filename='Name.zip',
                     as_attachment=True)




if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
