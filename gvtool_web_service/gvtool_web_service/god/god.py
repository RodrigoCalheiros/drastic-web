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

class God:

    def __init__(self, input_file_g, input_file_o, input_file_d, output_file, cellSize):
        self.input_file_g = input_file_g
        self.input_file_o = input_file_o
        self.input_file_d = input_file_d
        self.output_file = output_file
        self.cellSize = int(cellSize)
        

    def calculate(self, process_path):
        qgs = QgsApplication([], False)
        
        qgs.initQgis()
        Processing.initialize()
        QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

        gdal.AllRegister()

        process_path = process_path
        outPath = self.output_file
        cellSize = self.cellSize

        # read D raster
        inputLayer = self.input_file_g
        #bn_inputLayer = str(os.path.splitext(os.path.basename(inputLayer))[0])
        #teste = str(bn_inputLayer) + '@1\''
        #QMessageBox.about(self, "drastic", str(teste))
        # read R raster
        inputLayer2 = self.input_file_o
        #bn_inputLayer2 = str(os.path.splitext(os.path.basename(inputLayer2))[0])

        # read A raster
        inputLayer3 = self.input_file_d
        #bn_inputLayer3 = str(os.path.splitext(os.path.basename(inputLayer3))[0])

        # outpath
        #outPath = self.outputLayerCombo.text()  

        #gdal.AllRegister()
        
        # sum of the raster = DRASTIC
        # D
        gdalRaster = gdal.Open(str(inputLayer))
        # # multiply by weight
        # depth_weight = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/depth_weight"
        x = gdalRaster.RasterXSize
        y = gdalRaster.RasterYSize
        geo = gdalRaster.GetGeoTransform()
        # band = gdalRaster.GetRasterBand(1)
        # data = band.ReadAsArray(0,0,x,y)
        # mul = numpy.multiply(data, int(self.lineWeightD.value()))
        # # Create an output imagedriver with the reclassified values multiplied by the weight
        # driver = gdal.GetDriverByName( "GTiff" )
        # outData = driver.Create(str(depth_weight), x,y,1, gdal.GDT_Float32)
        # outData.GetRasterBand(1).WriteArray(mul)
        # outData.SetGeoTransform(geo)
        # outData = None
        #
        # geo = gdalRaster.GetGeoTransform()
        # # pixel size
        pixelSize = geo[1]
        #pixelSize = 30
        # extent
        minx = geo[0]
        maxy = geo[3]
        maxx = minx + geo[1]*x
        miny = maxy + geo[5]*y
        extent = str(minx) + "," + str(maxx) + "," + str(miny) + "," + str(maxy)
        band = gdalRaster.GetRasterBand(1)
        #data_d = band.ReadAsArray(0,0,x,y)

        Processing.initialize()

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

