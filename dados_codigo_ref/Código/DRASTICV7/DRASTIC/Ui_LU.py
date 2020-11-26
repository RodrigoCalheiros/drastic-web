from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *

class Ui_LU(object):
    
    def setupUi(self, LU_window):
        
        # create Impact_zone window
        LU_window.setWindowModality(QtCore.Qt.ApplicationModal)
        LU_window.resize(450,600)
        
        # input file
        # create gridLayout
        self.gridLayout1 = QGridLayout(LU_window)
        self.gridLayout1.setObjectName("gridLayout1")
        # create label in gridLayout 
        self.label = QLabel(LU_window)
        self.label.setObjectName("label")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label,0,0,1,1)
        # create select button to input file
        self.selectButton = QPushButton(LU_window)
        self.selectButton.setObjectName("selectButton")
        self.gridLayout1.addWidget(self.selectButton,0,2,1,1)
        self.inputLayerCombo = QComboBox(LU_window)
        self.inputLayerCombo.setObjectName("inputLayerCombo")
        self.gridLayout1.addWidget(self.inputLayerCombo, 0,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)       
        
        # define a groupbox to specify the cell size and attribute
        self.groupBox1 = QGroupBox(LU_window)
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout3 = QGridLayout(self.groupBox1)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox1, 1,0,1,-1)
        # define attribute "Elevation"
        self.labelAttrib = QLabel(LU_window)
        self.labelAttrib.setObjectName("labelAttrib")
        self.gridLayout3.addWidget(self.labelAttrib,0,0,-1,1)
        self.lineAttrib = QComboBox(LU_window)
        self.lineAttrib.setObjectName("lineAttrib")
        self.gridLayout3.addWidget(self.lineAttrib,0,1,-1,1)
        # define pixel size
        self.labelPix = QLabel(LU_window)
        self.labelPix.setObjectName("labelPix")
        self.gridLayout3.addWidget(self.labelPix, 0,3,-1,1)
        self.linePix = QSpinBox()
        self.linePix.setValue(29)
        self.linePix.stepBy(1)
        self.linePix.setObjectName("linePix")
        self.gridLayout3.addWidget(self.linePix,0,4,-1,1)          
        
        # define the indexs
        # create a group box
        self.groupBox = QGroupBox(LU_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox, 2,0,1,-1)
        # table for classes and indexes
        self.tableWidget = QTableWidget(9,2,LU_window)
        self.gridLayout2.addWidget(self.tableWidget,0,0,1,1)
        self.newItem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0,self.newItem)
        self.newItem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1,self.newItem)
        # set the description
        self.line = QLineEdit("Industrial discharge, landfill, mines")
        self.tableWidget.setItem(0,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Irrigation perimeters, paddy fields")
        self.tableWidget.setItem(1,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Quarry, shipyard")
        self.tableWidget.setItem(2,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Continuous urban zones, artificial covered zones, well laid out green zones")
        self.tableWidget.setItem(3,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Permanent cultures (vines, orchards, olive trees, etc)")
        self.tableWidget.setItem(4,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Discontinuous Urban zones")
        self.tableWidget.setItem(5,0,QTableWidgetItem(self.line.text())) 
        self.line = QLineEdit("Pastures and agro-forest zones")
        self.tableWidget.setItem(6,0,QTableWidgetItem(self.line.text())) 
        self.line = QLineEdit("Aquatic milieu (swamps, saline, etc)")
        self.tableWidget.setItem(7,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Forest and semi-natural zones")
        self.tableWidget.setItem(8,0,QTableWidgetItem(self.line.text()))
        # set the indexes values
        self.line = QLineEdit("100")
        self.tableWidget.setItem(0,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("90")
        self.tableWidget.setItem(1,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("80")
        self.tableWidget.setItem(2,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("75")
        self.tableWidget.setItem(3,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("70")
        self.tableWidget.setItem(4,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("70")
        self.tableWidget.setItem(5,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("50")
        self.tableWidget.setItem(6,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("50")
        self.tableWidget.setItem(7,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("0")
        self.tableWidget.setItem(8,1,QTableWidgetItem(self.line.text()))
        # create a box layout to insert the buttons Add and Remove
        self.boxLayout = QVBoxLayout()
        self.boxLayout.setObjectName("boxLayout")
        # button Add
        self.buttonAdd = QPushButton(LU_window)
        self.buttonAdd.setObjectName("buttonAdd")
        self.boxLayout.addWidget(self.buttonAdd)
        # button Remove
        self.buttonRemove = QPushButton(LU_window)
        self.buttonRemove.setObjectName("buttonRemove") 
        self.boxLayout.addWidget(self.buttonRemove)
        # attribute table button
        self.buttonAttribute = QPushButton(LU_window)
        self.buttonAttribute.setObjectName("buttonAttribute")
        self.boxLayout.addWidget(self.buttonAttribute)
        self.gridLayout2.addLayout(self.boxLayout,0,1,-1,1)        
        ## button weight
        #self.labelWeight = QLabel(LU_window)
        #self.labelWeight.setObjectName("labelWeight")
        #self.boxLayout.addWidget(self.labelWeight)
        #self.lineWeight = .QSpinBox()
        #self.lineWeight.setValue(4)
        #self.lineWeight.stepBy(1)
        #self.lineWeight.setObjectName("lineWeight")
        #self.boxLayout.addWidget(self.lineWeight)
        self.gridLayout2.addLayout(self.boxLayout,0,1,-1,1)        
        
        # output file
        # create label in gridLayout
        self.label3 = QLabel(LU_window)
        self.label3.setObjectName("label3")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label3,3,0,1,1)
        # create select button to input file
        self.selectButton3 = QPushButton(LU_window)
        self.selectButton3.setObjectName("selectButton3")
        self.gridLayout1.addWidget(self.selectButton3,3,2,1,1)
        self.inputLayerCombo3 = QLineEdit(LU_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")
        self.gridLayout1.addWidget(self.inputLayerCombo3, 3,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)        
        
        # button Ok, Close and Help
        self.buttonBox = QDialogButtonBox(LU_window)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Help|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 4, 1, 1, 1)           
        
        
        self.retranslateUi(LU_window)
        self.buttonBox.rejected.connect(LU_window.close)
                
    def retranslateUi(self, LU_window):
        LU_window.setWindowTitle( 'Land Use (LU)')
        self.label.setText( 'Input file:')
        self.selectButton.setText( 'Browse')        
        self.groupBox.setTitle( "Ratings")
        self.tableWidget.horizontalHeaderItem(0).setText("Land Use")
        self.tableWidget.horizontalHeaderItem(1).setText("Ratings")
        self.buttonAdd.setText( "Add")
        self.buttonRemove.setText( "Remove") 
        self.buttonAttribute.setText( "Attribute Table")
        self.label3.setText( 'Output file:')
        self.selectButton3.setText( 'Browse')        
        self.labelAttrib.setText( 'Attribute:') 
        self.labelPix.setText( 'Cell size:')    
        #self.labelWeight.setText( 'Weight:')