"""
Distance wrapper around pyproj
"""


import pyproj

GEOD = pyproj.Geod(ellps='WGS84')

def distance(lat1, lon1, lat2, lon2):
    """
    Return distance between two points in km
    """
    d = GEOD.inv(lon1, lat1, lon2, lat2)[2] / 1000
    return d
