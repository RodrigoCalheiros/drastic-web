import sys, os
from osgeo import gdal
from PyQt5.QtCore import *
from qgis.core import QgsProcessingRegistry
from qgis.analysis import QgsNativeAlgorithms
from qgis.core import *
QgsApplication.setPrefixPath('/usr', True)

sys.path.append('/usr/share/qgis/python/plugins/')
from processing.core.Processing import Processing

def convert(self):    
        
    gdal.AllRegister()
    # ------------------------ FIRST METHOD -------------------------------------------------
    #self.buttonBox.button(QDialogButtonBox.Ok).setDefault(False)
    d_prj = "\Dados\d.prj"
    d_sdat = "\Dados\d.sdat"
    dem_novo_clip = "\Dados\dem_novo_clip.tif"

    inputLayer = dem_novo_clip
    inputLayerMdt = ""

    #if self.inputLayerCombo.currentText()!="":
    if inputLayer != "":
        #inputLayer = self.inputLayerCombo.currentText()
        #inputMask = self.inputMaskCombo.currentText()
        inputMask = d_sdat

        # layer information
        layer = QgsVectorLayer(unicode(inputLayer).encode('utf8'), inputLayer , "ogr")  
        vectorlayer_vector =  layer.dataProvider()
        layer_mask = QgsVectorLayer(unicode(inputMask).encode('utf8'), inputMask , "ogr")  
        vectorlayer_mask =  layer_mask.dataProvider()      

        # mask extent
        extent_rect = vectorlayer_mask.extent()
        xmin = extent_rect.xMinimum()
        xmax = extent_rect.xMaximum()
        ymin = extent_rect.yMinimum()
        ymax = extent_rect.yMaximum()
        extent = str(xmin) + "," + str(xmax) + "," + str(ymin) + "," + str(ymax)

        # attribute
        Elevation = self.lineAttrib.currentText()

        # cellsize
        cellSize = int(self.linePix.value())
        outPath = self.inputLayerCombo3.text()
        
        # size of atributte table == number of points
        count = layer.featureCount()
        
        # points interpolation idw
        if self.comboBoxMethod.currentText()=="Inverse Distance Weighting":
            Processing.initialize()
            # grid directory (qgis2)
            idw_interpolation = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/idw_interpolation"        
            Processing.runAlgorithm("grass:v.surf.idw", None, inputLayer, count, 2.0, Elevation, False, extent, cellSize, -1.0, 0.0001, idw_interpolation)
            idw_int = idw_interpolation + "." + "tif"
            
            int_mask = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/int_mask"
            # clip grid(interpolation) with polygon (mask)
            Processing.runAlgorithm("saga:clipgridwithpolygon", None, idw_int, inputMask, int_mask)
            int_mask_zone = int_mask + "." + "tif"
        
        # indexes for topography
        numberRows = int(self.tableWidget.rowCount())
        numberColumns = int(self.tableWidget.columnCount())
        classes = ''
        lista = []
        for i in range(0,numberRows):
            for j in range(0,numberColumns):
                self.line = self.tableWidget.item(i,j)
                lista = lista + [str(self.line.text())]
                string = ","
                intervalos = string.join(lista)
        
        
        # reclassify idw interpolation
        if self.comboBoxMethod.currentText()=="Inverse Distance Weighting":
            idw_reclassify = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/idw_reclassify"
            Processing.runAlgorithm("saga:reclassifygridvalues", None, int_mask_zone, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, outPath)
            
            
            
            # add result into canvas
            file_info = QFileInfo(outPath)
            if file_info.exists():
                layer_name = file_info.baseName()
            else:
                return False
            rlayer_new = QgsRasterLayer(outPath, layer_name)
            if rlayer_new.isValid():
                QgsMapLayerRegistry.instance().addMapLayer(rlayer_new)
                layer = QgsMapCanvasLayer(rlayer_new)
                layerList = [layer]
                extent = self.iface.canvas.setExtent(rlayer_new.extent())
                self.iface.canvas.setLayerSet(layerList)
                self.iface.canvas.setVisible(True)         
                return True
            else:
                return False            
        
        # points interpolation kriging
        if self.comboBoxMethod.currentText()=="Kriging":
            Processing.initialize()
            # grid directory (qgis2)
            kriging_interpolation = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/kriging_interpolation"        
            Processing.runAlgorithm("saga:ordinarykrigingglobal", None, inputLayer, Elevation, True, 0, 1, False, 100, False, 0.0, 10, 1000, 1.0, 0.1, 1.0, 0.5, cellSize, True, extent, kriging_interpolation, None)
            kriging_int = kriging_interpolation + "." + "tif"
            
            int_mask_kriging = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/int_mask_kriging"
            # clip grid(interpolation) with polygon (mask)
            Processing.runAlgorithm("saga:clipgridwithpolygon", None, kriging_int, inputMask, int_mask_kriging)
            int_mask_zone_k = int_mask_kriging + "." + "tif"    
            
            kriging_reclassify = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/kriging_reclassify"
            Processing.runAlgorithm("saga:reclassifygridvalues", None, int_mask_zone_k, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, outPath)
            
            
            # add result into canvas
            file_info_k = QFileInfo(outPath)
            if file_info_k.exists():
                layer_name_k = file_info_k.baseName()
            else:
                return False
            rlayer_new_k = QgsRasterLayer(outPath, layer_name_k)
            if rlayer_new_k.isValid():
                QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_k)
                layer_k = QgsMapCanvasLayer(rlayer_new_k)
                layerList_k = [layer_k]
                extent_k = self.iface.canvas.setExtent(rlayer_new_k.extent())
                self.iface.canvas.setLayerSet(layerList_k)
                self.iface.canvas.setVisible(True)         
                return True
            else:
                return False             
    
            # points interpolation cubic spline
        if self.comboBoxMethod.currentText()=="Cubic spline approximation (SAGA)":
            Processing.initialize()
            # grid directory (qgis2)
            cubicSpline_interpolation = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/cubicSpline_interpolation"        
            Processing.runAlgorithm("saga:cubicsplineapproximation", None, inputLayer, Elevation, 0, 3, count, 5, 140.0, extent, cellSize, cubicSpline_interpolation)
            cubicSpline_int = cubicSpline_interpolation + "." + "tif"
            
            int_mask_cubicSpline = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/int_mask_cubicSpline"
            # clip grid(interpolation) with polygon (mask)
            Processing.runAlgorithm("saga:clipgridwithpolygon", None, cubicSpline_int, inputMask, int_mask_cubicSpline)
            int_mask_zone_cs = int_mask_cubicSpline + "." + "tif"    
            
            cubicSpline_reclassify = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/cubicSpline_reclassify"
            Processing.runAlgorithm("saga:reclassifygridvalues", None, int_mask_zone_cs, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, outPath)
            
        
            
            # add result into canvas
            file_info_cs = QFileInfo(outPath)
            if file_info_cs.exists():
                layer_name_cs = file_info_cs.baseName()
            else:
                return False
            rlayer_new_cs = QgsRasterLayer(outPath, layer_name_cs)
            if rlayer_new_cs.isValid():
                QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_cs)
                layer_cs = QgsMapCanvasLayer(rlayer_new_cs)
                layerList_cs = [layer_cs]
                extent_cs = self.iface.canvas.setExtent(rlayer_new_cs.extent())
                self.iface.canvas.setLayerSet(layerList_cs)
                self.iface.canvas.setVisible(True)         
                return True
            else:
                return False   
    
        if self.comboBoxMethod.currentText()=="Spatial approximation using spline with tension (GRASS)":
            Processing.initialize()
            # grid directory (qgis2)
            rst_interpolation = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/rst_interpolation"        
            Processing.runAlgorithm("grass:v.surf.rst", None, inputLayer, "", None, Elevation, 40, 40, 300, 0.001, 2.5, 1, 0, 0, False, False, extent, cellSize, -1, 0.0001, rst_interpolation, None, None, None, None, None)
            rst_int = rst_interpolation + "." + "tif"
            
            int_mask_rst = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/int_mask_rst"
            # clip grid(interpolation) with polygon (mask)
            Processing.runAlgorithm("saga:clipgridwithpolygon", None, rst_int, inputMask, int_mask_rst)
            int_mask_zone_rst = int_mask_rst + "." + "tif"    
            
            rst_reclassify = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/rst_reclassify"
            Processing.runAlgorithm("saga:reclassifygridvalues", None, int_mask_zone_rst, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, outPath)
            
            
            # add result into canvas
            file_info_rst = QFileInfo(outPath)
            if file_info_rst.exists():
                layer_name_rst = file_info_rst.baseName()
            else:
                return False
            rlayer_new_rst = QgsRasterLayer(outPath, layer_name_rst)
            if rlayer_new_rst.isValid():
                QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_rst)
                layer_rst = QgsMapCanvasLayer(rlayer_new_rst)
                layerList_rst = [layer_rst]
                extent_rst = self.iface.canvas.setExtent(rlayer_new_rst.extent())
                self.iface.canvas.setLayerSet(layerList_rst)
                self.iface.canvas.setVisible(True)         
                return True
            else:
                return False       
    
    # ----------------------- SECOND RASTER ----------------------------------------------------------------------------------------
    if self.inputLayerCombo_mdt!="":
        outPath2 = self.inputLayerCombo3.text() 
        # read raster
        inputRaster = self.inputLayerCombo_mdt.currentText()
        layer_raster = QgsRasterLayer(unicode(inputRaster).encode('utf8'), inputRaster , "gdal")      
        data_mdt = layer_raster.dataProvider()
        extent_raster = data_mdt.extent()
        xmin_raster = extent_raster.xMinimum()
        xmax_raster = extent_raster.xMaximum()
        ymin_raster = extent_raster.yMinimum()
        ymax_raster = extent_raster.yMaximum()
        extent_raster_str = str(xmin_raster) + "," + str(xmax_raster) + "," + str(ymin_raster) + "," + str(ymax_raster)     
        cellSize = layer_raster.rasterUnitsPerPixelX()
        
        
        # read maximum depth
        max_depth = self.line_max.value()
        # read distance
        distance = self.line_distance.value()   
        # minimum size
        size = self.line_size.value()
        
        Processing.initialize()
        # grid directory (qgis2)
        # generate stream segments
        stream = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/stream" 
        Processing.runAlgorithm("grass:r.watershed",None, inputRaster, None, None, None, None, size, 0,5,300,False, True, False, False, extent_raster_str, cellSize, None, None, None, stream, None, None, None, None)
        stream_tif = stream + "." + "tif"
        
        # condition stream > 1 to have the lines with value 1
        stream_ones = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/stream_ones" 
        
        Processing.runAlgorithm("gdalogr:rastercalculator", None, stream_tif, "1",None,"1",None,"1",None,"1",None,"1",None,"1","A>1","-9999",5,"", stream_ones)
        stream_ones_str = stream_ones + "." + "tif"
        
        # raster distance
        raster_distance = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/raster_distance.sdat" 
        
        Processing.runAlgorithm("saga:proximitygrid", None, stream_ones_str, raster_distance, None, None)
        
        # condition distance >=  200, always maximum depth meters
        dist_major_200 = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/dist_major_200"
        
        Processing.runAlgorithm("gdalogr:rastercalculator", None, raster_distance, "1",None,"1",None,"1",None,"1",None,"1",None,"1","A>="+str(distance),"-9999",5,"", dist_major_200)
        dist_major_200_str = dist_major_200 + "." + "tif"  
        
        dist_multiplication = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/dist_multiplication"
        
        Processing.runAlgorithm("gdalogr:rastercalculator", None, dist_major_200_str, "1",None,"1",None,"1",None,"1",None,"1",None,"1","A*"+str(max_depth),"-9999",5,"", dist_multiplication)
        dist_multiplication_str = dist_multiplication + "." + "tif"   
        
        # condition distance < 200, inteprolation between 0 and maximum depth
        dist_minor_200 = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/dist_minor_200"
        
        Processing.runAlgorithm("gdalogr:rastercalculator", None, raster_distance, "1",None,"1",None,"1",None,"1",None,"1",None,"1","A<"+str(distance),"-9999",5,"", dist_minor_200)
        dist_minor_200_str = dist_minor_200 + "." + "tif"  
        
        # multiplication by the raster distance
        dist_multiplication_dist = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/dist_multiplication_dist"
        
        Processing.runAlgorithm("gdalogr:rastercalculator", None, dist_minor_200_str, "1",raster_distance,"1",None,"1",None,"1",None,"1",None,"1","A*B","-9999",5,"", dist_multiplication_dist)
        dist_multiplication_dist_str = dist_multiplication_dist + "." + "tif"   
        
        # interpolation between 0 and distance
        interpolation_dist = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/interpolation_dist"
        
        Processing.runAlgorithm("gdalogr:rastercalculator", None,dist_multiplication_dist_str , "1",None,"1",None,"1",None,"1",None,"1",None,"1","A*"+str(max_depth)+"/"+str(distance),"-9999",5,"", interpolation_dist)
        interpolation_dist_str = interpolation_dist + "." + "tif"   
        
        # depth surface = sum of two conditions
        depth_surface = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/depth_surface"
        
        Processing.runAlgorithm("gdalogr:rastercalculator", None,dist_multiplication_str , "1",interpolation_dist_str,"1",None,"1",None,"1",None,"1",None,"1","A+B","-9999",5,"", depth_surface)
        depth_surface_tif = depth_surface + "." + "tif"        
        
        # indexes for topography
        numberRows = int(self.tableWidget.rowCount())
        numberColumns = int(self.tableWidget.columnCount())
        classes = ''
        lista = []
        for i in range(0,numberRows):
            for j in range(0,numberColumns):
                self.line = self.tableWidget.item(i,j)
                lista = lista + [str(self.line.text())]
                string = ","
                intervalos = string.join(lista)        
        
        depth_reclassify = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/depth_reclassify.sdat"
        Processing.runAlgorithm("saga:reclassifygridvalues", None, depth_surface_tif, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, depth_reclassify)
        #depth_rec_idw = depth_reclassify + "." + "tif"
        
        Processing.runAlgorithm("grass:r.surf.idw", None, depth_reclassify, 12, False, extent_raster_str, cellSize, outPath2)

        
        
        # add result into canvas
        file_info_norm = QFileInfo(outPath2)
        if file_info_norm.exists():
            layer_name_norm = file_info_norm.baseName()
        else:
            return False
        rlayer_new_norm = QgsRasterLayer(outPath2, layer_name_norm)
        if rlayer_new_norm.isValid():
            QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_norm)
            layer_norm = QgsMapCanvasLayer(rlayer_new_norm)
            layerList_norm = [layer_norm]
            extent_norm = self.iface.canvas.setExtent(rlayer_new_norm.extent())
            self.iface.canvas.setLayerSet(layerList_norm)
            self.iface.canvas.setVisible(True)         
            return True
        else:
            return False                 

    QMessageBox.information(self, self.tr( "Finished" ), self.tr( "Depth completed." ) ) 
    self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)

