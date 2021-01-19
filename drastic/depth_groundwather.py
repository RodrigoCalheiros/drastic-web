import sys, os
from osgeo import gdal
from PyQt5.QtCore import *
from qgis.core import QgsProcessingRegistry
from qgis.analysis import QgsNativeAlgorithms
from qgis.core import *
QgsApplication.setPrefixPath('/usr', True)

sys.path.append('/usr/share/qgis/python/plugins/')
from processing.core.Processing import Processing
qgs = QgsApplication([], False)
qgs.initQgis()
Processing.initialize()
      
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

class DepthGroundWather:

    def convert_mdt(self, input_mdt, max_depth, distance, min_size, ratings, output_path):
        
        
        gdal.AllRegister()

        #for alg in QgsApplication.processingRegistry().algorithms():
        #    print(alg.id(), "->", alg.displayName())

        # read raster
        inputRaster = input_mdt
        # read maximum depth
        max_depth = max_depth
        # read distance
        distance = distance   
        # minimum size
        size = min_size
        outPath2 = output_path 
        process_path = "/home/rodrigo/data/d/process" 

        

        layer_raster = QgsRasterLayer(inputRaster, os.path.basename(inputRaster), "gdal")
        data_mdt = layer_raster.dataProvider()
        extent_raster = data_mdt.extent()
        xmin_raster = extent_raster.xMinimum()
        xmax_raster = extent_raster.xMaximum()
        ymin_raster = extent_raster.yMinimum()
        ymax_raster = extent_raster.yMaximum()
        extent_raster_str = str(xmin_raster) + "," + str(xmax_raster) + "," + str(ymin_raster) + "," + str(ymax_raster)     
        cellSize = layer_raster.rasterUnitsPerPixelX()

        #stream = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/stream.tif"
        stream = process_path + "/stream.tif"
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
        #stream_ones = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/stream_ones.tif"
        stream_ones = process_path + "/stream_ones.tif"
        Processing.runAlgorithm("grass7:r.mapcalc.simple",{'a': str(stream),'b': None,'c': None, 'd': None, 'e': None, 'f': None,'expression': 'A>1','output': stream_ones, 'GRASS_REGION_PARAMETER': None,'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '','GRASS_RASTER_FORMAT_META': ''})



        # raster distance
        #raster_distance = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/raster_distance.tif"
        raster_distance = process_path + "/raster_distance.tif"
        
        #Processing.runAlgorithm("saga:proximitygrid", None, str(stream_ones_str), 3, str(raster_distance), None, None)

        #Processing.runAlgorithm("saga:proximityraster", {
        #    'FEATURES': str(stream_ones),
        #    'DISTANCE': str(raster_distance), 'DIRECTION': 'TEMPORARY_OUTPUT', 'ALLOCATION': 'TEMPORARY_OUTPUT'})
        
        Processing.runAlgorithm("grass7:r.grow.distance", {'input': str(stream_ones),
                    'metric': 0, '-m': False, '-': False, 'distance': str(raster_distance),
                    'value': 'TEMPORARY_OUTPUT', 'GRASS_REGION_PARAMETER': None,
                    'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
                    'GRASS_RASTER_FORMAT_META': ''})

        # condition distance >=  200, always maximum depth meters
        #dist_major_200 = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/dist_major_200.tif"
        dist_major_200 = process_path + "/dist_major_200.tif"

        Processing.runAlgorithm("grass7:r.mapcalc.simple",
                                {'a': str(raster_distance),
                                    'b': None,
                                    'c': None, 'd': None, 'e': None, 'f': None,
                                    'expression': "A>="+str(distance),
                                    'output': dist_major_200, 'GRASS_REGION_PARAMETER': None,
                                    'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
                                    'GRASS_RASTER_FORMAT_META': ''})
        
        #dist_multiplication = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/dist_multiplication.tif"
        dist_multiplication = process_path + "/dist_multiplication.tif"

        Processing.runAlgorithm("grass7:r.mapcalc.simple",
                                {'a': str(dist_major_200),
                                    'b': None,
                                    'c': None, 'd': None, 'e': None, 'f': None,
                                    'expression': "A*"+str(max_depth),
                                    'output': dist_multiplication, 'GRASS_REGION_PARAMETER': None,
                                    'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
                                    'GRASS_RASTER_FORMAT_META': ''})
        
        # condition distance < 200, inteprolation between 0 and maximum depth
        #dist_minor_200 = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/dist_minor_200.tif"
        dist_minor_200 = process_path + "/dist_minor_200.tif"
        Processing.runAlgorithm("grass7:r.mapcalc.simple",
                                {'a': str(raster_distance),
                                    'b': None,
                                    'c': None, 'd': None, 'e': None, 'f': None,
                                    'expression': "A<"+str(distance),
                                    'output': dist_minor_200, 'GRASS_REGION_PARAMETER': None,
                                    'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
                                    'GRASS_RASTER_FORMAT_META': ''})
        
        # multiplication by the raster distance
        #dist_multiplication_dist = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/dist_multiplication_dist.tif"
        dist_multiplication_dist = process_path + "/dist_multiplication_dist.tif"
        #Processing.runAlgorithm("grass7:r.mapcalc.simple",
        #                        {'a': str(dist_minor_200),
        #                            'b': str(dist_major_200),
        #                            'c': None, 'd': None, 'e': None, 'f': None,
        #                            'expression': 'A*B',
        #                            'output': dist_multiplication_dist, 'GRASS_REGION_PARAMETER': None,
        #                            'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
        #                            'GRASS_RASTER_FORMAT_META': ''})
        Processing.runAlgorithm("grass7:r.mapcalc.simple",
                            {'a': str(dist_minor_200),
                            'b': str(raster_distance),
                            'c': None, 'd': None, 'e': None, 'f': None,
                            'expression': 'A*B',
                            'output': dist_multiplication_dist, 'GRASS_REGION_PARAMETER': None,
                            'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
                            'GRASS_RASTER_FORMAT_META': ''})
        
        # interpolation between 0 and distance
        #interpolation_dist = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/interpolation_dist.tif"
        interpolation_dist = process_path + "/interpolation_dist.tif"
        Processing.runAlgorithm("grass7:r.mapcalc.simple",
                                {'a': str(dist_multiplication_dist),
                                    'b': None,
                                    'c': None, 'd': None, 'e': None, 'f': None,
                                    'expression': "A*"+str(max_depth)+"/"+str(distance),
                                    'output': interpolation_dist, 'GRASS_REGION_PARAMETER': None,
                                    'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
                                    'GRASS_RASTER_FORMAT_META': ''})
        
        # depth surface = sum of two conditions
        #depth_surface = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path() + "/depth_surface.tif"
        depth_surface = process_path + "/depth_surface.tif"
        Processing.runAlgorithm("grass7:r.mapcalc.simple",
                                {'a': str(dist_multiplication),
                                    'b': str(dist_multiplication_dist),
                                    'c': None, 'd': None, 'e': None, 'f': None,
                                    'expression': 'A+B',
                                    'output': depth_surface, 'GRASS_REGION_PARAMETER': None,
                                    'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
                                    'GRASS_RASTER_FORMAT_META': ''})

        
        # indexes for topography
    
    
        """rattings_lista = []
        for linha in ratings:
            for coluna in linha:
                rattings_lista = rattings_lista + [str(coluna)]
                string = ","
                intervalos = string.join(rattings_lista)
        results = list(map(float, rattings_lista))
        print(results)"""
        
        #Processing.runAlgorithm("saga:reclassifyvalues",{'INPUT': depth_surface, 'METHOD':2, 'OLD':0, 'NEW':1, 'SOPERATOR':0, 'MIN':0, 'MAX':1,
        #                                                    'RNEW':2, 'ROPERATOR':0, 'RETAB':results, 'TOPERATOR':0, 'NODATAOPT':True, 'NODATA':0,
        #                                                    'OTHEROPT':True, 'OTHERS':0, 'RESULT':outPath2})

        result = process_path + "/result.tif"
        Processing.runAlgorithm("native:reclassifybytable",
                {'INPUT_RASTER': str(depth_surface),
                    'RASTER_BAND': 1, 'TABLE': ratings,
                    'NO_DATA': -9999, 'RANGE_BOUNDARIES': 0, 'NODATA_FOR_MISSING': False, 'DATA_TYPE': 5,
                    'OUTPUT': result})
        
        out_raster = gdal.Open(result)
        gdal.Warp(outPath2, out_raster, dstSRS="EPSG:3857")

