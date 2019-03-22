# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 12:39:45 2018

@author: VI
"""

import os
import cdsapi
import urllib3

#--- config imports ---
from userconfig import mET_weap
from mET_weap import cf, path_to_osgeo, path_root
#----------------------

def geo_download_cdsapi(fname, window):
        
    c = cdsapi.Client(url = cf["CDSAPI"]["url"], key = cf["CDSAPI"]["key"])
       
    c.retrieve(
            
    'reanalysis-era5-single-levels',
    {
        'product_type':'reanalysis',
        'format':'netcdf',
        'variable':'geopotential',
        'area': window,
        'year':'2000',
        'time':'00:00',
        'month':'01',
        'day':'01'
    },
    fname
    )

