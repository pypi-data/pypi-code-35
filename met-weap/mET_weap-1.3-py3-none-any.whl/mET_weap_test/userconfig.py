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
from datetime import datetime
#------------------------

#--- internal imports ---
import mET_weap
#------------------------


mET_weap.path_root = os.path.join('C:'+os.sep+'HAOUZ'+os.sep+'mET_weap') # The root directory for output files
mET_weap.path_to_osgeo = os.path.join('C:'+os.sep+'OSGeo4W64'+os.sep+'bin') # the path for gdal binaries

mET_weap.cf = {
        
    # ---- Switchs to activate or deactivate the modules ----

    # Each Modis tile covers an area of 5°x5°, it may not be necessary to download it again to process another area.

    'do_get_modis'           : True,        # download modis files

    # If you already doanloaded ERAinterim files for your area and domain, don't do it again.

    'do_download_ERA5_cds'   : False,        # download weather dataset from CDS ERA5

    # The following toggles are processing steps,
    # Toggle the steps that already went ok to False

    'do_project_subset'      : False,        # projection and subset of the modis files
    'do_classification'      : False,        # yearly classification
    'do_kc_fc'               : False,        # compute Kc/Fc
    'do_ET0_rain_ERA5'       : False,        # compute daily ET0 and rainfall from ERA5
    'do_interp_ndvi_ERA5'    : False,        # temporal interpolation of NDVI and KC*ET0 with ERA5 data
    'do_synthesis_ERA5'      : False,        # spatio-temporal synthesis with ERA5 data
    
    # short description of the project
    'descr': {
        'NAME' : "FAO56_NDVI",
        'AUTHOR' : "Michel Le Page, CESBIO",
        'CODE' : "Michel Le Page, Cindy Gosset, CESBIO",
        'VERSION' : "1.1",
        'DATE' : "2016/09/26",
    },
    
    # ----- The CDSAPI key to download ERA5 data -----
    'CDSAPI':{
        'url':"https://cds.climate.copernicus.eu/api/v2",
        'key':"xxxx:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        },

    # ---- The MODIS login to download MODIS data ----
    'MODIS':{
        'username':"xxxxxxxxx",
        'password':"xxxxxxxxx"
        },

    # ----- the spatial domain to be processed -----
    'domain' : {
        "uly": 31.7,            # Upper left Y in dd (decimal degrees)
        "ulx": -8.6,            # Upper left X in dd
        'lry': 30.85,            # Lower right Y in dd
        'lrx': -7             # Lower Right X in dd
        },
    
    # ---- the scale ----
    'scale' : {
        "echelle" : 0.25,
        "resolution_ERA5": 0.25            
        },

    # -----  the temporal domain to be processed -----
    'period'  : {
        'begin': datetime(2015, 9, 1),           # the date of beginning as a datetime (yyyy,m,j)
        'end': datetime(2016, 8, 30)              # the date of ending as a datetime (yyyy,m,j)
        },

    # -----  definition of the agronomic year with the beginning month and ending month -----
    'agroyear'  : {
        'begin': 9,           # generally the agronomic year begins in september (9)
        'end': 8              # generally the agronomic year begins in august of the next year (8)
        },

    # -----  Kc and Fc to NDVI relationships -----
    'Relation_NDVI': {
        'scale_factor' : 0.0001,                                 # A scale factor to apply to NDVI data, typically 0.001 for MODIS
        'Ndvi_KcKcb' : os.path.join('Tab_ndvi_kc_fc', 'ndvi_kckcb.xlsx'),   # the XLS file for relations NDVI->Kc (Crop Coefficient)
        'Ndvi_Fc' : os.path.join('Tab_ndvi_kc_fc', 'NDVI-FC.xlsx'),   # the XLS file for relations NDVI->Fc (Fraction Cover)
        'do_senescence' : True,                                 # Optional: To compute or not the fraction cover plateau for annual crops. The computation is time consuming
        'do_stack':False,                                       # Optional: To output or not annual stacks. Those stacks may be useful for data vizualisation

        # rel OS is the table of relations between NDVI/Kcb and NDVI/Fraction covers
        # the syntax is: 'class_name' : [output_value, line of xls file for Kcb, line of xls file for Fc]
        # None if Kc is not computed for a particular class

        'rel_OS' : {
            'No_data' : [0, None, None],
            'Advent'  : [2, None, None],
            'Arb_Veg' : [3,    6,    5],
            'Arb_SN'  : [4,    0,    5],
            'C_Anu'   : [5,    6,    0],
            'Sol_Nu'  : [8, None, None]
            }
        },

    # -----  Synthesis -----
    'Synth': {
        'shapefile' : os.path.join('zonage'+os.sep+'Atlas_Piemont_Haouz.shp'),
        'shp_attrib' : 'c_zone_irr',    # column name of the attribute table
        'timerange' : "MONTH",		# an accumulation time which is either DAY, WEEK or MONTH
        'mode' : "SUM",			# MEAN or SUM
    },

    # -----  The path for the DEM input file -----
    'DEM': {
        'Description':'GTOPO30',
        'DEM_Filename': os.path.join('Gtopo30', 'gt30w020n40.tif'),
        'ERA_Filename_CDSAPI': os.path.join(''.join(os.path.split(mET_weap.path_root)[0]), 'geopotential_cdsapi.nc')
    },

    # ----- The paths of the output files -----
    'path': {
        'Temp_ERA5': os.path.join(''.join(mET_weap.path_root), "fishnet_era5"),                  # directory for temporary data
        
        'Data' : os.path.join(''.join(mET_weap.path_root), "data"),                              # the root directory to download data
        'MOD13Q1': os.path.join(''.join(mET_weap.path_root), "data"+os.sep+ "MOD13Q1"),          # the directory for downloading MODIS MOD13Q1
        'ERA5': os.path.join(''.join(mET_weap.path_root), os.path.join("data", "ERA5")),         # the directory to download ERA5 data

        'Tif' : os.path.join(''.join(mET_weap.path_root), "tif"),                                # the root directory for output data
        'MOD13Q1_tif': os.path.join(''.join(mET_weap.path_root), "tif"+os.sep+"MOD13Q1"),        # the  directory for NDVI Subsets
        'ERA5_tif': os.path.join(''.join(mET_weap.path_root), "tif"+os.sep+"ERA5"),              # the  directory for ERA5 processed input files

        'outputs_ERA5': os.path.join(''.join(mET_weap.path_root), "tif"+os.sep+"outputs_ERA5"),  # The directory for results used for synthesis ERA5
        
        'synthesis_ERA5': os.path.join(''.join(mET_weap.path_root), "synthesis_ERA5")            # The directory for synthesized results based on ERA5 meteorological data
    },
}
