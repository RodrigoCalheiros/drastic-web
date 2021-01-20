from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.core import *
from qgis.gui import *
from .Ui_Recharge import Ui_Recharge
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
from gdalconst import *
from processing import ProcessingPlugin
#from processing.outputs import OutputRaster
import sys, os
import numpy
from qgis.PyQt import QtCore, QtGui

class Recharge(QDialog, Ui_Recharge):
    
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        
        self.selectButton.clicked.connect(self.fillInputFileEdit)
        self.selectButton1.clicked.connect(self.fillInputFileEdit1)
        self.selectButton2.clicked.connect(self.fillInputFileEdit2)
        self.selectButton4.clicked.connect(self.fillInputFileEdit4)
        self.selectButton5.clicked.connect(self.fillInputFileEdit5)
        self.inputLayerCombo.currentIndexChanged.connect(self.fillInputAttrib)
        self.inputLayerCombo1.currentIndexChanged.connect(self.fillInputAttrib1)
        self.inputLayerCombo2.currentIndexChanged.connect(self.fillInputAttrib2)
        self.inputLayerCombo5.currentIndexChanged.connect(self.fillInputAttrib5)
        self.selectButton3.clicked.connect(self.fillOutputFileEdit)
        self.buttonAdd.clicked.connect(self.actionAdd)
        self.buttonRemove.clicked.connect(self.actionRemove)
        self.buttonBox.accepted.connect(self.convert)
        
        # connect help
        #QObject.connect(self.buttonBox.button(QtGui.QDialogButtonBox.Help), SIGNAL("clicked()"), self.help)             
      
# METHOD I
# INPUT VECTOR FILE PRECIPITATION
    def fillInputFileEdit(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedVectorFilter()
        inputFile, encoding = GdalTools_utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), GdalTools_utils.FileFilter.allVectorsFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.loadFields(inputFile)
        self.inputLayerCombo.addItem(inputFile)
        check = QFile(inputFile)    
        
    def fillInputAttrib(self, inputFile):
        self.layer = QgsVectorLayer(unicode(self.inputLayerCombo.currentText()).encode('utf8'), inputFile  , "ogr")
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
        
    def help(self):
        QMessageBox.about(self, "Net Recharge", """<p><b>Net Recharge factor</b></p> 
        <p><b>Definition:</b>The R factor assumes that the greater the aquifer recharge the greater the groundwater vulnerability to pollution. 
        The feature is composed by three methods to determine the recharge map. The user can choose the best method depending on the available information. 
        The first method estimates net recharge according to a simplified water budget (e.g., Charles et al. 1993; Custodio and Llamas 1996): Recharge = Precipitation - Overland Flow-Evapotranspiration. </p>
        <p><b>First method</b></p> 
        <p>Input files = precipitation, overland flow and evapotranspiration data (mm/year). The user must to define the attributes and the cell size. </p>
        <p><b>Second method</b></p> 
        <p>Input file = precipitation data. The second method requires the availability of recharge rates expressed as a percentage of mean annual precipitation data (mm/year). 
        In this case the user assumes that the spatial variability of precipitation and other factors that control aquifer recharge is not significant and therefore a constant 
        recharge value may be accepted for the entire study region. This type of data may be found in regional hydrogeological studies. The user must define the input precipitation data as well as the respective attribute.  </p>
        <p><b>Third method</b></p> 
        <p>Input file = DEM. If the spatial variability of precipitation is significant and is essentially controlled by altitude, a third method may be applied. 
        In this case, the spatial distribution of precipitation is calculated through a DEM coupled with a regression model expressing precipitation as a function of altitude. 
        Finally, a regional recharge rate expressed as percentage of annual precipitation is applied.  </p>
        <p><b>Ratings:</b>The ratings are adopted by Aller et al. but the user can modify the values, add or remove lines. </p>
        <p><b>Output file:</b> Net Recharge raster file</p>""")            

        
