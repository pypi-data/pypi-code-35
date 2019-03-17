#pyrsgis/raster

import gdal
import numpy as np

class createDS():

    def __init__(self, ds):
        self.Projection = ds.GetProjection()
        self.GeoTransform = ds.GetGeoTransform()
        self.RasterCount = ds.RasterCount
        self.RasterXSize = ds.RasterXSize
        self.RasterYSize = ds.RasterYSize

    def GetProjection(self):
        return(self.Projection)

    def GetGeoTransform(self):
        return(self.GeoTransform)

    def RasterCount(self):
        return(self.RasterCount)

    def RasterXSize(self):
        return(self.RasterXSize)

    def RasterYSize(self):
        return(self.RasterYSize)

def read(file, band='all'):
    ds = gdal.Open(file)
    if band=='all':
        array = ds.ReadAsArray()
    elif type(band) == type(list()):
        array = np.random.randint(1, size=(len(band), ds.RasterYSize, ds.RasterXSize))
        for n, index in enumerate(band):
            tempArray = ds.GetRasterBand(band[index])
            array[n, :, :] = tempArray.ReadAsArray()
    else:
        array = ds.GetRasterBand(band)
        array = array.ReadAsArray()
    ds = createDS(ds)
    return(ds, array)

def export(band, ds, filename='pyrsgis_outFile.tif', dtype='int', bands=1):
    if bands == 1:
        row, col = band.shape
        nBands = 1
    else:
        layers, row, col = band.shape
    if type(bands) == type('All'):
        nBands = layers
    elif type(bands) == type(1):
        nBands = 1
    elif type(bands) == type([1, 2, 3]):
        nBands = len(bands)
    driver = gdal.GetDriverByName("GTiff")
    if dtype == 'float':
            outdata = driver.Create(filename, col, row, nBands, 6) # option: GDT_UInt16, GDT_Float32
    elif dtype == 'int':
            outdata = driver.Create(filename, col, row, nBands, 3) # option: GDT_UInt16, GDT_Float32
    outdata.SetGeoTransform(ds.GetGeoTransform())
    outdata.SetProjection(ds.GetProjection())
    if nBands==1:
        outdata.GetRasterBand(bands).WriteArray(band)
        outdata.GetRasterBand(bands).SetNoDataValue(0)
    elif bands=='All':
        for bandNumber in range(1,layers+1):
            outdata.GetRasterBand(bandNumber).WriteArray(band[bandNumber-1,:,:])
            outdata.GetRasterBand(bandNumber).SetNoDataValue(0)##if you want these values transparent
    else:
        for bandNumber in range(1,len(bands)+1):
            outdata.GetRasterBand(bandNumber).WriteArray(band[bands[bandNumber]-1,:,:])
            outdata.GetRasterBand(bandNumber).SetNoDataValue(0)##if you want these values transparent
    outdata.FlushCache() 
    outdata = None

def northEast(array, layer='both'):
    row, col = array.shape
    north = np.linspace(1, row, row)
    east = np.linspace(1, col, col)
    east, north = np.meshgrid(east, north)
    if layer=='both':
        return(north, east)
    elif layer=='north':
        return(north)
    elif layer=='east':
        return(east)

def northing(referenceFile, outFile='pyrsgis_northing.tif', flip=True):
    ds, band = read(referenceFile, band=1)
    north = northEast(band, layer='north')
    if flip==True:
        north = np.flip(north, axis=0)
    export(north, ds, filename=outFile)

def easting(referenceFile, outFile='pyrsgis_easting.tif', flip=False):
    ds, band = read(referenceFile, band=1)
    east = northEast(band, layer='east')
    if flip==True:
        east = np.flip(east, axis=1)
    export(east, ds, filename=outFile)
    
    
