from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *
from .Ui_SINTACS import Ui_SINTACS
from .NormalI_window import NormalI_window
from .SevereI_window import SevereI_window
from .Seepage_window import Seepage_window
from .Karst_window import Karst_window
from .Fissured_window import Fissured_window
from .Nitrates_window import Nitrates_window
from . import GdalTools_utils

try:
    from qgis.PyQt.QtCore import QString
except ImportError:
    QString = str
import os, sys
from processing.core.Processing import Processing
from osgeo import ogr
from . import ftools_utils
from osgeo import gdal
import numpy
from qgis.PyQt import QtCore, QtGui


class SINTACS(QDialog, Ui_SINTACS):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.selectButton.clicked.connect(self.doNormalI_window)
        self.selectButton2.clicked.connect(self.doSevereI_window)
        self.selectButton3.clicked.connect(self.doSeepage_window)
        self.selectButton4.clicked.connect(self.doKarst_window)
        self.selectButton5.clicked.connect(self.doFissured_window)
        self.selectButton6.clicked.connect(self.doNitrates_window)


    def doNormalI_window(self):
        self.dlgwindow = NormalI_window(self)
        if NormalI_window ==0:
            return
        self.dlgwindow.show()

    def doSevereI_window(self):
        self.dlgwindow = SevereI_window(self)
        if SevereI_window ==0:
            return
        self.dlgwindow.show()

    def doSeepage_window(self):
        self.dlgwindow = Seepage_window(self)
        if Seepage_window == 0:
            return
        self.dlgwindow.show()

    def doKarst_window(self):
        self.dlgwindow = Karst_window(self)
        if Karst_window == 0:
            return
        self.dlgwindow.show()

    def doFissured_window(self):
        self.dlgwindow = Fissured_window(self)
        if Fissured_window == 0:
            return
        self.dlgwindow.show()

    def doNitrates_window(self):
        self.dlgwindow = Nitrates_window(self)
        if Nitrates_window == 0:
            return
        self.dlgwindow.show()