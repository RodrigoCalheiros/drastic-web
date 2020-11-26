from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *

class Ui_SI(object):
    
    def setupUi(self, SI_window):
        
        # create SI window
        SI_window.setWindowModality(QtCore.Qt.ApplicationModal)
        SI_window.resize(450,400)
        
        # input file
        # create gridLayout
        self.gridLayout1 = QGridLayout(SI_window)
        self.gridLayout1.setObjectName("gridLayout1")
        # group box to input files
        self.groupBox = QGroupBox(SI_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox,0,0,1,-1)        
        # create label in gridLayout 
        self.label = QLabel(SI_window)
        self.label.setObjectName("label")  
        self.label2 = QLabel(SI_window)
        self.label2.setObjectName("label2")  
        self.label3 = QLabel(SI_window)
        self.label3.setObjectName("label3")    
        self.label5 = QLabel(SI_window)
        self.label5.setObjectName("label5")   
        self.label6 = QLabel(SI_window)
        self.label6.setObjectName("label6")           
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout2.addWidget(self.label,0,0,1,1)
        self.gridLayout2.addWidget(self.label2,1,0,1,1)
        self.gridLayout2.addWidget(self.label3,2,0,1,1)
        self.gridLayout2.addWidget(self.label5,4,0,1,1)
        self.gridLayout2.addWidget(self.label6,5,0,1,1)
        # create select button to input file
        self.selectButton = QPushButton(SI_window)
        self.selectButton.setObjectName("selectButton")
        self.selectButton2 = QPushButton(SI_window)
        self.selectButton2.setObjectName("selectButton2")    
        self.selectButton3 = QPushButton(SI_window)
        self.selectButton3.setObjectName("selectButton3")  
        self.selectButton5 = QPushButton(SI_window)
        self.selectButton5.setObjectName("selectButton5")  
        self.selectButton6 = QPushButton(SI_window)
        self.selectButton6.setObjectName("selectButton6")  
        
        # button weight Depth to Groundwater
        self.labelWeightD = QLabel(SI_window)
        self.labelWeightD.setObjectName("labelWeightD")
        self.gridLayout2.addWidget(self.labelWeightD,0,2,1,1)
        self.lineWeightD = QDoubleSpinBox()
        self.lineWeightD.setValue(0.186)
        self.lineWeightD.stepBy(0.1)
        self.lineWeightD.setObjectName("lineWeightD")
        self.gridLayout2.addWidget(self.lineWeightD,0,3,1,1)        
        self.gridLayout2.addWidget(self.selectButton,0,4,1,1)
        
        # button weight Recharge
        self.labelWeightR = QLabel(SI_window)
        self.labelWeightR.setObjectName("labelWeightR")
        self.gridLayout2.addWidget(self.labelWeightR,1,2,1,1)
        self.lineWeightR = QDoubleSpinBox()
        self.lineWeightR.setValue(0.212)
        self.lineWeightR.stepBy(0.1)
        self.lineWeightR.setObjectName("lineWeightR")
        self.gridLayout2.addWidget(self.lineWeightR,1,3,1,1)        
        self.gridLayout2.addWidget(self.selectButton2,1,4,1,1)
        
        # button weight Aquifer
        self.labelWeightA = QLabel(SI_window)
        self.labelWeightA.setObjectName("labelWeightA")
        self.gridLayout2.addWidget(self.labelWeightA,2,2,1,1)
        self.lineWeightA = QDoubleSpinBox()
        self.lineWeightA.setValue(0.259)
        self.lineWeightA.stepBy(0.1)
        self.lineWeightA.setObjectName("lineWeightA")
        self.gridLayout2.addWidget(self.lineWeightA,2,3,1,1)        
        self.gridLayout2.addWidget(self.selectButton3,2,4,1,1)
        
        # button weight Topography
        self.labelWeightT = QLabel(SI_window)
        self.labelWeightT.setObjectName("labelWeightT")
        self.gridLayout2.addWidget(self.labelWeightT,4,2,1,1)
        self.lineWeightT = QDoubleSpinBox()
        self.lineWeightT.setValue(0.121)
        self.lineWeightT.stepBy(0.1)
        self.lineWeightT.setObjectName("lineWeightT")
        self.gridLayout2.addWidget(self.lineWeightT,4,3,1,1)        
        self.gridLayout2.addWidget(self.selectButton5,4,4,1,1)
        
        # button weight LU
        self.labelWeightLU = QLabel(SI_window)
        self.labelWeightLU.setObjectName("labelWeightI")
        self.gridLayout2.addWidget(self.labelWeightLU,5,2,1,1)
        self.lineWeightLU = QDoubleSpinBox()
        self.lineWeightLU.setValue(0.222)
        self.lineWeightLU.stepBy(0.1)
        self.lineWeightLU.setObjectName("lineWeightI")
        self.gridLayout2.addWidget(self.lineWeightLU,5,3,1,1)
        self.gridLayout2.addWidget(self.selectButton6,5,4,1,1)
   
        
        self.inputLayerCombo = QComboBox(SI_window)
        self.inputLayerCombo.setObjectName("inputLayerCombo")  
        self.inputLayerCombo2 = QComboBox(SI_window)
        self.inputLayerCombo2.setObjectName("inputLayerCombo2")  
        self.inputLayerCombo3 = QComboBox(SI_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")  
        self.inputLayerCombo5 = QComboBox(SI_window)
        self.inputLayerCombo5.setObjectName("inputLayerCombo5")  
        self.inputLayerCombo6 = QComboBox(SI_window)
        self.inputLayerCombo6.setObjectName("inputLayerCombo6")  
        self.gridLayout2.addWidget(self.inputLayerCombo,0,1,1,1)
        self.gridLayout2.addWidget(self.inputLayerCombo2,1,1,1,1)
        self.gridLayout2.addWidget(self.inputLayerCombo3,2,1,1,1)
        self.gridLayout2.addWidget(self.inputLayerCombo5,4,1,1,1)
        self.gridLayout2.addWidget(self.inputLayerCombo6,5,1,1,1)
   
        # stretch to extend the widget in column 1
        self.gridLayout2.setColumnStretch(1,1)  
        
        # output file
        # group box to output files
        self.groupBox2 = QGroupBox(SI_window)
        self.groupBox2.setObjectName("groupBox2")
        self.gridLayout3 = QGridLayout(self.groupBox2)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox2,1,0,1,-1)        
        # create label in gridLayout
        self.label_out = QLabel(SI_window)
        self.label_out.setObjectName("label_out")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout3.addWidget(self.label_out,0,0,1,1)
        # create select button to output file
        self.selectButton_out = QPushButton(SI_window)
        self.selectButton_out.setObjectName("selectButton_out")
        self.gridLayout3.addWidget(self.selectButton_out,0,2,1,1)
        self.outputLayerCombo = QLineEdit(SI_window)
        self.outputLayerCombo.setObjectName("outputLayerCombo")
        self.gridLayout3.addWidget(self.outputLayerCombo, 0,1,1,1)
        # # output color
        # # create label in gridLayout
        # self.label_color = QLabel(SI_window)
        # self.label_color.setObjectName("label_color")
        # # define label (QWidget, row, column, QtAlignement)
        # self.gridLayout3.addWidget(self.label_color,2,0,1,1)
        # # create select button to output file
        # self.selectButton_color = QPushButton(SI_window)
        # self.selectButton_color.setObjectName("selectButton_color")
        # self.gridLayout3.addWidget(self.selectButton_color,2,2,1,1)
        # self.outputLayerCombo_color = QLineEdit(SI_window)
        # self.outputLayerCombo_color.setObjectName("outputLayerCombo_color")
        # self.gridLayout3.addWidget(self.outputLayerCombo_color, 2,1,1,1)
        
        # checkbox to define the output
        self.label_checkSI = QLabel(SI_window)
        self.label_checkSI.setObjectName("label_checkSI")
        self.gridLayout3.addWidget(self.label_checkSI,1,1,1,1)
        self.checkSI = QCheckBox(SI_window)
        self.checkSI.setObjectName("checkSI")
        self.gridLayout3.addWidget(self.checkSI,1,0,1,1)
        
        # self.label_checkcolor = QLabel(SI_window)
        # self.label_checkcolor.setObjectName("label_checkcolor")
        # self.gridLayout3.addWidget(self.label_checkcolor,3,1,1,1)
        # self.checkcolor = QCheckBox(SI_window)
        # self.checkcolor.setObjectName("checkcolor")
        # self.gridLayout3.addWidget(self.checkcolor,3,0,1,1)

    
        # button Ok, Close and Help
        self.buttonBox = QDialogButtonBox(SI_window)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Help|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 2, 1, 1, 1)          
        
        self.retranslateUi(SI_window)
        self.buttonBox.rejected.connect(SI_window.close)
    
    def retranslateUi(self, SI_window):
        SI_window.setWindowTitle( 'SI')   
        self.label.setText( 'D')
        self.label2.setText( 'R')
        self.label3.setText( 'A')
        self.label5.setText( 'T')
        self.label6.setText( 'LU')
        self.selectButton.setText( 'Browse')   
        self.selectButton2.setText( 'Browse')
        self.selectButton3.setText( 'Browse')
        self.selectButton5.setText( 'Browse')
        self.selectButton6.setText( 'Browse')
        self.selectButton_out.setText( 'Browse')
        self.label_out.setText( 'SI:')
        self.groupBox.setTitle( "Input")
        self.groupBox2.setTitle( "Output")
        #self.selectButton_color.setText( 'Browse')
        #self.label_color.setText( 'SI COLORED:')
        self.label_checkSI.setText( 'Load raster into canvas')
        #self.label_checkcolor.setText( 'Load colored raster into canvas')
        self.labelWeightD.setText( 'Weight:')
        self.labelWeightR.setText( 'Weight:')
        self.labelWeightA.setText( 'Weight:')
        self.labelWeightT.setText( 'Weight:')
        self.labelWeightLU.setText( 'Weight:')
      
        