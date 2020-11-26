from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *
from .Ui_DGroundwater import Ui_DGroundwater
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

class DGroundwater(QDialog, Ui_DGroundwater):
    
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.selectButton.clicked.connect(self.fillInputFileEdit)
        self.selectMask.clicked.connect(self.fillInputMask)
        self.selectButton_mdt.clicked.connect(self.fillInputMDT)
        self.inputLayerCombo.currentIndexChanged.connect(self.fillInputAttrib)
        self.selectButton3.clicked.connect(self.fillOutputFileEdit)
        self.buttonAdd.clicked.connect(self.actionAdd)
        self.buttonRemove.clicked.connect(self.actionRemove)
        self.buttonBox.accepted.connect(self.convert)
        
        # connect help
        #QObject.connect(self.buttonBox.button(QtGui.QDialogButtonBox.Help), SIGNAL("clicked()"), self.help)
        
      
    # INPUT VECTOR FILE
    def fillInputFileEdit(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedVectorFilter()
        inputFile, encoding = GdalTools_utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), GdalTools_utils.FileFilter.allVectorsFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.loadFields(inputFile)
        self.inputLayerCombo.addItem(inputFile)
        check = QFile(inputFile)    
        
    def fillInputAttrib(self, inputFile):
        self.layer = QgsVectorLayer(self.inputLayerCombo.currentText(), (QFileInfo(str(self.inputLayerCombo.currentText()))).baseName() , "ogr")
        self.lineAttrib.clear()    
        changedField = ftools_GdalTools_utils.getFieldList(self.layer)
        for f in changedField:
            if f.type() == QVariant.Int or f.type() == QVariant.String or f.type()==QVariant.Double:
                self.lineAttrib.addItem(unicode(f.name()))   
                
    def loadFields(self, vectorFile = QString()):
        if vectorFile == None:
            return
        try:
            (fields, names) = GdalTools_utils.getVectorFields(vectorFile)
        except Exception as e:
            QErrorMessage(self).showMessage( str(e) )          
        self.inputLayerCombo.clearEditText()
        ncodec = QTextCodec.codecForName(self.lastEncoding)    
        
    # INPUT MASK SHAPEFILE
    def fillInputMask(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedVectorFilter()
        inputFile, encoding = GdalTools_utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), GdalTools_utils.FileFilter.allVectorsFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputMaskCombo.addItem(inputFile)
        check = QFile(inputFile)    
        
    # INPUT MDT
    def fillInputMDT(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedRasterFilter()
        inputRaster, encoding = GdalTools_utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), GdalTools_utils.FileFilter.allRastersFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo_mdt.addItem(inputRaster)
        check = QFile(inputRaster)     

    # ------------------------------ // ------------------------------------ // ----------------------------
    
    # OUTPUT RASTER FILE
    def fillOutputFileEdit(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedRasterFilter()
        outputFile = GdalTools_utils.FileDialog.getSaveFileName(self, self.tr( "Select the raster file to save the results to" ), GdalTools_utils.FileFilter.allRastersFilter(), ".sdat" )
        self.inputLayerCombo3.setText(outputFile)
        
   # -------------------------------- // --------------------------------- // -------------------------------
   
   # BUTTON ADD AND REMOVE CLASSES
    def actionAdd(self):
        n = self.tableWidget.rowCount()
        self.tableWidget.insertRow(n)
        n = self.tableWidget.rowCount()
        return True
                   
    def actionRemove(self):
        n = self.tableWidget.rowCount()
        for i in range(1,n):
            self.tableWidget.removeRow(n-1)
        n = self.tableWidget.rowCount()
        return True
   
   # ---------------------------------- // ----------------------------- // ------------------------------------
   
   # POINTS INTERPOLATION
    def convert(self):    
        
        gdal.AllRegister()
    # ------------------------ FIRST METHOD -------------------------------------------------
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(False)
        if self.inputLayerCombo.currentText()!="":
            inputLayer = self.inputLayerCombo.currentText()
            inputMask = self.inputMaskCombo.currentText()
            # layer information
            layer = QgsVectorLayer(inputLayer, inputLayer , "ogr")
            vectorlayer_vector =  layer.dataProvider()
            layer_mask = QgsVectorLayer(inputMask, inputMask , "ogr")
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
            layer_raster = QgsRasterLayer(inputRaster, inputRaster , "gdal")
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
            stream = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/stream"
            Processing.runAlgorithm("grass7:r.watershed", {'elevation': inputRaster, 'depression': None,
                                                           'flow': None, 'disturbed_land': None, 'blocking': None,
                                                           'threshold': size,
                                                           'max_slope_length': None, 'convergence': 5, 'memory': 300,
                                                           '-s': False, '-m': False,
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
                                                           'GRASS_REGION_CELLSIZE_PARAMETER': cellSize,
                                                           'GRASS_RASTER_FORMAT_OPT': '',
                                                           'GRASS_RASTER_FORMAT_META': ''})

            # condition stream > 1 to have the lines with value 1
            stream_ones = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/stream_ones"
           
            Processing.runAlgorithm("gdal:rastercalculator",
                                    {'INPUT_A': stream, 'BAND_A': 1, 'INPUT_B': None, 'BAND_B': -1, 'INPUT_C': None,
                                     'BAND_C': -1, 'INPUT_D': None,
                                     'BAND_D': -1, 'INPUT_E': None, 'BAND_E': -1, 'INPUT_F': None, 'BAND_F': -1,
                                     'FORMULA': "A>1", 'NO_DATA': None, 'RTYPE': 5, 'EXTRA': '', 'OPTIONS': '',
                                     'OUTPUT': stream_ones})
            
            # raster distance
            raster_distance = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/raster_distance.sdat"
           
            Processing.runAlgorithm("gdal:proximity",
                                    {'INPUT': str(stream_ones), 'BAND': 1, 'VALUES': '1', 'UNITS': 0, 'MAX_DISTANCE': 0,
                                     'REPLACE': 0, 'NODATA': 0, 'OPTIONS': '',
                                     'DATA_TYPE': 5,
                                     'OUTPUT': str(raster_distance)})
            # condition distance >=  200, always maximum depth meters
            dist_major_200 = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/dist_major_200"
          
            Processing.runAlgorithm("gdal:rastercalculator",
                                    {'INPUT_A': raster_distance, 'BAND_A': 1, 'INPUT_B': None, 'BAND_B': -1,
                                     'INPUT_C': None, 'BAND_C': -1, 'INPUT_D': None,
                                     'BAND_D': -1, 'INPUT_E': None, 'BAND_E': -1, 'INPUT_F': None, 'BAND_F': -1,
                                     'FORMULA': "A>=" + str(distance), 'NO_DATA': None, 'RTYPE': 5, 'EXTRA': '',
                                     'OPTIONS': '',
                                     'OUTPUT': dist_major_200})
            
            dist_multiplication = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/dist_multiplication"
            
            Processing.runAlgorithm("gdal:rastercalculator",
                                    {'INPUT_A': dist_major_200, 'BAND_A': 1, 'INPUT_B': None, 'BAND_B': -1,
                                     'INPUT_C': None, 'BAND_C': -1, 'INPUT_D': None,
                                     'BAND_D': -1, 'INPUT_E': None, 'BAND_E': -1, 'INPUT_F': None, 'BAND_F': -1,
                                     'FORMULA': "A*" + str(max_depth), 'NO_DATA': None, 'RTYPE': 5, 'EXTRA': '',
                                     'OPTIONS': '',
                                     'OUTPUT': dist_multiplication})
            
            # condition distance < 200, inteprolation between 0 and maximum depth
            dist_minor_200 = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/dist_minor_200"
         
            Processing.runAlgorithm("gdal:rastercalculator",
                                    {'INPUT_A': raster_distance, 'BAND_A': 1, 'INPUT_B': None, 'BAND_B': -1,
                                     'INPUT_C': None, 'BAND_C': -1, 'INPUT_D': None,
                                     'BAND_D': -1, 'INPUT_E': None, 'BAND_E': -1, 'INPUT_F': None, 'BAND_F': -1,
                                     'FORMULA': "A<" + str(distance), 'NO_DATA': None, 'RTYPE': 5, 'EXTRA': '',
                                     'OPTIONS': '',
                                     'OUTPUT': dist_minor_200})
            
            # multiplication by the raster distance
            dist_multiplication_dist = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/dist_multiplication_dist"
          
            Processing.runAlgorithm("gdal:rastercalculator",
                                    {'INPUT_A': dist_minor_200, 'BAND_A': 1, 'INPUT_B': raster_distance, 'BAND_B': 1,
                                     'INPUT_C': None, 'BAND_C': -1, 'INPUT_D': None,
                                     'BAND_D': -1, 'INPUT_E': None, 'BAND_E': -1, 'INPUT_F': None, 'BAND_F': -1,
                                     'FORMULA': "A*B", 'NO_DATA': None, 'RTYPE': 5, 'EXTRA': '', 'OPTIONS': '',
                                     'OUTPUT': dist_multiplication_dist})
            
            # interpolation between 0 and distance
            interpolation_dist = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/interpolation_dist"
          
            Processing.runAlgorithm("gdal:rastercalculator",
                                    {'INPUT_A': dist_multiplication_dist, 'BAND_A': 1, 'INPUT_B': None, 'BAND_B': -1,
                                     'INPUT_C': None, 'BAND_C': -1, 'INPUT_D': None,
                                     'BAND_D': -1, 'INPUT_E': None, 'BAND_E': -1, 'INPUT_F': None, 'BAND_F': -1,
                                     'FORMULA': "A*" + str(max_depth) + "/" + str(distance), 'NO_DATA': None,
                                     'RTYPE': 5, 'EXTRA': '', 'OPTIONS': '',
                                     'OUTPUT': interpolation_dist})
            
            # depth surface = sum of two conditions
            depth_surface = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/depth_surface"
          
            Processing.runAlgorithm("gdal:rastercalculator",
                                    {'INPUT_A': dist_multiplication, 'BAND_A': 1, 'INPUT_B': interpolation_dist,
                                     'BAND_B': 1, 'INPUT_C': None, 'BAND_C': -1, 'INPUT_D': None,
                                     'BAND_D': -1, 'INPUT_E': None, 'BAND_E': -1, 'INPUT_F': None, 'BAND_F': -1,
                                     'FORMULA': "A+B", 'NO_DATA': None, 'RTYPE': 5, 'EXTRA': '', 'OPTIONS': '',
                                     'OUTPUT': depth_surface})
            
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
            results = list(map(float, lista))
            
            depth_reclassify = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/depth_reclassify.sdat"
            Processing.runAlgorithm("saga:reclassifyvalues",
                                    {'INPUT': depth_surface, 'METHOD': 2, 'OLD': 0, 'NEW': 1, 'SOPERATOR': 0, 'MIN': 0,
                                     'MAX': 1,
                                     'RNEW': 2, 'ROPERATOR': 0, 'RETAB': results, 'TOPERATOR': 0, 'NODATAOPT': True,
                                     'NODATA': 0,
                                     'OTHEROPT': True, 'OTHERS': 0, 'RESULT': outPath2})

            #Processing.runAlgorithm("grass:r.surf.idw", None, depth_reclassify, 12, False, extent_raster_str, cellSize, outPath2)
    
         
            
            # add result into canvas
            # add result into canvas
            file_info_norm = QFileInfo(str(outPath2))
            # QMessageBox.about(self, "teste", str(file_info_norm))
            rlayer_new_norm = QgsRasterLayer(outPath2, file_info_norm.fileName(), 'gdal')
            # QMessageBox.about(self, "teste", str(rlayer_new_norm))
            QgsProject.instance().addMapLayer(rlayer_new_norm)
            self.iface.canvas.setExtent(rlayer_new_norm.extent())
            # set the map canvas layer set
            self.iface.canvas.setLayers([rlayer_new_norm])

            # file_info_norm = QFileInfo(outPath2)
            # if file_info_norm.exists():
            #     layer_name_norm = file_info_norm.baseName()
            # else:
            #     return False
            # rlayer_new_norm = QgsRasterLayer(outPath2, layer_name_norm)
            # if rlayer_new_norm.isValid():
            #     QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_norm)
            #     layer_norm = QgsMapCanvasLayer(rlayer_new_norm)
            #     layerList_norm = [layer_norm]
            #     extent_norm = self.iface.canvas.setExtent(rlayer_new_norm.extent())
            #     self.iface.canvas.setLayerSet(layerList_norm)
            #     self.iface.canvas.setVisible(True)
            #     return True
            # else:
            #     return False

        QMessageBox.information(self, self.tr( "Finished" ), self.tr( "Depth completed." ) ) 
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
        
        
    def help(self):
        QMessageBox.about(self, "Depth Groundwater", """<p><b>Depth to Groundwater factor</b></p> 
        <p><b>Definition:</b>The D factor contributes to control the distance that pollutants must travel before reaching the aquifer and allows creating a surface map according to depth values measured in the wells. It can be created by two methods: the base method, which allows interpolating data point with the depth to groundwater values into a raster file, and an improvement method, which allows to create a depth to groundwater surface from DEM (Digital Elevation Model).</p>
        <p><b>Base method</b></p> 
        <p>Input files = points file with the depth values and a mask file with the study area extension. The user must to choose the attribute field with the depth values and the cell size. The user must to choose between different <b>interpolation methods</p> to estimate the depth to groundwater map.  </p>
        <p><b>Improved method</b></p> 
        <p>Input file = DEM. The method intends to create a surface through drainage network segments (rivers or streams). A new surface is generated with values ranging from 0 m to a maximum depth value which can be modified by the user (<b>Maximum depth</b> field). A distance raster is created from drainage network segments data and a condition is imposed. The user defines a distance (<b>Distance</b> field) to streams or rivers value, and if the distance is smaller than this threshold, the depth values are interpolated between 0 m (at river or stream segments) and the maximum depth (in places located at the defined maximum distance). </p>
        <p><b>Ratings:</b>The ratings are adopted by Aller et al. but the user can modify the values, add or remove lines. </p>
        <p><b>Output file:</b> Depth to Groundwater raster file</p>""")            

    