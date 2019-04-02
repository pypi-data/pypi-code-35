"""
tupu: fast geodesic distances
================================
tupu is a Python package that calculates
`geodesic distances<https://en.wikipedia.org/wiki/Geodesics_on_an_ellipsoid>`_
between points or sets of points.

Its goal is to be able to efficiently compute distances to lists of points.
For instance, if you have a list of N points and M cities, and want to compute
the closest city to each point, it avoids brute-force computation of the NxM
distances, and instead indexes each city through
`R-Trees<https://en.wikipedia.org/wiki/R-tree>`_.

tupu is build on two key packages:

1. Geodesic distances are computed through pyproj, a Python interface to the PROJ.4 library (written in C).
2. Spatial indexing is done through the `rtree<http://toblerity.org/rtree/>`_ package,
a Python wrapper to the `libspatialindex<https://libspatialindex.org/>`_ library.
"""


from .utils import load_csv, save_csv, get_args_from_filename, get_coords
from .distance import distance
from .geoindex import GeoIndex
from .table import Table
from .io import cli
