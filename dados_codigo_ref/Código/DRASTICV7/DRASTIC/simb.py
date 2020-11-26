from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *
from .Ui_simb import Ui_simb

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
#from .simb_window import simb_window


class simb(QDialog, Ui_simb):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.selectButton3.clicked.connect(self.fillOutputFileEdit)
        self.buttonBox.accepted.connect(self.convert)
        self.plugin_dir = os.path.dirname(__file__)
        layers = [layer for layer in QgsProject.instance().mapLayers().values()]
        self.layers_directory = [layer.source() for layer in QgsProject.instance().mapLayers().values()]

        self.layer_list = []
        # For every item (which we call "layer") in all loaded layers
        for layer in layers:
            # Add it to the list
            self.layer_list.append(layer.source())
        # Clear comboBox (useful so we don't create duplicate items in list)
        self.inputLayerCombo.clear()
        self.inputLayerCombo1.clear()
        self.inputLayerCombo2.clear()
        self.inputLayerCombo3.clear()
        # Add all items in list to comboBox
        self.inputLayerCombo.addItems(self.layer_list)
        self.inputLayerCombo1.addItems(self.layer_list)
        self.inputLayerCombo2.addItems(self.layer_list)
        self.inputLayerCombo3.addItems(self.layer_list)


    # OUTPUT RASTER FILE
    def fillOutputFileEdit(self):
        lastUsedFilter = GdalTools_utils.FileFilter.lastUsedRasterFilter()
        outputFile = GdalTools_utils.FileDialog.getSaveFileName(self, self.tr(
            "Select the html file to save the results to"), ".qml",
                                                                lastUsedFilter)

        self.inputLayerCombo4.setText(outputFile + '.qml')

    def convert(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(False)


        if self.selectDRASTIC.isChecked():
            inputLayer = QgsRasterLayer(self.inputLayerCombo.currentText(), 'DRASTIC')
            QgsProject.instance().addMapLayer(inputLayer)

            # editing the new column
            numberRows = int(self.tableWidget.rowCount())
            numberColumns = int(self.tableWidget.columnCount())
            classes = ''
            lista = []
            for i in range(0, numberColumns):
                for j in range(1, numberRows):
                    self.line = self.tableWidget.item(j, i)
                    lista = lista + [str(self.line.text())]

            algorithm = QgsContrastEnhancement.StretchToMinimumMaximum
            #limits = QgsRaster.ContrastEnhancementMinMax
            inputLayer.setContrastEnhancement(algorithm)


            s = QgsRasterShader()
            c = QgsColorRampShader()
            c.setColorRampType(QgsColorRampShader.Interpolated)
            i = []
            qri = QgsColorRampShader.ColorRampItem
            i.append(qri(float(lista[7]), QColor(43, 131, 186, 255), str(lista[7])))
            i.append(qri(float(lista[6]), QColor(199, 233, 173, 255), str(lista[6])))
            i.append(qri(float(lista[5]), QColor(254, 201, 128, 255), str(lista[5])))
            i.append(qri(float(lista[4]), QColor(215, 25, 28, 255), str(lista[4])))
            c.setColorRampItemList(i)
            s.setRasterShaderFunction(c)
            ps = QgsSingleBandPseudoColorRenderer(inputLayer.dataProvider(), 1, s)
            inputLayer.setRenderer(ps)
            QgsProject.instance().addMapLayer(inputLayer)
            outPath = self.inputLayerCombo4.text()
            inputLayer.saveNamedStyle(outPath)

        if self.selectGOD.isChecked():
            inputLayer = QgsRasterLayer(self.inputLayerCombo1.currentText(), 'GOD')
            QgsProject.instance().addMapLayer(inputLayer)

            # editing the new column
            numberRows = int(self.tableWidget.rowCount())
            numberColumns = int(self.tableWidget.columnCount())
            classes = ''
            lista = []
            for i in range(0, numberColumns):
                for j in range(1, numberRows):
                    self.line = self.tableWidget.item(j, i)
                    lista = lista + [str(self.line.text())]

            algorithm = QgsContrastEnhancement.StretchToMinimumMaximum
            # limits = QgsRaster.ContrastEnhancementMinMax
            inputLayer.setContrastEnhancement(algorithm)

            s = QgsRasterShader()
            c = QgsColorRampShader()
            c.setColorRampType(QgsColorRampShader.Interpolated)
            i = []
            qri = QgsColorRampShader.ColorRampItem
            i.append(qri(float(lista[11]), QColor(43, 131, 186, 255), str(lista[11])))
            i.append(qri(float(lista[10]), QColor(199, 233, 173, 255), str(lista[10])))
            i.append(qri(float(lista[9]), QColor(254, 201, 128, 255), str(lista[9])))
            i.append(qri(float(lista[8]), QColor(215, 25, 28, 255), str(lista[8])))
            c.setColorRampItemList(i)
            s.setRasterShaderFunction(c)
            ps = QgsSingleBandPseudoColorRenderer(inputLayer.dataProvider(), 1, s)
            inputLayer.setRenderer(ps)
            QgsProject.instance().addMapLayer(inputLayer)
            outPath = self.inputLayerCombo4.text()
            inputLayer.saveNamedStyle(outPath)

        if self.selectSI.isChecked():
            inputLayer = QgsRasterLayer(self.inputLayerCombo2.currentText(), 'SI')
            QgsProject.instance().addMapLayer(inputLayer)

            # editing the new column
            numberRows = int(self.tableWidget.rowCount())
            numberColumns = int(self.tableWidget.columnCount())
            classes = ''
            lista = []
            for i in range(0, numberColumns):
                for j in range(1, numberRows):
                    self.line = self.tableWidget.item(j, i)
                    lista = lista + [str(self.line.text())]

            algorithm = QgsContrastEnhancement.StretchToMinimumMaximum
            # limits = QgsRaster.ContrastEnhancementMinMax
            inputLayer.setContrastEnhancement(algorithm)

            s = QgsRasterShader()
            c = QgsColorRampShader()
            c.setColorRampType(QgsColorRampShader.Interpolated)
            i = []
            qri = QgsColorRampShader.ColorRampItem
            i.append(qri(float(lista[15]), QColor(43, 131, 186, 255), str(lista[15])))
            i.append(qri(float(lista[14]), QColor(199, 233, 173, 255), str(lista[14])))
            i.append(qri(float(lista[13]), QColor(254, 201, 128, 255), str(lista[13])))
            i.append(qri(float(lista[12]), QColor(215, 25, 28, 255), str(lista[12])))
            c.setColorRampItemList(i)
            s.setRasterShaderFunction(c)
            ps = QgsSingleBandPseudoColorRenderer(inputLayer.dataProvider(), 1, s)
            inputLayer.setRenderer(ps)
            QgsProject.instance().addMapLayer(inputLayer)
            outPath = self.inputLayerCombo4.text()
            inputLayer.saveNamedStyle(outPath)

        if self.selectSINTACS.isChecked():
            inputLayer = QgsRasterLayer(self.inputLayerCombo3.currentText(), 'SINTACS')
            QgsProject.instance().addMapLayer(inputLayer)

            # editing the new column
            numberRows = int(self.tableWidget.rowCount())
            numberColumns = int(self.tableWidget.columnCount())
            classes = ''
            lista = []
            for i in range(0, numberColumns):
                for j in range(1, numberRows):
                    self.line = self.tableWidget.item(j, i)
                    lista = lista + [str(self.line.text())]

            algorithm = QgsContrastEnhancement.StretchToMinimumMaximum
            # limits = QgsRaster.ContrastEnhancementMinMax
            inputLayer.setContrastEnhancement(algorithm)

            s = QgsRasterShader()
            c = QgsColorRampShader()
            c.setColorRampType(QgsColorRampShader.Interpolated)
            i = []
            qri = QgsColorRampShader.ColorRampItem
            i.append(qri(float(lista[19]), QColor(43, 131, 186, 255), str(lista[19])))
            i.append(qri(float(lista[18]), QColor(199, 233, 173, 255), str(lista[18])))
            i.append(qri(float(lista[17]), QColor(254, 201, 128, 255), str(lista[17])))
            i.append(qri(float(lista[16]), QColor(215, 25, 28, 255), str(lista[16])))
            c.setColorRampItemList(i)
            s.setRasterShaderFunction(c)
            ps = QgsSingleBandPseudoColorRenderer(inputLayer.dataProvider(), 1, s)
            inputLayer.setRenderer(ps)
            QgsProject.instance().addMapLayer(inputLayer)
            outPath = self.inputLayerCombo4.text()
            inputLayer.saveNamedStyle(outPath)


        QMessageBox.information(self, self.tr("Finished"), self.tr("Map completed."))

        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)