def convert_mdt(input_mdt, max_depth, distance, min_size, ratings, output_path):
    
    qgs = QgsApplication([], False)
    qgs.initQgis()
    Processing.initialize()
    
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
    gdal.AllRegister()

    for alg in QgsApplication.processingRegistry().algorithms():
        print(alg.id(), "->", alg.displayName())

    # read raster
    inputRaster = input_mdt
    # read maximum depth
    max_depth = max_depth
    # read distance
    distance = distance   
    # minimum size
    size = min_size
    outPath2 = output_path 

    

    layer_raster = QgsRasterLayer(inputRaster, os.path.basename(inputRaster), "gdal")
    data_mdt = layer_raster.dataProvider()
    extent_raster = data_mdt.extent()
    xmin_raster = extent_raster.xMinimum()
    xmax_raster = extent_raster.xMaximum()
    ymin_raster = extent_raster.yMinimum()
    ymax_raster = extent_raster.yMaximum()
    extent_raster_str = str(xmin_raster) + "," + str(xmax_raster) + "," + str(ymin_raster) + "," + str(ymax_raster)     
    cellSize = layer_raster.rasterUnitsPerPixelX()

    stream = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/stream.tif"
    #QMessageBox.about(self, "teste", str(stream))
    Processing.runAlgorithm("grass7:r.watershed",{'elevation': inputRaster, 'depression': None,
                    'flow': None, 'disturbed_land': None, 'blocking': None, 'threshold': size,
                    'max_slope_length': None, 'convergence': 5, 'memory': 300, '-s': False, '-m': False,
                    '-4': False, '-a': False, '-b': False, 'accumulation': None,
                    'drainage': None,
                    'basin': None,
                    'stream': stream,
                    'half_basin': None,
                    'length_slope': None,
                    'slope_steepness': None,
                    'tci': None,
                    'spi': None,
                    'GRASS_REGION_PARAMETER': extent_raster_str + '[EPSG:3763]',
                    'GRASS_REGION_CELLSIZE_PARAMETER': cellSize, 'GRASS_RASTER_FORMAT_OPT': '',
                    'GRASS_RASTER_FORMAT_META': ''})

    
    # condition stream > 1 to have the lines with value 1
    stream_ones = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/stream_ones.tif"

    Processing.runAlgorithm("grass7:r.mapcalc.simple",
                            {'a': str(stream),
                                'b': None,
                                'c': None, 'd': None, 'e': None, 'f': None,
                                'expression': 'A>1',
                                'output': stream_ones, 'GRASS_REGION_PARAMETER': None,
                                'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
                                'GRASS_RASTER_FORMAT_META': ''})



    # raster distance
    raster_distance = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/raster_distance.tif"
    
    #Processing.runAlgorithm("saga:proximitygrid", None, str(stream_ones_str), 3, str(raster_distance), None, None)

    Processing.runAlgorithm("saga:proximityraster", {
        'FEATURES': str(stream_ones),
        'DISTANCE': str(raster_distance), 'DIRECTION': 'TEMPORARY_OUTPUT', 'ALLOCATION': 'TEMPORARY_OUTPUT'})


    # condition distance >=  200, always maximum depth meters
    dist_major_200 = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/dist_major_200.tif"

    Processing.runAlgorithm("grass7:r.mapcalc.simple",
                            {'a': str(raster_distance),
                                'b': None,
                                'c': None, 'd': None, 'e': None, 'f': None,
                                'expression': "A>="+str(distance),
                                'output': dist_major_200, 'GRASS_REGION_PARAMETER': None,
                                'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
                                'GRASS_RASTER_FORMAT_META': ''})
    
    dist_multiplication = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/dist_multiplication.tif"

    Processing.runAlgorithm("grass7:r.mapcalc.simple",
                            {'a': str(dist_major_200),
                                'b': None,
                                'c': None, 'd': None, 'e': None, 'f': None,
                                'expression': "A*"+str(max_depth),
                                'output': dist_multiplication, 'GRASS_REGION_PARAMETER': None,
                                'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
                                'GRASS_RASTER_FORMAT_META': ''})
    
    # condition distance < 200, inteprolation between 0 and maximum depth
    dist_minor_200 = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/dist_minor_200.tif"

    Processing.runAlgorithm("grass7:r.mapcalc.simple",
                            {'a': str(raster_distance),
                                'b': None,
                                'c': None, 'd': None, 'e': None, 'f': None,
                                'expression': "A<"+str(distance),
                                'output': dist_minor_200, 'GRASS_REGION_PARAMETER': None,
                                'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
                                'GRASS_RASTER_FORMAT_META': ''})
    
    # multiplication by the raster distance
    dist_multiplication_dist = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/dist_multiplication_dist.tif"

    Processing.runAlgorithm("grass7:r.mapcalc.simple",
                            {'a': str(dist_minor_200),
                                'b': None,
                                'c': None, 'd': None, 'e': None, 'f': None,
                                'expression': 'A*B',
                                'output': dist_multiplication_dist, 'GRASS_REGION_PARAMETER': None,
                                'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
                                'GRASS_RASTER_FORMAT_META': ''})
    
    # interpolation between 0 and distance
    interpolation_dist = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/interpolation_dist.tif"

    Processing.runAlgorithm("grass7:r.mapcalc.simple",
                            {'a': str(dist_multiplication_dist),
                                'b': None,
                                'c': None, 'd': None, 'e': None, 'f': None,
                                'expression': "A*"+str(max_depth)+"/"+str(distance),
                                'output': interpolation_dist, 'GRASS_REGION_PARAMETER': None,
                                'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
                                'GRASS_RASTER_FORMAT_META': ''})
    
    # depth surface = sum of two conditions
    depth_surface = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/depth_surface.tif"

    Processing.runAlgorithm("grass7:r.mapcalc.simple",
                            {'a': str(dist_multiplication),
                                'b': None,
                                'c': None, 'd': None, 'e': None, 'f': None,
                                'expression': 'A+B',
                                'output': depth_surface, 'GRASS_REGION_PARAMETER': None,
                                'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
                                'GRASS_RASTER_FORMAT_META': ''})

    
    # indexes for topography
    numberRows = int(self.tableWidget.rowCount())
    numberColumns = int(self.tableWidget.columnCount())
    classes = ''
    lista = []
    for i in range(0,numberRows):
        for j in range(0,numberColumns):
            self.line = self.tableWidget.item(i,j)
            lista = lista + [self.line.text()]
            string = ","
            intervalos = string.join(lista)
    results = list(map(float, lista))

    Processing.runAlgorithm("saga:reclassifyvalues",{'INPUT': depth_surface, 'METHOD':2, 'OLD':0, 'NEW':1, 'SOPERATOR':0, 'MIN':0, 'MAX':1,
                                                        'RNEW':2, 'ROPERATOR':0, 'RETAB':results, 'TOPERATOR':0, 'NODATAOPT':True, 'NODATA':0,
                                                        'OTHEROPT':True, 'OTHERS':0, 'RESULT':outPath2})


    # add result into canvas
    file_info_norm = QFileInfo(str(outPath2))
    #QMessageBox.about(self, "teste", str(file_info_norm))
    rlayer_new_norm = QgsRasterLayer(outPath2, file_info_norm.fileName(), 'gdal')
    #QMessageBox.about(self, "teste", str(rlayer_new_norm))
    QgsProject.instance().addMapLayer(rlayer_new_norm)
    self.iface.canvas.setExtent(rlayer_new_norm.extent())
    # set the map canvas layer set
    self.iface.canvas.setLayers([rlayer_new_norm])



input_mdt = "/home/rodrigo/data/d/d.sdat"
max_depth = 20
distance = 200
min_size = 50
ratings = [ [0, 1.5, 10], [1.5, 4.6, 9], [4.6, 9.1, 7], [9.1, 15.2, 5], [15.2, 22.9, 3], [22.9, 30.5, 2], [30.5, 200, 1]]
output_path = "/home/rodrigo/data/d/dem_rodrigo.tif"
convert_mdt(input_mdt, max_depth, distance, min_size, ratings, output_path)

