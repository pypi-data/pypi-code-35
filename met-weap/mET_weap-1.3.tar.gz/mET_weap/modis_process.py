# Copyright (C) 2014-2018 Michel Le Page
#
# mET_weap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mET_weap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#--- external imports ---
import glob
import datetime
from osgeo import gdal
import numpy as np
import os
from scipy.interpolate import InterpolatedUnivariateSpline
from osgeo import ogr, osr
#------------------------

#--- config imports ---
from userconfig import mET_weap
from mET_weap import cf, path_to_osgeo, path_root
#----------------------


"""
Created on Wed May 27 13:00:23 2015

@author: michel le page
@version 0.1, 2016/09/08

ndvi_daily(): Interpolation at daily time step of NDVI
albedo_daily(): Computation of Albedo from white_sky and black_sky, and interpolation at daily time step
scale_offset(): Apply a scale_factor and offset to a dataset
scale_offset_UTCtime(): compute UTCtime and SolarLocalTime from MOD11A1 input data
scale_offset_angle(): compute day_view_angle in radians and the quality mask
"""


def modis_tile_id(lon, lat):

	# Spatial Reference System
	source = osr.SpatialReference()
	source.ImportFromEPSG(4326)

	target = osr.SpatialReference()
	target.ImportFromWkt('PROJCS["MODIS Sinusoidal", GEOGCS["WGS 84",DATUM["WGS_1984", SPHEROID["WGS 84", 6378137, 298.257223563, AUTHORITY["EPSG","7030"]], AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG", "8901"]], UNIT["degree", 0.01745329251994328, AUTHORITY["EPSG", "9122"]], AUTHORITY["EPSG", "4326"]], PROJECTION["Sinusoidal"], PARAMETER["false_easting", 0.0], PARAMETER["false_northing", 0.0], PARAMETER["central_meridian", 0.0], PARAMETER["semi_major", 6371007.181], PARAMETER["semi_minor", 6371007.181], UNIT["m", 1.0], AUTHORITY["SR-ORG", "6974"]]')

	transform = osr.CoordinateTransformation(source, target)

	## create a geometry from coordinates
	point = ogr.Geometry(ogr.wkbPoint)
	point.AddPoint(lon, lat)

	point.Transform(transform)

	#  https://code.env.duke.edu/projects/mget/wiki/SinusoidalMODIS
	tile_size = (20015109.354 + 20015109.354)/36

	hh = int((point.GetX()+20015109.354)/tile_size)
	vv = int(18-((point.GetY()+10007554.677)/tile_size))

	print("Lon=", lon, " Lat=", lat, "   HH : ", str("%02d"%hh), " VV : ", str("%02d"%vv))

	return(str("%02d"%hh), str("%02d"%vv))

def ndvi_daily(infile, outfile, prefix):
    scale_factor = 0.0001 # attention dans le produit NDVI le scale factor qui est indiqué est 10000, hors il faut diviser par 10000.

    Noms_ndvi = sorted(glob.glob(os.path.join(infile, prefix+'*.tif')))
    Dates_ndvi = list()
    short_ndvi = list()
    #recuperation des dates
    for n in range(len(Noms_ndvi)):              # Boucle sur les noms des images MODIS dans la période de temps considérée
        file = Noms_ndvi[n]
#        date = file.split("\\")[-1]                    # decoupe de expression par \\
        date = file.split(os.sep)[-1]                    # decoupe de expression par \\
        date = date.split(prefix+'_')[1].split('.tif')[0]       # decoupe de date et .tif
        short_ndvi.append(date)
        Dates_ndvi.append(datetime.datetime.strptime(str(date), '%Y.%m.%d'))

    #import des ndvi pour chaque dates mod13Q1
    for j in range(len(short_ndvi)):
        if j == 0:
            NDVI1 = gdal.Open(os.path.join(infile, prefix+'_'+short_ndvi[j]+'.tif'))
            NDVI = NDVI1.ReadAsArray()*scale_factor
            cols = NDVI1.RasterXSize
            rows = NDVI1.RasterYSize
            driver = NDVI1.GetDriver()
            GT = NDVI1.GetGeoTransform()
            PJ = NDVI1.GetProjection()
        elif j == 1:
            NDVI = np.append([NDVI], [gdal.Open(os.path.join(infile, prefix+'_'+short_ndvi[j]+'.tif')).ReadAsArray()*scale_factor], axis=0)
        else:
            NDVI = np.append(NDVI, [gdal.Open(os.path.join(infile, prefix+'_'+short_ndvi[j]+'.tif')).ReadAsArray()*scale_factor], axis=0)
    #nouveau fichier avecensemble des dates
            #dates 2 en 2
    for i in range(1, len(Dates_ndvi)):
        delta = Dates_ndvi[i]-Dates_ndvi[i-1]
        nb_das = max(int(delta.days), 0)
        if nb_das > 1:
            new_NDVI = np.zeros((nb_das, rows, cols)) #contiendra 16 dates
            xi = [i-1, i]
            Das = np.linspace(xi[0], xi[-1], nb_das+1) #cree 17 valeurs
            Das = np.delete(Das, -1) #enlève la 17ème valeur qui sera égal à la 1ere de la prochaine boucle
            #remplissage pixel par pixel
            for r in range(rows):
                for c in range(cols):
                    yi = NDVI[i-1:i+1, r, c]
                    s = InterpolatedUnivariateSpline(xi, yi, k=1)
                    new_NDVI[:, r, c] = s(Das)
            #sortir new_NDVI avec Dates correspondant à idas
            for d in range(nb_das):
                day = Dates_ndvi[i-1]+datetime.timedelta(d)
                fname_out = os.path.join(outfile, prefix+'_'+day.strftime('%Y.%m.%d')+'.tif')
                if os.path.exists(fname_out):
                    os.remove(fname_out)
                outDs = driver.Create(fname_out, cols, rows, 1, gdal.GDT_Float32)
                outDs.SetGeoTransform(GT)
                outDs.SetProjection(PJ)
                bando = outDs.GetRasterBand(1)
                bando.WriteArray(new_NDVI[d, :, :])
                del outDs