# INPUT VECTOR FILE SURFACE RUNNOFF
    def fillInputFileEdit1(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedVectorFilter()
        inputFile, encoding = GdalTools_utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), GdalTools_utils.FileFilter.allVectorsFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.loadFields1(inputFile)
        self.inputLayerCombo1.addItem(inputFile)
        check = QFile(inputFile)      

    def fillInputAttrib1(self, inputFile):
        self.layer = QgsVectorLayer(unicode(self.inputLayerCombo1.currentText()).encode('utf8'), inputFile  , "ogr")
        self.lineAttribRunoff.clear()    
        changedField = ftools_GdalTools_utils.getFieldList(self.layer)
        for f in changedField:
            if f.type() == QVariant.Int or f.type() == QVariant.String or f.type()==QVariant.Double:
                self.lineAttribRunoff.addItem(unicode(f.name()))  
                
    def loadFields1(self, vectorFile = QString()):
        if vectorFile == None:
            return
        try:
            (fields, names) = GdalTools_utils.getVectorFields(vectorFile)
        except Exception as e:
            QErrorMessage(self).showMessage( str(e) )          
        self.inputLayerCombo1.clearEditText()
        ncodec = QTextCodec.codecForName(self.lastEncoding)    
        
# INPUT VECTOR FILE EVAPOTRANSPIRATION
    def fillInputFileEdit2(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedVectorFilter()
        inputFile, encoding = GdalTools_utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), GdalTools_utils.FileFilter.allVectorsFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.loadFields2(inputFile)
        self.inputLayerCombo2.addItem(inputFile)
        check = QFile(inputFile)    
        
    def fillInputAttrib2(self, inputFile):
        self.layer = QgsVectorLayer(unicode(self.inputLayerCombo1.currentText()).encode('utf8'), inputFile  , "ogr")
        self.lineAttribEvap.clear()    
        changedField = ftools_GdalTools_utils.getFieldList(self.layer)
        for f in changedField:
            if f.type() == QVariant.Int or f.type() == QVariant.String or f.type()==QVariant.Double:
                self.lineAttribEvap.addItem(unicode(f.name()))  
                
    def loadFields2(self, vectorFile = QString()):
        if vectorFile == None:
            return
        try:
            (fields, names) = GdalTools_utils.getVectorFields(vectorFile)
        except Exception as e:
            QErrorMessage(self).showMessage( str(e) )          
        self.inputLayerCombo2.clearEditText()
        ncodec = QTextCodec.codecForName(self.lastEncoding) 
                    
