from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *


class Ui_Infiltrazione(object):

    def setupUi(self, Infiltrazione_window):
        # create Infiltrazione window
        Infiltrazione_window.setWindowModality(QtCore.Qt.ApplicationModal)
        Infiltrazione_window.resize(450, 450)

        # input file
        # create gridLayout
        self.gridLayout1 = QGridLayout(Infiltrazione_window)
        self.gridLayout1.setObjectName("gridLayout1")
        # define a groupbox to specify the input method 1
        self.groupBox0 = QGroupBox(Infiltrazione_window)
        self.groupBox0.setObjectName("groupBox0")
        self.groupBox0.setTitle("Base")
        self.gridLayout = QGridLayout(self.groupBox0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout1.addWidget(self.groupBox0, 0, 0, 1, -1)
        # create label in gridLayout 
        self.label = QLabel(Infiltrazione_window)
        self.label.setObjectName("label")
        self.label1 = QLabel(Infiltrazione_window)
        self.label1.setObjectName("label1")
        self.label2 = QLabel(Infiltrazione_window)
        self.label2.setObjectName("label2")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.label1, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.label2, 2, 0, 1, 1)
        # create select button to input file
        self.selectButton = QPushButton(Infiltrazione_window)
        self.selectButton.setObjectName("selectButton")
        self.gridLayout.addWidget(self.selectButton, 0, 2, 1, 1)
        self.selectButton1 = QPushButton(Infiltrazione_window)
        self.selectButton1.setObjectName("selectButton1")
        self.gridLayout.addWidget(self.selectButton1, 1, 2, 1, 1)
        self.selectButton2 = QPushButton(Infiltrazione_window)
        self.selectButton2.setObjectName("selectButton2")
        self.gridLayout.addWidget(self.selectButton2, 2, 2, 1, 1)
        self.inputLayerCombo = QComboBox(Infiltrazione_window)
        self.inputLayerCombo.setObjectName("inputLayerCombo")
        self.gridLayout.addWidget(self.inputLayerCombo, 0, 1, 1, 1)
        self.inputLayerCombo1 = QComboBox(Infiltrazione_window)
        self.inputLayerCombo1.setObjectName("inputLayerCombo1")
        self.gridLayout.addWidget(self.inputLayerCombo1, 1, 1, 1, 1)
        self.inputLayerCombo2 = QComboBox(Infiltrazione_window)
        self.inputLayerCombo2.setObjectName("inputLayerCombo2")
        self.gridLayout.addWidget(self.inputLayerCombo2, 2, 1, 1, 1)
        # stretch to extend the widget in column 1
        self.gridLayout.setColumnStretch(1, 1)

        # define a groupbox to specify the input method 2
        self.groupBox4 = QGroupBox(Infiltrazione_window)
        self.groupBox4.setObjectName("groupBox4")
        self.groupBox4.setTitle("Improvement")
        self.gridLayout4 = QGridLayout(self.groupBox4)
        self.gridLayout4.setObjectName("gridLayout4")
        self.gridLayout1.addWidget(self.groupBox4, 2, 0, 1, -1)
        self.selectButton4 = QPushButton(Infiltrazione_window)
        self.selectButton4.setObjectName("selectButton4")
        self.gridLayout4.addWidget(self.selectButton4, 0, 2, 1, 1)
        self.inputLayerCombo4 = QComboBox(Infiltrazione_window)
        self.inputLayerCombo4.setObjectName("inputLayerCombo4")
        self.gridLayout4.addWidget(self.inputLayerCombo4, 0, 1, 1, 1)
        self.label4 = QLabel(Infiltrazione_window)
        self.label4.setObjectName("label4")
        self.gridLayout4.addWidget(self.label4, 0, 0, 1, 1)
        self.gridLayout4.setColumnStretch(1, 1)

        # define a groupbox to specify the cell size and attribute
        self.groupBox1 = QGroupBox(Infiltrazione_window)
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout3 = QGridLayout(self.groupBox1)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox1, 1, 0, 1, -1)
        # define attribute "Elevation" for precipitation
        self.labelAttrib = QLabel(Infiltrazione_window)
        self.labelAttrib.setObjectName("labelAttrib")
        self.gridLayout3.addWidget(self.labelAttrib, 0, 0, 1, 1)
        self.lineAttrib = QComboBox(Infiltrazione_window)
        self.lineAttrib.setObjectName("lineAttrib")
        self.gridLayout3.addWidget(self.lineAttrib, 0, 1, 1, 1)
        # define attribute for surface runoff
        self.labelAttribRunoff = QLabel(Infiltrazione_window)
        self.labelAttribRunoff.setObjectName("labelAttribRunoff")
        self.gridLayout3.addWidget(self.labelAttribRunoff, 1, 0, 1, 1)
        self.lineAttribRunoff = QComboBox(Infiltrazione_window)
        self.lineAttribRunoff.setObjectName("lineAttribRunoff")
        self.gridLayout3.addWidget(self.lineAttribRunoff, 1, 1, 1, 1)
        # define attribute for evapotranspiration
        self.labelAttribEvap = QLabel(Infiltrazione_window)
        self.labelAttribEvap.setObjectName("labelAttribEvap")
        self.gridLayout3.addWidget(self.labelAttribEvap, 2, 0, 1, 1)
        self.lineAttribEvap = QComboBox(Infiltrazione_window)
        self.lineAttribEvap.setObjectName("lineAttribEvap")
        self.gridLayout3.addWidget(self.lineAttribEvap, 2, 1, 1, 1)
        # define pixel size
        self.labelPix = QLabel(Infiltrazione_window)
        self.labelPix.setObjectName("labelPix")
        self.gridLayout3.addWidget(self.labelPix, 0, 3, 1, 1)
        self.linePix = QSpinBox()
        self.linePix.setValue(29)
        self.linePix.stepBy(1)
        self.linePix.setObjectName("linePix")
        self.gridLayout3.addWidget(self.linePix, 0, 4, 1, 1)

        ## button weight
        # self.labelWeight = .QLabel(Infiltrazione_window)
        # self.labelWeight.setObjectName("labelWeight")
        # self.boxLayout.addWidget(self.labelWeight)
        # self.lineWeight = .QSpinBox()
        # self.lineWeight.setValue(3)
        # self.lineWeight.stepBy(1)
        # self.lineWeight.setObjectName("lineWeight")
        # self.boxLayout.addWidget(self.lineWeight)


        # output file
        # create label in gridLayout
        self.label3 = QLabel(Infiltrazione_window)
        self.label3.setObjectName("label3")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label3, 5, 0, 1, 1)
        # create select button to input file
        self.selectButton3 = QPushButton(Infiltrazione_window)
        self.selectButton3.setObjectName("selectButton3")
        self.gridLayout1.addWidget(self.selectButton3, 5, 2, 1, 1)
        self.inputLayerCombo3 = QLineEdit(Infiltrazione_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")
        self.gridLayout1.addWidget(self.inputLayerCombo3, 5, 1, 1, 1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1, 1)

        # button Ok, Close and Help
        self.buttonBox = QDialogButtonBox(Infiltrazione_window)
        # self.buttonBox.setMaximumSize(QtCore.QSize(200, 16777215))
        # self.buttonBox.setBaseSize(QtCore.QSize(110, 0))
        # self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Help | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 7, 1, 1, 1)

        self.retranslateUi(Infiltrazione_window)
        self.buttonBox.rejected.connect(Infiltrazione_window.close)

    def retranslateUi(self, Infiltrazione_window):
        Infiltrazione_window.setWindowTitle('Net Infiltrazione (R)')
        self.label.setText('Precipitation (mm/year):')
        self.label1.setText('Overland Flow (mm/year):')
        self.label2.setText('Evapotranspiration (mm/year):')
        self.label4.setText('DEM (m):')
        self.selectButton.setText('Browse')
        self.selectButton1.setText('Browse')
        self.selectButton2.setText('Browse')
        self.label3.setText('Output file:')
        self.selectButton3.setText('Browse')
        self.selectButton4.setText('Browse')
        # self.labelWeight.setText(.QApplication.translate('Net Infiltrazione (R)', 'Weight:', None, .QApplication.UnicodeUTF8))
        self.labelPix.setText('Cell size:')
        self.labelAttrib.setText('Attribute Precipitation:')
        self.labelAttribRunoff.setText('Attribute Surface Runoff:')
        self.labelAttribEvap.setText('Attribute Evapotranspiration:')