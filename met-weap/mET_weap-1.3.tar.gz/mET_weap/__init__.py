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


__version__ = '1.1'

#--- internal imports ---

from mET_weap.download_geopotential_cdsapi import geo_download_cdsapi
from mET_weap.DEM_1km import DEM_1km_CDSAPI
from mET_weap.get_modis import return_url, parse_modis_dates, get_modisfiles
from mET_weap.modis_process import modis_tile_id, ndvi_daily, albedo_daily, scale_offset, scale_offset_angle
from mET_weap.hdf2tif import hdf2tif
from mET_weap.Classification import classif_ijrs1997
from mET_weap.ecmwf_daily import gradient, PIL_resize, era5_daily, Atm_Press, psychrometric_const, e0t_from_tair, msvp_day, ssvp, ea_from_rhmean, Extraterrestrial_radiation, Clearsky_radiation_z, Net_shortwave_radiation, Net_longwave_radiation, Net_Radiation, et0_pm2
from mET_weap.utils import select_files_agroyear_16j, select_files_agroyear_all, get_date_ecmwf, get_date_modis
from mET_weap.Kc_Fc import savitzky_golay, local_min_max, KC_FC_calc, PIL_resize, ET_actual_ERA5
from mET_weap.synthesize import synthesize_init, synthesize_init_part2, synthesize_part1, synthesize_part2, synthesize_part3, synthesize_part2_areas, do_croisement_shape, do_synthese_areas, do_synthese_classes, do_synthese
import mET_weap.synthesize as synth
from mET_weap.download_ERA5_cds import download_ERA5_cds
