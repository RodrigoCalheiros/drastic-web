from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *


class Ui_Nitrates_window(object):

    def setupUi(self, Nitrates_window):
        # create Nitrates window
        Nitrates_window.setWindowModality(QtCore.Qt.ApplicationModal)
        Nitrates_window.resize(450, 400)

        # input file
        # create gridLayout
        self.gridLayout1 = QGridLayout(Nitrates_window)
        self.gridLayout1.setObjectName("gridLayout1")
        # group box to input files
        self.groupBox = QGroupBox(Nitrates_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox, 0, 0, 1, -1)
        # create label in gridLayout 
        self.label = QLabel(Nitrates_window)
        self.label.setObjectName("label")
        self.label2 = QLabel(Nitrates_window)
        self.label2.setObjectName("label2")
        self.label3 = QLabel(Nitrates_window)
        self.label3.setObjectName("label3")
        self.label4 = QLabel(Nitrates_window)
        self.label4.setObjectName("label4")
        self.label5 = QLabel(Nitrates_window)
        self.label5.setObjectName("label5")
        self.label6 = QLabel(Nitrates_window)
        self.label6.setObjectName("label6")
        self.label7 = QLabel(Nitrates_window)
        self.label7.setObjectName("label7")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout2.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout2.addWidget(self.label2, 1, 0, 1, 1)
        self.gridLayout2.addWidget(self.label3, 2, 0, 1, 1)
        self.gridLayout2.addWidget(self.label4, 3, 0, 1, 1)
        self.gridLayout2.addWidget(self.label5, 4, 0, 1, 1)
        self.gridLayout2.addWidget(self.label6, 5, 0, 1, 1)
        self.gridLayout2.addWidget(self.label7, 6, 0, 1, 1)
        # create select button to input file
        self.selectButton = QPushButton(Nitrates_window)
        self.selectButton.setObjectName("selectButton")
        self.selectButton2 = QPushButton(Nitrates_window)
        self.selectButton2.setObjectName("selectButton2")
        self.selectButton3 = QPushButton(Nitrates_window)
        self.selectButton3.setObjectName("selectButton3")
        self.selectButton4 = QPushButton(Nitrates_window)
        self.selectButton4.setObjectName("selectButton4")
        self.selectButton5 = QPushButton(Nitrates_window)
        self.selectButton5.setObjectName("selectButton5")
        self.selectButton6 = QPushButton(Nitrates_window)
        self.selectButton6.setObjectName("selectButton6")
        self.selectButton7 = QPushButton(Nitrates_window)
        self.selectButton7.setObjectName("selectButton7")

        # button weight Depth to Groundwater
        self.labelWeightD = QLabel(Nitrates_window)
        self.labelWeightD.setObjectName("labelWeightD")
        self.gridLayout2.addWidget(self.labelWeightD, 0, 2, 1, 1)
        self.lineWeightD = QSpinBox()
        self.lineWeightD.setValue(4)
        self.lineWeightD.stepBy(1)
        self.lineWeightD.setObjectName("lineWeightD")
        self.gridLayout2.addWidget(self.lineWeightD, 0, 3, 1, 1)
        self.gridLayout2.addWidget(self.selectButton, 0, 4, 1, 1)

        # button weight Recharge
        self.labelWeightR = QLabel(Nitrates_window)
        self.labelWeightR.setObjectName("labelWeightR")
        self.gridLayout2.addWidget(self.labelWeightR, 1, 2, 1, 1)
        self.lineWeightR = QSpinBox()
        self.lineWeightR.setValue(4)
        self.lineWeightR.stepBy(1)
        self.lineWeightR.setObjectName("lineWeightR")
        self.gridLayout2.addWidget(self.lineWeightR, 1, 3, 1, 1)
        self.gridLayout2.addWidget(self.selectButton2, 1, 4, 1, 1)

        # button weight Aquifer
        self.labelWeightA = QLabel(Nitrates_window)
        self.labelWeightA.setObjectName("labelWeightA")
        self.gridLayout2.addWidget(self.labelWeightA, 2, 2, 1, 1)
        self.lineWeightA = QSpinBox()
        self.lineWeightA.setValue(3)
        self.lineWeightA.stepBy(1)
        self.lineWeightA.setObjectName("lineWeightA")
        self.gridLayout2.addWidget(self.lineWeightA, 2, 3, 1, 1)
        self.gridLayout2.addWidget(self.selectButton3, 2, 4, 1, 1)

        # button weight Soil
        self.labelWeightS = QLabel(Nitrates_window)
        self.labelWeightS.setObjectName("labelWeightS")
        self.gridLayout2.addWidget(self.labelWeightS, 3, 2, 1, 1)
        self.lineWeightS = QSpinBox()
        self.lineWeightS.setValue(4)
        self.lineWeightS.stepBy(1)
        self.lineWeightS.setObjectName("lineWeightS")
        self.gridLayout2.addWidget(self.lineWeightS, 3, 3, 1, 1)
        self.gridLayout2.addWidget(self.selectButton4, 3, 4, 1, 1)

        # button weight Topography
        self.labelWeightT = QLabel(Nitrates_window)
        self.labelWeightT.setObjectName("labelWeightT")
        self.gridLayout2.addWidget(self.labelWeightT, 4, 2, 1, 1)
        self.lineWeightT = QSpinBox()
        self.lineWeightT.setValue(1)
        self.lineWeightT.stepBy(1)
        self.lineWeightT.setObjectName("lineWeightT")
        self.gridLayout2.addWidget(self.lineWeightT, 4, 3, 1, 1)
        self.gridLayout2.addWidget(self.selectButton5, 4, 4, 1, 1)

        # button weight Impact of Vadose Zone
        self.labelWeightI = QLabel(Nitrates_window)
        self.labelWeightI.setObjectName("labelWeightI")
        self.gridLayout2.addWidget(self.labelWeightI, 5, 2, 1, 1)
        self.lineWeightI = QSpinBox()
        self.lineWeightI.setValue(1)
        self.lineWeightI.stepBy(1)
        self.lineWeightI.setObjectName("lineWeightI")
        self.gridLayout2.addWidget(self.lineWeightI, 5, 3, 1, 1)
        self.gridLayout2.addWidget(self.selectButton6, 5, 4, 1, 1)

        # button weight Hydraulic
        self.labelWeightC = QLabel(Nitrates_window)
        self.labelWeightC.setObjectName("labelWeightC")
        self.gridLayout2.addWidget(self.labelWeightC, 6, 2, 1, 1)
        self.lineWeightC = QSpinBox()
        self.lineWeightC.setValue(2)
        self.lineWeightC.stepBy(1)
        self.lineWeightC.setObjectName("lineWeightC")
        self.gridLayout2.addWidget(self.lineWeightC, 6, 3, 1, 1)
        self.gridLayout2.addWidget(self.selectButton7, 6, 4, 1, 1)

        self.inputLayerCombo = QComboBox(Nitrates_window)
        self.inputLayerCombo.setObjectName("inputLayerCombo")
        self.inputLayerCombo2 = QComboBox(Nitrates_window)
        self.inputLayerCombo2.setObjectName("inputLayerCombo2")
        self.inputLayerCombo3 = QComboBox(Nitrates_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")
        self.inputLayerCombo4 = QComboBox(Nitrates_window)
        self.inputLayerCombo4.setObjectName("inputLayerCombo4")
        self.inputLayerCombo5 = QComboBox(Nitrates_window)
        self.inputLayerCombo5.setObjectName("inputLayerCombo5")
        self.inputLayerCombo6 = QComboBox(Nitrates_window)
        self.inputLayerCombo6.setObjectName("inputLayerCombo6")
        self.inputLayerCombo7 = QComboBox(Nitrates_window)
        self.inputLayerCombo7.setObjectName("inputLayerCombo7")
        self.gridLayout2.addWidget(self.inputLayerCombo, 0, 1, 1, 1)
        self.gridLayout2.addWidget(self.inputLayerCombo2, 1, 1, 1, 1)
        self.gridLayout2.addWidget(self.inputLayerCombo3, 2, 1, 1, 1)
        self.gridLayout2.addWidget(self.inputLayerCombo4, 3, 1, 1, 1)
        self.gridLayout2.addWidget(self.inputLayerCombo5, 4, 1, 1, 1)
        self.gridLayout2.addWidget(self.inputLayerCombo6, 5, 1, 1, 1)
        self.gridLayout2.addWidget(self.inputLayerCombo7, 6, 1, 1, 1)
        # stretch to extend the widget in column 1
        self.gridLayout2.setColumnStretch(1, 1)

        # output file
        # group box to output files
        self.groupBox2 = QGroupBox(Nitrates_window)
        self.groupBox2.setObjectName("groupBox2")
        self.gridLayout3 = QGridLayout(self.groupBox2)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox2, 1, 0, 1, -1)
        # create label in gridLayout
        self.label_out = QLabel(Nitrates_window)
        self.label_out.setObjectName("label_out")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout3.addWidget(self.label_out, 0, 0, 1, 1)
        # create select button to output file
        self.selectButton_out = QPushButton(Nitrates_window)
        self.selectButton_out.setObjectName("selectButton_out")
        self.gridLayout3.addWidget(self.selectButton_out, 0, 2, 1, 1)
        self.outputLayerCombo = QLineEdit(Nitrates_window)
        self.outputLayerCombo.setObjectName("outputLayerCombo")
        self.gridLayout3.addWidget(self.outputLayerCombo, 0, 1, 1, 1)

        # checkbox to define the output
        self.label_checkNitrates = QLabel(Nitrates_window)
        self.label_checkNitrates.setObjectName("label_checkNitrates")
        self.gridLayout3.addWidget(self.label_checkNitrates, 1, 1, 1, 1)
        self.checkNitrates = QCheckBox(Nitrates_window)
        self.checkNitrates.setObjectName("checkNitrates")
        self.gridLayout3.addWidget(self.checkNitrates, 1, 0, 1, 1)

        # button Ok, Close and Help
        self.buttonBox = QDialogButtonBox(Nitrates_window)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Help | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 2, 1, 1, 1)

        self.retranslateUi(Nitrates_window)
        self.buttonBox.rejected.connect(Nitrates_window.close)

    def retranslateUi(self, Nitrates_window):
        Nitrates_window.setWindowTitle('Nitrates')
        self.label.setText('S')
        self.label2.setText('I')
        self.label3.setText('N')
        self.label4.setText('T')
        self.label5.setText('A')
        self.label6.setText('C')
        self.label7.setText('S')
        self.selectButton.setText('Browse')
        self.selectButton2.setText('Browse')
        self.selectButton3.setText('Browse')
        self.selectButton4.setText('Browse')
        self.selectButton5.setText('Browse')
        self.selectButton6.setText('Browse')
        self.selectButton7.setText('Browse')
        self.selectButton_out.setText('Browse')
        self.label_out.setText('Nitrates:')
        self.groupBox.setTitle("Input")
        self.groupBox2.setTitle("Output")
        self.label_checkNitrates.setText('Load raster into canvas')
        self.labelWeightD.setText('Weight:')
        self.labelWeightR.setText('Weight:')
        self.labelWeightA.setText('Weight:')
        self.labelWeightS.setText('Weight:')
        self.labelWeightT.setText('Weight:')
        self.labelWeightI.setText('Weight:')
        self.labelWeightC.setText('Weight:')



