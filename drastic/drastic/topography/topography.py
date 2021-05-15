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

class Topography:

    def __init__(self, input_file, output_file, cellSize, rattings):
        self.input_file = input_file
        self.output_file = output_file
        self.cellSize = int(cellSize)
        self.rattings = rattings
        

    def calculate(self, process_path):
        qgs = QgsApplication([], False)
        
        qgs.initQgis()
        Processing.initialize()
        QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

        gdal.AllRegister() 

        inputLayer_dem = self.input_file
        outPath = self.output_file
        cellSize = self.cellSize
        lista_table = self.rattings

        #inputLayer_dem = self.inputLayerCombo_dem.currentText()
        #QMessageBox.about(self, "recharge", str(inputRaster))
        gdalRaster = gdal.Open(str(inputLayer_dem))
        #QMessageBox.about(self, "recharge", str(gdalRaster))
        x = gdalRaster.RasterXSize
        y = gdalRaster.RasterYSize
        geo = gdalRaster.GetGeoTransform()  
        minx = geo[0]
        maxy = geo[3]
        maxx = minx + geo[1]*x
        miny = maxy + geo[5]*y
        extent_raster = str(minx) + "," + str(maxx) + "," + str(miny) + "," + str(maxy)  
        pixelSize = geo[1]            

        ## layer information
        #layer_raster = QgsRasterLayer(unicode(inputLayer_dem).encode('utf8'), inputLayer_dem , "gdal")         
        #rasterlayer =  layer_raster.dataProvider()
        ## extent
        #extent_rect = rasterlayer.extent()
        #xmin = extent_rect.xMinimum()
        #xmax = extent_rect.xMaximum()
        #ymin = extent_rect.yMinimum()
        #ymax = extent_rect.yMaximum()
        #extent = str(xmin) + "," + str(xmax) + "," + str(ymin) + "," + str(ymax)
        ##QMessageBox.about(self, "Topography", str(extent))
        ## cellsize
        #cellSize = layer_raster.rasterUnitsPerPixelX()
        ##cellSize = int(self.linePix.value())
        ##QMessageBox.about(self, "Topography", str(cellSize))
   
            
        # pixel size is the same as the dem raster, miss reamostragem
    
        ######Processing.initialize()
        # mdt_interp = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/mdt_interp"
        # Processing.runAlgorithm("grass7:r.surf.idw", None, inputLayer_dem, 12, False, extent_raster, pixelSize, mdt_interp)
        # mdt = mdt_interp + "." + "tif"
        
        
        #gdalMDT = gdal.Open(str(mdt_interp) + "." + "tif")
        #x_mdt = gdalMDT.RasterXSize
        #y_mdt = gdalMDT.RasterYSize            
        #geo_mdt = gdalMDT.GetGeoTransform() 
        #band_mdt = gdalMDT.GetRasterBand(1)
        #data_mdt = band_mdt.ReadAsArray(0,0,x_mdt,y_mdt)   
        #geo_mdt = gdalMDT.GetGeoTransform()  
        #minx = geo_mdt[0]
        #maxy = geo_mdt[3]
        #maxx = minx + geo_mdt[1]*x_mdt
        #miny = maxy + geo_mdt[5]*y_mdt
        #extent_raster_new = str(minx) + "," + str(maxx) + "," + str(miny) + "," + str(maxy)  
        #pixelSize_new = geo_mdt[1]            

        # slope from DEM
        ########userSlope_dem = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/slope_dem.tif"
        userSlope_dem = process_path + "/slope_dem.tif"
        Processing.runAlgorithm("grass7:r.slope.aspect",
                        {'elevation': inputLayer_dem , 'format': 1, 'precision': 0,
                        '-a': True, 'zscale': 1, 'min_slope': 0,
                        'slope': userSlope_dem,
                        'aspect': None,
                        'pcurvature': None,
                        'tcurvature': None,
                        'dx': None,
                        'dy': None,
                        'dxx': None,
                        'dyy': None,
                        'dxy': None,
                        'GRASS_REGION_PARAMETER': extent_raster + '[EPSG:3763]',
                        'GRASS_REGION_CELLSIZE_PARAMETER': pixelSize, 'GRASS_RASTER_FORMAT_OPT': '',
                        'GRASS_RASTER_FORMAT_META': ''})

        # reclassify slope raster
        #outSlope_dem = userSlope_dem + "." + "tif"
        #userSlopeRec_dem = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/slopeRec_dem"
        
        # indexes for topography
        #numberRows = int(self.tableWidget.rowCount())
        #numberColumns = int(self.tableWidget.columnCount())
        #classes = ''
        #lista = []
        #for i in range(0,numberRows):
        #    for j in range(0,numberColumns):
        #        self.line = self.tableWidget.item(i,j)
        #        lista = lista + [str(self.line.text())]
        #        string = ","
        #        intervalos = string.join(lista)
        #results = list(map(int, lista))

        #QMessageBox.about(self, "Topography", str(userSlope_dem))

        Processing.runAlgorithm("native:reclassifybytable",
                                    {'INPUT_RASTER': str(userSlope_dem),
                                     'RASTER_BAND': 1, 'TABLE': lista_table,
                                     'NO_DATA': -9999, 'RANGE_BOUNDARIES': 0, 'NODATA_FOR_MISSING': False,
                                     'DATA_TYPE': 5,
                                     'OUTPUT': outPath})
