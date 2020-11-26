from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *


class Ui_Soggicenza(object):

    def setupUi(self, Soggicenza):
        # create Depth window
        Soggicenza.setWindowModality(QtCore.Qt.ApplicationModal)
        Soggicenza.resize(400, 400)

        # input file points
        # create gridLayout
        self.gridLayout1 = QGridLayout(Soggicenza)
        self.gridLayout1.setObjectName("gridLayout1")
        # create groupBox method I
        self.groupBox_m1 = QGroupBox(Soggicenza)
        self.groupBox_m1.setObjectName("groupBox_m1")
        self.groupBox_m1.setTitle("Base")
        self.gridLayout_m1 = QGridLayout(self.groupBox_m1)
        self.gridLayout_m1.setObjectName("gridLayout_m1")
        self.gridLayout1.addWidget(self.groupBox_m1, 0, 0, 1, -1)
        # create label in gridLayout 
        self.label = QLabel(Soggicenza)
        self.label.setObjectName("label")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout_m1.addWidget(self.label, 0, 0, 1, 1)
        # create select button to input file
        self.selectButton = QPushButton(Soggicenza)
        self.selectButton.setObjectName("selectButton")
        self.gridLayout_m1.addWidget(self.selectButton, 0, 2, 1, 1)
        self.inputLayerCombo = QComboBox(Soggicenza)
        self.inputLayerCombo.setEditable(True)
        self.inputLayerCombo.setObjectName("inputLayerCombo")
        self.gridLayout_m1.addWidget(self.inputLayerCombo, 0, 1, 1, 1)
        # stretch to extend the widget in column 1
        self.gridLayout_m1.setColumnStretch(1, 1)

        # field to mask shapefile input
        self.maskLabel = QLabel(Soggicenza)
        self.maskLabel.setObjectName("maskLabel")
        self.gridLayout_m1.addWidget(self.maskLabel, 1, 0, 1, 1)
        # create select button to input mask
        self.selectMask = QPushButton(Soggicenza)
        self.selectMask.setObjectName("selectMask")
        self.gridLayout_m1.addWidget(self.selectMask, 1, 2, 1, 1)
        self.inputMaskCombo = QComboBox(Soggicenza)
        self.inputMaskCombo.setEditable(True)
        self.inputMaskCombo.setObjectName("inputMaskCombo")
        self.gridLayout_m1.addWidget(self.inputMaskCombo, 1, 1, 1, 1)
        # stretch to extend the widget in column1
        self.gridLayout_m1.setColumnStretch(1, 1)

        # field to interpolation method (the user must to choose)
        self.methodLabel = QLabel(Soggicenza)
        self.methodLabel.setObjectName("methodLabel")
        self.gridLayout1.addWidget(self.methodLabel, 2, 0, 1, 1)
        # combobox to choose the method
        self.comboBoxMethod = QComboBox(Soggicenza)
        self.comboBoxMethod.setObjectName("comboBoxMethod")
        self.gridLayout1.addWidget(self.comboBoxMethod, 2, 1, 1, -1)
        self.styles = ['Inverse Distance Weighting', 'Kriging', 'Cubic spline approximation (SAGA)',
                       'Spatial approximation using spline with tension (GRASS)']
        self.comboBoxMethod.addItems(self.styles)

        # define a groupbox to specify the cell size and attribute
        self.groupBox1 = QGroupBox(Soggicenza)
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout3 = QGridLayout(self.groupBox1)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox1, 1, 0, 1, -1)
        # define attribute "Elevation"
        self.labelAttrib = QLabel(Soggicenza)
        self.labelAttrib.setObjectName("labelAttrib")
        self.gridLayout3.addWidget(self.labelAttrib, 0, 0, -1, 1)
        self.lineAttrib = QComboBox(Soggicenza)
        self.lineAttrib.setObjectName("lineAttrib")
        self.gridLayout3.addWidget(self.lineAttrib, 0, 1, -1, 1)
        # define pixel size
        self.labelPix = QLabel(Soggicenza)
        self.labelPix.setObjectName("labelPix")
        self.gridLayout3.addWidget(self.labelPix, 0, 3, -1, 1)
        self.linePix = QSpinBox()
        self.linePix.setValue(29)
        self.linePix.stepBy(1)
        self.linePix.setObjectName("linePix")
        self.gridLayout3.addWidget(self.linePix, 0, 4, -1, 1)

        # input file mdt
        # create groupBox method II
        self.groupBox_m2 = QGroupBox(Soggicenza)
        self.groupBox_m2.setObjectName("groupBox_m2")
        self.groupBox_m2.setTitle("Improvement")
        self.gridLayout_m2 = QGridLayout(self.groupBox_m2)
        self.gridLayout_m2.setObjectName("gridLayout_m2")
        self.gridLayout1.addWidget(self.groupBox_m2, 3, 0, 1, -1)
        # create label 
        self.label_mdt = QLabel(Soggicenza)
        self.label_mdt.setObjectName("label_mdt")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout_m2.addWidget(self.label_mdt, 0, 0, 1, 1)
        # create select button to input file
        self.selectButton_mdt = QPushButton(Soggicenza)
        self.selectButton_mdt.setObjectName("selectButton_mdt")
        self.gridLayout_m2.addWidget(self.selectButton_mdt, 0, 2, 1, 1)
        self.inputLayerCombo_mdt = QComboBox(Soggicenza)
        self.inputLayerCombo_mdt.setEditable(True)
        self.inputLayerCombo_mdt.setObjectName("inputLayerCombo_mdt")
        self.gridLayout_m2.addWidget(self.inputLayerCombo_mdt, 0, 1, 1, 1)
        self.gridLayout_m2.setColumnStretch(1, 1)

        # define a groupbox to specify the maximum depth and distance
        self.groupBox_max = QGroupBox(Soggicenza)
        self.groupBox_max.setObjectName("groupBox_max")
        self.gridLayout5 = QGridLayout(self.groupBox_max)
        self.gridLayout5.setObjectName("gridLayout5")
        self.gridLayout1.addWidget(self.groupBox_max, 4, 0, 1, -1)
        # field to maximum depth
        self.label_max_depth = QLabel(Soggicenza)
        self.label_max_depth.setObjectName("label_max_depth")
        self.gridLayout5.addWidget(self.label_max_depth, 0, 0, 1, 1)
        self.line_max = QSpinBox()
        self.line_max.setValue(19)
        self.line_max.stepBy(1)
        self.line_max.setObjectName("line_max")
        self.gridLayout5.addWidget(self.line_max, 0, 1, 1, 1)
        # field to distance
        self.label_distance = QLabel(Soggicenza)
        self.label_distance.setObjectName("label_distance")
        self.gridLayout5.addWidget(self.label_distance, 0, 2, 1, 1)
        self.line_distance = QSpinBox()
        self.line_distance.setMinimum(100)
        self.line_distance.setMaximum(1000)
        self.line_distance.setValue(199)
        self.line_distance.stepBy(1)
        self.line_distance.setObjectName("line_distance")
        self.gridLayout5.addWidget(self.line_distance, 0, 3, 1, 1)
        # field to define the minimum size of basin
        self.label_size = QLabel(Soggicenza)
        self.label_size.setObjectName("label_size")
        self.gridLayout5.addWidget(self.label_size, 0, 4, 1, 1)
        self.line_size = QSpinBox()
        self.line_size.setMinimum(49)
        self.line_size.setMaximum(1000)
        self.line_size.setValue(49)
        self.line_size.stepBy(1)
        self.line_size.setObjectName("line_size")
        self.gridLayout5.addWidget(self.line_size, 0, 5, 1, 1)
        # stretch to extend the widget in column 1
        self.gridLayout5.setColumnStretch(1, 1)

        # define the indexs
        # create a group box
        self.groupBox = QGroupBox(Soggicenza)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox, 5, 0, 1, -1)


        # output file
        # create label in gridLayout
        self.label3 = QLabel(Soggicenza)
        self.label3.setObjectName("label3")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label3, 6, 0, 1, 1)
        # create select button to input file
        self.selectButton3 = QPushButton(Soggicenza)
        self.selectButton3.setObjectName("selectButton3")
        self.gridLayout1.addWidget(self.selectButton3, 6, 2, 1, 1)
        self.inputLayerCombo3 = QLineEdit(Soggicenza)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")
        self.gridLayout1.addWidget(self.inputLayerCombo3, 6, 1, 1, 1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1, 1)

        # button Ok, Close and Help
        self.buttonBox = QDialogButtonBox(Soggicenza)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Help | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 7, 1, 1, 1)

        self.retranslateUi(Soggicenza)
        self.buttonBox.rejected.connect(Soggicenza.close)

    def retranslateUi(self, Soggicenza):
        Soggicenza.setWindowTitle('Soggicenza (S)')
        self.label.setText('Input file points:')
        self.label_mdt.setText('Input file MDT:')
        self.selectButton.setText('Browse')
        self.selectButton_mdt.setText('Browse')
        self.selectMask.setText('Browse')
        self.methodLabel.setText("Interpolation Method")
        self.maskLabel.setText("Mask:")
        self.label3.setText('Output file:')
        self.selectButton3.setText('Browse')
        # self.labelWeight.setText(QtGui.QApplication.translate('Depth Groundwater (D)', 'Weight:', None, QtGui.QApplication.UnicodeUTF8))
        self.labelAttrib.setText('Attribute:')
        self.labelPix.setText('Cell size:')
        self.label_max_depth.setText('Maximum depth:')
        self.label_distance.setText('Distance:')
        self.label_size.setText('Minimum size of watershed basin:')