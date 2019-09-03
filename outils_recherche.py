from tika import parser
from ui_cv_interface import Ui_MainWindow
import re


class Outils_rech():

    def cv_toString(self,cv):
        # cv_path ='cv/'#juste pour les test avec cv dans rep
        raw = parser.from_file(cv)
        cv_text = raw['content']
        cv_text = cv_text.lower()
        return cv_text

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

        for mot in mot_clefs:


               if len(mot) == 1  :

                   mot=' '+mot+' '


                   if text.find(mot) > -1:
                       trouver = True

               elif text.find(mot) > -1:
                   trouver = True

        return trouver

    def est_dans_Cv_v2(self, liste_motClef, cv):

        trouver = False
        text = self.cv_toString(cv)

        mot_clefs = self.traitement_motClef(liste_motClef)

        for mot in mot_clefs:

           if re.search(r'\W{}\W'.format(mot),text) != None:
               trouver = True

        return trouver

    def rechercheDansCvs(self,liste_motClef,liste_cv):

        cv_match=[]

        for cv in liste_cv :

            if self.est_dans_Cv_v2(liste_motClef,cv):
                cv_match.append(cv)
        return cv_match
