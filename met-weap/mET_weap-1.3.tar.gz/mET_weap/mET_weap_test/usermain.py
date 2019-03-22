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
import operator
import glob
from osgeo import gdal, osr
gdal.UseExceptions()
import numpy as np
from datetime import datetime, timedelta
#--------------------------

#--- internal imports ---
import mET_weap
import mET_weap.synthesize as synth
from mET_weap.synthesize import do_croisement_shape, do_synthese_areas, do_synthese_classes, do_synthese
from mET_weap.download_geopotential_cdsapi import geo_download_cdsapi
from mET_weap.DEM_1km import DEM_1km_CDSAPI
from mET_weap.get_modis import get_modisfiles
from mET_weap.modis_process import modis_tile_id
from mET_weap.hdf2tif import hdf2tif
from mET_weap.Classification import classif_ijrs1997
from mET_weap.Kc_Fc import KC_FC_calc, ET_actual_ERA5
from mET_weap.download_ERA5_cds import download_ERA5_cds
from mET_weap.ecmwf_daily import era5_daily
#------------------------

#--- config imports ---
from userconfig import mET_weap
from mET_weap import cf, path_to_osgeo, path_root
#----------------------

if __name__ == "__main__":

    echelle = mET_weap.cf['scale']['echelle']
    debut = str(datetime.now())
    print("Init at "+debut)

    # -------------- DOMAIN ------------------
    win_xleft = mET_weap.cf['domain']['ulx']
    win_xright = mET_weap.cf['domain']['lrx']
    win_ybottom = mET_weap.cf['domain']['lry']
    win_ytop = mET_weap.cf['domain']['uly']

    win_domain = [win_xleft, win_ytop, win_xright, win_ybottom]

    hh, vv = mET_weap.modis_tile_id((win_xleft+win_xright)/2, (win_ytop+win_ybottom)/2)
    print(hh, vv)

    # ------------- DIRECTORIES -----------------

    liste = sorted(mET_weap.cf['path'].items(), key=operator.itemgetter(1)) # on trie la liste des répertoires pour bien les créer dans le bon ordre

    if os.path.isdir(''.join(mET_weap.path_root)) is False:
        print("Creating directory ", mET_weap.path_root)
        os.makedirs(mET_weap.path_root)

    for pp in liste:
        if os.path.isdir(pp[1]) is False:
            print("Creating directory ", pp[1])
            os.makedirs(pp[1])
        else:
            print(pp[0], ' : ', pp[1], ' is ok')
    
    # ------------- DOWNLOAD GEOPOTENTIAL CDSAPI --------------------
    
    if os.path.exists(cf['DEM']['ERA_Filename_CDSAPI']) is False:
      
        window = [win_ytop + (cf['scale']['resolution_ERA5'])/2, win_xleft - (cf['scale']['resolution_ERA5'])/2, win_ybottom - (cf['scale']['resolution_ERA5'])/2, win_xright + (cf['scale']['resolution_ERA5'])/2]

        fname = os.path.join(cf['DEM']['ERA_Filename_CDSAPI'])
        fname = geo_download_cdsapi(fname, window)

    # ------------- GET MODIS DATA --------------------

    if mET_weap.cf['do_get_modis'] == True:
        print("=== GET MODIS DATA ===")

        # MOD13Q1 : NDVI
        username = mET_weap.cf['MODIS']['username']
        password = mET_weap.cf['MODIS']['password']
        platform = "MOLT"
        product_name = "MOD13Q1"
        product = "MOD13Q1.006"
        tile = "h17v05"
        out_dir = mET_weap.cf['path'][product_name]
        date_begin = mET_weap.cf['period']['begin']
        year_begin = date_begin.timetuple().tm_year
        day_begin = 1
        date_end = mET_weap.cf['period']['end']
        year_end = date_end.timetuple().tm_year
        day_end = 366

        count2 = mET_weap.get_modisfiles(username, password, platform, product, year_begin, tile, doy_start=day_begin, out_dir=out_dir, proxy=None, verbose=True,)
        count2 = mET_weap.get_modisfiles(username, password, platform, product, year_end, tile, doy_end=day_end, out_dir=out_dir, proxy=None, verbose=True,)
    
    # ------------- DOWNLOAD ERA5 CDS -------------------------

    if mET_weap.cf['do_download_ERA5_cds'] == True:

        window = [win_ytop + (cf['scale']['resolution_ERA5'])/2, win_xleft - (cf['scale']['resolution_ERA5'])/2, win_ybottom - (cf['scale']['resolution_ERA5'])/2, win_xright + (cf['scale']['resolution_ERA5'])/2]

        ddd = (mET_weap.cf['period']['end']-mET_weap.cf['period']['begin']).days
        for dd in range(ddd):
            d1 = mET_weap.cf['period']['begin']+timedelta(dd)
            from_year = d1.year
            from_month = d1.month
            from_day = d1.day

            d2 = mET_weap.cf['period']['begin']+timedelta(dd)
            to_year = d2.year
            to_month = d2.month
            to_day = d2.day

            date_ecmwf = str('%04d'%from_year)+'-'+str('%02d'%from_month)+'-'+str('%02d'%from_day)

            fname = os.path.join(mET_weap.cf['path']["ERA5"], "era5_"+date_ecmwf.replace('/', '_')+".nc")

            fname = mET_weap.download_ERA5_cds(date_ecmwf, window, fname)

    # ------------- PROJ & SUBSET --------------------

    if mET_weap.cf['do_project_subset'] == True:
        print("=== PROJECTION & SUBSET ===")

        # --- MOD13Q1 ---
        List_Fich_name = glob.glob(os.path.join(mET_weap.cf['path']["MOD13Q1"], "*.hdf"))
        variable = ':MODIS_Grid_16DAY_250m_500m_VI:"250m 16 days NDVI"'
        mET_weap.hdf2tif(List_Fich_name, mET_weap.cf['path']["MOD13Q1_tif"], path_to_osgeo, win_xleft, win_xright, win_ybottom, win_ytop, variable)
	
	# ------------- DEM extraction with CDSAPI geopotential. If no DEM, z is set to 100 --------------------

    Dz = 0
    if len(glob.glob(os.path.join(cf['path']["MOD13Q1_tif"], "250m16daysNDVI_*.tif"))) != 0:
        print("=== COMPUTE delta altitude ===")
        DEM_cdsapi, Dz = mET_weap.DEM_1km_CDSAPI(echelle)

    # --------------- YEARLY CLASSIFICATION ---------------

    if mET_weap.cf['do_classification'] == True:
        print("=== CLASSIFICATION IJRS1997 ===")

        from_year = mET_weap.cf['period']['begin'].year          # premiere annee
        to_year = mET_weap.cf['period']['end'].year              # derniere annee
        prefix = '250m16daysNDVI'

        for year in range(from_year, to_year+1):
            list_fnames = mET_weap.utils.select_files_agroyear_all(mET_weap.cf['path']["MOD13Q1_tif"], prefix, year, year)
            fname_out_ERA5 = os.path.join(mET_weap.cf['path']["outputs_ERA5"], "class_"+str(year)+".tif")
            mET_weap.classif_ijrs1997(list_fnames, fname_out_ERA5, valsn=0.22, valanu=0.32, valdev=0.3)

    # ------------- KC/FC --------------------

    if mET_weap.cf['do_kc_fc'] == True:
        print("=== COMPUTE KC & FC ===")
        from_year = mET_weap.cf['period']['begin'].year          # premiere annee
        to_year = mET_weap.cf['period']['end'].year              # derniere annee
        prefix = '250m16daysNDVI'
        mET_weap.KC_FC_calc(prefix, from_year, to_year)

    # ------------- COMPUTE DAILY ET0 AND RAINFALL from ERA5 --------------------

    if mET_weap.cf['do_ET0_rain_ERA5'] == True:
        print("=== DAILY ET0 & RAINFALL FROM ERA5  ===")

        # pour récupérer la dimension de l'image de sortie, je prends une des images NDVI
        list_fname = glob.glob(os.path.join(mET_weap.cf['path']["MOD13Q1_tif"], "250m16daysNDVI_*.tif"))
        ref_img = gdal.Open(list_fname[0])
        dims = [int(ref_img.RasterXSize * echelle), int(ref_img.RasterYSize * echelle)]
        GT = ref_img.GetGeoTransform()
        ref_img = None

        Lat = np.arange(dims[1])    # création d'une ligne de latitudes
        Lat = GT[3]+Lat*GT[5]*echelle  # calcul des longitudes avec les GT
        Lat = np.repeat(Lat, dims[0])
        Lat = Lat.reshape((dims[1], dims[0]))

        # resize GT with echelle...
        GT = np.array(GT) # 'tuple' object does not support item assignment
        GT[1] = GT[1] / echelle
        GT[5] = GT[5] / echelle

        list_fname = glob.glob(os.path.join(mET_weap.cf['path']["ERA5"], "*.nc"))
        for fname in list_fname:
            varname = mET_weap.era5_daily(fname, dims, GT, win_domain, Lat, Dz, DEM_cdsapi)
        
    # --------------- TEMPORAL INTERPOLATION of NDVI and KC*ET0 ERA5 ---------------

    if mET_weap.cf['do_interp_ndvi_ERA5'] == True:
        print("=== TEMPORAL INTERPOLATION of NDVI & KC*ET0 ERA5 ===")

        from_year = mET_weap.cf['period']['begin'].year          # premiere annee
        to_year = mET_weap.cf['period']['end'].year              # derniere annee
        Kc_path = mET_weap.cf['path']["outputs_ERA5"]
        ET0_path = mET_weap.cf['path']["ERA5_tif"]
        out_path = mET_weap.cf['path']["outputs_ERA5"]
        prefix_Kc = 'Kc'
        prefix_ET0 = 'ET0'
        prefix_ETa = "ETc"

        mET_weap.ET_actual_ERA5(from_year, to_year, Kc_path, ET0_path, out_path, prefix_Kc, prefix_ET0, prefix_ETa, echelle)

    # ----------------- SPATIO-TEMPORAL SYNTHESIS ERA5 --------------------

    if mET_weap.cf['do_synthesis_ERA5'] == True:
        print("=== SPATIO-TEMPORAL SYNTHESIS ERA5 ===")

        #  ============ CROISEMENT du SHAPE et de l'image pour resolution MODIS =============
        
        croisement = do_croisement_shape(shp_file=mET_weap.cf['Synth']['shapefile'], shp_att=mET_weap.cf['Synth']['shp_attrib'], prefix="ETc_", path_in=mET_weap.cf['path']["outputs_ERA5"], tempdir=mET_weap.cf['path']["Temp_ERA5"])
                       
        # ========= SYNTHESE AREAS des classes 3 (Mixte),4 (Arbre), 5 (Annuels) =========

        do_synthese_areas(croisement, shp_file=mET_weap.cf['Synth']['shapefile'], prefix="class_", path_in=mET_weap.cf['path']["synthesis_ERA5"], path_out=mET_weap.cf['path']["outputs_ERA5"])

        # ========= SYNTHESE AREAS des différentes classes =========

        do_synthese_classes(croisement, shp_file=mET_weap.cf['Synth']['shapefile'], prefix="class_", path_in=mET_weap.cf['path']["synthesis_ERA5"], path_out=mET_weap.cf['path']["outputs_ERA5"], path_rel=mET_weap.cf['Relation_NDVI']["rel_OS"])
            
        # ========= SYNTHESE ETc =========

        do_synthese(croisement, shp_file=mET_weap.cf['Synth']['shapefile'], shp_att=mET_weap.cf['Synth']['shp_attrib'], prefix="ETc_", path_in=mET_weap.cf['path']["outputs_ERA5"], path_out=mET_weap.cf['path']["synthesis_ERA5"])

        # ========= SYNTHESE Kc =========

        do_synthese(croisement, shp_file=mET_weap.cf['Synth']['shapefile'], shp_att=mET_weap.cf['Synth']['shp_attrib'], prefix="Kc_", path_in=mET_weap.cf['path']["outputs_ERA5"], path_out=mET_weap.cf['path']["synthesis_ERA5"])

        #  ============ CROISEMENT du SHAPE et de l'image pour resolution METEO =============

        croisement = do_croisement_shape(shp_file=mET_weap.cf['Synth']['shapefile'], shp_att=mET_weap.cf['Synth']['shp_attrib'], prefix="ET0_", path_in=mET_weap.cf['path']["ERA5_tif"], tempdir=os.path.join(mET_weap.cf['path']['ERA5_tif'], 'fishnet'))
              
        # ========= SYNTHESE ET0 =========
        do_synthese(croisement, shp_file=mET_weap.cf['Synth']['shapefile'], shp_att=mET_weap.cf['Synth']['shp_attrib'],prefix="ET0_", path_in=mET_weap.cf['path']["ERA5_tif"], path_out=mET_weap.cf['path']["synthesis_ERA5"])
        
        # ========= SYNTHESE Rain =========
        do_synthese(croisement, shp_file=mET_weap.cf['Synth']['shapefile'], shp_att=mET_weap.cf['Synth']['shp_attrib'],prefix="Rain_", path_in=mET_weap.cf['path']["ERA5_tif"], path_out=mET_weap.cf['path']["synthesis_ERA5"])
        
        # ========= SYNTHESE Temp =========
        do_synthese(croisement, shp_file=mET_weap.cf['Synth']['shapefile'], shp_att=mET_weap.cf['Synth']['shp_attrib'],prefix="Temp_", path_in=mET_weap.cf['path']["ERA5_tif"], path_out=mET_weap.cf['path']["synthesis_ERA5"])

    # ------------- THE END --------------------

    print(debut)
    print("Finished at "+str(datetime.now()))
