import sys
from PySide2.QtWidgets import QApplication, QMainWindow,QFileDialog,QListWidgetItem,QInputDialog
from PySide2.QtCore import QFileInfo
from ui_cv_interface import Ui_MainWindow
from outils_recherche import  Outils_rech
import re

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.f_rech = Outils_rech()
        self.listeCv=[]

    ######## Connection entre interface et fonctionalité ################


        self.ui.pb_ajouter.clicked.connect(self.ajoutCv_liste)
        self.ui.pb_lancer_rech.clicked.connect(self.lancerRecherche)
        self.ui.pb_enlever.clicked.connect(self.enlever_cv)
        self.ui.pb_effacer_liste.clicked.connect(self.effacer_liste)

    ####################### fonction / action interface ####################
    def recup_mot_clef(self):
        ch = self.ui.lineEdit_rech.text()
        tabMotClef = ch.split()
        return tabMotClef

    def ajoutCv_liste(self):

        fileNames = QFileDialog.getOpenFileNames(self, "choix cv", "C:/Users/AELION/Desktop")
        for file in fileNames[0]:
            fInfo = QFileInfo(file)

            fShortName = fInfo.baseName()
            item = QListWidgetItem(fShortName)
            item.setToolTip(file)
            if item.toolTip() not in self.listeCv :

                self.ui.listW_cv_entree.addItem(item)
                self.listeCv.append(file)


    def ajout_cv_sortie(self,fileNames):
        self.ui.listW_cv_sortie.clear()
        for file in fileNames:
            fInfo = QFileInfo(file)
            fShortName = fInfo.baseName()
            item = QListWidgetItem(fShortName)
            self.ui.listW_cv_sortie.addItem(item)
            item.setToolTip(file)

    def enlever_cv(self):
        rowItem = self.ui.listW_cv_entree.currentRow()
        if rowItem != -1:
            self.ui.listW_cv_entree.takeItem(rowItem)

    def lancerRecherche(self):

        print(self.listeCv)
        print(self.recup_mot_clef())
        cv_sortie = self.f_rech.rechercheDansCvs(self.recup_mot_clef(),self.listeCv)
        print(cv_sortie)
        self.ajout_cv_sortie(cv_sortie)

    def effacer_liste(self):
        self.ui.listW_cv_entree.clear()


if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

    # ch = 'ok juste un test'
    # print(ch.split())

    ############################## test rec cv #######################################

    # mesOutil = Outils_rech()
    # mot_clef=['C']
    # liste_Cv=['CV_Colomban_RENIE_Dev_Python_Junior.pdf','CV_Bulent BARRIS_Dev PYTHON Junior.pdf','CV_Coralie_CARRON_Dev PYTHON Junior.pdf','CV NickAndriambahiny_ Dev PYTHON Junior.pdf']
    # res= mesOutil.cv_toString('CV_Colomban_RENIE_Dev_Python_Junior.pdf')
    # cv= 'CV_Colomban_RENIE_Dev_Python_Junior.pdf'
    #
    # res =mesOutil.traitement_motClef(mot_clef)
    #
    # ch = ' ok la la '
    # l=['git']
    #
    # res = ch.find(' a ')
    #
    # res=mesOutil.rechercheDansCvs(mot_clef,liste_Cv)
    #
    #
    # # print(est_dans_Cv(mot_clef,'CV_Coralie_CARRON_Dev PYTHON Junior.pdf'))
    # print(res)

    # print(re.search(r'[^a-zA-Z]{}\W'.format('mot'), 'mot motus'))