from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *
from .Ui_conducibilita import Ui_Conducibilita
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


class Conducibilita(QDialog, Ui_Conducibilita):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.selectButton.clicked.connect(self.fillInputFileEdit)
        self.inputLayerCombo.currentIndexChanged.connect(self.fillInputAttrib)
        self.selectButton3.clicked.connect(self.fillOutputFileEdit)
        self.buttonAdd.clicked.connect(self.actionAdd)
        self.buttonRemove.clicked.connect(self.actionRemove)
        self.buttonBox.accepted.connect(self.convert)
        self.plugin_dir = os.path.dirname(__file__)

        # connect help
        # QObject.connect(self.buttonBox.button(QtGui.QDialogButtonBox.Help), SIGNAL("clicked()"), self.help)

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
        self.layer = QgsVectorLayer(self.inputLayerCombo.currentText(),
                                    (QFileInfo(str(self.inputLayerCombo.currentText()))).baseName(), "ogr")
        self.lineAttrib.clear()
        changedField = ftools_utils.getFieldList(self.layer)
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
        QMessageBox.about(self, "Hydraulic Conductivity", """<p><b>Hydraulic Conductivity factor</b></p> 
        <p><b>Definition:</b>The C factor relies on the fact that the higher the hydraulic conductivity of the aquifer material, the higher the groundwater vulnerability to pollution. 
        Hydraulic conductivity values are usually obtained from pumping tests and may be introduced by the user in the attribute table of the geological vector file. 
        If the user does not have access to specific hydraulic conductivity values for the region under study, typical values for the prevailing hydrogeological conditions may be adopted.  </p>
        <p><b>Method</b></p> 
        <p>Input file = geological map or a map with hydraulic conductivity values. The user must to define the attribute and the cell size. </p>
        <p><b>Ratings:</b>The ratings are adopted by Aller et al. but the user can modify the values, add or remove lines. </p>
        <p><b>Output file:</b> Hydraulic Conductivity raster file</p>""")

        # ------------------------------ // ------------------------------------ // ----------------------------   

    # OUTPUT RASTER FILE
    def fillOutputFileEdit(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedRasterFilter()
        outputFile = GdalTools_utils.FileDialog.getSaveFileName(self, self.tr(
            "Select the raster file to save the results to"), '.sdat',
                                                                lastUsedFilter)
        self.inputLayerCombo3.setText(outputFile+'.sdat')

    # -------------------------------- // --------------------------------- // -------------------------------     

    # BUTTON ADD AND REMOVE CLASSES
    def actionAdd(self):
        n = self.tableWidget.rowCount()
        self.tableWidget.insertRow(n)
        n = self.tableWidget.rowCount()
        return True

    def actionRemove(self):
        n = self.tableWidget.rowCount()
        for i in range(1, n):
            self.tableWidget.removeRow(n - 1)
        n = self.tableWidget.rowCount()
        return True

    # ---------------------------------- // ----------------------------- // ------------------------------------       

    # CONVERT SHAPEFILE TO RASTER
    def convert(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(False)
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
        # attribute
        Elevation = self.lineAttrib.currentText()
        # cellsize
        cellSize = int(self.linePix.value())
        outPath = self.inputLayerCombo3.text()

        # indexes for hidraulic conductivity
        numberRows = int(self.tableWidget.rowCount())
        numberColumns = int(self.tableWidget.columnCount())
        classes = ''
        lista = []
        for i in range(0, numberRows):
            for j in range(0, numberColumns):
                self.line = self.tableWidget.item(i, j)
                lista = lista + [str(self.line.text())]
                string = ","
                intervals = string.join(lista)
        results = list(map(float, lista))

        Processing.initialize()
        conductivity = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/conductivity"

        Processing.runAlgorithm("grass7:v.to.rast",
                                {'input': inputLayer, 'type': [0, 1, 3], 'where': '', 'use': 0,
                                 'attribute_column': Elevation, 'rgb_column': None, 'label_column': None,
                                 'value': None, 'memory': 300,
                                 'output': conductivity, 'GRASS_REGION_PARAMETER': extent,
                                 'GRASS_REGION_CELLSIZE_PARAMETER': cellSize, 'GRASS_RASTER_FORMAT_OPT': '',
                                 'GRASS_RASTER_FORMAT_META': '',
                                 'GRASS_SNAP_TOLERANCE_PARAMETER': -1, 'GRASS_MIN_AREA_PARAMETER': 0.0001})

        # list_new = []
        # list_new_x = []
        # list_new_y = []
        # # QMessageBox.about(self, 'teste', str(self.plugin_dir))
        # # FILE = os.path.join(self.plugin_dir, "//SINTACS grafico D.txt")
        # with open(os.path.join(self.plugin_dir, "SINTACS grafico C.txt"), 'r') as f:
        #     d = {line.split('\t')[0]: line.split('\t')[1] for line in f}
        # #QMessageBox.about(self, "teste", str(d))
        # # read raster values
        # raster = gdal.Open(str(conductivity))
        # data_mdt = raster.ReadAsArray()
        # values_raster = numpy.unique(data_mdt)
        # # QMessageBox.about(self, 'teste', values_raster)
        # for element in values_raster:
        #     # get the key of a certain value
        #     target = element
        #     # key, value = min(d.items(), key=lambda kv: abs(float(kv[1]) - target))
        #     m = d.get(target, d[min(d.keys(), key=lambda k: abs(float(k) - target))])
        #     # remove \n from list
        #     m_new = m.replace('\n', '')
        #     list_new_x = list_new_x + [element]
        #     list_new_y = list_new_y + [float(m_new)]
        # for ii in range(len(list_new_x)):
        #     list_new.append(list_new_x[ii])
        #     list_new.append(list_new_x[ii] + float(0.01))
        #     list_new.append(list_new_y[ii])
        # QMessageBox.about(self, "teste", str(list_new))

        Processing.runAlgorithm("grass7:r.reclass", {
            'input': conductivity,
            'rules': os.path.join(self.plugin_dir, "SINTACS grafico C.txt"), 'txtrules': '',
            'output': outPath,
            'GRASS_REGION_PARAMETER': None, 'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_RASTER_FORMAT_META': ''})


        # cond_reclassify = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/cond_reclassify.sdat"
        # Processing.runAlgorithm("saga:reclassifyvalues",
        #                         {'INPUT': conductivity, 'METHOD': 2, 'OLD': 0, 'NEW': 1, 'SOPERATOR': 0, 'MIN': 0,
        #                          'MAX': 1,
        #                          'RNEW': 2, 'ROPERATOR': 0, 'RETAB': list_new, 'TOPERATOR': 0, 'NODATAOPT': True,
        #                          'NODATA': 0,
        #                          'OTHEROPT': True, 'OTHERS': 0, 'RESULT': outPath})

        # Processing.runAlgorithm("grass7:r.surf.idw", None, cond_reclassify, 12, False, extent, cellSize, outPath)

        # add result into canvas
        file_info_norm = QFileInfo(str(outPath + '.sdat'))
        # QMessageBox.about(self, "teste", str(file_info_norm))
        rlayer_new_norm = QgsRasterLayer(outPath + '.sdat', file_info_norm.fileName(), 'gdal')
        # QMessageBox.about(self, "teste", str(rlayer_new_norm))
        QgsProject.instance().addMapLayer(rlayer_new_norm)
        self.iface.canvas.setExtent(rlayer_new_norm.extent())
        # set the map canvas layer set
        self.iface.canvas.setLayers([rlayer_new_norm])
        # add result into canvas
        # file_info = QFileInfo(outPath)
        # if file_info.exists():
        #     layer_name = file_info.baseName()
        # else:
        #     return False
        # rlayer_new = QgsRasterLayer(outPath, layer_name)
        # if rlayer_new.isValid():
        #     QgsMapLayerRegistry.instance().addMapLayer(rlayer_new)
        #     layer = QgsMapCanvasLayer(rlayer_new)
        #     layerList = [layer]
        #     extent = self.iface.canvas.setExtent(rlayer_new.extent())
        #     self.iface.canvas.setLayerSet(layerList)
        #     self.iface.canvas.setVisible(True)
        #     return True
        # else:
        #     return False
        # QMessageBox.information(self, self.tr( "Finished" ), self.tr( "Hidraulic conductivity completed." ) )

        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)