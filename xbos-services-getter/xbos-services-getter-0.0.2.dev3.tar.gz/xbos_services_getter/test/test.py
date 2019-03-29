
import datetime
import pytz

import xbos_services_utils3 as utils

import os

import xbos_services_getter

all_buildings = utils.get_buildings()

# Comfortband Test

for iter_bldg in all_buildings:
	print("Starting Building: %s" % iter_bldg)
	for iter_zone in utils.get_zones(iter_bldg):
		print("Getting zone: %s" % iter_zone)
		start = datetime.datetime(year=2018, month=1, day=1, hour=0, minute=0).replace(tzinfo=pytz.utc)
		end = start + datetime.timedelta(days=7)
		window = "15m"

		temperature_band_stub = xbos_services_getter.get_temperature_band_stub()

		comfortband = xbos_services_getter.get_comfortband(temperature_band_stub, iter_bldg, iter_zone, start, end, window)
	print("\n")

