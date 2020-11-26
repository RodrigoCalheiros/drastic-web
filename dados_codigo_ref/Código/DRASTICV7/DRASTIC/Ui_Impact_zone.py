from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *

class Ui_Impact_zone(object):
    
    def setupUi(self, Impact_zone_window):
        
        # create Impact_zone window
        Impact_zone_window.setWindowModality(QtCore.Qt.ApplicationModal)
        Impact_zone_window.resize(450,600)
        
        # input file
        # create gridLayout
        self.gridLayout1 = QGridLayout(Impact_zone_window)
        self.gridLayout1.setObjectName("gridLayout1")
        # create label in gridLayout 
        self.label = QLabel(Impact_zone_window)
        self.label.setObjectName("label")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label,0,0,1,1)
        # create select button to input file
        self.selectButton = QPushButton(Impact_zone_window)
        self.selectButton.setObjectName("selectButton")
        self.gridLayout1.addWidget(self.selectButton,0,2,1,1)
        self.inputLayerCombo = QComboBox(Impact_zone_window)
        self.inputLayerCombo.setObjectName("inputLayerCombo")
        self.gridLayout1.addWidget(self.inputLayerCombo, 0,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)       
        
        # define a groupbox to specify the cell size and attribute
        self.groupBox1 = QGroupBox(Impact_zone_window)
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout3 = QGridLayout(self.groupBox1)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox1, 1,0,1,-1)
        # define attribute "Elevation"
        self.labelAttrib = QLabel(Impact_zone_window)
        self.labelAttrib.setObjectName("labelAttrib")
        self.gridLayout3.addWidget(self.labelAttrib,0,0,-1,1)
        self.lineAttrib = QComboBox(Impact_zone_window)
        self.lineAttrib.setObjectName("lineAttrib")
        self.gridLayout3.addWidget(self.lineAttrib,0,1,-1,1)
        # define pixel size
        self.labelPix = QLabel(Impact_zone_window)
        self.labelPix.setObjectName("labelPix")
        self.gridLayout3.addWidget(self.labelPix, 0,3,-1,1)
        self.linePix = QSpinBox()
        self.linePix.setValue(29)
        self.linePix.stepBy(1)
        self.linePix.setObjectName("linePix")
        self.gridLayout3.addWidget(self.linePix,0,4,-1,1)          
        
        # define the indexs
        # create a group box
        self.groupBox = QGroupBox(Impact_zone_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox, 2,0,1,-1)
        # table for classes and indexes
        self.tableWidget = QTableWidget(11,2,Impact_zone_window)
        self.gridLayout2.addWidget(self.tableWidget,0,0,1,1)
        self.newItem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0,self.newItem)
        self.newItem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1,self.newItem)
        # set the description
        self.line = QLineEdit("Confining Layer")
        self.tableWidget.setItem(0,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Silt/Clay")
        self.tableWidget.setItem(1,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Shale")
        self.tableWidget.setItem(2,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Limestone")
        self.tableWidget.setItem(3,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Sandstone")
        self.tableWidget.setItem(4,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Bedded Limestone, Sandstone, Shale")
        self.tableWidget.setItem(5,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Sand and Gravel with significant Silt and Clay")
        self.tableWidget.setItem(6,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Metamorphic/Igneous")
        self.tableWidget.setItem(7,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Sand and Gravel")
        self.tableWidget.setItem(8,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Basalt")
        self.tableWidget.setItem(9,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Karst Limestone")
        self.tableWidget.setItem(10,0,QTableWidgetItem(self.line.text()))
        # set the indexes values
        self.line = QLineEdit("1")
        self.tableWidget.setItem(0,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("3")
        self.tableWidget.setItem(1,1,QTableWidgetItem(self.line.text()))
        self.line =QLineEdit("3")
        self.tableWidget.setItem(2,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("3")
        self.tableWidget.setItem(3,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("6")
        self.tableWidget.setItem(4,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("6")
        self.tableWidget.setItem(5,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("6")
        self.tableWidget.setItem(6,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("4")
        self.tableWidget.setItem(7,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("8")
        self.tableWidget.setItem(8,1,QTableWidgetItem(self.line.text()))
        self.line =QLineEdit("9")
        self.tableWidget.setItem(9,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("10")
        self.tableWidget.setItem(10,1,QTableWidgetItem(self.line.text()))
        # create a box layout to insert the buttons Add and Remove
        self.boxLayout = QVBoxLayout()
        self.boxLayout.setObjectName("boxLayout")
        # button Add
        self.buttonAdd = QPushButton(Impact_zone_window)
        self.buttonAdd.setObjectName("buttonAdd")
        self.boxLayout.addWidget(self.buttonAdd)
        # button Remove
        self.buttonRemove = QPushButton(Impact_zone_window)
        self.buttonRemove.setObjectName("buttonRemove") 
        self.boxLayout.addWidget(self.buttonRemove)
        # attribute table button
        self.buttonAttribute = QPushButton(Impact_zone_window)
        self.buttonAttribute.setObjectName("buttonAttribute")
        self.boxLayout.addWidget(self.buttonAttribute)
        self.gridLayout2.addLayout(self.boxLayout,0,1,-1,1)        
        ## button weight
        #self.labelWeight = .QLabel(Impact_zone_window)
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
        self.label3 = QLabel(Impact_zone_window)
        self.label3.setObjectName("label3")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label3,3,0,1,1)
        # create select button to input file
        self.selectButton3 = QPushButton(Impact_zone_window)
        self.selectButton3.setObjectName("selectButton3")
        self.gridLayout1.addWidget(self.selectButton3,3,2,1,1)
        self.inputLayerCombo3 = QLineEdit(Impact_zone_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")
        self.gridLayout1.addWidget(self.inputLayerCombo3, 3,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)        
        
        # button Ok, Close and Help
        self.buttonBox = QDialogButtonBox(Impact_zone_window)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Help|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 4, 1, 1, 1)           
        
        
        self.retranslateUi(Impact_zone_window)
        self.buttonBox.rejected.connect(Impact_zone_window.close)
                
    def retranslateUi(self, Impact_zone_window):
        Impact_zone_window.setWindowTitle('Impact Vadose Zone (I)')
        self.label.setText('Input file:')
        self.selectButton.setText( 'Browse')
        self.groupBox.setTitle("Ratings")
        self.tableWidget.horizontalHeaderItem(0).setText("Impact Vadose Zone")
        self.tableWidget.horizontalHeaderItem(1).setText("Ratings")
        self.buttonAdd.setText("Add")
        self.buttonRemove.setText( "Remove")
        self.buttonAttribute.setText("Attribute Table")
        self.label3.setText('Output file:')
        self.selectButton3.setText( 'Browse')
        self.labelAttrib.setText('Attribute:')
        self.labelPix.setText('Cell size:')
        #self.labelWeight.setText(.QApplication.translate('Impact Vadose Zone (I)', 'Weight:', None, .QApplication.UnicodeUTF8))