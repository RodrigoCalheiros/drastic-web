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

class Si:

    def __init__(self, input_file_g, input_file_r, input_file_a, input_file_t, input_file_lu, weight_g, weight_r, weight_a, weight_t, weight_lu, output_file, cellSize):
        self.input_file_g = input_file_g
        self.input_file_r = input_file_r
        self.input_file_a = input_file_a
        self.input_file_t = input_file_t
        self.input_file_lu = input_file_lu
        self.weight_g = weight_g
        self.weight_r = weight_r
        self.weight_a = weight_a
        self.weight_t = weight_t
        self.weight_lu = weight_lu
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
        inputLayer2 = self.input_file_r
        #bn_inputLayer2 = str(os.path.splitext(os.path.basename(inputLayer2))[0])

        # read A raster
        inputLayer3 = self.input_file_a
        #bn_inputLayer3 = str(os.path.splitext(os.path.basename(inputLayer3))[0])

        # read S raster
        inputLayer4 = self.input_file_t
        #bn_inputLayer4 = str(os.path.splitext(os.path.basename(inputLayer4))[0])

        # read T raster
        inputLayer5 = self.input_file_lu
        #bn_inputLayer5 = str(os.path.splitext(os.path.basename(inputLayer5))[0])

        
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

        #resamp_d = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/resamp_d_drastic.sdat"
        resamp_g = process_path + "resamp_g.sdat"

        params = {
            'input' : inputLayer,
            'output' : resamp_g,
            'GRASS_REGION_PARAMETER':extent,
            'GRASS_REGION_CELLSIZE_PARAMETER':0,
            'GRASS_RASTER_FORMAT_OPT':'',
            'GRASS_RASTER_FORMAT_META':''
        }

        Processing.runAlgorithm("grass7:r.resample", params)
        
        # Processing.runAlgorithm("saga:resampling", None, recharge_weight, True, 0, 0, extent, pixelSize, resamp_r)
        #try:
        #    Processing.runAlgorithm("saga:resampling",
        #                            {'INPUT': inputLayer, 'KEEP_TYPE': True, 'SCALE_UP': 0,
        #                             'SCALE_DOWN': 0,
        #                             'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': extent + '[EPSG:3763]',
        #                             'TARGET_USER_SIZE': pixelSize, 'TARGET_USER_FITS': 0, 'TARGET_TEMPLATE': None,
        #                             'OUTPUT': resamp_d})
        #except:
        #    Processing.runAlgorithm("saga:resampling",
        #                            {'INPUT': inputLayer, 'KEEP_TYPE': True, 'SCALE_UP': 0,
        #                             'SCALE_DOWN': 0,
        #                             'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': extent + '[EPSG:3763]',
        #                             'TARGET_USER_SIZE': pixelSize, 'TARGET_USER_FITS': 0, 'TARGET_TEMPLATE': None,
        #                             'OUTPUT': resamp_d})

        #resamp_r = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/resamp_r_drastic.sdat"
        resamp_r = process_path + "resamp_r.sdat"

        params = {
            'input' : inputLayer2,
            'output' : resamp_r,
            'GRASS_REGION_PARAMETER':extent,
            'GRASS_REGION_CELLSIZE_PARAMETER':0,
            'GRASS_RASTER_FORMAT_OPT':'',
            'GRASS_RASTER_FORMAT_META':''
        }

        Processing.runAlgorithm("grass7:r.resample", params)

        #try:
        #    Processing.runAlgorithm("saga:resampling",
        #                            {'INPUT': inputLayer2, 'KEEP_TYPE': True, 'SCALE_UP': 0,
        #                             'SCALE_DOWN': 0,
        #                             'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': extent + '[EPSG:3763]',
        #                             'TARGET_USER_SIZE': pixelSize, 'TARGET_USER_FITS': 0, 'TARGET_TEMPLATE': None,
        #                             'OUTPUT': resamp_r})
        #except:
        #    Processing.runAlgorithm("saga:resampling",
        #                            {'INPUT': inputLayer2, 'KEEP_TYPE': True, 'SCALE_UP': 0,
        #                             'SCALE_DOWN': 0,
        #                             'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': extent + '[EPSG:3763]',
        #                             'TARGET_USER_SIZE': pixelSize, 'TARGET_USER_FITS': 0, 'TARGET_TEMPLATE': None,
        #                             'OUTPUT': resamp_r})



        #resamp_a = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/resamp_a_drastic.sdat"
        resamp_a = process_path + "resamp_a.sdat"

        params = {
            'input' : inputLayer3,
            'output' : resamp_a,
            'GRASS_REGION_PARAMETER':extent,
            'GRASS_REGION_CELLSIZE_PARAMETER':0,
            'GRASS_RASTER_FORMAT_OPT':'',
            'GRASS_RASTER_FORMAT_META':''
        }

        Processing.runAlgorithm("grass7:r.resample", params)
        
        #try:
        # Processing.runAlgorithm("saga:resampling", None, recharge_weight, True, 0, 0, extent, pixelSize, resamp_r)
        #    Processing.runAlgorithm("saga:resampling",
        #                            {'INPUT': inputLayer3, 'KEEP_TYPE': True, 'SCALE_UP': 0,
        #                             'SCALE_DOWN': 0,
        #                             'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': extent + '[EPSG:3763]',
        #                             'TARGET_USER_SIZE': pixelSize, 'TARGET_USER_FITS': 0, 'TARGET_TEMPLATE': None,
        #                             'OUTPUT': resamp_a})
        #except:
        #    Processing.runAlgorithm("saga:resampling",
        #                            {'INPUT': inputLayer3, 'KEEP_TYPE': True, 'SCALE_UP': 0,
        #                             'SCALE_DOWN': 0,
        #                             'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': extent + '[EPSG:3763]',
        #                             'TARGET_USER_SIZE': pixelSize, 'TARGET_USER_FITS': 0, 'TARGET_TEMPLATE': None,
        #                             'OUTPUT': resamp_a})

        #resamp_s = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/resamp_s_drastic.sdat"
        resamp_t = process_path + "resamp_t.sdat"

        params = {
            'input' : inputLayer4,
            'output' : resamp_t,
            'GRASS_REGION_PARAMETER':extent,
            'GRASS_REGION_CELLSIZE_PARAMETER':0,
            'GRASS_RASTER_FORMAT_OPT':'',
            'GRASS_RASTER_FORMAT_META':''
        }

        Processing.runAlgorithm("grass7:r.resample", params)
        #try:
        # Processing.runAlgorithm("saga:resampling", None, recharge_weight, True, 0, 0, extent, pixelSize, resamp_r)
        #    Processing.runAlgorithm("saga:resampling",
        #                            {'INPUT': inputLayer4, 'KEEP_TYPE': True, 'SCALE_UP': 0,
        #                             'SCALE_DOWN': 0,
        #                             'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': extent + '[EPSG:3763]',
        #                             'TARGET_USER_SIZE': pixelSize, 'TARGET_USER_FITS': 0, 'TARGET_TEMPLATE': None,
        #                             'OUTPUT': resamp_s})
        #except:
        #    Processing.runAlgorithm("saga:resampling",
        #                            {'INPUT': inputLayer4, 'KEEP_TYPE': True, 'SCALE_UP': 0,
        #                             'SCALE_DOWN': 0,
        #                             'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': extent + '[EPSG:3763]',
        #                             'TARGET_USER_SIZE': pixelSize, 'TARGET_USER_FITS': 0, 'TARGET_TEMPLATE': None,
        #                             'OUTPUT': resamp_s})

        #resamp_t = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/resamp_t_drastic.sdat"
        resamp_lu = process_path + "resamp_lu.sdat"

        params = {
            'input' : inputLayer5,
            'output' : resamp_lu,
            'GRASS_REGION_PARAMETER':extent,
            'GRASS_REGION_CELLSIZE_PARAMETER':0,
            'GRASS_RASTER_FORMAT_OPT':'',
            'GRASS_RASTER_FORMAT_META':''
        }

        Processing.runAlgorithm("grass7:r.resample", params)

        si = process_path + "si.sdat"

        Processing.runAlgorithm("grass7:r.mapcalc.simple", {
            'a': resamp_g,
            'b': resamp_r, 
            'c': resamp_a, 
            'd': resamp_t, 
            'e': resamp_lu, 
            'f': None, 
            'expression': 'A*' + str(self.weight_g) + '+B*' + str(self.weight_r) + '+C*' + str(self.weight_a) + '+D*' + str(self.weight_t) + '+E*' + str(self.weight_lu),
            'output': outPath,
            'GRASS_REGION_PARAMETER': extent+' [EPSG:3763]',
            'GRASS_REGION_CELLSIZE_PARAMETER': pixelSize, 'GRASS_RASTER_FORMAT_OPT': '', 'GRASS_RASTER_FORMAT_META': ''})
