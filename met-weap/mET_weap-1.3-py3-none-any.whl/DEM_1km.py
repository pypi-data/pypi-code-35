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
import os
import glob
import numpy as np
from osgeo import gdal, osr
from netCDF4 import Dataset
#------------------------

#--- config imports ---
from userconfig import mET_weap
from mET_weap import cf, path_to_osgeo, path_root
#----------------------


def DEM_1km_CDSAPI(echelle):
    """
    Extract the DEM from the geopotential and the local topography and compute the difference Dz
    float echelle: the scale at which the Meteo Data will be processed compared
    to the Modis NDVI dataset (1: 250M, 0.25:1000m)
    """

    fname_tmp = os.path.join(cf['path']['Tif'], "tmp_cdsapi.tif")
    fname_out = os.path.join(cf['path']['Tif'], "DEM_cdsapi.tif")

    if os.path.exists(fname_out):
        DEM_cdsapi_img = gdal.Open(fname_out)
        cols = DEM_cdsapi_img.RasterXSize
        rows = DEM_cdsapi_img.RasterYSize
        DEM_cdsapi = DEM_cdsapi_img.GetRasterBand(1).ReadAsArray()
        DEM_cdsapi_img = None
    else:
        if len(glob.glob(cf['DEM']['DEM_Filename'])) != 0:
            # pour récupérer la dimension de l'image de sortie, je prends une des images NDVI
            list_fname = glob.glob(os.path.join(cf['path']["MOD13Q1_tif"], "250m16daysNDVI_*.tif"))
            ref_img = gdal.Open(list_fname[0])
            GT = ref_img.GetGeoTransform()
            rows = int(ref_img.RasterYSize)
            cols = int(ref_img.RasterXSize)
            rows_out = int(ref_img.RasterYSize * echelle)
            cols_out = int(ref_img.RasterXSize * echelle)
            ref_img = None

            gdalwarp = os.path.join(path_to_osgeo, "gdalwarp")

            # Avec GDAL>2.0, on peut utiliser l'option -te_srs pour faire le subset sinon, on est obligé de le faire en deux fois
            #print(gdalwarp + ' -te_srs EPSG:4326 -te '+str(GT[0])+' '+str(GT[3])+' '+str(GT[0]+GT[1]*cols)+' '+str(GT[3]+GT[5]*rows)+" -ts "+ str(cols)+" "+str(rows)+" -r cubicspline " + fname_tmp +" "+ fname_out)

            print(gdalwarp + ' -t_srs EPSG:4326  -overwrite -of GTiff "'+cf['DEM']['DEM_Filename'] +'" "'+  fname_tmp +'"')
            os.system(gdalwarp + ' -t_srs EPSG:4326  -overwrite -of GTiff "'+cf['DEM']['DEM_Filename'] +'" "'+  fname_tmp +'"')

            #print(gdalwarp + ' -te '+str(GT[0])+' '+str(GT[3])+' '+str(GT[0]+GT[1]*cols)+' '+str(GT[3]+GT[5]*rows)+" -ts "+ str(cols)+" "+str(rows)+' -r cubicspline "' + fname_tmp +'" "'+ fname_out+'"')
            print(gdalwarp + ' -te '+str(GT[0])+' '+str(GT[3]+GT[5]*rows)+' '+str(GT[0]+GT[1]*cols)+' '+str(GT[3])+" -ts "+ str(cols_out)+" "+str(rows_out)+' -r cubicspline -ot Float32 -overwrite "' + fname_tmp +'" "'+ fname_out+'"')
            os.system(gdalwarp + ' -te '+str(GT[0])+' '+str(GT[3]+GT[5]*rows)+' '+str(GT[0]+GT[1]*cols)+' '+str(GT[3])+" -ts "+ str(cols_out)+" "+str(rows_out)+' -r cubicspline -ot Float32 -overwrite "' + fname_tmp +'" "'+ fname_out+'"')

            os.remove(fname_tmp)

            DEM_cdsapi_img = gdal.Open(fname_out)
            DEM_cdsapi = DEM_cdsapi_img.GetRasterBand(1).ReadAsArray()
            DEM_cdsapi_img = None
        else:
            DEM_cdsapi = np.zeros(cols_out*rows_out)
            DEM_cdsapi = DEM_cdsapi+100

    fname_tmp = os.path.join(cf['path']['Tif'], "tmp_cdsapi.tif")
    fname_out = os.path.join(cf['path']['Tif'], "DEM_ERA_cdsapi.tif")

    if os.path.exists(fname_out):
        DEM_cdsapi_img = gdal.Open(fname_out)
        cols = DEM_cdsapi_img.RasterXSize
        rows = DEM_cdsapi_img.RasterYSize
        DEM_ERA_cdsapi = DEM_cdsapi_img.GetRasterBand(1).ReadAsArray()
