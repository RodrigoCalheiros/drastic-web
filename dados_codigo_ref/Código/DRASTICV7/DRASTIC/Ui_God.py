from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *

class Ui_God(object):
    
    def setupUi(self, God):
        
        # create Drastic window
        God.setWindowModality(QtCore.Qt.ApplicationModal)
        God.resize(450,400)
        
        # input file
        # create gridLayout
        self.gridLayout1 = QGridLayout(God)
        self.gridLayout1.setObjectName("gridLayout1")
        # group box to input files
        self.groupBox = QGroupBox(God)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox,0,0,1,-1)        
        # create label in gridLayout 
        self.label = QLabel(God)
        self.label.setObjectName("label")  
        self.label2 = QLabel(God)
        self.label2.setObjectName("label2")  
        self.label3 = QLabel(God)
        self.label3.setObjectName("label3")  
               
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout2.addWidget(self.label,0,0,1,1)
        self.gridLayout2.addWidget(self.label2,1,0,1,1)
        self.gridLayout2.addWidget(self.label3,2,0,1,1)
    
        # create select button to input file
        self.selectButton = QPushButton(God)
        self.selectButton.setObjectName("selectButton")
        self.selectButton2 = QPushButton(God)
        self.selectButton2.setObjectName("selectButton2")    
        self.selectButton3 = QPushButton(God)
        self.selectButton3.setObjectName("selectButton3")  
          
        
        # button weight Depth to Groundwater
       
        self.gridLayout2.addWidget(self.selectButton,0,4,1,1)
        
        # button weight Recharge
         
        self.gridLayout2.addWidget(self.selectButton2,1,4,1,1)
        
        # button weight Aquifer
           
        self.gridLayout2.addWidget(self.selectButton3,2,4,1,1)        
        
        
        self.inputLayerCombo = QComboBox(God)
        self.inputLayerCombo.setObjectName("inputLayerCombo")  
        self.inputLayerCombo2 = QComboBox(God)
        self.inputLayerCombo2.setObjectName("inputLayerCombo2")  
        self.inputLayerCombo3 = QComboBox(God)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")  
        
              
        self.gridLayout2.addWidget(self.inputLayerCombo,0,1,1,1)
        self.gridLayout2.addWidget(self.inputLayerCombo2,1,1,1,1)
        self.gridLayout2.addWidget(self.inputLayerCombo3,2,1,1,1)
        #self.gridLayout2.addWidget(self.inputLayerCombo4,3,1,1,1)
      
        # stretch to extend the widget in column 1
        self.gridLayout2.setColumnStretch(1,1)  
        
        # output file
        # group box to output files
        self.groupBox2 = QGroupBox(God)
        self.groupBox2.setObjectName("groupBox2")
        self.gridLayout3 = QGridLayout(self.groupBox2)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox2,1,0,1,-1)        
        # create label in gridLayout
        self.label_out = QLabel(God)
        self.label_out.setObjectName("label_out")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout3.addWidget(self.label_out,0,0,1,1)
        # create select button to output file
        self.selectButton_out = QPushButton(God)
        self.selectButton_out.setObjectName("selectButton_out")
        self.gridLayout3.addWidget(self.selectButton_out,0,2,1,1)
        self.outputLayerCombo = QLineEdit(God)
        self.outputLayerCombo.setObjectName("outputLayerCombo")
        self.gridLayout3.addWidget(self.outputLayerCombo, 0,1,1,1)
        # output color
        # create label in gridLayout
        # self.label_color = QLabel(God)
        # self.label_color.setObjectName("label_color")
        # # define label (QWidget, row, column, QtAlignement)
        # self.gridLayout3.addWidget(self.label_color,2,0,1,1)
        # # create select button to output file
        # self.selectButton_color = QPushButton(God)
        # self.selectButton_color.setObjectName("selectButton_color")
        # self.gridLayout3.addWidget(self.selectButton_color,2,2,1,1)
        # self.outputLayerCombo_color = QLineEdit(God)
        # self.outputLayerCombo_color.setObjectName("outputLayerCombo_color")
        # self.gridLayout3.addWidget(self.outputLayerCombo_color, 2,1,1,1)
        
        # checkbox to define the output
        self.label_checkdrastic = QLabel(God)
        self.label_checkdrastic.setObjectName("label_checkdrastic")
        self.gridLayout3.addWidget(self.label_checkdrastic,1,1,1,1)
        self.checkdrastic = QCheckBox(God)
        self.checkdrastic.setObjectName("checkdrastic")
        self.gridLayout3.addWidget(self.checkdrastic,1,0,1,1)
        
        # self.label_checkcolor = QLabel(God)
        # self.label_checkcolor.setObjectName("label_checkcolor")
        # self.gridLayout3.addWidget(self.label_checkcolor,3,1,1,1)
        # self.checkcolor = QCheckBox(God)
        # self.checkcolor.setObjectName("checkcolor")
        # self.gridLayout3.addWidget(self.checkcolor,3,0,1,1)

    
        # button Ok, Close and Help
        self.buttonBox = QDialogButtonBox(God)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Help|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 2, 1, 1, 1)          
        
        self.retranslateUi(God)
        self.buttonBox.rejected.connect(God.close)
    
    def retranslateUi(self, God):
        God.setWindowTitle( 'GOD')   
        self.label.setText( 'G')
        self.label2.setText( 'O')
        self.label3.setText( 'D')
        self.selectButton.setText( 'Browse')   
        self.selectButton2.setText( 'Browse')
        self.selectButton3.setText( 'Browse')
        self.selectButton_out.setText( 'Browse')
        self.label_out.setText( 'GOD:')
        self.groupBox.setTitle( "Input")
        self.groupBox2.setTitle( "Output")
        #self.selectButton_color.setText( 'Browse')
        #self.label_color.setText( 'GOD COLORED:')
        self.label_checkdrastic.setText( 'Load raster into canvas')
        #self.label_checkcolor.setText( 'Load colored raster into canvas')
       