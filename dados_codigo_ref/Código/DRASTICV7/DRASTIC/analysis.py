from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *
from .Ui_analysis import Ui_analysis

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
#from .analysis_window import analysis_window


class analysis(QDialog, Ui_analysis):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.selectButton.clicked.connect(self.fillInputFileEdit)
        self.selectButton2.clicked.connect(self.fillInputFileEdit2)
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

        inputLayer = self.inputLayerCombo.currentText()
        gdal.AllRegister()
        gdalRaster = gdal.Open(str(inputLayer))
        band = gdalRaster.GetRasterBand(1)
        # get minimum and maximum raster
        # Get raster statistics
        stats = band.GetStatistics(True, True)
        min1 = stats[0]
        max1 = stats[1]
        self.linePixmin.setValue(int(min1))
        self.linePixmax.setValue(int(max1))

    # INPUT VECTOR FILE PRECIPITATION
    def fillInputFileEdit2(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedVectorFilter()
        inputFile, encoding = GdalTools_utils.FileDialog.getOpenFileName(self, self.tr("Select the input file"),
                                                                         GdalTools_utils.FileFilter.allVectorsFilter(),
                                                                         lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo2.addItem(inputFile)
        check = QFile(inputFile)

        inputLayer2 = self.inputLayerCombo2.currentText()
        gdal.AllRegister()
        gdalRaster2 = gdal.Open(str(inputLayer2))
        band2 = gdalRaster2.GetRasterBand(1)
        # get minimum and maximum raster
        # Get raster statistics
        stats2 = band2.GetStatistics(True, True)
        min2 = stats2[0]
        max2 = stats2[1]
        self.linePixmin2.setValue(int(min2))
        self.linePixmax2.setValue(int(max2))

    # OUTPUT RASTER FILE
    def fillOutputFileEdit(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedRasterFilter()
        outputFile = GdalTools_utils.FileDialog.getSaveFileName(self, self.tr(
            "Select the raster file to save the results to"), '.sdat',
                                                                lastUsedFilter)

        self.inputLayerCombo3.setText(outputFile + '.sdat')

    def convert(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(False)

        inputLayer = self.inputLayerCombo.currentText()
        inputLayer2 = self.inputLayerCombo2.currentText()
        gdal.AllRegister()

        # sum of the raster = SI
        # D
        gdalRaster = gdal.Open(str(inputLayer))
        # # multiply by weight
        # depth_weight = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/depth_weight"
        x = gdalRaster.RasterXSize
        y = gdalRaster.RasterYSize
        geo = gdalRaster.GetGeoTransform()
        # # pixel size
        pixelSize = geo[1]
        # extent
        minx = geo[0]
        maxy = geo[3]
        maxx = minx + geo[1] * x
        miny = maxy + geo[5] * y
        extent = str(minx) + "," + str(maxx) + "," + str(miny) + "," + str(maxy)
        band = gdalRaster.GetRasterBand(1)

        outPath = self.inputLayerCombo3.text()


        Processing.initialize()

        normalize1 = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/normalize1"
        Processing.runAlgorithm("grass7:r.rescale",
                       {'input': inputLayer,
                        'from': [self.linePixmin.value(), self.linePixmax.value()], 'to': [0, 100],
                        'output': normalize1,
                        'GRASS_REGION_PARAMETER': str(extent) + '[EPSG:3763]',
                        'GRASS_REGION_CELLSIZE_PARAMETER': pixelSize, 'GRASS_RASTER_FORMAT_OPT': '',
                        'GRASS_RASTER_FORMAT_META': ''})

        normalize2 = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/normalize2"
        Processing.runAlgorithm("grass7:r.rescale",
                                {'input': inputLayer2,
                                 'from': [self.linePixmin2.value(), self.linePixmax2.value()], 'to': [0, 100],
                                 'output': normalize2,
                                 'GRASS_REGION_PARAMETER': str(extent) + '[EPSG:3763]',
                                 'GRASS_REGION_CELLSIZE_PARAMETER': pixelSize, 'GRASS_RASTER_FORMAT_OPT': '',
                                 'GRASS_RASTER_FORMAT_META': ''})



        # Processing.runAlgorithm("gdal:rastercalculator", {'INPUT_A': normalize1 + '.sdat', 'BAND_A': 1,
        #                                          'INPUT_B': normalize2 + '.sdat', 'BAND_B': 1,
        #                                          'INPUT_C': None, 'BAND_C': -1, 'INPUT_D': None, 'BAND_D': -1,
        #                                          'INPUT_E': None, 'BAND_E': -1, 'INPUT_F': None, 'BAND_F': -1,
        #                                          'FORMULA': 'A-B', 'NO_DATA': None, 'RTYPE': 6, 'OPTIONS': '',
        #                                          'OUTPUT': outPath})

        Processing.runAlgorithm("grass7:r.mapcalc.simple", {'a': normalize1 + '.sdat',
                                                            'b': normalize2+'.sdat',
                                                            'c': normalize2+'.sdat',
                                                            'd': normalize1+'.sdat',
                                                            'e': normalize2+'.sdat',
                                                            'f': normalize1+'.sdat',
                                                            'expression': 'A-B',
                                                            'output': outPath,
                                                            'GRASS_REGION_PARAMETER': extent + '[EPSG:3763]',
                                                            'GRASS_REGION_CELLSIZE_PARAMETER': 30,
                                                            'GRASS_RASTER_FORMAT_OPT': '',
                                                            'GRASS_RASTER_FORMAT_META': ''})

        # add result into canvas
        # add result into canvas
        file_info_norm = QFileInfo(str(outPath))
        # QMessageBox.about(self, "teste", str(file_info_norm))
        rlayer_new_norm = QgsRasterLayer(outPath, file_info_norm.fileName(), 'gdal')
        # QMessageBox.about(self, "teste", str(rlayer_new_norm))
        QgsProject.instance().addMapLayer(rlayer_new_norm)
        self.iface.canvas.setExtent(rlayer_new_norm.extent())
        # set the map canvas layer set
        self.iface.canvas.setLayers([rlayer_new_norm])
        QMessageBox.information(self, self.tr("Finished"), self.tr("Analysis completed."))

        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)