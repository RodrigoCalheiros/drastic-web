from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *


class Ui_SINTACS(object):

    def setupUi(self, SINTACS_window):
        # create SINTACS window
        SINTACS_window.setWindowModality(QtCore.Qt.ApplicationModal)
        SINTACS_window.resize(450, 400)

        # input file
        # create gridLayout
        self.gridLayout1 = QGridLayout(SINTACS_window)
        self.gridLayout1.setObjectName("gridLayout1")
        # group box to input files
        self.groupBox = QGroupBox(SINTACS_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox, 0, 0, 1, -1)

        # create select button to input file
        self.selectButton = QPushButton(SINTACS_window)
        self.selectButton.setObjectName("selectButton")
        self.selectButton2 = QPushButton(SINTACS_window)
        self.selectButton2.setObjectName("selectButton2")
        self.selectButton3 = QPushButton(SINTACS_window)
        self.selectButton3.setObjectName("selectButton3")
        self.selectButton4 = QPushButton(SINTACS_window)
        self.selectButton4.setObjectName("selectButton4")
        self.selectButton5 = QPushButton(SINTACS_window)
        self.selectButton5.setObjectName("selectButton5")
        self.selectButton6 = QPushButton(SINTACS_window)
        self.selectButton6.setObjectName("selectButton6")
        self.gridLayout2.addWidget(self.selectButton, 0, 4, 1, 1)
        self.gridLayout2.addWidget(self.selectButton2, 1, 4, 1, 1)
        self.gridLayout2.addWidget(self.selectButton3, 2, 4, 1, 1)
        self.gridLayout2.addWidget(self.selectButton4, 3, 4, 1, 1)
        self.gridLayout2.addWidget(self.selectButton5, 4, 4, 1, 1)
        self.gridLayout2.addWidget(self.selectButton6, 5, 4, 1, 1)

        # button Ok, Close and Help
        self.buttonBox = QDialogButtonBox(SINTACS_window)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Help | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 2, 1, 1, 1)

        self.retranslateUi(SINTACS_window)
        self.buttonBox.rejected.connect(SINTACS_window.close)

    def retranslateUi(self, SINTACS_window):
        SINTACS_window.setWindowTitle('SINTACS')
        self.groupBox.setTitle("Hydrogeological Impact")
        self.selectButton.setText('Normal Impact')
        self.selectButton2.setText('Severe Impact')
        self.selectButton3.setText('Seepage')
        self.selectButton4.setText('Karst')
        self.selectButton5.setText('Fissured')
        self.selectButton6.setText('Nitrates')