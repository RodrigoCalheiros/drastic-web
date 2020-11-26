from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *
from .Ui_Topography import Ui_Topography
from . import GdalTools_utils
try:
    from qgis.PyQt.QtCore import QString
except ImportError:
    QString = str
from processing.core.Processing import Processing
#from processing.core.ProcessingGdalTools_utils import ProcessingGdalTools_utils
from . import ftools_utils
from osgeo import ogr
from processing import *
from osgeo.gdalconst import GA_ReadOnly
from osgeo import gdal
from processing import ProcessingPlugin
from processing.core.Processing import Processing
#from processing.outputs import OutputRaster
import sys, os
import numpy
from .Ui_God import Ui_God
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis.PyQt import QtCore, QtGui

class God(QDialog, Ui_God):
    
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)  
    
        self.selectButton.clicked.connect(self.fillInputFileEdit)
        self.selectButton2.clicked.connect(self.fillInputFileEdit2)
        self.selectButton3.clicked.connect(self.fillInputFileEdit3)
       
        self.selectButton_out.clicked.connect(self.fillOutputFileEdit)
        #self.selectButton_color.clicked.connect(self.fillOutputFileEdit_color)
        self.buttonBox.accepted.connect(self.convert)
        
        # connect help
        #self.buttonBox.button(QtGui.QDialogButtonBox.Help), SIGNAL("clicked()"), self.help)
        
    def help(self):
        QMessageBox.about(self, "DRASTIC", """<p><b>DRASTIC Index</b></p> 
        <p><b>Definition:</b>The last feature, the DRASTIC index, corresponds to the final map, which results from the sum of the seven factor
        maps created before multiplied by the corresponding weights as defined in equation 1, according to Aller et al. (1987).  </p>
        <p><b>DRASTIC</b> = DR x DW + RR x RW + AR x AW + SR x SW + TR x TW + IR x IW + CR x CW	(1)</p>
        <p>R and W (in subscript) correspond to the rating and weight for each factor, respectively. 
        The DRASTIC interface is composed by seven input files corresponding to D, R, A, S, T, I and C raster files, and an output file corresponding to DRASTIC index map. </p>
        <p><b>Method</b></p> 
        <p>Input files = seven raster created before. The user must to define the weight values which are defined according Aller et al (1987) by default.  </p>
        <p><b>Output file:</b> DRASTIC raster file without color or DRASTIC COLORED with the colors and intervals defined according to Aller et al. (1987)</p>""")  
      
 # INPUT RASTER FILE
    def fillInputFileEdit(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedRasterFilter()
        inputFile, encoding = GdalTools_utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), GdalTools_utils.FileFilter.allRastersFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo.addItem(inputFile)
        check = QFile(inputFile)     
        
    def fillInputFileEdit2(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedRasterFilter()
        inputFile, encoding = GdalTools_utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), GdalTools_utils.FileFilter.allRastersFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo2.addItem(inputFile)
        check = QFile(inputFile)    
        
    def fillInputFileEdit3(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedRasterFilter()
        inputFile, encoding = GdalTools_utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), GdalTools_utils.FileFilter.allRastersFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo3.addItem(inputFile)
        check = QFile(inputFile) 
            
   
            
# --------------------------------------- // ----------------------------------------------------- // ------------------------------------------------------------------------------

