from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *

class Ui_Topography(object):
    
    def setupUi(self, Topography_window):
        
        # create Topography window
        Topography_window.setWindowModality(QtCore.Qt.ApplicationModal)
        Topography_window.resize(450,400)
        
        # input file contour
        # create gridLayout
        self.gridLayout1 = QGridLayout(Topography_window)
        self.gridLayout1.setObjectName("gridLayout1")
        # create label in gridLayout 
        self.label = QLabel(Topography_window)
        self.label.setObjectName("label")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label,0,0,1,1)
        # create select button to input file
        self.selectButton = QPushButton(Topography_window)
        self.selectButton.setObjectName("selectButton")
        self.gridLayout1.addWidget(self.selectButton,0,2,1,1)
        self.inputLayerCombo = QComboBox(Topography_window)
        self.inputLayerCombo.setObjectName("inputLayerCombo")
        self.gridLayout1.addWidget(self.inputLayerCombo, 0,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)     
        
        # input raster DEM
        # create label in gridLayout 
        self.label_dem = QLabel(Topography_window)
        self.label_dem.setObjectName("label_dem")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label_dem,1,0,1,1)
        # create select button to input file
        self.selectButton_dem = QPushButton(Topography_window)
        self.selectButton_dem.setObjectName("selectButton_dem")
        self.gridLayout1.addWidget(self.selectButton_dem,1,2,1,1)
        self.inputLayerCombo_dem = QComboBox(Topography_window)
        self.inputLayerCombo_dem.setObjectName("inputLayerCombo_dem")
        self.gridLayout1.addWidget(self.inputLayerCombo_dem, 1,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)             
        
        # define a groupbox to specify the cell size and attribute
        self.groupBox1 = QGroupBox(Topography_window)
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout3 = QGridLayout(self.groupBox1)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox1, 2,0,1,-1)
        # define attribute "Elevation"
        self.labelAttrib = QLabel(Topography_window)
        self.labelAttrib.setObjectName("labelAttrib")
        self.gridLayout3.addWidget(self.labelAttrib,0,0,-1,1)
        self.lineAttrib = QComboBox(Topography_window)
        self.lineAttrib.setObjectName("lineAttrib")
        self.gridLayout3.addWidget(self.lineAttrib,0,1,-1,1)
        # define pixel size
        self.labelPix = QLabel(Topography_window)
        self.labelPix.setObjectName("labelPix")
        self.gridLayout3.addWidget(self.labelPix, 0,3,-1,1)
        self.linePix = QSpinBox()
        self.linePix.setValue(29)
        self.linePix.stepBy(1)
        self.linePix.setObjectName("linePix")
        self.gridLayout3.addWidget(self.linePix,0,4,-1,1)         
        
        # define the indexs
        # create a group box
        self.groupBox = QGroupBox(Topography_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox, 3,0,1,-1)
        # table for classes and indexes
        self.tableWidget = QTableWidget(5,3,Topography_window)
        self.gridLayout2.addWidget(self.tableWidget,0,0,1,1)
        self.newItem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0,self.newItem)
        self.newItem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1,self.newItem)
        self.newItem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2,self.newItem)        
        # set the values (intervals)
        self.line = QLineEdit("0")
        self.tableWidget.setItem(0,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("2")
        self.tableWidget.setItem(0,1,QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(1,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("6")
        self.tableWidget.setItem(1,1,QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(2,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("12")
        self.tableWidget.setItem(2,1,QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(3,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("18")
        self.tableWidget.setItem(3,1,QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(4,0,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("200")
        self.tableWidget.setItem(4,1,QTableWidgetItem(self.line.text()))
        # set the indexes values
        self.line = QLineEdit("10")
        self.tableWidget.setItem(0,2,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("9")
        self.tableWidget.setItem(1,2,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("5")
        self.tableWidget.setItem(2,2,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("3")
        self.tableWidget.setItem(3,2,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("1")
        self.tableWidget.setItem(4,2,QTableWidgetItem(self.line.text()))
        # create a box layout to insert the buttons Add and Remove
        self.boxLayout = QVBoxLayout()
        self.boxLayout.setObjectName("boxLayout")
        # button Add
        self.buttonAdd = QPushButton(Topography_window)
        self.buttonAdd.setObjectName("buttonAdd")
        self.boxLayout.addWidget(self.buttonAdd)
        # button Remove
        self.buttonRemove = QPushButton(Topography_window)
        self.buttonRemove.setObjectName("buttonRemove") 
        self.boxLayout.addWidget(self.buttonRemove)
        self.gridLayout2.addLayout(self.boxLayout,0,1,-1,1)
        ## button weight
        #self.labelWeight = .QLabel(Topography_window)
        #self.labelWeight.setObjectName("labelWeight")
        #self.boxLayout.addWidget(self.labelWeight)
        #self.lineWeight = .QSpinBox()
        #self.lineWeight.setValue(0)
        #self.lineWeight.stepBy(1)
        #self.lineWeight.setObjectName("lineWeight")
        #self.boxLayout.addWidget(self.lineWeight)
        self.gridLayout2.addLayout(self.boxLayout,0,1,-1,1)        
        
        # output file
        # create label in gridLayout
        self.label3 = QLabel(Topography_window)
        self.label3.setObjectName("label3")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label3,4,0,1,1)
        # create select button to input file
        self.selectButton3 = QPushButton(Topography_window)
        self.selectButton3.setObjectName("selectButton3")
        self.gridLayout1.addWidget(self.selectButton3,4,2,1,1)
        self.inputLayerCombo3 = QLineEdit(Topography_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")
        self.gridLayout1.addWidget(self.inputLayerCombo3, 4,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)   
        
        # button Ok, Close and Help
        self.buttonBox = QDialogButtonBox(Topography_window)
        #self.buttonBox.setMaximumSize(QtCore.QSize(200, 16777215))
        #self.buttonBox.setBaseSize(QtCore.QSize(110, 0))
        #self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Help|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 5, 1, 1, 1)           
        
        self.retranslateUi(Topography_window)
        self.buttonBox.rejected.connect(Topography_window.close)
                
    def retranslateUi(self, Topography_window):
        Topography_window.setWindowTitle('Topography (T)')
        self.label.setText('Input contour:')
        self.label_dem.setText('Input DEM:')
        self.selectButton.setText( 'Browse')
        self.selectButton_dem.setText( 'Browse')
        self.groupBox.setTitle("Ratings")
        self.tableWidget.horizontalHeaderItem(0).setText("Topography(%)")
        self.tableWidget.horizontalHeaderItem(1).setText("Topography(%)")
        self.tableWidget.horizontalHeaderItem(2).setText("Ratings")
        self.buttonAdd.setText("Add")
        self.buttonRemove.setText( "Remove")
        self.label3.setText('Output file:')
        self.selectButton3.setText( 'Browse')
        #self.labelWeight.setText(.QApplication.translate('Topography (T)', 'Weight:', None, .QApplication.UnicodeUTF8))
        self.labelPix.setText('Cell size:')
        self.labelAttrib.setText( 'Attribute:')