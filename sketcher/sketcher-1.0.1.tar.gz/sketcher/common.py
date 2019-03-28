from __future__ import division
import math
from math import sin, cos, pi, acos
color_tab = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'grey': (127, 127, 127),
}


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vec2({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        return (isinstance(other, Vec2)
                and self.x == other.x
                and self.y == other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __getitem__(self, n):
        if n == 0 or n == 'x':
            return self.x
        elif n == 1 or n == 'y':
            return self.y
        else:
            raise IndexError('vector index unknown')

    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other):
        assert isinstance(other, Vec2)
        return Vec2(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        assert isinstance(other, Vec2)
        return Vec2(self.x-other.x, self.y-other.y)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __mul__(self, a):
        assert isinstance(a, (float, int))
        return Vec2(self.x*a, self.y*a)

    def __rmul__(self, a):
        return self * a

    def __truediv__(self, a):
        assert isinstance(a, (float, int))
        return Vec2(self.x/a, self.y/a)

    def rotate(self, angle):
        xp = self.x * cos(angle) - self.y * sin(angle)
        yp = self.x * sin(angle) + self.y * cos(angle)
        return Vec2(xp, yp)

    def dot(self, other):
        assert isinstance(other, Vec2)
        return self.x * other.x + self.y * other.y

    def det(self, other):
        assert isinstance(other, Vec2)
        return self.x * other.y - self.y * other.x

    def norm(self):
        return (self.x**2 + self.y**2)**0.5

    def normed(self):
        n = self.norm()
        if n > 0:
            return Vec2(self.x/n, self.y/n)
        else:
            return self

    def angle(self, other):
        on = other.normed()
        sn = self.normed()
        cos = sn.dot(on)
        sin = sn.det(on)
        if sin > 0:
            return acos(cos)
        else:
            return -acos(cos)

    @classmethod
    def from_angle(cls, angle, norm=1):
        return cls(norm*cos(angle), norm*sin(angle))

    def dist(self, other):
        return (self - other).norm()


class Shape:
    def __init__(self, vertex):
        assert len(vertex) >= 3
        self.vertex = list(Vec2(x, y) for x, y in vertex)
        self._tri_cache = None

    def __iter__(self):
        for v in self.vertex:
            yield v

    def center(self):
        n = len(self.vertex)
        return sum(self.vertex, Vec2(0, 0))/n

    def rotate(self, angle, pivot='center'):
        if pivot == 'center':
            pivot = self.center()
        else:
            pivot = Vec2(*pivot)
        return self.__class__([
            ((v - pivot).rotate(angle) + pivot) for v in self.vertex
        ])

    def translate(self, vec):
        vec = Vec2(*vec)
        return self.__class__([v + vec for v in self.vertex])

    def copy(self):
        return self.__class__(self.vertex.copy())

    def to_tris(self):
        if not self._tri_cache:
            self._tri_cache = self._to_tris()
        return self._tri_cache

    def _to_tris(self):
        '''
            Break a polygon into several triangles
        '''
        def is_ear(vtx, k):
            n = len(vtx)
            a, b, c = vtx[k], vtx[(k+1) % n], vtx[(k+2) % n]
            ab = b - a
            ac = c - a
            bc = c - b
            if ab.det(bc) > 0:
                return False
            for i in range(len(vtx)):
                if i == k or i == (k+1) % n or i == (k+2) % n:
                    continue
                else:
                    p = vtx[i]
                    ap = p - a
                    bp = p - b
                    cp = p - c
                    if ap.det(ab) * ap.det(ac) <= 0 \
                       and bp.det(bc) * bp.det(-ab) <= 0 \
                       and cp.det(-ac) * cp.det(-bc) <= 0:
                        return False
            return True

        tris = []
        vertex = self.vertex.copy()
        cursor = 0

        nv = len(vertex)
        while nv > 3:
            stcr = cursor
            while not is_ear(vertex, cursor):
                cursor = (cursor + 1) % nv
                if cursor == stcr:
                    raise Exception('Cannot split this shape into triangles.'
                                    ' Make sure vertex are given in clock-wise'
                                    ' order.')
            tris.append(Tri((vertex[cursor],
                             vertex[(cursor+1) % nv],
                             vertex[(cursor+2) % nv])))
            vertex.pop((cursor+1) % nv)
            nv -= 1
        tris.append(Tri(vertex))

        return tris


class Tri(Shape):
    def __init__(self, vertex):
        assert len(vertex) == 3, "Tri have 3 vertex by definition."
        Shape.__init__(self, vertex)

    def _to_tris(self):
        return (self,)


class Ellipse(Shape):
    def __init__(self, x, y, a, b=0, angle=0, n=0):
        if b == 0:
            b = a
        if n == 0:
            n = max(16, int(max(a, b)/2) + 1)

        self.a = a
        self.b = b
        self.angle = angle
        self.center = Vec2(x, y)

        step = 2*pi/n
        vertex = [
            Vec2(
                a * cos(k*step),
                b * sin(k*step)
            ).rotate(angle) + self.center for k in range(n)
        ]
        Shape.__init__(self, vertex)

    def _to_tris(self):
        tris = []
        for i in range(len(self.vertex)):
            tris.append(Tri((self.center, self.vertex[i], self.vertex[i-1])))
        return tris


class Color:
    def __init__(self, col):
        self.r = 0
        self.g = 0
        self.b = 0
        if isinstance(col, str):
            self.r, self.g, self.b = color_tab[col]
        elif isinstance(col, Color):
            self.r = col.r
            self.g = col.g
            self.b = col.b
        elif isinstance(col, float) or isinstance(col, int):
            if math.isnan(col):
                col = 255
            elif col < 0:
                col = 0
            elif col > 255:
                col = 255
            self.r = int(col)
            self.g = int(col)
            self.b = int(col)
        elif hasattr(col, '__iter__'):
            self.r, self.g, self.b = col
        else:
            raise TypeError('{} is not a valid color initial value.'
                            .format(col))

    def hashtag(self):
        r = hex(int(self.r))[2:]
        g = hex(int(self.g))[2:]
        b = hex(int(self.b))[2:]
        if len(r) != 2:
            r = '0' + r
        if len(g) != 2:
            g = '0' + g
        if len(b) != 2:
            b = '0' + b
        return '#{}{}{}'.format(r, g, b)

    def tupple255(self):
        return (int(self.r), int(self.g), int(self.b))

    def tupple255alpha(self):
        return (int(self.r), int(self.g), int(self.b), 255)


class MouseState:
    def __init__(self):
        self.pos = (0, 0)
        self.pressed = set()
        self.released = set()

    def copy(self):
        cp = MouseState()
        cp.pos = self.pos.copy()
        cp.pressed = self.pressed.copy()
        cp.released = self.released.copy()
        return cp

    def flush(self):
        self.pressed.clear()
        self.released.clear()

    def clean(self):
        still_pressed = self.pressed - self.released
        releasing = self.released.intersection(self.pressed)

        self.pressed = still_pressed
        self.released = releasing


class KeyboardState:
    def __init__(self):
        self.pressed = set()
        self.released = set()

    def copy(self):
        cp = KeyboardState()
        cp.pressed = self.pressed.copy()
        cp.released = self.released.copy()
        return cp

    def flush(self):
        self.pressed.clear()
        self.released.clear()

    def clean(self):
        still_pressed = self.pressed - self.released
        releasing = self.released.intersection(self.pressed)

        self.pressed = still_pressed
        self.released = releasing
