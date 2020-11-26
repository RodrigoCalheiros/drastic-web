from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *
from .Ui_stats import Ui_stats

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
#from .stats_window import stats_window


class stats(QDialog, Ui_stats):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.selectButton.clicked.connect(self.fillInputFileEdit)
        self.selectButton3.clicked.connect(self.fillOutputFileEdit)
        self.buttonBox.accepted.connect(self.convert)
        self.plugin_dir = os.path.dirname(__file__)

    # INPUT VECTOR FILE PRECIPITATION
    def fillInputFileEdit(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedVectorFilter()
        inputFile, encoding = GdalTools_utils.FileDialog.getOpenFileName(self, self.tr("Select the input file"),
                                                                         GdalTools_utils.FileFilter.allVectorsFilter(),
                                                                         lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo.addItem(inputFile)
        check = QFile(inputFile)

    # OUTPUT RASTER FILE
    def fillOutputFileEdit(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedRasterFilter()
        outputFile = GdalTools_utils.FileDialog.getSaveFileName(self, self.tr(
            "Select the html file to save the results to"), ".html",
                                                                lastUsedFilter)

        self.inputLayerCombo3.setText(outputFile + '.html')

    def convert(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(False)

        inputLayer = self.inputLayerCombo.currentText()
        gdal.AllRegister()

        outPath = self.inputLayerCombo3.text()

        Processing.initialize()

        Processing.runAlgorithm("qgis:rasterlayerstatistics",
                       {'INPUT': inputLayer, 'BAND': 1,
                        'OUTPUT_HTML_FILE': outPath})

        if self.checkbox2.isChecked():
            outPath2 = outPath + '.rtf'
            Processing.runAlgorithm("qgis:rasterlayerstatistics",
                                    {'INPUT': inputLayer, 'BAND': 1,
                                     'OUTPUT_HTML_FILE': outPath2})


        QMessageBox.information(self, self.tr("Finished"), self.tr("Statistics completed. Please check the folder."))

        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)