def albedo_daily(infile, outfile, prefix_white_sky, prefix_black_sky, prefix_albedo):
    scale_factor = 0.001

    Noms_white_sky = sorted(glob.glob(os.path.join(infile, '*'+prefix_white_sky+'*.tif')))
    Dates_white_sky = list()
    short_white_sky = list()
    #recuperation des dates
    for n in range(len(Noms_white_sky)):              # Boucle sur les noms des images MODIS dans la période de temps considérée
        file = Noms_white_sky[n]
#        date=file.split("\\")[-1]                   # decoupe de expression par \\
        date = file.split(os.sep)[-1]                   # decoupe de expression par \\
        date = date.split(prefix_white_sky+'_')[1].split('.tif')[0]       # decoupe de date et .tif
        short_white_sky.append(date)
        Dates_white_sky.append(datetime.datetime.strptime(str(date), '%Y.%m.%d'))

    #import des ndvi pour chaque dates mod13Q1
    for j in range(len(short_white_sky)):
        if j == 0:
            albedo_white_sky_1 = gdal.Open(os.path.join(infile, prefix_white_sky+'_'+short_white_sky[j]+'.tif'))
            albedo_white_sky = albedo_white_sky_1.ReadAsArray()*scale_factor
            cols = albedo_white_sky_1.RasterXSize
            rows = albedo_white_sky_1.RasterYSize
            driver = albedo_white_sky_1.GetDriver()
            GT = albedo_white_sky_1.GetGeoTransform()
            PJ = albedo_white_sky_1.GetProjection()
            albedo_black_sky_1 = gdal.Open(os.path.join(infile, prefix_black_sky+'_'+short_white_sky[j]+'.tif'))
            albedo_black_sky = albedo_black_sky_1.ReadAsArray()*scale_factor
            ALBEDO = albedo_white_sky*.15 + albedo_black_sky*.85
        elif j == 1:
            albedo_white_sky = gdal.Open(os.path.join(infile, prefix_white_sky+'_'+short_white_sky[j]+'.tif')).ReadAsArray()*scale_factor
            albedo_black_sky = gdal.Open(os.path.join(infile, prefix_black_sky+'_'+short_white_sky[j]+'.tif')).ReadAsArray()*scale_factor
            ALBEDO = np.append([ALBEDO], [albedo_white_sky*.15 + albedo_black_sky*.85], axis=0)
        else:
            albedo_white_sky = gdal.Open(os.path.join(infile, prefix_white_sky+'_'+short_white_sky[j]+'.tif')).ReadAsArray()*scale_factor
            albedo_black_sky = gdal.Open(os.path.join(infile, prefix_black_sky+'_'+short_white_sky[j]+'.tif')).ReadAsArray()*scale_factor
            ALBEDO = np.append(ALBEDO, [albedo_white_sky*.15 + albedo_black_sky*.85], axis=0)
    #nouveau fichier avecensemble des dates
            #dates 2 en 2
    for i in range(1, len(Dates_white_sky)):
        delta = Dates_white_sky[i]-Dates_white_sky[i-1]
        nb_das = max(int(delta.days), 0)
        if nb_das > 1:
            new_ALBEDO = np.zeros((nb_das, rows, cols)) #contiendra 16 dates
            xi = [i-1, i]
            Das = np.linspace(xi[0], xi[-1], nb_das+1) #cree 17 valeurs
            Das = np.delete(Das, -1) #enlève la 17ème valeur qui sera égal à la 1ere de la prochaine boucle
            #remplissage pixel par pixel
            for r in range(rows):
                for c in range(cols):
                    yi = ALBEDO[i-1:i+1, r, c]
                    s = InterpolatedUnivariateSpline(xi, yi, k=1)
                    new_ALBEDO[:, r, c] = s(Das)
            #sortir new_NDVI avec Dates correspondant à idas
            for d in range(nb_das):
                day = Dates_white_sky[i-1]+datetime.timedelta(d)
                fname_out = os.path.join(outfile, prefix_albedo+'_'+day.strftime('%Y.%m.%d')+'.tif')
                if os.path.exists(fname_out):
                    os.remove(fname_out)
                outDs = driver.Create(fname_out, cols, rows, 1, gdal.GDT_Float32)
                outDs.SetGeoTransform(GT)
                outDs.SetProjection(PJ)
                bando = outDs.GetRasterBand(1)
                bando.WriteArray(new_ALBEDO[d, :, :])
                del outDs