# INPUT MDT (METHOD II)
    def fillInputFileEdit4(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedRasterFilter()
        inputFile, encoding = GdalTools_utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), GdalTools_utils.FileFilter.allRastersFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo4.addItem(inputFile)
        check = QFile(inputFile)

    # INPUT MDT (METHOD III)
    def fillInputFileEdit5(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedRasterFilter()
        inputFile, encoding = GdalTools_utils.FileDialog.getOpenFileName(self, self.tr("Select the input file"),
                                                                         GdalTools_utils.FileFilter.allRastersFilter(),
                                                                         lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo5.addItem(inputFile)
        check = QFile(inputFile)

    def fillInputAttrib5(self, inputFile):
        self.layer = QgsVectorLayer(self.inputLayerCombo5.currentText(),
                                    (QFileInfo(str(self.inputLayerCombo5.currentText()))).baseName(), "ogr")
        self.lineAttrib5.clear()
        changedField = ftools_utils.getFieldList(self.layer)
        for f in changedField:
            if f.type() == QVariant.Int or f.type() == QVariant.String or f.type() == QVariant.Double:
                self.lineAttrib5.addItem(unicode(f.name()))

            # ------------------------------ // ------------------------------------ // ----------------------------
                
# OUTPUT RASTER FILE
    def fillOutputFileEdit(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedRasterFilter()
        outputFile = GdalTools_utils.FileDialog.getSaveFileName(self, self.tr( "Select the raster file to save the results to" ), '.sdat', lastUsedFilter )
      
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
        
# ------------------------------ // ---------------------------------- // -----------------------------------                  

# CONVERT VECTOR TO GRID
    def convert(self):    
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(False)
        if self.inputLayerCombo.currentText()!="":
            inputLayer = self.inputLayerCombo.currentText()
            inputLayer1 = self.inputLayerCombo1.currentText()
            inputLayer2 = self.inputLayerCombo2.currentText()
            # layer information
            layer = QgsVectorLayer(unicode(inputLayer).encode('utf8'), inputLayer , "ogr")  
            layer1 = QgsVectorLayer(unicode(inputLayer1).encode('utf8'), inputLayer1 , "ogr")
            layer2 = QgsVectorLayer(unicode(inputLayer2).encode('utf8'), inputLayer2 , "ogr")
            vectorlayer_vector =  layer.dataProvider()
            vectorlayer_vector1 =  layer1.dataProvider()
            vectorlayer_vector2 =  layer2.dataProvider()
            # extent
            extent_rect = vectorlayer_vector.extent()
            xmin = extent_rect.xMinimum()
            xmax = extent_rect.xMaximum()
            ymin = extent_rect.yMinimum()
            ymax = extent_rect.yMaximum()
            extent = str(xmin) + "," + str(xmax) + "," + str(ymin) + "," + str(ymax)
            # attribute
            Elevation = self.lineAttrib.currentText()
            Attrib1 = self.lineAttribRunoff.currentText()
            Attrib2 = self.lineAttribEvap.currentText()
            # cellsize
            cellSize = int(self.linePix.value())
            outPath = self.inputLayerCombo3.text()
        
            Processing.initialize()
            # grid directory (qgis2)
            filedir = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/pret" 
            filedir1 = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/runoff"
            filedir2 = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/evapo"
            Processing.runAlgorithm("grass7:v.to.rast", {'input': inputLayer, 'type': [0, 1, 3], 'where': '', 'use': 0,
                                                         'attribute_column': Elevation, 'rgb_column': None,
                                                         'label_column': None, 'value': None, 'memory': 300,
                                                         'output': filedir, 'GRASS_REGION_PARAMETER': extent,
                                                         'GRASS_REGION_CELLSIZE_PARAMETER': cellSize,
                                                         'GRASS_RASTER_FORMAT_OPT': '', 'GRASS_RASTER_FORMAT_META': '',
                                                         'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
                                                         'GRASS_MIN_AREA_PARAMETER': 0.0001})
             
            
            # map subtraction in case of having the three shapefiles
            if self.inputLayerCombo1.currentText()!="":
                Processing.runAlgorithm("grass7:v.to.rast",
                                        {'input': inputLayer1, 'type': [0, 1, 3], 'where': '', 'use': 0,
                                         'attribute_column': Attrib1, 'rgb_column': None, 'label_column': None,
                                         'value': None, 'memory': 300,
                                         'output': filedir1, 'GRASS_REGION_PARAMETER': extent,
                                         'GRASS_REGION_CELLSIZE_PARAMETER': cellSize, 'GRASS_RASTER_FORMAT_OPT': '',
                                         'GRASS_RASTER_FORMAT_META': '',
                                         'GRASS_SNAP_TOLERANCE_PARAMETER': -1, 'GRASS_MIN_AREA_PARAMETER': 0.0001})
                Processing.runAlgorithm("grass7:v.to.rast",
                                        {'input': inputLayer2, 'type': [0, 1, 3], 'where': '', 'use': 0,
                                         'attribute_column': Attrib2, 'rgb_column': None, 'label_column': None,
                                         'value': None, 'memory': 300,
                                         'output': filedir2, 'GRASS_REGION_PARAMETER': extent,
                                         'GRASS_REGION_CELLSIZE_PARAMETER': cellSize, 'GRASS_RASTER_FORMAT_OPT': '',
                                         'GRASS_RASTER_FORMAT_META': '',
                                         'GRASS_SNAP_TOLERANCE_PARAMETER': -1, 'GRASS_MIN_AREA_PARAMETER': 0.0001})
                recharge = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/recharge"
                gdalRaster_prec = gdal.Open(str(out))
                x_prec = gdalRaster_prec.RasterXSize
                y_prec = gdalRaster_prec.RasterYSize
                geo_prec = gdalRaster_prec.GetGeoTransform()
                band_prec = gdalRaster_prec.GetRasterBand(1)
                data_prec = band_prec.ReadAsArray(0,0,x_prec,y_prec)
                gdalRaster_runoff = gdal.Open(str(outRunoff))
                x_runoff = gdalRaster_runoff.RasterXSize
                y_runoff = gdalRaster_runoff.RasterYSize
                geo_runoff = gdalRaster_runoff.GetGeoTransform()
                band_runoff = gdalRaster_runoff.GetRasterBand(1)
                data_runoff = band_runoff.ReadAsArray(0,0,x_runoff,y_runoff)   
                gdalRaster_evapo = gdal.Open(str(outEvap))
                x_evapo = gdalRaster_evapo.RasterXSize
                y_evapo = gdalRaster_evapo.RasterYSize
                geo_evapo = gdalRaster_evapo.GetGeoTransform()
                band_evapo = gdalRaster_evapo.GetRasterBand(1)
                data_evapo = band_evapo.ReadAsArray(0,0,x_evapo,y_evapo)   
                sub1 = numpy.subtract(data_prec, data_runoff)
                sub2 = numpy.subtract(sub1, data_evapo)
                # Create an output imagedriver with the substraction result
                driver_out = gdal.GetDriverByName( "GTiff" ) 
                outData_recharge = driver_out.Create(str(recharge), x_prec,y_prec,1, gdal.GDT_Float32)
                outData_recharge.GetRasterBand(1).WriteArray(sub2)
                outData_recharge.SetGeoTransform(geo_prec)  
                outData_recharge = None   
            
            # multiplication of precipitation by 0.1, in case of having only the precipitation shapefile
            if self.inputLayerCombo1.currentText()=="":
                userReclassify = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/reclassify"
                # recharge = precipitation * 0.1 (10% of precipitation)
                gdalRaster = gdal.Open(str(out))
                x = gdalRaster.RasterXSize
                y = gdalRaster.RasterYSize
                geo = gdalRaster.GetGeoTransform()
                band = gdalRaster.GetRasterBand(1)
                data = band.ReadAsArray(0,0,x,y)    
                mul = numpy.multiply(data, 0.1)
                # Create an output imagedriver with the multiplication result
                driver = gdal.GetDriverByName( "GTiff" ) 
                outData = driver.Create(str(userReclassify), x,y,1, gdal.GDT_Float32)
                outData.GetRasterBand(1).WriteArray(mul)
                outData.SetGeoTransform(geo)  
                outData = None 
            
            # indexes for topography for the two methods
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
            
            # reclassification of recharge values in case of having only the precipitation shapefile
            if self.inputLayerCombo1.currentText()=="":
                recharge_prec = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/recharge_prec"
                Processing.runAlgorithm("saga:reclassifygridvalues", None, userReclassify, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, outPath)
                
                
                # add result into canvas
                file_info_prec = QFileInfo(outPath)
                if file_info_prec.exists():
                    layer_name_prec = file_info_prec.baseName()
                else:
                    return False
                rlayer_new_prec = QgsRasterLayer(outPath, layer_name_prec)
                if rlayer_new_prec.isValid():
                    QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_prec)
                    layer_prec = QgsMapCanvasLayer(rlayer_new_prec)
                    layerList_prec = [layer_prec]
                    extent_prec = self.iface.canvas.setExtent(rlayer_new_prec.extent())
                    self.iface.canvas.setLayerSet(layerList_prec)
                    self.iface.canvas.setVisible(True)         
                    return True
                else:
                    return False    
                QMessageBox.information(self, self.tr( "Finished" ), self.tr( "Net Recharge completed." ) )           
            
            # reclassification of recharge values in case of having the three shapefiles
            if self.inputLayerCombo1.currentText()!="":
                recharge_prec_run_evap = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/recharge_prec_run_evap"
                Processing.runAlgorithm("saga:reclassifygridvalues", None, recharge, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, outPath)
    
                
                # add result into canvas
                file_info_prec_runoff_evapo = QFileInfo(outPath)
                if file_info_prec_runoff_evapo.exists():
                    layer_name_prec_runoff_evapo = file_info_prec_runoff_evapo.baseName()
                else:
                    return False
                rlayer_new_prec_runoff_evapo = QgsRasterLayer(outPath, layer_name_prec_runoff_evapo)
                if rlayer_new_prec_runoff_evapo.isValid():
                    QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_prec_runoff_evapo)
                    layer_prec_runoff_evapo = QgsMapCanvasLayer(rlayer_new_prec_runoff_evapo)
                    layerList_prec_runoff_evapo = [layer_prec_runoff_evapo]
                    extent_prec_runoff_evapo = self.iface.canvas.setExtent(rlayer_new_prec_runoff_evapo.extent())
                    self.iface.canvas.setLayerSet(layerList_prec_runoff_evapo)
                    self.iface.canvas.setVisible(True)         
                    return True
                else:
                    return False    
                QMessageBox.information(self, self.tr( "Finished" ), self.tr( "Net Recharge completed." ) )            
            
        if self.inputLayerCombo4.currentText()!="":
            gdal.AllRegister()
            # read mdt data
            outPath2 = self.inputLayerCombo3.text()
            inputRaster = self.inputLayerCombo4.currentText()

            gdalRaster = gdal.Open(str(inputRaster))

            x = gdalRaster.RasterXSize
            y = gdalRaster.RasterYSize
            geo = gdalRaster.GetGeoTransform()  
            minx = geo[0]
            maxy = geo[3]
            maxx = minx + geo[1]*x
            miny = maxy + geo[5]*y
            extent_raster = str(minx) + "," + str(maxx) + "," + str(miny) + "," + str(maxy)  
            pixelSize = geo[1]
            band_mdt = gdalRaster.GetRasterBand(1)
            data_mdt = band_mdt.ReadAsArray(0, 0, x, y)
            
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
            recharge_without_rec = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/recharge_without_rec"
            Processing.runAlgorithm("gdal:rastercalculator",
                           {'INPUT_A': inputRaster, 'BAND_A': 1, 'INPUT_B': None,
                            'BAND_B': -1, 'INPUT_C': None, 'BAND_C': -1, 'INPUT_D': None, 'BAND_D': -1, 'INPUT_E': None,
                            'BAND_E': -1, 'INPUT_F': None, 'BAND_F': -1, 'FORMULA': '(A*0.99+542.22)*0.15',
                            'NO_DATA': None, 'RTYPE': 6, 'EXTRA': '', 'OPTIONS': '',
                            'OUTPUT':recharge_without_rec})
            # Create an output imagedriver with the multiplication result
            # driver2 = gdal.GetDriverByName( "GTiff" )
            # outData2 = driver2.Create(str(recharge_without_rec+'.'+'tif'), x,y,1, gdal.GDT_Float32)
            # outData2.GetRasterBand(1).WriteArray(recharge)
            # outData2.SetGeoTransform(geo)
            #outData2 = None

            Processing.runAlgorithm("gdal:assignprojection",
                           {'INPUT': recharge_without_rec,
                            'CRS': QgsCoordinateReferenceSystem('EPSG:3763')})

            # indexes for topography for the two methods
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
            results = list(map(int, lista))
            QMessageBox.about(self, 'teste', str(results))
          
            Processing.initialize()

            Processing.runAlgorithm("native:reclassifybytable", {
                'INPUT_RASTER': recharge_without_rec,
                'RASTER_BAND': 1, 'TABLE': results,
                'NO_DATA': -9999, 'RANGE_BOUNDARIES': 0, 'NODATA_FOR_MISSING': False, 'DATA_TYPE': 5,
                'OUTPUT': outPath2})

            # add result into canvas
            file_info_norm = QFileInfo(str(outPath2))
            # QMessageBox.about(self, "teste", str(file_info_norm))
            rlayer_new_norm = QgsRasterLayer(outPath2, file_info_norm.fileName(), 'gdal')
            # QMessageBox.about(self, "teste", str(rlayer_new_norm))
            QgsProject.instance().addMapLayer(rlayer_new_norm)
            self.iface.canvas.setExtent(rlayer_new_norm.extent())
            # set the map canvas layer set
            self.iface.canvas.setLayers([rlayer_new_norm])
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
            QMessageBox.information(self, self.tr( "Finished" ), self.tr( "Net Recharge completed." ) )

        if self.inputLayerCombo5.currentText()!="":
            inputLayer = self.inputLayerCombo5.currentText()
            layer = QgsVectorLayer(inputLayer, 'inputLayer', "ogr")
            vectorlayer_vector = layer.dataProvider()
            # extent
            extent_rect = vectorlayer_vector.extent()
            xmin = extent_rect.xMinimum()
            xmax = extent_rect.xMaximum()
            ymin = extent_rect.yMinimum()
            ymax = extent_rect.yMaximum()
            extent = str(xmin) + "," + str(xmax) + "," + str(ymin) + "," + str(ymax)
            # attribute
            Elevation = self.lineAttrib5.currentText()
            # cellsize
            cellSize = int(self.linePix.value())
            prec_value = int(self.lineprec.value())
            outPath = self.inputLayerCombo3.text()

            Processing.initialize()
            raster = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/raster.tif"
            Processing.runAlgorithm("grass7:v.to.rast", {
                'input': inputLayer,
                'type': [0, 1, 3], 'where': '', 'use': 0, 'attribute_column': Elevation, 'rgb_column': '',
                'label_column': '', 'value': 1, 'memory': 300, 'output': raster,
                'GRASS_REGION_PARAMETER': extent + ' [EPSG:3763]',
                'GRASS_REGION_CELLSIZE_PARAMETER': cellSize, 'GRASS_RASTER_FORMAT_OPT': '', 'GRASS_RASTER_FORMAT_META': '',
                'GRASS_SNAP_TOLERANCE_PARAMETER': -1, 'GRASS_MIN_AREA_PARAMETER': 0.0001})

            precipitacao = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/precipitacao.tif"
            Processing.runAlgorithm("grass7:r.mapcalc.simple", {
                'a': raster,
                'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'expression': 'A*'+ str(prec_value) + '/100',
                'output': precipitacao,
                'GRASS_REGION_PARAMETER': extent +' [EPSG:3763]',
                'GRASS_REGION_CELLSIZE_PARAMETER': cellSize, 'GRASS_RASTER_FORMAT_OPT': '', 'GRASS_RASTER_FORMAT_META': ''})

            # indexes for topography
            numberRows = int(self.tableWidget.rowCount())
            numberColumns = int(self.tableWidget.columnCount())
            classes = ''
            lista = []
            for i in range(0, numberRows):
                for j in range(0, numberColumns):
                    self.line = self.tableWidget.item(i, j)
                    lista = lista + [self.line.text()]
                    string = ","
                    intervalos = string.join(lista)
            results = list(map(float, lista))

            # Processing.runAlgorithm("saga:reclassifyvalues",
            #                         {'INPUT': precipitacao, 'METHOD': 2, 'OLD': 0, 'NEW': 1, 'SOPERATOR': 0, 'MIN': 0,
            #                          'MAX': 1,
            #                          'RNEW': 2, 'ROPERATOR': 0, 'RETAB': results, 'TOPERATOR': 0, 'NODATAOPT': True,
            #                          'NODATA': 0,
            #                          'OTHEROPT': True, 'OTHERS': 0, 'RESULT': outPath})

            Processing.runAlgorithm("native:reclassifybytable",
                                    {'INPUT_RASTER': str(precipitacao),
                                     'RASTER_BAND': 1, 'TABLE': results,
                                     'NO_DATA': -9999, 'RANGE_BOUNDARIES': 0, 'NODATA_FOR_MISSING': False,
                                     'DATA_TYPE': 5,
                                     'OUTPUT': outPath})

            # add result into canvas
            file_info_norm = QFileInfo(str(outPath))
            # QMessageBox.about(self, "teste", str(file_info_norm))
            rlayer_new_norm = QgsRasterLayer(outPath, file_info_norm.fileName(), 'gdal')
            # QMessageBox.about(self, "teste", str(rlayer_new_norm))
            QgsProject.instance().addMapLayer(rlayer_new_norm)
            self.iface.canvas.setExtent(rlayer_new_norm.extent())
            # set the map canvas layer set
            self.iface.canvas.setLayers([rlayer_new_norm])
            QMessageBox.information(self, self.tr("Finished"), self.tr("Net Recharge completed."))


        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)