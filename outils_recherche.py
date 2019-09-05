from tika import parser
from ui_cv_interface import Ui_MainWindow
import re


class Outils_rech():

    # Entree : string representant le path du cv
    # Sortie : String contenant le texte du cv en lower case

    def cv_toString(self,cv):
        # cv_path ='cv/'#juste pour les test avec cv dans rep
        raw = parser.from_file(cv)
        cv_text = raw['content']
        cv_text = cv_text.lower()
        return cv_text

    # Entree : list : string => de mot clef
    # Sortie : retourne List : string contenant les mot clef en lowercase

    def traitement_motClef(self,liste_motClef):

        listMot=[]

        for mot in liste_motClef:
            mot = mot.lower()
            listMot.append(mot)

        return listMot


    # entree : mot clef :liste de mot clef a rechercher List[string],
    #                cv : string représentant nom du fichier(cv)
    # sortie: Booleen retourne true si les mot clef sont trouvé false sinon

    def est_dans_Cv(self,liste_motClef,cv):

        trouver = False
        text = self.cv_toString(cv)

        mot_clefs= self.traitement_motClef(liste_motClef)
        print(mot_clefs)

        for mot in mot_clefs:


               if len(mot) == 1  :

                   mot=' '+mot+' '


                   if text.find(mot) > -1:
                       trouver = True

               elif text.find(mot) > -1:
                   trouver = True

        return trouver

    ## V2 petite amelioration recherche mot
    def est_dans_Cv_v2(self, liste_motClef, cv):

        trouver = False
        text = self.cv_toString(cv)

        mot_clefs = self.traitement_motClef(liste_motClef)

        for mot in mot_clefs:
           motEscape = re.escape(mot)
           if re.search(r'\W{}\W'.format(motEscape),text) != None:
               trouver = True

        return trouver

    ## V3 sortie: Booleen retourne true si les mot clef sont trouvé false sinon
     #            liste des mot clef trouve List[String]

    def est_dans_Cv_v3(self, liste_motClef, cv):

        motClef_trouver = []

        trouver = False
        text = self.cv_toString(cv)

        mot_clefs = self.traitement_motClef(liste_motClef)

        for mot in mot_clefs:
           motEscape = re.escape(mot)
           if re.search(r'\W{}\W'.format(motEscape),text) != None:
               trouver = True
               motClef_trouver.append(mot)

        return trouver,motClef_trouver
################################################################################

    ##
    #entree :   liste des motClef list[string]
    #           liste des path de cv list[string]
    #Sortie : liste des cv selectionnee list[string]
    #

    def rechercheDansCvs(self,liste_motClef,liste_cv):

        cv_match=[]

        for cv in liste_cv :

            if self.est_dans_Cv_v2(liste_motClef,cv):
                cv_match.append(cv)
        return cv_match

    ##
    # entree :   liste des motClef list[string]
    #           liste des path de cv list[string]
    # Sortie : liste des cv selectionnee list[string]
    #
    def rechercheDansCvs_v2(self,liste_motClef,liste_cv):

        cv_match=[]


        for cv in liste_cv :
            trouver = self.est_dans_Cv_v2(liste_motClef,cv)
            if trouver:
                cv_match.append(cv)

        return cv_match

    ##
    # entree :   liste des motClef list[string]
    #           liste des path de cv list[string]
    # Sortie : dictionaire des cv selectionnee avec une liste des mot clef list[string]
    #
    def rechercheDansCvs_v3(self, liste_motClef, liste_cv):

        cv_match = {}
        mot_clef_trouver=[]

        for cv in liste_cv:
            trouver,mot_clef_trouver = self.est_dans_Cv_v3(liste_motClef, cv)
            if trouver:
                cv_match.update({cv : mot_clef_trouver})

        return cv_match