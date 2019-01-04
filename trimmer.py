import os.path
from osgeo import gdal

gdal.UseExceptions()


def crop_raster(raster_path, shapefile_path, outfile='./clipped.tif'):
    raster_exists = os.path.exists(raster_path)
    shapefile_exists = os.path.exists(shapefile_path)
    print(raster_exists, shapefile_exists)

    if ((not raster_exists) or (not shapefile_exists)):
        raise Exception('Insert the real files path.')

    # Clip the input Raster
    result = gdal.Warp(
        outfile,
        raster_path,
        cutlineDSName=shapefile_path,
        cropToCutline=True
    )
    print(result)
    if result:
        print("Done")
    else:
        raise Exception("Error")
