from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *


class Ui_Tipologia(object):

    def setupUi(self, Tipologia_window):
        # create Aquifer window
        Tipologia_window.setWindowModality(QtCore.Qt.ApplicationModal)
        Tipologia_window.resize(450, 800)

        # input file
        # create gridLayout
        self.gridLayout1 = QGridLayout(Tipologia_window)
        self.gridLayout1.setObjectName("gridLayout1")
        # create label in gridLayout 
        self.label = QLabel(Tipologia_window)
        self.label.setObjectName("label")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label, 0, 0, 1, 1)
        # create select button to input file
        self.selectButton = QPushButton(Tipologia_window)
        self.selectButton.setObjectName("selectButton")
        self.gridLayout1.addWidget(self.selectButton, 0, 2, 1, 1)
        self.inputLayerCombo = QComboBox(Tipologia_window)
        self.inputLayerCombo.setObjectName("inputLayerCombo")
        self.gridLayout1.addWidget(self.inputLayerCombo, 0, 1, 1, 1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1, 1)

        # define a groupbox to specify the cell size and attribute
        self.groupBox1 = QGroupBox(Tipologia_window)
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout3 = QGridLayout(self.groupBox1)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox1, 1, 0, 1, -1)
        # define attribute "Elevation"
        self.labelAttrib = QLabel(Tipologia_window)
        self.labelAttrib.setObjectName("labelAttrib")
        self.gridLayout3.addWidget(self.labelAttrib, 0, 0, -1, 1)
        self.lineAttrib = QComboBox(Tipologia_window)
        self.lineAttrib.setObjectName("lineAttrib")
        self.gridLayout3.addWidget(self.lineAttrib, 0, 1, -1, 1)
        # define pixel size
        self.labelPix = QLabel(Tipologia_window)
        self.labelPix.setObjectName("labelPix")
        self.gridLayout3.addWidget(self.labelPix, 0, 3, -1, 1)
        self.linePix = QSpinBox()
        self.linePix.setValue(29)
        self.linePix.stepBy(1)
        self.linePix.setObjectName("linePix")
        self.gridLayout3.addWidget(self.linePix, 0, 4, -1, 1)

        # define the indexs
        # create a group box
        self.groupBox = QGroupBox(Tipologia_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox, 2, 0, 1, -1)
        # table for classes and indexes
        self.tableWidget = QTableWidget(10, 2, Tipologia_window)
        self.gridLayout2.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.newItem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, self.newItem)
        self.newItem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, self.newItem)
        # set the description
        self.line = QLineEdit("Thin or absent")
        self.tableWidget.setItem(0, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Clean gravel")
        self.tableWidget.setItem(1, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Clean sand")
        self.tableWidget.setItem(2, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Sandy")
        self.tableWidget.setItem(3, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Peat")
        self.tableWidget.setItem(4, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Sandy clay")
        self.tableWidget.setItem(5, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Sandy loam")
        self.tableWidget.setItem(6, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Sandy clay loam")
        self.tableWidget.setItem(7, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Loam")
        self.tableWidget.setItem(8, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Silt loam")
        self.tableWidget.setItem(9, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Silty clay loam")
        self.tableWidget.setItem(10, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Clay loam")
        self.tableWidget.setItem(11, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Silty-clay")
        self.tableWidget.setItem(12, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Muck")
        self.tableWidget.setItem(13, 0, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("Clay")
        self.tableWidget.setItem(14, 0, QTableWidgetItem(self.line.text()))

        # set the indexes values
        self.line = QLineEdit("9.8-10")
        self.tableWidget.setItem(0, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("9.7-10")
        self.tableWidget.setItem(1, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("8.9-9.5")
        self.tableWidget.setItem(2, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("8.0-8.5")
        self.tableWidget.setItem(3, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("7.5-8.2")
        self.tableWidget.setItem(4, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("6.1-7.0")
        self.tableWidget.setItem(5, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("5.5-6.0")
        self.tableWidget.setItem(6, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("4.5-5.3")
        self.tableWidget.setItem(7, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("4.0-5.0")
        self.tableWidget.setItem(8, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("3.5-4.2")
        self.tableWidget.setItem(9, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("3.0-4.0")
        self.tableWidget.setItem(10, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("2.0-3.0")
        self.tableWidget.setItem(11, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("1.4-2.0")
        self.tableWidget.setItem(12, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("1.2-2")
        self.tableWidget.setItem(13, 1, QTableWidgetItem(self.line.text()))
        self.line = QLineEdit("1.0-1.4")
        self.tableWidget.setItem(14, 1, QTableWidgetItem(self.line.text()))

        # create a box layout to insert the buttons Add and Remove
        self.boxLayout = QVBoxLayout()
        self.boxLayout.setObjectName("boxLayout")
        # button Add
        self.buttonAdd = QPushButton(Tipologia_window)
        self.buttonAdd.setObjectName("buttonAdd")
        self.boxLayout.addWidget(self.buttonAdd)
        # button Remove
        self.buttonRemove = QPushButton(Tipologia_window)
        self.buttonRemove.setObjectName("buttonRemove")
        self.boxLayout.addWidget(self.buttonRemove)
        # attribute table button
        self.buttonAttribute = QPushButton(Tipologia_window)
        self.buttonAttribute.setObjectName("buttonAttribute")
        self.boxLayout.addWidget(self.buttonAttribute)
        self.gridLayout2.addLayout(self.boxLayout, 0, 1, -1, 1)
        ## button weight
        # self.labelWeight = .QLabel(Tipologia_window)
        # self.labelWeight.setObjectName("labelWeight")
        # self.boxLayout.addWidget(self.labelWeight)
        # self.lineWeight = .QSpinBox()
        # self.lineWeight.setValue(2)
        # self.lineWeight.stepBy(1)
        # self.lineWeight.setObjectName("lineWeight")
        # self.boxLayout.addWidget(self.lineWeight)
        self.gridLayout2.addLayout(self.boxLayout, 0, 1, -1, 1)

        # output file
        # create label in gridLayout
        self.label3 = QLabel(Tipologia_window)
        self.label3.setObjectName("label3")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label3, 3, 0, 1, 1)
        # create select button to input file
        self.selectButton3 = QPushButton(Tipologia_window)
        self.selectButton3.setObjectName("selectButton3")
        self.gridLayout1.addWidget(self.selectButton3, 3, 2, 1, 1)
        self.inputLayerCombo3 = QLineEdit(Tipologia_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")
        self.gridLayout1.addWidget(self.inputLayerCombo3, 3, 1, 1, 1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1, 1)

        # button Ok, Close and Help
        self.buttonBox = QDialogButtonBox(Tipologia_window)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Help | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 4, 1, 1, 1)

        self.retranslateUi(Tipologia_window)
        self.buttonBox.rejected.connect(Tipologia_window.close)

    def retranslateUi(self, Tipologia_window):
        Tipologia_window.setWindowTitle('Tipologia della copertura (T)')
        self.label.setText('Input file:')
        self.selectButton.setText('Browse')
        self.groupBox.setTitle("Ratings")
        self.tableWidget.horizontalHeaderItem(0).setText("Tipologia")
        self.tableWidget.horizontalHeaderItem(1).setText("Ratings")
        self.buttonAdd.setText("Add")
        self.buttonRemove.setText("Remove")
        self.buttonAttribute.setText("Attribute Table")
        self.label3.setText('Output file:')
        self.selectButton3.setText('Browse')
        self.labelAttrib.setText('Attribute:')
        self.labelPix.setText('Cell size:')
