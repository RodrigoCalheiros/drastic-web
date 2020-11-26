from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *
from .Ui_Superficie_topografica import Ui_Superficie_topografica
from . import GdalTools_utils

try:
    from qgis.PyQt.QtCore import QString
except ImportError:
    QString = str
from processing.core.Processing import Processing
# from processing.core.ProcessingGdalTools_utils import ProcessingGdalTools_utils
from . import ftools_utils
from osgeo import ogr
from processing import *
from osgeo.gdalconst import GA_ReadOnly
from osgeo import gdal
from processing import ProcessingPlugin
# from processing.outputs import OutputRaster
import sys, os
import numpy
from qgis.PyQt import QtCore, QtGui


class Superficie_topografica(QDialog, Ui_Superficie_topografica):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.selectButton.clicked.connect(self.fillInputFileEdit)
        self.inputLayerCombo.currentIndexChanged.connect(self.fillInputAttrib)
        self.selectButton_dem.clicked.connect(self.fillInputRasterEdit)
        self.selectButton3.clicked.connect(self.fillOutputFileEdit)
        self.buttonAdd.clicked.connect(self.actionAdd)
        self.buttonRemove.clicked.connect(self.actionRemove)
        self.buttonBox.accepted.connect(self.convert)
        self.plugin_dir = os.path.dirname(__file__)
        # self.btnCancel = self.buttonBox.button( QDialogButtonBox.Cancel )
        # QObject.connect(self.btnCancel, SIGNAL( "clicked()" ), self.stopProcessing)

        # connect help
        # QObject.connect(self.buttonBox.button(QtGui.QDialogButtonBox.Help), SIGNAL("clicked()"), self.help)
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)

    # INPUT VECTOR FILE
    def fillInputFileEdit(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedVectorFilter()
        inputFile, encoding = GdalTools_utils.FileDialog.getOpenFileName(self, self.tr("Select the input file"),
                                                                         GdalTools_utils.FileFilter.allVectorsFilter(),
                                                                         lastUsedFilter, True)
        self.lastEncoding = encoding
        self.loadFields(inputFile)
        self.inputLayerCombo.addItem(inputFile)
        check = QFile(inputFile)

    def fillInputAttrib(self, inputFile):
        self.layer = QgsVectorLayer(unicode(self.inputLayerCombo.currentText()).encode('utf8'), inputFile, "ogr")
        self.lineAttrib.clear()
        changedField = ftools_GdalTools_utils.getFieldList(self.layer)
        for f in changedField:
            if f.type() == QVariant.Int or f.type() == QVariant.String or f.type() == QVariant.Double:
                self.lineAttrib.addItem(unicode(f.name()))

    def loadFields(self, vectorFile=QString()):
        if vectorFile == None:
            return

        try:
            (fields, names) = GdalTools_utils.getVectorFields(vectorFile)
        except Exception as e:
            QErrorMessage(self).showMessage(str(e))

        self.inputLayerCombo.clearEditText()
        ncodec = QTextCodec.codecForName(self.lastEncoding)

    def help(self):
        QMessageBox.about(self, "Superficie_topografica", """<p><b>Superficie_topografica factor</b></p> 
        <p><b>Definition:</b>The T factor concerns the terrain surface slope and its influence on the infiltration of polluted water into the soil. 
        The Superficie_topografica section implements two different methods. If a contour shapefile is available with elevation values, the feature creates the DEM, derives from it the slope and reclassifies according to the defined ratings. 
        If the user does not have the contour file but already has the DEM (raster file), he specifies it as input file, and the DEM generation step is skipped. 
        As before, the slope is calculated and reclassified. </p>
        <p><b>First method</b></p> 
        <p>Input file = contour lines. The user must define the attribute and the cell size. </p>
        <p><b>Second method</b></p> 
        <p>Input file = DEM.</p>
        <p><b>Ratings:</b>The ratings are adopted by Aller et al. but the user can modify the values, add or remove lines.</p>
        <p><b>Output file:</b> Superficie_topografica raster file</p>""")

        # ------------------------------ // ------------------------------------ // ----------------------------

    # INPUT RASTER FILE
    def fillInputRasterEdit(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedRasterFilter()
        inputFile, encoding = GdalTools_utils.FileDialog.getOpenFileName(self, self.tr("Select the input DEM"),
                                                                         GdalTools_utils.FileFilter.allVectorsFilter(),
                                                                         lastUsedFilter, True)
        self.lastEncoding = encoding
        # self.loadFields(inputFile)
        self.inputLayerCombo_dem.addItem(inputFile)
        # check = QFile(inputFile)    

    # OUTPUT RASTER FILE
    def fillOutputFileEdit(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedRasterFilter()
        outputFile = GdalTools_utils.FileDialog.getSaveFileName(self, self.tr(
            "Select the raster file to save the results to"), '.sdat',
                                                                lastUsedFilter)
        self.inputLayerCombo3.setText(outputFile + '.sdat')

    # -------------------------------- // --------------------------------- // -------------------------------

    # BUTTON ADD AND REMOVE CLASSES
    def actionAdd(self):
        n = self.tableWidget.rowCount()
        QMessageBox.about(self, "Superficie_topografica", str(n))
        self.tableWidget.insertRow(n)
        n = self.tableWidget.rowCount()
        return True

    def actionRemove(self):
        n = self.tableWidget.rowCount()
        for i in range(1, n):
            self.tableWidget.removeRow(n - 1)
        n = self.tableWidget.rowCount()
        return True

    # ------------------------------- // ------------------------------------ // --------------------------------

    # CONVERT VECTOR TO GRID
    def convert(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(False)
        if self.inputLayerCombo.currentText() != "":
            inputLayer = self.inputLayerCombo.currentText()
            # layer information
            layer = QgsVectorLayer(inputLayer, inputLayer, "ogr")
            vectorlayer_vector = layer.dataProvider()
            # extent
            extent_rect = vectorlayer_vector.extent()
            xmin = extent_rect.xMinimum()
            xmax = extent_rect.xMaximum()
            ymin = extent_rect.yMinimum()
            ymax = extent_rect.yMaximum()
            extent = str(xmin) + "," + str(xmax) + "," + str(ymin) + "," + str(ymax)
            # elevation attribute
            Elevation = self.lineAttrib.currentText()
            # cellsize
            cellSize = int(self.linePix.value())
            outPath = self.inputLayerCombo3.text()

            Processing.initialize()
            # grid directory (qgis2)
            filedir = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/raster"

            Processing.runAlgorithm("grass7:v.to.rast", {'input': inputLayer, 'type': [0, 1, 3], 'where': '', 'use': 0,
                                                         'attribute_column': Elevation, 'rgb_column': None,
                                                         'label_column': None, 'value': None, 'memory': 300,
                                                         'output': filedir, 'GRASS_REGION_PARAMETER': extent,
                                                         'GRASS_REGION_CELLSIZE_PARAMETER': cellSize,
                                                         'GRASS_RASTER_FORMAT_OPT': '', 'GRASS_RASTER_FORMAT_META': '',
                                                         'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
                                                         'GRASS_MIN_AREA_PARAMETER': 0.0001})

            userDir = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/grid"
            Processing.runAlgorithm("grass7:r.surf.contour", None, out, extent, cellSize, userDir)

            # slope
            userSlope = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/slope"
            outGrid = userDir + "." + "tif"
            Processing.runAlgorithm("grass7:r.slope.aspect", None, outGrid, 1, 1, 1.0, 0.0, extent, cellSize, userSlope,
                                    None, None, None, None, None, None, None, None)

            # reclassify slope raster
            outSlope = userSlope + "." + "tif"
            userSlopeRec = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/slopeRec"

        if self.inputLayerCombo.currentText() == "":
            gdal.AllRegister()
            inputLayer_dem = self.inputLayerCombo_dem.currentText()
            # QMessageBox.about(self, "recharge", str(inputRaster))
            gdalRaster = gdal.Open(str(inputLayer_dem))
            # QMessageBox.about(self, "recharge", str(gdalRaster))
            x = gdalRaster.RasterXSize
            y = gdalRaster.RasterYSize
            geo = gdalRaster.GetGeoTransform()
            minx = geo[0]
            maxy = geo[3]
            maxx = minx + geo[1] * x
            miny = maxy + geo[5] * y
            extent_raster = str(minx) + "," + str(maxx) + "," + str(miny) + "," + str(maxy)
            pixelSize = geo[1]

            ## layer information
            # layer_raster = QgsRasterLayer(unicode(inputLayer_dem).encode('utf8'), inputLayer_dem , "gdal")         
            # rasterlayer =  layer_raster.dataProvider()
            ## extent
            # extent_rect = rasterlayer.extent()
            # xmin = extent_rect.xMinimum()
            # xmax = extent_rect.xMaximum()
            # ymin = extent_rect.yMinimum()
            # ymax = extent_rect.yMaximum()
            # extent = str(xmin) + "," + str(xmax) + "," + str(ymin) + "," + str(ymax)
            ##QMessageBox.about(self, "Superficie_topografica", str(extent))
            ## cellsize
            # cellSize = layer_raster.rasterUnitsPerPixelX()
            ##cellSize = int(self.linePix.value())
            ##QMessageBox.about(self, "Superficie_topografica", str(cellSize))
            outPath = self.inputLayerCombo3.text()

            # pixel size is the same as the dem raster, miss reamostragem

            Processing.initialize()
            # mdt_interp = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/mdt_interp"
            # Processing.runAlgorithm("grass7:r.surf.idw", None, inputLayer_dem, 12, False, extent_raster, pixelSize, mdt_interp)
            # mdt = mdt_interp + "." + "tif"

            # gdalMDT = gdal.Open(str(mdt_interp) + "." + "tif")
            # x_mdt = gdalMDT.RasterXSize
            # y_mdt = gdalMDT.RasterYSize            
            # geo_mdt = gdalMDT.GetGeoTransform() 
            # band_mdt = gdalMDT.GetRasterBand(1)
            # data_mdt = band_mdt.ReadAsArray(0,0,x_mdt,y_mdt)   
            # geo_mdt = gdalMDT.GetGeoTransform()  
            # minx = geo_mdt[0]
            # maxy = geo_mdt[3]
            # maxx = minx + geo_mdt[1]*x_mdt
            # miny = maxy + geo_mdt[5]*y_mdt
            # extent_raster_new = str(minx) + "," + str(maxx) + "," + str(miny) + "," + str(maxy)  
            # pixelSize_new = geo_mdt[1]            

            # slope from DEM
            userSlope_dem = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/slope_dem.tif"
            Processing.runAlgorithm("grass7:r.slope.aspect",
                                    {'elevation': inputLayer_dem, 'format': 1, 'precision': 0,
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
            # outSlope_dem = userSlope_dem + "." + "tif"
            # userSlopeRec_dem = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/slopeRec_dem"

            # indexes for Superficie_topografica
            # numberRows = int(self.tableWidget.rowCount())
            # numberColumns = int(self.tableWidget.columnCount())
            # classes = ''
            # lista = []
            # for i in range(0, numberRows):
            #     for j in range(0, numberColumns):
            #         self.line = self.tableWidget.item(i, j)
            #         lista = lista + [str(self.line.text())]
            #         string = ","
            #         intervalos = string.join(lista)
            # results = list(map(int, lista))

            # QMessageBox.about(self, "Superficie_topografica", str(userSlope_dem))

            # list_new = []
            # list_new_x = []
            # list_new_y = []
            # # QMessageBox.about(self, 'teste', str(self.plugin_dir))
            # # FILE = os.path.join(self.plugin_dir, "//SINTACS grafico D.txt")
            # with open(os.path.join(self.plugin_dir, "SINTACS grafico S.txt"), 'r') as f:
            #     d = {line.split('\t')[0]: line.split('\t')[1] for line in f}
            # #QMessageBox.about(self, "teste", str(d))
            # # read raster values
            # raster = gdal.Open(str(userSlope_dem))
            # data_mdt = raster.ReadAsArray()
            # values_raster = numpy.unique(data_mdt)
            # # QMessageBox.about(self, 'teste', values_raster)
            # for element in values_raster:
            #     #QMessageBox.about(self, 'teste', str(element))
            #     if element <= 24.42:
            #         #QMessageBox.about(self, 'teste', str(element))
            #         # get the key of a certain value
            #         target = element
            #         # key, value = min(d.items(), key=lambda kv: abs(float(kv[1]) - target))
            #         m = d.get(target, d[min(d.keys(), key=lambda k: abs(float(k) - target))])
            #         # remove \n from list
            #         m_new = m.replace('\n', '')
            #         list_new_x = list_new_x + [element]
            #         list_new_y = list_new_y + [float(m_new)]
            #
            # # Set the path for the output file
            # output_file = open('C:\Artigos\DRASTIC_melhoria/file.txt', 'w')
            # for ii in range(len(list_new_x)):
            #     list_new.append(list_new_x[ii])
            #     list_new.append(list_new_x[ii] + float(0.01))
            #     list_new.append(list_new_y[ii])
            # list_new = list_new + [24.43]
            # list_new = list_new + [1000]
            # list_new = list_new + [0.9717]
            # QMessageBox.about(self, "teste", str(list_new))

            # Get the features and properly rewrite them as lines
            # for feat in list_new:
            #     output_file.write(str(feat)+'/t')
            # output_file.close()
            #QMessageBox.about(self, 'teste', str(list_new[20:]))

            # if self.inputLayerCombo.currentText() != "":
            #     Processing.runAlgorithm("saga:reclassifyvalues",
            #                             {'INPUT': outSlope, 'METHOD': 2, 'OLD': 0, 'NEW': 1, 'SOPERATOR': 0, 'MIN': 0,
            #                              'MAX': 1,
            #                              'RNEW': 2, 'ROPERATOR': 0, 'RETAB': list_new, 'TOPERATOR': 0, 'NODATAOPT': True,
            #                              'NODATA': 0,
            #                              'OTHEROPT': True, 'OTHERS': 0, 'RESULT': outPath})


            # reclassify slope_dem values
            #if self.inputLayerCombo.currentText() == "":
            # topo_interp = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/topo_interp.tif"
            # Processing.runAlgorithm("saga:reclassifyvalues",
            #                         {'INPUT': userSlope_dem, 'METHOD': 2, 'OLD': 0, 'NEW': 1, 'SOPERATOR': 0, 'MIN': 0,
            #                          'MAX': 1,
            #                          'RNEW': 2, 'ROPERATOR': 0, 'RETAB': list_new, 'TOPERATOR': 0, 'NODATAOPT': True,
            #                          'NODATA': 0,
            #                          'OTHEROPT': True, 'OTHERS': 0, 'RESULT': outPath})

            Processing.runAlgorithm("grass7:r.reclass", {
                'input': userSlope_dem,
                'rules': os.path.join(self.plugin_dir, "SINTACS grafico S - Copy.txt"), 'txtrules': '',
                'output': outPath,
                'GRASS_REGION_PARAMETER': None, 'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
                'GRASS_RASTER_FORMAT_META': ''})

            # topo = topo_interp + "." + "tif"

            # Processing.runAlgorithm("grass7:r.surf.idw", None, topo_interp, 12, False, extent_raster, pixelSize, outPath)

            ## multiply by weight
            # fileInfo_dem = QFileInfo(outSlopeRec_dem)
            # baseName_dem = fileInfo_dem.baseName()
            # rlayer_dem = QgsRasterLayer(outSlopeRec_dem, baseName_dem)
            # gdalRaster_dem = gdal.Open(str(outSlopeRec_dem))
            # x_dem = gdalRaster_dem.RasterXSize
            # y_dem = gdalRaster_dem.RasterYSize
            # geo_dem = gdalRaster_dem.GetGeoTransform()
            # band_dem = gdalRaster_dem.GetRasterBand(1)
            # data_dem = band_dem.ReadAsArray(0,0,x_dem,y_dem)    
            # mul_dem = numpy.multiply(data_dem, int(self.lineWeight.value()))
            ## Create an output imagedriver
            # driver_dem = gdal.GetDriverByName( "GTiff" ) 
            # outData_dem = driver_dem.Create(str(outPath), x_dem,y_dem,1, gdal.GDT_Float32)
            # outData_dem.GetRasterBand(1).WriteArray(mul_dem)
            # outData_dem.SetGeoTransform(geo_dem)  
            # outData_dem = None

            # add result into canvas
            file_info_norm = QFileInfo(str(outPath + '.sdat'))
            # QMessageBox.about(self, "teste", str(file_info_norm))
            rlayer_new_norm = QgsRasterLayer(outPath + '.sdat', file_info_norm.fileName(), 'gdal')
            # QMessageBox.about(self, "teste", str(rlayer_new_norm))
            QgsProject.instance().addMapLayer(rlayer_new_norm)
            self.iface.canvas.setExtent(rlayer_new_norm.extent())
            # set the map canvas layer set
            self.iface.canvas.setLayers([rlayer_new_norm])
            # file_info_dem = QFileInfo(outPath)
            # if file_info_dem.exists():
            #     layer_name_dem = file_info_dem.baseName()
            # else:
            #     return False
            # rlayer_new_dem = QgsRasterLayer(outPath, layer_name_dem)
            # if rlayer_new_dem.isValid():
            #     QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_dem)
            #     layer_dem = QgsMapCanvasLayer(rlayer_new_dem)
            #     layerList_dem = [layer_dem]
            #     extent_dem = self.iface.canvas.setExtent(rlayer_new_dem.extent())
            #     self.iface.canvas.setLayerSet(layerList_dem)
            #     self.iface.canvas.setVisible(True)
            #     return True
            # else:
            #     return False

        QMessageBox.information(self, self.tr("Finished"), self.tr("Superficie_topografica completed."))
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)

# ----------------------------------- // ---------------------------------------- // -----------------------------------




