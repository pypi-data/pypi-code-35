class CoordConverter:
    """Coordinate conversions to/from Normalized Device Coords."""
    
    def __init__(self, minval, maxval, inverted=False):
        """Construct a coordinate converted with the supplied bounds."""
        self.minval = minval
        self.maxval = maxval
        self.delta = maxval - minval
        self.inverted = inverted

    def to_ndc(self, a):
        """Convert coordinate to normalized device coordinate [0..1]"""
        an = (a - self.minval) / self.delta
        if self.inverted:
            an = 1 - an
        return an

    def from_ndc(self, an):
        """Get coordinate from normalized device coordinates [0..1]"""
        if self.inverted:
            an = 1 - an
        return an * self.delta + self.minval

    def in_range(self, a):
        """Check if value is within the bounds for this coordinate system."""
        return self.minval <= a <= self.maxval

    def __str__(self):
        return ('CoordConverter(min=%f,max=%f,inv=%s)' % 
                    (self.minval, self.maxval, self.inverted)
        )


class CoordSys2D:
    """Pair of coordinate converters for X and Y"""

    def __init__(self, x_min, x_max, y_min, y_max, 
        x_inverted=False, y_inverted=False):
        self.xconv = CoordConverter(x_min, x_max, x_inverted)
        self.yconv = CoordConverter(y_min, y_max, y_inverted)

    def to_ndc(self, x, y):
        """Convert a point to normalized device coordinates [0..1]"""
        return self.xconv.to_ndc(x), self.yconv.to_ndc(y)

    def from_ndc(self, xn, yn):
        """Get coordinates from normalized device coordinates [0..1]"""
        return self.xconv.from_ndc(xn), self.yconv.from_ndc(yn)

    def in_range(self, x, y):
        """Check if value is within the range."""
        return self.xconv.in_range(x) and self.yconv.in_range(y)

    def __str__(self):
        return ('CoordSys[X(min=%f,max=%f,inv=%s),Y(min=%f,max=%f,inv=%s)]' % 
                    (self.xconv.minval, self.xconv.maxval, self.xconv.inverted,
                     self.yconv.minval, self.yconv.maxval, self.yconv.inverted)
        )


if __name__ == '__main__':
    coordSys = CoordSys2D(10, 20, -30, -10, y_inverted=True)
    x, y = 15, -10
    xn, yn = coordSys.to_ndc(x, y)
    x2, y2 = coordSys.from_ndc(xn, yn)
    print('  Original Coords: %s' % ([x, y]))
    print('Normalized Coords: %s' % ([xn, yn]))
    print('  Loopback Coords: %s' % ([x2, y2]))

