import sys, os
from osgeo import gdal, ogr
from qgis.core import *

class Shp:
    def __init__(self, filename):
        self.filename = filename

    def get_header(self):
        layer = QgsVectorLayer(self.filename, self.filename , "ogr")
        fields = layer.fields()
        field_names = [field.name() for field in fields]
        return (field_names)

    def get_values(self, field):
        values = []
        layer = QgsVectorLayer(self.filename, self.filename , "ogr")
        fields = layer.fields()
        index = -1
        for i in range(0,len(fields)):
            if fields[i].name()==str(field):
                index = i
        for features in layer.getFeatures():
            attributes = features.attributes()
            values.append(attributes[index])
        return values

    def getVectorFields(self, vectorFile):
        hds = ogr.Open(vectorFile)
        if hds == None:
            print ("erro")

        fields = []
        names = []

        layer = hds.GetLayer(0)
        defn = layer.GetLayerDefn()

        for i in range(defn.GetFieldCount()):
            fieldDefn = defn.GetFieldDefn(i)
            fieldType = fieldDefn.GetType()
            if fieldType == 0 or fieldType == 2:
                fields.append(fieldDefn)
                names.append(fieldDefn.GetName())

        return (fields, names)
    