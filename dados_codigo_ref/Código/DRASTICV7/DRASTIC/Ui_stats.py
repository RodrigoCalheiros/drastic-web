from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *


class Ui_stats(object):

    def setupUi(self, stats_window):
        # create stats window
        stats_window.setWindowModality(QtCore.Qt.ApplicationModal)
        stats_window.resize(450, 400)

        # input file
        # create gridLayout
        self.gridLayout1 = QGridLayout(stats_window)
        self.gridLayout1.setObjectName("gridLayout1")

        # create select button to input file 1
        # create label in gridLayout
        self.label = QLabel(stats_window)
        self.label.setObjectName("label")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label, 0, 0, 1, 1)
        self.inputLayerCombo = QComboBox(stats_window)
        self.inputLayerCombo.setObjectName("inputLayerCombo")
        self.gridLayout1.addWidget(self.inputLayerCombo, 0, 1, 1, 1)
        self.selectButton = QPushButton(stats_window)
        self.selectButton.setObjectName("selectButton")
        self.gridLayout1.addWidget(self.selectButton, 0, 2, 1, 1)


        # output file
        # create label in gridLayout
        self.label3 = QLabel(stats_window)
        self.label3.setObjectName("label3")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label3, 1, 0, 1, 1)
        # create select button to input file
        self.selectButton3 = QPushButton(stats_window)
        self.selectButton3.setObjectName("selectButton3")
        self.gridLayout1.addWidget(self.selectButton3, 1, 2, 1, 1)
        self.inputLayerCombo3 = QLineEdit(stats_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")
        self.gridLayout1.addWidget(self.inputLayerCombo3, 1, 1, 1, 1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1, 1)

        # output in different format (word pad)
        self.label2 = QLabel(stats_window)
        self.label2.setObjectName("label2")
        self.gridLayout1.addWidget(self.label2, 2, 0, 1, 1)
        self.checkbox2 = QCheckBox(stats_window)
        self.checkbox2.setObjectName("checkbox2")
        self.gridLayout1.addWidget(self.checkbox2, 2, 1, 1, 1)


        # button Ok, Close and Help
        self.buttonBox = QDialogButtonBox(stats_window)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Help | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 3, 1, 1, 1)

        self.retranslateUi(stats_window)
        self.buttonBox.rejected.connect(stats_window.close)

    def retranslateUi(self, stats_window):
        stats_window.setWindowTitle('Map Statistics')
        self.selectButton.setText('Browse')
        self.selectButton3.setText('Browse')
        self.label.setText('Input raster file:')
        self.label2.setText('Save in txt format')
        self.label3.setText('Output file (html):')

