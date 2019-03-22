# Copyright (C) 2014-2018 Michel Le Page
#
# preproc_weap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# preproc_weap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import cdsapi
import urllib3

#--- config imports ---
from userconfig import mET_weap
from mET_weap import cf, path_to_osgeo, path_root
#----------------------


def download_ERA5_cds(date_ecmwf,window,fname):
    
    c = cdsapi.Client(url = cf["CDSAPI"]["url"], key = cf["CDSAPI"]["key"])

    c.retrieve(
    
	#  urllib3.disable_warnings(),

    'reanalysis-era5-single-levels',
    {
        'variable':[
            '10m_u_component_of_wind','10m_v_component_of_wind','2m_dewpoint_temperature',
            '2m_temperature','surface_pressure', 'surface_solar_radiation_downwards','total_precipitation',
            'TOA incident solar radiation'
        ],
        'product_type':'reanalysis',
        'date': date_ecmwf,
        'area': window,
        'grid': [0.25, 0.25],
        'time':[
                '03:00','06:00','09:00',
                '12:00','15:00','18:00',
                '21:00','00:00'
                ],
        'format':'netcdf'
    },
    fname
    )
