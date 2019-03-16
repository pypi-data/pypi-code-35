"""Define a point in hyperbolic space 
"""


import functools
import numpy
import typing
from pyperbolic import util


def as_points(f):
    """Decorator utility to help coerce arguments as points
    """
    @functools.wraps(f)
    def wrapper(*ps):
        return f(*(coerce_to_point(p) for p in ps))
    return wrapper


class Point:
    """Fundamental object of hyperbolic geometry. The point is an ordered n-tuple of real numbers,
    represented as a numpy array (for performance reasons).
    """
    __slots__ = ('_coords', '_dim', '_arr')

    def __init__(self, *coords: typing.Tuple[float]):
        if len(coords) == 1 and isinstance(coords[0], (tuple, list, numpy.ndarray)):
            coords = numpy.array(coords[0])
            if not coords.ndim == 1:
                raise util.PyperbolicError('Can only construct Point from numpy.ndarray of ndim = 1, not {}'.format(coords.ndim))
            self._coords = coords
        else:
            coords = numpy.array(coords)
        if not coords.dtype.kind in ('i', 'f'):
            raise util.PyperbolicError('Invalid data type for Point {}, only i and f numpy.kinds accepted'.format(coords.dtype.kind))
        self._coords = coords 
        self._dim = self._coords.size

    @as_points
    def __add__(self, other):
        return Point(self.coords + other.coords)

    @as_points
    def __sub__(self, other):
        return Point(self.coords - other.coords)

    def __mul__(self, other):
        if not isinstance(other, (int, float, numpy.float64, numpy.int64)):
            raise TypeError('Multiplication only defined for Points and scalars, not type {}'.format(type(other)))
        return Point(other*self.coords)

    def __truediv__(self, other):
        if not isinstance(other, (int, float, numpy.float64, numpy.int64)):
            raise TypeError('Multiplication only defined for Points and scalars, not type {}'.format(type(other)))
        return Point(other/self.coords)

    def __rmul__(self, other):
        return self * other

    def __rtruediv__(self, other):
        return self / other

    def __eq__(self, other):
        try:
            other = coerce_to_point(other)
        except:
            return False
        return self.coords == other.coords

    def __neg__(self):
        return (-1)*self

    @as_points
    def __radd__(self, other):
        return Point(other.coords + self.coords)

    @as_points
    def __rsub__(self, other):
        return Point(other.coords - self.coords)

    def __repr__(self):
        return '({})'.format(', '.join(str(c) for c in self.coords))

    def __str__(self):
        return repr(self)

    @property
    def coords(self):
        return self._coords

    @property
    def dim(self):
        return self._dim


def coerce_to_point(p: typing.Union[tuple, numpy.ndarray, Point]) -> Point:
    """Coerce acceptable inputs to a Point instance, otherwise raise

    Args:
        p:
            tuple or numpy.ndarray or Point

    Returns:
        Point
    """
    if isinstance(p, Point):
        pass
    elif isinstance(p, (tuple, list)):
        p = Point(*p)
    elif isinstance(p, numpy.ndarray):
        p = Point(p)
    else:
        raise util.PyperbolicError('Unable to coerce {} of type {} to Point'.format(p, type(p)))
    return p