# ------------------------------------------------------------------------
# Application de scale_factor et add_offset sur un répertoire de fichiers TIF
# -----------------------------------------------------------------------

def scale_offset(ref_file, dataset, variable, input_dir, output_dir):

    inds = gdal.Open(ref_file)
    MD = inds.GetMetadata_Dict()
    if 'scale_factor' in MD:
        scale_factor = float(MD.get('scale_factor'))
    else:
        scale_factor = 1.

    if 'add_offset' in MD:
        add_offset = float(MD.get('add_offset'))
    else:
        add_offset = 1.

    inDs = None

    List_Fich_name = sorted(glob.glob(os.path.join(input_dir, variable+"*.tif")))
    for infile in List_Fich_name:
        inDs = gdal.Open(infile)
        data = inDs.ReadAsArray()
        data = data*scale_factor+add_offset
        cols = inDs.RasterXSize
        rows = inDs.RasterYSize
        driver = inDs.GetDriver()
        GT = inDs.GetGeoTransform()
        PJ = inDs.GetProjection()
        del inDs

        fname = infile.split(os.sep)[-1]
        fname_out = os.path.join(output_dir, fname)
        if os.path.exists(fname_out):
            os.remove(fname_out)
        outDs = driver.Create(fname_out, cols, rows, 1, gdal.GDT_Float32)
        outDs.SetGeoTransform(GT)
        outDs.SetProjection(PJ)
        outDs.GetRasterBand(1).WriteArray(data)
        del outDs

# ------------------------------------------------------------------------
# Application de sclae_factor et add_offset sur un répertoire de fichiers TIF
# On convertis les angles en radian et on masque ce qui est >45°
# -----------------------------------------------------------------------

def scale_offset_angle(ref_file, dataset, variable, input_dir, output_dir):

    inds = gdal.Open(ref_file)
    MD = inds.GetMetadata_Dict()
    if 'scale_factor' in MD:
        scale_factor = float(MD.get('scale_factor'))
    else:
        scale_factor = 1.

    if 'add_offset' in MD:
        add_offset = float(MD.get('add_offset'))
    else:
        add_offset = 1.

    inDs = None

    List_Fich_name = sorted(glob.glob(os.path.join(input_dir, variable+"*.tif")))
    for infile in List_Fich_name:
        inDs = gdal.Open(infile)
        data = inDs.ReadAsArray()
        data = (data*scale_factor+add_offset)
        mask_angle = np.less_equal(np.absolute(data), 45)
        data = data*3.14/180 # conversion radians
        cols = inDs.RasterXSize
        rows = inDs.RasterYSize
        driver = inDs.GetDriver()
        GT = inDs.GetGeoTransform()
        PJ = inDs.GetProjection()
        del inDs

        # Bit No. 	Name 	Legend
        # 00–01 	Mandatory QA flag
        # 00 = Pixel produced, good quality, not necessary to examine detailed QA
        # 01 = Pixel produced, unreliable or unquantifiable quality, recommend examination of more detailed QA
        # 10 = Pixel not produced due to cloud effects
        # 11 = Pixel not produced primarily due to reasons other than clouds
        # QC_day: on garde uniquement les QC=0 et les angles<45°
        infile_QC = infile.replace("Day_view_angl", "QC_Day")
        print(infile_QC)
        inDs = gdal.Open(infile_QC)
        mask = inDs.ReadAsArray()
        # ---- masque qui prends uniquement les QC == 0
        mask = np.float32(np.less_equal(mask, 0) * mask_angle)
        # ---- masque qui prends les QC = 00 et 01 (second bit == 0)
        #mask = ( np.right_shift(mask,1) & 1 != 1 ) * mask_angle
        del inDs

        # Ecriture des angles en radians
        fname = infile.split(os.sep)[-1]
        fname_out = os.path.join(output_dir, fname)
        if os.path.exists(fname_out):
            os.remove(fname_out)
        outDs = driver.Create(fname_out, cols, rows, 1, gdal.GDT_Float32)
        outDs.SetGeoTransform(GT)
        outDs.SetProjection(PJ)
        outDs.GetRasterBand(1).WriteArray(data)
        del outDs

        # Ecriture du masque
        fname = infile_QC.split(os.sep)[-1]
        fname_out = os.path.join(output_dir, fname)
        if os.path.exists(fname_out):
            os.remove(fname_out)
        outDs = driver.Create(fname_out, cols, rows, 1, gdal.GDT_Float32)
        outDs.SetGeoTransform(GT)
        outDs.SetProjection(PJ)
        outDs.GetRasterBand(1).WriteArray(mask)
        del outDs
