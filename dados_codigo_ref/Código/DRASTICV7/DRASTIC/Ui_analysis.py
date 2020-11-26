from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *


class Ui_analysis(object):

    def setupUi(self, analysis_window):
        # create analysis window
        analysis_window.setWindowModality(QtCore.Qt.ApplicationModal)
        analysis_window.resize(450, 400)

        # input file
        # create gridLayout
        self.gridLayout1 = QGridLayout(analysis_window)
        self.gridLayout1.setObjectName("gridLayout1")

        # create select button to input file 1
        # create label in gridLayout
        self.label = QLabel(analysis_window)
        self.label.setObjectName("label")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label, 0, 0, 1, 1)
        self.inputLayerCombo = QComboBox(analysis_window)
        self.inputLayerCombo.setObjectName("inputLayerCombo")
        self.gridLayout1.addWidget(self.inputLayerCombo, 0, 1, 1, 1)
        self.selectButton = QPushButton(analysis_window)
        self.selectButton.setObjectName("selectButton")
        self.gridLayout1.addWidget(self.selectButton, 0, 2, 1, 1)

        # create a group box
        self.groupBox = QGroupBox(analysis_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox, 1, 0, 1, 1)
        # minimum and maximum
        # create label in gridLayout
        self.labelmin = QLabel(analysis_window)
        self.labelmin.setObjectName("labelmin")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout2.addWidget(self.labelmin, 0, 0, 1, 1)
        self.linePixmin = QSpinBox()
        self.linePixmin.setRange(0,1000)
        self.linePixmin.stepBy(1)
        self.linePixmin.setObjectName("linePixmin")
        self.gridLayout2.addWidget(self.linePixmin, 0, 1, 1, 1)
        # create label in gridLayout
        self.labelmax = QLabel(analysis_window)
        self.labelmax.setObjectName("labelmax")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout2.addWidget(self.labelmax, 0, 2, 1, 1)
        self.linePixmax = QSpinBox()
        self.linePixmax.setRange(0,1000)
        self.linePixmax.stepBy(1)
        self.linePixmax.setObjectName("linePixmax")
        self.gridLayout2.addWidget(self.linePixmax, 0, 3, 1, 1)


        # create select button to input file 2
        # create label in gridLayout
        self.label2 = QLabel(analysis_window)
        self.label2.setObjectName("label2")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label2, 2, 0, 1, 1)
        self.inputLayerCombo2 = QComboBox(analysis_window)
        self.inputLayerCombo2.setObjectName("inputLayerCombo2")
        self.gridLayout1.addWidget(self.inputLayerCombo2, 2, 1, 1, 1)
        self.selectButton2 = QPushButton(analysis_window)
        self.selectButton2.setObjectName("selectButton2")
        self.gridLayout1.addWidget(self.selectButton2, 2, 2, 1, 1)

        # minimum and maximum
        self.groupBox2 = QGroupBox(analysis_window)
        self.groupBox2.setObjectName("groupBox2")
        self.gridLayout3 = QGridLayout(self.groupBox2)
        self.gridLayout3.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox2, 3, 0, 1, 1)
        # create label in gridLayout
        self.labelmin2 = QLabel(analysis_window)
        self.labelmin2.setObjectName("labelmin2")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout3.addWidget(self.labelmin2, 0, 0, 1, 1)
        self.linePixmin2 = QSpinBox()
        self.linePixmin2.setRange(0,1000)
        self.linePixmin2.stepBy(1)
        self.linePixmin2.setObjectName("linePixmin2")
        self.gridLayout3.addWidget(self.linePixmin2, 0, 1, 1, 1)
        # create label in gridLayout
        self.labelmax2 = QLabel(analysis_window)
        self.labelmax2.setObjectName("labelmax2")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout3.addWidget(self.labelmax2, 0, 2, 1, 1)
        self.linePixmax2 = QSpinBox()
        self.linePixmax2.setRange(0,1000)
        self.linePixmax2.stepBy(1)
        self.linePixmax2.setObjectName("linePixmax2")
        self.gridLayout3.addWidget(self.linePixmax2, 0, 3, 1, 1)

        # output file
        # create label in gridLayout
        self.label3 = QLabel(analysis_window)
        self.label3.setObjectName("label3")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label3, 4, 0, 1, 1)
        # create select button to input file
        self.selectButton3 = QPushButton(analysis_window)
        self.selectButton3.setObjectName("selectButton3")
        self.gridLayout1.addWidget(self.selectButton3, 4, 2, 1, 1)
        self.inputLayerCombo3 = QLineEdit(analysis_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")
        self.gridLayout1.addWidget(self.inputLayerCombo3, 4, 1, 1, 1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1, 1)


        # button Ok, Close and Help
        self.buttonBox = QDialogButtonBox(analysis_window)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Help | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 5, 1, 1, 1)

        self.retranslateUi(analysis_window)
        self.buttonBox.rejected.connect(analysis_window.close)

    def retranslateUi(self, analysis_window):
        analysis_window.setWindowTitle('Comparative analysis')
        self.selectButton.setText('Browse')
        self.selectButton2.setText('Browse')
        self.selectButton3.setText('Browse')
        self.label.setText('Input file:')
        self.label2.setText('Input file:')
        self.label3.setText('Output file:')
        self.labelmin.setText('Min:')
        self.labelmax.setText('Max:')
        self.labelmin2.setText('Min:')
        self.labelmax2.setText('Max:')

