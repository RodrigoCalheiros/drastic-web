from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *

class Ui_Depth_groundwater(object):
    
    def setupUi(self, Depth_window):
        
        # create Depth window
        Depth_window.setWindowModality(QtCore.Qt.ApplicationModal)
        Depth_window.resize(400,400)
        
        # input file points
        # create gridLayout
        self.gridLayout1 = QGridLayout(Depth_window)
        self.gridLayout1.setObjectName("gridLayout1")
        # create groupBox method I
        self.groupBox_m1 = QGroupBox(Depth_window)
        self.groupBox_m1.setObjectName("groupBox_m1")
        self.groupBox_m1.setTitle("Base")
        self.gridLayout_m1 = QGridLayout(self.groupBox_m1)
        self.gridLayout_m1.setObjectName("gridLayout_m1")
        self.gridLayout1.addWidget(self.groupBox_m1, 0,0,1,-1)        
        # create label in gridLayout 
        self.label = QLabel(Depth_window)
        self.label.setObjectName("label")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout_m1.addWidget(self.label,0,0,1,1)
        # create select button to input file
        self.selectButton = QPushButton(Depth_window)
        self.selectButton.setObjectName("selectButton")
        self.gridLayout_m1.addWidget(self.selectButton,0,2,1,1)
        self.inputLayerCombo = QComboBox(Depth_window)
        self.inputLayerCombo.setEditable(True)
        self.inputLayerCombo.setObjectName("inputLayerCombo")
        self.gridLayout_m1.addWidget(self.inputLayerCombo, 0,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout_m1.setColumnStretch(1,1)
        
        # field to mask shapefile input
        self.maskLabel = QLabel(Depth_window)
        self.maskLabel.setObjectName("maskLabel")
        self.gridLayout_m1.addWidget(self.maskLabel, 1,0,1,1)
        # create select button to input mask
        self.selectMask = QPushButton(Depth_window)
        self.selectMask.setObjectName("selectMask")
        self.gridLayout_m1.addWidget(self.selectMask, 1,2,1,1)
        self.inputMaskCombo = QComboBox(Depth_window)
        self.inputMaskCombo.setEditable(True)
        self.inputMaskCombo.setObjectName("inputMaskCombo")
        self.gridLayout_m1.addWidget(self.inputMaskCombo, 1,1,1,1)
        # stretch to extend the widget in column1
        self.gridLayout_m1.setColumnStretch(1,1)
        
        # field to interpolation method (the user must to choose)
        self.methodLabel = QLabel(Depth_window)
        self.methodLabel.setObjectName("methodLabel")
        self.gridLayout1.addWidget(self.methodLabel, 2,0,1,1)
        # combobox to choose the method
        self.comboBoxMethod = QComboBox(Depth_window)
        self.comboBoxMethod.setObjectName("comboBoxMethod")
        self.gridLayout1.addWidget(self.comboBoxMethod,2,1,1,-1)
        self.styles = ['Inverse Distance Weighting', 'Kriging', 'Cubic spline approximation (SAGA)', 'Spatial approximation using spline with tension (GRASS)']
        self.comboBoxMethod.addItems(self.styles)
        
        # define a groupbox to specify the cell size and attribute
        self.groupBox1 = QGroupBox(Depth_window)
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout3 = QGridLayout(self.groupBox1)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox1, 1,0,1,-1)
        # define attribute "Elevation"
        self.labelAttrib = QLabel(Depth_window)
        self.labelAttrib.setObjectName("labelAttrib")
        self.gridLayout3.addWidget(self.labelAttrib,0,0,-1,1)
        self.lineAttrib = QComboBox(Depth_window)
        self.lineAttrib.setObjectName("lineAttrib")
        self.gridLayout3.addWidget(self.lineAttrib,0,1,-1,1)
        # define pixel size
        self.labelPix = QLabel(Depth_window)
        self.labelPix.setObjectName("labelPix")
        self.gridLayout3.addWidget(self.labelPix, 0,3,-1,1)
        self.linePix = QSpinBox()
        self.linePix.setValue(29)
        self.linePix.stepBy(1)
        self.linePix.setObjectName("linePix")
        self.gridLayout3.addWidget(self.linePix,0,4,-1,1)     
        
        
        # input file mdt
        # create groupBox method II
        self.groupBox_m2 = QGroupBox(Depth_window)
        self.groupBox_m2.setObjectName("groupBox_m2")
        self.groupBox_m2.setTitle("Improvement")
        self.gridLayout_m2 = QGridLayout(self.groupBox_m2)
        self.gridLayout_m2.setObjectName("gridLayout_m2")
        self.gridLayout1.addWidget(self.groupBox_m2, 3,0,1,-1)            
        # create label 
        self.label_mdt = QLabel(Depth_window)
        self.label_mdt.setObjectName("label_mdt")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout_m2.addWidget(self.label_mdt,0,0,1,1)
        # create select button to input file
        self.selectButton_mdt = QPushButton(Depth_window)
        self.selectButton_mdt.setObjectName("selectButton_mdt")
        self.gridLayout_m2.addWidget(self.selectButton_mdt,0,2,1,1)
        self.inputLayerCombo_mdt = QComboBox(Depth_window)
        self.inputLayerCombo_mdt.setEditable(True)
        self.inputLayerCombo_mdt.setObjectName("inputLayerCombo_mdt")
        self.gridLayout_m2.addWidget(self.inputLayerCombo_mdt, 0,1,1,1)
        self.gridLayout_m2.setColumnStretch(1,1)     
        
        # define a groupbox to specify the maximum depth and distance
        self.groupBox_max = QGroupBox(Depth_window)
        self.groupBox_max.setObjectName("groupBox_max")
        self.gridLayout5 = QGridLayout(self.groupBox_max)
        self.gridLayout5.setObjectName("gridLayout5")
        self.gridLayout1.addWidget(self.groupBox_max, 4,0,1,-1)
        # field to maximum depth
        self.label_max_depth = QLabel(Depth_window)
        self.label_max_depth.setObjectName("label_max_depth")    
        self.gridLayout5.addWidget(self.label_max_depth,0,0,1,1)
        self.line_max = QSpinBox()
        self.line_max.setValue(19)
        self.line_max.stepBy(1)
        self.line_max.setObjectName("line_max")
        self.gridLayout5.addWidget(self.line_max,0,1,1,1)
        # field to distance
        self.label_distance = QLabel(Depth_window)
        self.label_distance.setObjectName("label_distance")    
        self.gridLayout5.addWidget(self.label_distance,0,2,1,1)
        self.line_distance = QSpinBox()
        self.line_distance.setMinimum(10)
        self.line_distance.setMaximum(1000)
        self.line_distance.setValue(199)
        self.line_distance.stepBy(1)
        self.line_distance.setObjectName("line_distance")
        self.gridLayout5.addWidget(self.line_distance,0,3,1,1)    
        # field to define the minimum size of basin
        self.label_size = QLabel(Depth_window)
        self.label_size.setObjectName("label_size")    
        self.gridLayout5.addWidget(self.label_size,0,4,1,1)
        self.line_size = QSpinBox()
        self.line_size.setMinimum(49)
        self.line_size.setMaximum(1000)
        self.line_size.setValue(49)
        self.line_size.stepBy(1)
        self.line_size.setObjectName("line_size")
        self.gridLayout5.addWidget(self.line_size,0,5,1,1)           
        # stretch to extend the widget in column 1
        self.gridLayout5.setColumnStretch(1,1)        
        
        # define the indexs
        # create a group box
        self.groupBox = QGroupBox(Depth_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox, 5,0,1,-1)
        # table for classes and indexes
        self.tableWidget = QTableWidget(7,3,Depth_window)
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
        self.line = QLineEdit("1.5")
        self.tableWidget.setItem(1,0,QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(0,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("4.6")
        self.tableWidget.setItem(2,0,QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(1,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("9.1")
        self.tableWidget.setItem(3,0,QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(2,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("15.2")
        self.tableWidget.setItem(4,0,QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(3,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("22.9")
        self.tableWidget.setItem(5,0,QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(4,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("30.5")
        self.tableWidget.setItem(6,0,QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(5,1,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("200")
        self.tableWidget.setItem(6,1,QTableWidgetItem(self.line.text()))
        # set the indexes values
        self.line = QLineEdit("10")
        self.tableWidget.setItem(0,2,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("9")
        self.tableWidget.setItem(1,2,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("7")
        self.tableWidget.setItem(2,2,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("5")
        self.tableWidget.setItem(3,2,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("3")
        self.tableWidget.setItem(4,2,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("2")
        self.tableWidget.setItem(5,2,QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("1")
        self.tableWidget.setItem(6,2,QTableWidgetItem(self.line.text()))
        # create a box layout to insert the buttons Add and Remove
        self.boxLayout = QVBoxLayout()
        self.boxLayout.setObjectName("boxLayout")
        # button Add
        self.buttonAdd = QPushButton(Depth_window)
        self.buttonAdd.setObjectName("buttonAdd")
        self.boxLayout.addWidget(self.buttonAdd)
        # button Remove
        self.buttonRemove = QPushButton(Depth_window)
        self.buttonRemove.setObjectName("buttonRemove") 
        self.boxLayout.addWidget(self.buttonRemove)
        ## button weight
        #self.labelWeight = QtGui.QLabel(Depth_window)
        #self.labelWeight.setObjectName("labelWeight")
        #self.boxLayout.addWidget(self.labelWeight)
        #self.lineWeight = QtGui.QSpinBox()
        #self.lineWeight.setValue(4)
        #self.lineWeight.stepBy(1)
        #self.lineWeight.setObjectName("lineWeight")
        #self.boxLayout.addWidget(self.lineWeight)
        self.gridLayout2.addLayout(self.boxLayout,0,1,-1,1)
        
        # output file
        # create label in gridLayout
        self.label3 = QLabel(Depth_window)
        self.label3.setObjectName("label3")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label3,6,0,1,1)
        # create select button to input file
        self.selectButton3 = QPushButton(Depth_window)
        self.selectButton3.setObjectName("selectButton3")
        self.gridLayout1.addWidget(self.selectButton3,6,2,1,1)
        self.inputLayerCombo3 = QLineEdit(Depth_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")
        self.gridLayout1.addWidget(self.inputLayerCombo3, 6,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)   
        
        # button Ok, Close and Help
        self.buttonBox = QDialogButtonBox(Depth_window)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Help|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 7, 1, 1, 1)        
        
        self.retranslateUi(Depth_window)
        self.buttonBox.rejected.connect(Depth_window.close)
        
    def retranslateUi(self, Depth_window):
        Depth_window.setWindowTitle('Depth Groundwater (D)')
        self.label.setText('Input file points:')
        self.label_mdt.setText('Input file MDT:')
        self.selectButton.setText('Browse')
        self.selectButton_mdt.setText('Browse')
        self.selectMask.setText('Browse')
        self.methodLabel.setText("Interpolation Method")
        self.maskLabel.setText("Mask:")
        self.groupBox.setTitle("Ratings")
        self.tableWidget.horizontalHeaderItem(0).setText("Depth(m)")
        self.tableWidget.horizontalHeaderItem(1).setText("Depth(m)")
        self.tableWidget.horizontalHeaderItem(2).setText("Ratings")
        self.buttonAdd.setText("Add")
        self.buttonRemove.setText("Remove")
        self.label3.setText('Output file:')
        self.selectButton3.setText('Browse')
        #self.labelWeight.setText(QtGui.QApplication.translate('Depth Groundwater (D)', 'Weight:', None, QtGui.QApplication.UnicodeUTF8))
        self.labelAttrib.setText( 'Attribute:')
        self.labelPix.setText('Cell size:')
        self.label_max_depth.setText('Maximum depth:')
        self.label_distance.setText('Distance:')
        self.label_size.setText('Minimum size of watershed basin:')