"""
Spatial index using an R-Tree
"""


# ---------------------------
# Imports
# ---------------------------

import pyproj
import rtree
from .distance import distance

# ---------------------------
# Classes
# ---------------------------

class GeoIndex:

    def __init__(self, data=None, leaf_capacity=100, near_minimum_overlap_factor=32):
        """ <data> is an iterator containing (id, x, y) elements.
        User must ensure that id is unique!
        """

        self.coords = dict()    # id -> (lat, lon)
        self.xy = dict()        # id -> (x, y)

        # API: https://pyproj4.github.io/pyproj/html/api/proj.html#pyproj-proj
        # Projection: Albers Equal Area, https://proj4.org/operations/projections/aea.html
        self.proj = pyproj.Proj('+proj=aea +lat_1=29.5 +lat_2=42.5')

        # Reference: https://libspatialindex.org/overview.html#the-rtree-package
        p = rtree.index.Property()
        p.leaf_capacity = leaf_capacity
        p.near_minimum_overlap_factor = near_minimum_overlap_factor

        if data is None:
            self.idx = rtree.index.Index(properties=p)
        else:
            # stream takes an iterable of the form (id, (x,y,x,y), object) where object is MANDATORY but can be none
            data_generator = rtree_generator(self.proj, self.coords, self.xy, data)
            self.idx = rtree.index.Index(data_generator, properties=p)
            assert len(self.coords), 'Index is empty even though a stream was provided'


    def insert(self, identifier, lat, lon):
        assert type(identifier) == int
        assert type(lat) == type(lon) == float
        assert identifier not in self.coords
        x, y = self.proj(lon, lat)
        
        self.coords[identifier] = (lat, lon)
        self.xy[identifier] = (x, y)
        self.idx.insert(identifier, (x, y, x, y) )


    def delete(self, identifier):
        self.coords.pop(identifier)
        x, y = self.xy.pop(identifier)
        self.idx.delete(identifier, (x, y, x, y) )


    def nearest(self, lat, lon, identifier=None, num_results=1):
        """Return the N elements closest to a (lat, lon) point.
        - If identifier is not None, we will exclude answers with that id (which we take as "self")
        - Each element is returned as (ID, distance)
        """
        
        #assert num_results==1
        # TODO: Allow nearest N (need to get the Nth and then use that as pivot)
        # TODO: Allow nearest by group?? but that probably is multiple indexes
        # see original rtreegeo.py code for more sanity checks

        x, y = self.proj(lon, lat)
        _ = (x, y, x, y)
        candidates = [c for c in self.idx.nearest(_, num_results + 1) if c != identifier]
        return candidates[0]


# ---------------------------
# Functions
# ---------------------------

def rtree_generator(proj, coords, xy, data):
    for identifier, lat, lon in data:
        assert type(identifier) == int
        assert type(lat) in (float, int) and type(lon) in (float, int), (lat, lon)
        assert identifier not in coords
        x, y = proj(lon, lat)
        coords[identifier] = (lat, lon)
        xy[identifier] = (x, y)
        yield (identifier, (x, y, x, y), None)