#        DEM_ERA_cdsapi = (28035.389409195857 + DEM_ERA_cdsapi * 0.8979394207879999) / 9.80665
        DEM_cdsapi_img = None
    else:
        if len(cf['DEM']['ERA_Filename_CDSAPI']) != 0:
            # pour récupérer la dimension de l'image de sortie, je prends une des images NDVI
            list_fname = glob.glob(os.path.join(cf['path']["MOD13Q1_tif"], "250m16daysNDVI_*.tif"))
            ref_img = gdal.Open(list_fname[0])
            GT = ref_img.GetGeoTransform()
            rows = int(ref_img.RasterYSize)
            cols = int(ref_img.RasterXSize)
            rows_out = int(ref_img.RasterYSize * echelle)
            cols_out = int(ref_img.RasterXSize * echelle)
            ref_img = None

            gdalwarp = os.path.join(path_to_osgeo, "gdalwarp")

            # Avec GDAL>2.0, on peut utiliser l'option -te_srs pour faire le subset sinon, on est obligé de le faire en deux fois
            #print(gdalwarp + ' -te_srs EPSG:4326 -te '+str(GT[0])+' '+str(GT[3])+' '+str(GT[0]+GT[1]*cols)+' '+str(GT[3]+GT[5]*rows)+" -ts "+ str(cols)+" "+str(rows)+" -r cubicspline " + fname_tmp +" "+ fname_out)

            print(gdalwarp + ' -t_srs EPSG:4326  -overwrite -of GTiff "'+cf['DEM']['ERA_Filename_CDSAPI'] +'" "'+  fname_tmp +'"')
            os.system(gdalwarp + ' -t_srs EPSG:4326  -overwrite -of GTiff "'+cf['DEM']['ERA_Filename_CDSAPI'] +'" "'+  fname_tmp +'"')
            
#            print(gdalwarp + ' -t_srs EPSG:4326 -of GTiff "'+ fname_tmp +'" "'+  fname_out +'"')
#            os.system(gdalwarp + ' -t_srs EPSG:4326 -of GTiff "'+ fname_tmp +'" "'+  fname_out +'"')
            
#            print(gdalwarp + ' -te '+str(GT[0])+' '+str(GT[3]+GT[5]*rows)+' '+str(GT[0]+GT[1]*cols)+' '+str(GT[3])+" -ts "+ str(cols_out)+" "+str(rows_out)+' -r cubicspline + "' + cf['DEM']['ERA_Filename_CDSAPI'] +'" "'+ fname_out+'"')
            print(gdalwarp + ' -te '+str(GT[0])+' '+str(GT[3]+GT[5]*rows)+' '+str((GT[0]+GT[1]*cols))+' '+str(GT[3])+" -ts "+ str(cols_out)+" "+str(rows_out)+' -r cubicspline -ot Float32 -overwrite "' + cf['DEM']['ERA_Filename_CDSAPI'] +'" "'+ fname_out+'"')
            os.system(gdalwarp + ' -te '+str(GT[0])+' '+str(GT[3]+GT[5]*rows)+' '+str((GT[0]+GT[1]*cols))+' '+str(GT[3])+" -ts "+ str(cols_out)+" "+str(rows_out)+' -r cubicspline -ot Float32 -overwrite "' + cf['DEM']['ERA_Filename_CDSAPI'] +'" "'+ fname_out+'"')

            #os.remove(fname_tmp)
            
            geopotential_cdsapi = Dataset(cf['DEM']['ERA_Filename_CDSAPI'])
            scale_factor_ERA5 = geopotential_cdsapi.variables['z'].scale_factor
            add_offset_ERA5 = geopotential_cdsapi.variables['z'].add_offset

            DEM_cdsapi_img = gdal.Open(fname_out)
            DEM_ERA_cdsapi = DEM_cdsapi_img.GetRasterBand(1).ReadAsArray()
            DEM_ERA_cdsapi = (add_offset_ERA5 + DEM_ERA_cdsapi * scale_factor_ERA5) / 9.80665
            DEM_cdsapi_img = None
            
            PJ = osr.SpatialReference()
            PJ.SetWellKnownGeogCS("EPSG:4326")
            driver = gdal.GetDriverByName("GTiff")
            outDs = driver.Create(fname_out, cols_out, rows_out, 1, gdal.GDT_Float32)
            GT2=list(GT)
            GT2[1]=GT2[1]/echelle
            GT2[5]=GT2[5]/echelle
            outDs.SetGeoTransform(GT2)
            outDs.SetProjection(PJ.ExportToWkt())
            outDs.GetRasterBand(1).WriteArray(DEM_ERA_cdsapi)
            outDs = None            
        else:
            DEM_cdsapi = np.zeros(cols_out*rows_out)
            DEM_ERA_cdsapi = DEM_ERA_cdsapi+100

    return(DEM_cdsapi, DEM_ERA_cdsapi-DEM_cdsapi)