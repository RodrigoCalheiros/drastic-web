import sys, os
from . import GdalTools_utils
from qgis.core import *

class Shp:
    def __init__(self, filename):
        self.filename = filename

    def get_header(self):
        (fields, names) = GdalTools_utils.getVectorFields(self.filename)
        return (fields, names)

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
    