# OUTPUT RASTER FILE
    def fillOutputFileEdit(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedRasterFilter()
        outputFile = GdalTools_utils.FileDialog.getSaveFileName(self, self.tr( "Select the raster file to save the results to" ), GdalTools_utils.FileFilter.allRastersFilter(), lastUsedFilter )
        self.outputLayerCombo.setText(outputFile)
        

    def fillOutputFileEdit_color(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedRasterFilter()
        outputFile = GdalTools_utils.FileDialog.getSaveFileName(self, self.tr( "Select the raster file to save the results to" ), GdalTools_utils.FileFilter.allRastersFilter(), ".sdat" )
        self.outputLayerCombo_color.setText(outputFile)

# DRASTIC CALCULATION
    def convert(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(False)
        # read D raster
        inputLayer = self.inputLayerCombo.currentText()
        # read R raster
        inputLayer2 = self.inputLayerCombo2.currentText()
        # read A raster
        inputLayer3 = self.inputLayerCombo3.currentText()
        
        # outpath
        outPath = self.outputLayerCombo.text()

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

        # resamp_g = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/resamp_g_god.sdat"
        # # Processing.runAlgorithm("saga:resampling", None, impact_weight, True, 0, 0, extent, pixelSize, resamp_i)
        # Processing.runAlgorithm("saga:resampling",
        #                         {'INPUT': inputLayer, 'KEEP_TYPE': True, 'SCALE_UP': 0,
        #                          'SCALE_DOWN': 0,
        #                          'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': extent + '[EPSG:3763]',
        #                          'TARGET_USER_SIZE': pixelSize, 'TARGET_USER_FITS': 0, 'TARGET_TEMPLATE': None,
        #                          'OUTPUT': resamp_g})
        #
        # resamp_o = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/resamp_o_god.sdat"
        # # Processing.runAlgorithm("saga:resampling", None, impact_weight, True, 0, 0, extent, pixelSize, resamp_i)
        # Processing.runAlgorithm("saga:resampling",
        #                         {'INPUT': inputLayer2, 'KEEP_TYPE': True, 'SCALE_UP': 0,
        #                          'SCALE_DOWN': 0,
        #                          'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': extent + '[EPSG:3763]',
        #                          'TARGET_USER_SIZE': pixelSize, 'TARGET_USER_FITS': 0, 'TARGET_TEMPLATE': None,
        #                          'OUTPUT': resamp_o})
        #
        # resamp_d = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/resamp_d_god.sdat"
        # # Processing.runAlgorithm("saga:resampling", None, impact_weight, True, 0, 0, extent, pixelSize, resamp_i)
        # Processing.runAlgorithm("saga:resampling",
        #                         {'INPUT': inputLayer3, 'KEEP_TYPE': True, 'SCALE_UP': 0,
        #                          'SCALE_DOWN': 0,
        #                          'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': extent + '[EPSG:3763]',
        #                          'TARGET_USER_SIZE': pixelSize, 'TARGET_USER_FITS': 0, 'TARGET_TEMPLATE': None,
        #                          'OUTPUT': resamp_d})

        # Processing.runAlgorithm("gdal:rastercalculator",
        #                         {'INPUT_A': resamp_g,
        #                          'BAND_A': 1,
        #                          'INPUT_B': resamp_o,
        #                          'BAND_B': 1,
        #                          'INPUT_C': resamp_d,
        #                          'BAND_C': 1,
        #                          'INPUT_D': None,
        #                          'BAND_D': -1, 'INPUT_E': None, 'BAND_E': -1, 'INPUT_F': None, 'BAND_F': -1,
        #                          'FORMULA': 'A*B*C',
        #                          'NO_DATA': None, 'RTYPE': 5, 'EXTRA': '', 'OPTIONS': '',
        #                          'OUTPUT': outPath})

        Processing.runAlgorithm("grass7:r.mapcalc.simple", {'a': inputLayer,
                                                            'b': inputLayer2,
                                                            'c': inputLayer3,
                                                            'd': inputLayer,
                                                            'e': inputLayer,
                                                            'f': inputLayer,
                                                            'expression': 'A*B*C',
                                                            'output': outPath,
                                                            'GRASS_REGION_PARAMETER': extent + '[EPSG:3763]',
                                                            'GRASS_REGION_CELLSIZE_PARAMETER': pixelSize,
                                                            'GRASS_RASTER_FORMAT_OPT': '',
                                                            'GRASS_RASTER_FORMAT_META': ''})




        # lista = []
        # lista.append(inputLayer2)
        # lista.append(inputLayer3)
        #
        # gdal.AllRegister()
        # Processing.initialize()
        # Processing.runAlgorithm("saga:rastercalculator", None,inputLayer, ';'.join(lista), "a*b*c", 3, False, 7, outPath)

        file_info_norm = QFileInfo(str(outPath))
        # QMessageBox.about(self, "teste", str(file_info_norm))
        rlayer_new_norm = QgsRasterLayer(outPath, file_info_norm.fileName(), 'gdal')
        # QMessageBox.about(self, "teste", str(rlayer_new_norm))
        QgsProject.instance().addMapLayer(rlayer_new_norm)
        self.iface.canvas.setExtent(rlayer_new_norm.extent())
        # set the map canvas layer set
        self.iface.canvas.setLayers([rlayer_new_norm])

        # colorfile = 'C:/OSGeo4W64/apps/qgis/python/plugins/DRASTIC/colorfile.clr'
        # outPath_color = self.outputLayerCombo_color.text()
        # from colorize import raster2png
        #
        #
        #
        # if self.checkcolor.isChecked():
        #     # add result into canvas
        #     file_info = QFileInfo(outPath_color)
        #     if file_info.exists():
        #         layer_name = file_info.baseName()
        #     else:
        #         return False
        #     rlayer_new = QgsRasterLayer(outPath_color, layer_name)
        #     if rlayer_new.isValid():
        #         QgsMapLayerRegistry.instance().addMapLayer(rlayer_new)
        #         layer = QgsMapCanvasLayer(rlayer_new)
        #         layerList = [layer]
        #         extent = self.iface.canvas.setExtent(rlayer_new.extent())
        #         self.iface.canvas.setLayerSet(layerList)
        #         self.iface.canvas.setVisible(True)
        #         return True
        #     else:
        #         return False
        #     QMessageBox.information(self, self.tr( "Finished" ), self.tr( "DRASTIC completed." ) )
        
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True) 