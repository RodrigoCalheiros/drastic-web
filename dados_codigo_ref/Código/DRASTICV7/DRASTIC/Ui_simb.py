from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *


class Ui_simb(object):

    def setupUi(self, simb_window):
        # create simb window
        simb_window.setWindowModality(QtCore.Qt.ApplicationModal)
        simb_window.resize(900, 500)

        # input file
        # create gridLayout
        self.gridLayout1 = QGridLayout(simb_window)
        self.gridLayout1.setObjectName("gridLayout1")

        # define the indexs
        # create a group box
        self.groupBox = QGroupBox(simb_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox, 1, 0, 1, -1)
        # table for classes and indexes

        self.tableWidget = QTableWidget(5, 5, simb_window)
        self.gridLayout2.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.newItem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, self.newItem)
        self.newItem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, self.newItem)
        self.newItem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, self.newItem)
        self.newItem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, self.newItem)
        self.newItem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, self.newItem)
        self.tableWidget.resizeColumnToContents(8)

        # set the description
        self.line = QLineEdit("")
        self.tableWidget.setItem(0, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Very High")
        self.tableWidget.setItem(1, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("High")
        self.tableWidget.setItem(2, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Moderate")
        self.tableWidget.setItem(3, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Low")
        self.tableWidget.setItem(4, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Input")

        self.inputLayerCombo = QComboBox(simb_window)
        self.inputLayerCombo.setObjectName("inputLayerCombo")

        self.tableWidget.setCellWidget(0, 1, self.inputLayerCombo)
        self.line = QLineEdit("1000")
        self.tableWidget.setItem(1, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("199")
        self.tableWidget.setItem(2, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("159")
        self.tableWidget.setItem(3, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("120")
        self.tableWidget.setItem(4, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Input")

        self.inputLayerCombo1 = QComboBox(simb_window)
        self.inputLayerCombo1.setObjectName("inputLayerCombo1")

        self.tableWidget.setCellWidget(0, 2, self.inputLayerCombo1)
        self.line = QLineEdit("1.0")
        self.tableWidget.setItem(1, 2, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("0.7")
        self.tableWidget.setItem(2, 2, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("0.5")
        self.tableWidget.setItem(3, 2, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("0.3")
        self.tableWidget.setItem(4, 2, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Input")

        self.inputLayerCombo2 = QComboBox(simb_window)
        self.inputLayerCombo2.setObjectName("inputLayerCombo2")

        self.tableWidget.setCellWidget(0, 4, self.inputLayerCombo2)
        self.line = QLineEdit("100")
        self.tableWidget.setItem(1, 4, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("85")
        self.tableWidget.setItem(2, 4, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("65")
        self.tableWidget.setItem(3, 4, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("45")
        self.tableWidget.setItem(4, 4, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Input")

        self.inputLayerCombo3 = QComboBox(simb_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")

        self.tableWidget.setCellWidget(0, 3, self.inputLayerCombo3)
        self.line = QLineEdit("1000")
        self.tableWidget.setItem(1, 3, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("210")
        self.tableWidget.setItem(2, 3, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("186")
        self.tableWidget.setItem(3, 3, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("105")
        self.tableWidget.setItem(4, 3, QTableWidgetItem(self.line.text()))

        # define the indexs
        # create a group box
        self.groupBox2 = QGroupBox(simb_window)
        self.groupBox2.setObjectName("groupBox2")
        self.gridLayout3 = QGridLayout(self.groupBox2)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox2, 2, 0, 1, -1)

        # checkbox to each index
        # create label in gridLayout
        self.label_DRASTIC = QLabel(simb_window)
        self.label_DRASTIC.setObjectName("label3_DRASTIC")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout3.addWidget(self.label_DRASTIC, 1, 0, 1, 1)
        # create select button to input file
        self.selectDRASTIC = QCheckBox(simb_window)
        self.selectDRASTIC.setObjectName("selectDRASTIC")
        self.gridLayout3.addWidget(self.selectDRASTIC, 1, 1, 1, 1)

        self.label_GOD = QLabel(simb_window)
        self.label_GOD.setObjectName("label_GOD")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout3.addWidget(self.label_GOD, 1, 2, 1, 1)
        # create select button to input file
        self.selectGOD = QCheckBox(simb_window)
        self.selectGOD.setObjectName("selectGOD")
        self.gridLayout3.addWidget(self.selectGOD, 1, 3, 1, 1)

        self.label_si = QLabel(simb_window)
        self.label_si.setObjectName("label_si")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout3.addWidget(self.label_si, 1, 6, 1, 1)
        # create select button to input file
        self.selectSI = QCheckBox(simb_window)
        self.selectSI.setObjectName("selectSI")
        self.gridLayout3.addWidget(self.selectSI, 1, 7, 1, 1)

        self.label_SINTACS = QLabel(simb_window)
        self.label_SINTACS.setObjectName("label_SINTACS")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout3.addWidget(self.label_SINTACS, 1, 4, 1, 1)
        # create select button to input file
        self.selectSINTACS = QCheckBox(simb_window)
        self.selectSINTACS.setObjectName("selectSINTACS")
        self.gridLayout3.addWidget(self.selectSINTACS, 1, 5, 1, 1)


        # output file
        # create label in gridLayout
        self.label3 = QLabel(simb_window)
        self.label3.setObjectName("label3")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label3, 3, 0, 1, 1)
        # create select button to input file
        self.selectButton3 = QPushButton(simb_window)
        self.selectButton3.setObjectName("selectButton3")
        self.gridLayout1.addWidget(self.selectButton3,3, 2, 1, 1)
        self.inputLayerCombo4 = QLineEdit(simb_window)
        self.inputLayerCombo4.setObjectName("inputLayerCombo4")
        self.gridLayout1.addWidget(self.inputLayerCombo4, 3, 1, 1, 1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1, 1)

        # button Ok, Close and Help
        self.buttonBox = QDialogButtonBox(simb_window)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Help | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 4, 1, 1, 1)

        self.retranslateUi(simb_window)
        self.buttonBox.rejected.connect(simb_window.close)

    def retranslateUi(self, simb_window):
        simb_window.setWindowTitle('Apply Symbology')
        self.selectButton3.setText('Browse')
        self.label3.setText('Output file (qml):')
        self.label_DRASTIC.setText('DRASTIC')
        self.label_GOD.setText('GOD')
        self.label_si.setText('SI')
        self.label_SINTACS.setText('SINTACS')
        self.tableWidget.horizontalHeaderItem(0).setText("Vulnerability Class")
        self.tableWidget.horizontalHeaderItem(1).setText("DRASTIC")
        self.tableWidget.horizontalHeaderItem(2).setText("GOD")
        self.tableWidget.horizontalHeaderItem(4).setText("SI")
        self.tableWidget.horizontalHeaderItem(3).setText("SINTACS")


