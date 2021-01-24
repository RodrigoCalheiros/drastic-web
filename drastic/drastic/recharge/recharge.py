import sys, os
from osgeo import gdal
from PyQt5.QtCore import *
from qgis.core import QgsProcessingRegistry
from qgis.analysis import QgsNativeAlgorithms
from qgis.core import *
QgsApplication.setPrefixPath('/usr', True)

sys.path.append('/usr/share/qgis/python/plugins/')
from processing.core.Processing import Processing

class Recharge:

    def __init__(self, input_file, output_file, rattings):
        self.input_mdt = input_file
        self.output_file = output_file
        self.rattings = rattings
        

    def convert_mdt(self, process_path):
        qgs = QgsApplication([], False)
        qgs.initQgis()
        Processing.initialize()
            
        QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

        gdal.AllRegister()

        #for alg in QgsApplication.processingRegistry().algorithms():
        #    print(alg.id(), "->", alg.displayName())

        # read mdt data
        inputRaster = self.input_mdt
        process_path = process_path
        outPath2 = self.output_file
        
        
        gdalRaster = gdal.Open(str(inputRaster))

        x = gdalRaster.RasterXSize
        y = gdalRaster.RasterYSize
        geo = gdalRaster.GetGeoTransform()  
        minx = geo[0]
        maxy = geo[3]
        maxx = minx + geo[1]*x
        miny = maxy + geo[5]*y
        #extent_raster = str(minx) + "," + str(maxx) + "," + str(miny) + "," + str(maxy)  
        #pixelSize = geo[1]
        band_mdt = gdalRaster.GetRasterBand(1)
        #data_mdt = band_mdt.ReadAsArray(0, 0, x, y)
        
        Processing.initialize()
        # mdt_interp = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/mdt_interp"
        # Processing.runAlgorithm("grass7:r.surf.idw", None, inputRaster, 12, False, extent_raster, pixelSize, mdt_interp)
        # mdt = mdt_interp + "." + "tif"
        #
        # gdalMDT = gdal.Open(str(mdt_interp) + "." + "tif")
        # x_mdt = gdalMDT.RasterXSize
        # y_mdt = gdalMDT.RasterYSize
        # geo_mdt = gdalMDT.GetGeoTransform()
        # band_mdt = gdalMDT.GetRasterBand(1)
        # data_mdt = band_mdt.ReadAsArray(0,0,x_mdt,y_mdt)
        # coeficients a and b of the regression lines, y = ax + b, used for mean monthly precipitation, y(mm), as a function of altitude, x(m)
        # a = 0.99
        # b = 542.22
        # precip_mul = numpy.multiply(data_mdt,a)
        # precipitat = precip_mul + b
        # precipitation = numpy.array(precipitat)
        # recharge = numpy.multiply(precipitation, 0.15)
        recharge_without_rec = process_path + "recharge_without_rec"
        #Processing.runAlgorithm("gdal:rastercalculator",{
        #    'INPUT_A': inputRaster,
        #    'BAND_A': 1,
        #    'INPUT_B': None,
        #    'BAND_B': -1,
        #    'INPUT_C': None,
        #    'BAND_C': -1,
        #    'INPUT_D': None,
        #    'BAND_D': -1,
        #    'INPUT_E': None,
        #    'BAND_E': -1,
        #    'INPUT_F': None,
        #    'BAND_F': -1,
        #    'FORMULA': '(A*0.99+542.22)*0.15',
        #    'NO_DATA': None,
        #    'RTYPE': 6,
        #    'EXTRA': '',
        #    'OPTIONS': '',
        #    'OUTPUT':recharge_without_rec
        #})
        Processing.runAlgorithm("grass7:r.mapcalc.simple", {
            'a': str(inputRaster),
            'b': None,
            'c': None,
            'd': None,
            'e': None,
            'f': None,
            'expression': "(A*0.99+542.22)*0.15",
            'output': recharge_without_rec,
            'GRASS_REGION_PARAMETER': None,
            'GRASS_REGION_CELLSIZE_PARAMETER': 0,
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_RASTER_FORMAT_META': ''
        })
        # Create an output imagedriver with the multiplication result
        # driver2 = gdal.GetDriverByName( "GTiff" )
        # outData2 = driver2.Create(str(recharge_without_rec+'.'+'tif'), x,y,1, gdal.GDT_Float32)
        # outData2.GetRasterBand(1).WriteArray(recharge)
        # outData2.SetGeoTransform(geo)
        #outData2 = None
        
        recharge_without_rec_file = gdal.Open(recharge_without_rec)
        recharge_without_rec_rep = process_path + "recharge_without_rec"
        gdal.Warp(recharge_without_rec_rep, recharge_without_rec_file, dstSRS="EPSG:3763")

        #Processing.runAlgorithm("gdal:assignprojection",
        #                {'INPUT': recharge_without_rec,
        #                'CRS': QgsCoordinateReferenceSystem('EPSG:3763')})

        # indexes for topography for the two methods
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
        #QMessageBox.about(self, 'teste', str(results))
        
        Processing.initialize()
        result = process_path + "/result.tif"
        Processing.runAlgorithm("native:reclassifybytable", {
            'INPUT_RASTER': recharge_without_rec_rep,
            'RASTER_BAND': 1, 'TABLE': self.rattings,
            'NO_DATA': -9999, 'RANGE_BOUNDARIES': 0, 'NODATA_FOR_MISSING': False, 'DATA_TYPE': 5,
            'OUTPUT': result})

        # add result into canvas
        #file_info_norm = QFileInfo(str(outPath2))
        # QMessageBox.about(self, "teste", str(file_info_norm))
        #rlayer_new_norm = QgsRasterLayer(outPath2, file_info_norm.fileName(), 'gdal')
        # QMessageBox.about(self, "teste", str(rlayer_new_norm))
        #QgsProject.instance().addMapLayer(rlayer_new_norm)
        #self.iface.canvas.setExtent(rlayer_new_norm.extent())
        # set the map canvas layer set
        #self.iface.canvas.setLayers([rlayer_new_norm])
        # add result into canvas
        # file_info_recharge = QFileInfo(outPath2)
        # if file_info_recharge.exists():
        #     layer_name_recharge = file_info_recharge.baseName()
        # else:
        #     return False
        # rlayer_new_recharge = QgsRasterLayer(outPath2, layer_name_recharge)
        # if rlayer_new_recharge.isValid():
        #     QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_recharge)
        #     layer_prec_recharge = QgsMapCanvasLayer(rlayer_new_recharge)
        #     layerList_recharge = [layer_prec_recharge]
        #     extent_recharge = self.iface.canvas.setExtent(rlayer_new_recharge.extent())
        #     self.iface.canvas.setLayerSet(layerList_recharge)
        #     self.iface.canvas.setVisible(True)
        #     return True
        # else:
        #     return False
        #QMessageBox.information(self, self.tr( "Finished" ), self.tr( "Net Recharge completed." ) )
        
        out_raster = gdal.Open(result)
        gdal.Warp(outPath2, out_raster, dstSRS="EPSG:3857")