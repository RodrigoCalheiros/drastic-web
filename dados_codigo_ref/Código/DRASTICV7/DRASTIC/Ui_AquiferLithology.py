from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *

class Ui_AquiferLithology(object):
    
    def setupUi(self, Aquifer_window):
        
        # create Aquifer window
        Aquifer_window.setWindowModality(QtCore.Qt.ApplicationModal)
        Aquifer_window.resize(450,500)
        
        # input file
        # create gridLayout
        self.gridLayout1 = QGridLayout(Aquifer_window)
        self.gridLayout1.setObjectName("gridLayout1")
        # create label in gridLayout 
        self.label = QLabel(Aquifer_window)
        self.label.setObjectName("label")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label,0,0,1,1)
        # create select button to input file
        self.selectButton = QPushButton(Aquifer_window)
        self.selectButton.setObjectName("selectButton")
        self.gridLayout1.addWidget(self.selectButton,0,2,1,1)
        self.inputLayerCombo = QComboBox(Aquifer_window)
        self.inputLayerCombo.setObjectName("inputLayerCombo")
        self.gridLayout1.addWidget(self.inputLayerCombo, 0,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)       
        
        # define a groupbox to specify the cell size and attribute
        self.groupBox1 = QGroupBox(Aquifer_window)
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout3 = QGridLayout(self.groupBox1)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox1, 1,0,1,-1)
        # define attribute "Elevation"
        self.labelAttrib = QLabel(Aquifer_window)
        self.labelAttrib.setObjectName("labelAttrib")
        self.gridLayout3.addWidget(self.labelAttrib,0,0,-1,1)
        self.lineAttrib = QComboBox(Aquifer_window)
        self.lineAttrib.setObjectName("lineAttrib")
        self.gridLayout3.addWidget(self.lineAttrib,0,1,-1,1)
        # define pixel size
        self.labelPix = QLabel(Aquifer_window)
        self.labelPix.setObjectName("labelPix")
        self.gridLayout3.addWidget(self.labelPix, 0,3,-1,1)
        self.linePix = QSpinBox()
        self.linePix.setValue(29)
        self.linePix.stepBy(1)
        self.linePix.setObjectName("linePix")
        self.gridLayout3.addWidget(self.linePix,0,4,-1,1)            
        
        # define the indexs
        # create a group box
        self.groupBox = QGroupBox(Aquifer_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox, 2,0,1,-1)
        # table for classes and indexes
        self.tableWidget = QTableWidget(10,2,Aquifer_window)
        self.gridLayout2.addWidget(self.tableWidget,0,0,1,1)
        self.newItem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0,self.newItem)
        self.newItem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1,self.newItem)      
        # set the description
        self.line = QLineEdit("Massive Shale")
        self.tableWidget.setItem(0,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Metamorphic/Igneous")
        self.tableWidget.setItem(1,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Weathered Metamorphic/Igneous")
        self.tableWidget.setItem(2,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Glacial Till")
        self.tableWidget.setItem(3,0,QTableWidgetItem(self.line.text()))        
        self.line = QLineEdit("Bedded Sanstone, Limestone and Shale Sequences")
        self.tableWidget.setItem(4,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Massive Sandstone")
        self.tableWidget.setItem(5,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Massive Limestone")
        self.tableWidget.setItem(6,0,QTableWidgetItem(self.line.text())) 
        self.line = QLineEdit("Sand and Gravel")
        self.tableWidget.setItem(7,0,QTableWidgetItem(self.line.text())) 
        self.line = QLineEdit("Basalt")
        self.tableWidget.setItem(8,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Karst Limestone")
        self.tableWidget.setItem(9,0,QTableWidgetItem(self.line.text()))        
        # set the indexes values
        self.line = QLineEdit("2")
        self.tableWidget.setItem(0,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("3")
        self.tableWidget.setItem(1,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("4")
        self.tableWidget.setItem(2,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("5")        
        self.tableWidget.setItem(3,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("6")
        self.tableWidget.setItem(4,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("6")
        self.tableWidget.setItem(5,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("6")
        self.tableWidget.setItem(6,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("8")
        self.tableWidget.setItem(7,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("9")
        self.tableWidget.setItem(8,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("10")
        self.tableWidget.setItem(9,1,QTableWidgetItem(self.line.text()))        
        # create a box layout to insert the buttons Add and Remove
        self.boxLayout = QVBoxLayout()
        self.boxLayout.setObjectName("boxLayout")
        # button Add
        self.buttonAdd = QPushButton(Aquifer_window)
        self.buttonAdd.setObjectName("buttonAdd")
        self.boxLayout.addWidget(self.buttonAdd)
        # button Remove
        self.buttonRemove = QPushButton(Aquifer_window)
        self.buttonRemove.setObjectName("buttonRemove") 
        self.boxLayout.addWidget(self.buttonRemove)
        # attribute table button
        self.buttonAttribute = QPushButton(Aquifer_window)
        self.buttonAttribute.setObjectName("buttonAttribute")
        self.boxLayout.addWidget(self.buttonAttribute)
        self.gridLayout2.addLayout(self.boxLayout,0,1,-1,1)
        ## button weight
        #self.labelWeight = QLabel(Aquifer_window)
        #self.labelWeight.setObjectName("labelWeight")
        #self.boxLayout.addWidget(self.labelWeight)
        #self.lineWeight = QSpinBox()
        #self.lineWeight.setValue(2)
        #self.lineWeight.stepBy(1)
        #self.lineWeight.setObjectName("lineWeight")
        #self.boxLayout.addWidget(self.lineWeight)
        self.gridLayout2.addLayout(self.boxLayout,0,1,-1,1)        
        
        # output file
        # create label in gridLayout
        self.label3 = QLabel(Aquifer_window)
        self.label3.setObjectName("label3")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label3,3,0,1,1)
        # create select button to input file
        self.selectButton3 = QPushButton(Aquifer_window)
        self.selectButton3.setObjectName("selectButton3")
        self.gridLayout1.addWidget(self.selectButton3,3,2,1,1)
        self.inputLayerCombo3 = QLineEdit(Aquifer_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")
        self.gridLayout1.addWidget(self.inputLayerCombo3, 3,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)     
        
        # button Ok, Close and Help
        self.buttonBox = QDialogButtonBox(Aquifer_window)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Help|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 4, 1, 1, 1)           

        self.retranslateUi(Aquifer_window)
        self.buttonBox.rejected.connect(Aquifer_window.close)
                
    def retranslateUi(self, Aquifer_window):
        Aquifer_window.setWindowTitle( 'Aquifer Media (A)')
        self.label.setText( 'Input file:')
        self.selectButton.setText( 'Browse')
        self.groupBox.setTitle("Ratings")
        self.tableWidget.horizontalHeaderItem(0).setText("Aquifer Media")
        self.tableWidget.horizontalHeaderItem(1).setText("Ratings")
        self.buttonAdd.setText( "Add")
        self.buttonRemove.setText( "Remove")
        self.buttonAttribute.setText( "Attribute Table")
        self.label3.setText('Output file:')
        self.selectButton3.setText( 'Browse')
        self.labelAttrib.setText( 'Attribute:')
        self.labelPix.setText('Cell size:')
        #self.labelWeight.setText('Aquifer Media (A)', 'Weight:')