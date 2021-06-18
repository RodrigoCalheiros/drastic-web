from osgeo import gdal
class Raster:
    def get_statistcs(self, file):
        gtif = gdal.Open(file)
        srcband = gtif.GetRasterBand(1)
        stats = srcband.GetStatistics(True, True)
        return ({"minimum": stats[0], "maximum": stats[1], "mean": stats[2]})