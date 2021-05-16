import sys, os
import settings
import glob
from shutil import copyfile
from osgeo import gdal
from PyQt5.QtCore import *
from qgis.core import QgsProcessingRegistry
from qgis.analysis import QgsNativeAlgorithms
from qgis.core import *
QgsApplication.setPrefixPath('/usr', True)

sys.path.append('/usr/share/qgis/python/plugins/')
from processing.core.Processing import Processing

class HidraulicConductivity:

    def __init__(self, input_file, output_file, cellSize, elevation, rattings):
        self.input_file = input_file
        self.output_file = output_file
        self.cellSize = int(cellSize)
        self.elevation = elevation
        self.rattings = rattings
        

    def calculate(self, process_path):
        qgs = QgsApplication([], False)
        
        qgs.initQgis()
        Processing.initialize()
        QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

        gdal.AllRegister()

        inputLayer = self.input_file
        process_path = process_path
        outPath = self.output_file
        cellSize = self.cellSize
        Elevation = self.elevation
        results = self.rattings

        layer = QgsVectorLayer(inputLayer, inputLayer , "ogr")
        vectorlayer_vector =  layer.dataProvider()
        # extent
        extent_rect = vectorlayer_vector.extent()
        xmin = extent_rect.xMinimum()
        xmax = extent_rect.xMaximum()
        ymin = extent_rect.yMinimum()
        ymax = extent_rect.yMaximum()
        extent = str(xmin) + "," + str(xmax) + "," + str(ymin) + "," + str(ymax)

        
        Processing.initialize()
        #conductivity = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/conductivity"
        conductivity = process_path + "/conductivity"
       
        Processing.runAlgorithm("grass7:v.to.rast",
                                {'input': inputLayer, 'type': [0, 1, 3], 'where': '', 'use': 0,
                                 'attribute_column': Elevation, 'rgb_column': None, 'label_column': None,
                                 'value': None, 'memory': 300,
                                 'output': conductivity, 'GRASS_REGION_PARAMETER': extent,
                                 'GRASS_REGION_CELLSIZE_PARAMETER': cellSize, 'GRASS_RASTER_FORMAT_OPT': '',
                                 'GRASS_RASTER_FORMAT_META': '',
                                 'GRASS_SNAP_TOLERANCE_PARAMETER': -1, 'GRASS_MIN_AREA_PARAMETER': 0.0001})

        #cond_reclassify = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/cond_reclassify.sdat"
        #Processing.runAlgorithm("saga:reclassifyvalues",
        #                        {'INPUT': conductivity, 'METHOD': 2, 'OLD': 0, 'NEW': 1, 'SOPERATOR': 0, 'MIN': 0,
        #                         'MAX': 1,
        #                         'RNEW': 2, 'ROPERATOR': 0, 'RETAB': results, 'TOPERATOR': 0, 'NODATAOPT': True,
        #                         'NODATA': 0,
        #                         'OTHEROPT': True, 'OTHERS': 0, 'RESULT': outPath})

        Processing.runAlgorithm("native:reclassifybytable",
                                    {'INPUT_RASTER': conductivity,
                                     'RASTER_BAND': 1, 'TABLE': results,
                                     'NO_DATA': -9999, 'RANGE_BOUNDARIES': 0, 'NODATA_FOR_MISSING': False,
                                     'DATA_TYPE': 5,
                                     'OUTPUT': outPath})

