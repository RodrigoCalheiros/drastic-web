import sys, os
import settings
from osgeo import gdal
from PyQt5.QtCore import *
from qgis.core import QgsProcessingRegistry
from qgis.analysis import QgsNativeAlgorithms
from qgis.core import *
QgsApplication.setPrefixPath('/usr', True)

sys.path.append('/usr/share/qgis/python/plugins/')
from processing.core.Processing import Processing

class Aquifer:

    def __init__(self, input_file, output_file, cellSize, elevation, rattings):
        self.input_mdt = input_file
        self.output_file = output_file
        self.cellSize = int(cellSize)
        self.elevation = elevation
        self.rattings = rattings
        

    def convert_mdt(self, process_path):
        qgs = QgsApplication([], False)
        qgs.initQgis()
        Processing.initialize()
            
        QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

        gdal.AllRegister()

        inputLayer = self.input_mdt
        process_path = process_path
        outPath = self.output_file
        cellSize = self.cellSize
        #select field
        Elevation = self.elevation
        
        layer = QgsVectorLayer(inputLayer, inputLayer , "ogr")
        vectorlayer_vector =  layer.dataProvider()
        # extent
        extent_rect = vectorlayer_vector.extent()
        xmin = extent_rect.xMinimum()
        xmax = extent_rect.xMaximum()
        ymin = extent_rect.yMinimum()
        ymax = extent_rect.yMaximum()
        extent = str(xmin) + "," + str(xmax) + "," + str(ymin) + "," + str(ymax)

        # read fields and add a new column with the indexes
        fields = layer.fields()
        new_field = QgsField("Indexes", QVariant.Int)
        layer_new = vectorlayer_vector.addAttributes([new_field])
        layer.updateFields()
        newFieldIndex = vectorlayer_vector.fieldNameIndex(new_field.name())
        allAttrs = vectorlayer_vector.attributeIndexes()
        # editing the new column
        #numberRows = int(self.tableWidget.rowCount())
        #numberColumns = int(self.tableWidget.columnCount())
        #classes = ''
        #lista = []
        #for i in range(0,numberRows):
        #    for j in range(0,numberColumns):
        #        self.line = self.tableWidget.item(i,j)
        #        lista = lista + [str(self.line.text())]
        #QMessageBox.about(self,'teste', str(lista))
               
        # list of description on tool table
        #lista_table = lista
        #lista_table = ["1, 3", "2, 5", "3, 8", "5, 10"]
        lista_table = self.rattings
        
        field_names = [field.name() for field in fields]
        n = len(field_names)
        lista_attrib = []
        for i in range(0,n):
            f = field_names[i]
            if f==str(Elevation):
                print ("atributo")
                print (f)
                number = i
                for feat in layer.getFeatures():
                    attrb = feat.attributes()
                    attribute_read = attrb[number]
                    lista_attrib = lista_attrib + [str(attribute_read)]
        # list of description on attribute table of shapefile
        lista_attributes = lista_attrib   
        print ("lista atributos")
        print (lista_attributes)

    
        # obtain the indexes of the description of shapefile attribute table
        description_common = set(lista_attributes).intersection(lista_table)
        listDescription = list(description_common)

        listElem = []
        listElements = []
        for j in range(0,len(listDescription)):
            elem = lista_table.index(listDescription[j])
            listElements = listElements + [elem]
  
            elem_index = lista_table[int(elem+1)]
            listElem = listElem + [int(elem_index)]
   
            
        for l in range(0, len(listElem)):
            layer.startEditing()
            exp = QgsExpression(str(listElem[l]))
            #exp.prepare(fields)
            elemDescription = lista_table[listElements[l]]
            for f in layer.getFeatures():
                # get attributes of column defined by the user
                attrb_elem = f[number]
                if attrb_elem==elemDescription: 
                    f[newFieldIndex] = exp.evaluate()
                    layer.updateFeature(f)  
            layer.commitChanges()   
        list_attrb_newField = []
        for features in layer.getFeatures():
            attrb_newField = features.attributes()
            attrb_newField_read = attrb_newField[number+1]
            
        # update and read the new field
        fieldsNew = layer.fields()
        field_names_new = [newField.name() for newField in fieldsNew]          
        parameter_indexes = field_names_new[newFieldIndex]
        
        Processing.initialize()
        #aquifer = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/aquifer"
        Processing.runAlgorithm("grass7:v.to.rast", {'input': inputLayer, 'type': [0, 1, 3], 'where': '', 'use': 0,
                                                     'attribute_column': parameter_indexes, 'rgb_column': None,
                                                     'label_column': None, 'value': None, 'memory': 300,
                                                     'output': outPath, 'GRASS_REGION_PARAMETER': extent,
                                                     'GRASS_REGION_CELLSIZE_PARAMETER': cellSize,
                                                     'GRASS_RASTER_FORMAT_OPT': '', 'GRASS_RASTER_FORMAT_META': '',
                                                     'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
                                                     'GRASS_MIN_AREA_PARAMETER': 0.0001})
