from qgis.PyQt import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *

class Ui_Drastic_window(object):
    def setupUi(self, Window):
        
        # create main window
        Window.setWindowModality(QtCore.Qt.ApplicationModal)
        Window.resize(1000,600)        
       
        
        # create menubar with File, DRASTIC and Help sections
        Window.menuBar = QMenuBar()
        Window.menuFile = QMenu("File", self)
        Window.menuDrastic = QMenu("DRASTIC", self)
        Window.menuGod = QMenu("GOD", self)
        Window.menuSI = QMenu("Susceptibility Index", self)
        Window.menuSINTACS = QMenu("SINTACS", self)
        Window.menuAnalysis = QMenu("Comparative Analysis", self)
        Window.menuStats = QMenu("Map Statistics", self)
        Window.menuSimb = QMenu("Apply Symbology", self)
        Window.menuHelp = QMenu("Help", self)
        Window.setMenuBar(Window.menuBar)
                
    
        self.retranslateUi(Window)
        #QtCore.QMetaObject.connectSlotsByName(Window)
        
        Window.show()
    
    def retranslateUi(self, Window):
        Window.setWindowTitle("GVTool")
        
    