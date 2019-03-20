import math

from rover_position_rjg.json_aware.json_aware import JsonAware


class Vector(JsonAware['Vector']):
    """A 3D vector"""
    _tolerance = 1e-6

    @staticmethod
    def zero():
        return Vector([0, 0, 0])

    @staticmethod
    def one():
        return Vector([1, 1, 1])

    def __init__(self, values: list):
        self.values = values

    @property
    def x(self):
        return self.values[0]

    @property
    def y(self):
        return self.values[1]

    @property
    def z(self):
        return self.values[2]

    def enu_to_ned(self):
        """Converts from the East North Up axis convention that we use
        to the commonly used aircraft convention of North East Down."""
        return Vector([self.y, self.x, -self.z])

    def ned_to_enu(self):
        """Converts from the aircraft convention of North East Down
        to the land vehicle convention of East North Up that we use."""
        return self.enu_to_ned()

    def __eq__(self, other) -> bool:
        if isinstance(other, Vector):
            return math.isclose(self.x, other.x, rel_tol=Vector._tolerance) and \
                   math.isclose(self.y, other.y, rel_tol=Vector._tolerance) and \
                   math.isclose(self.z, other.z, rel_tol=Vector._tolerance)
        return False

    def __add__(self, other) -> 'Vector':
        return Vector([self.x + other.x, self.y + other.y, self.z + other.z])

    def __sub__(self, other) -> 'Vector':
        return Vector([self.x - other.x, self.y - other.y, self.z - other.z])

    def __mul__(self, other: float) -> 'Vector':
        return Vector([self.x * other, self.y * other, self.z * other])

    def __truediv__(self, other: float) -> 'Vector':
        return Vector([self.x / other, self.y / other, self.z / other])

    def scale(self, other) -> 'Vector':
        """Scales each element of this vector by the corresponding element of other."""
        return Vector([self.x * other.x, self.y * other.y, self.z * other.z])

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def change_hand(self) -> 'Vector':
        """Flips from the left hand rule to the right hand rule or vice versa
        by swapping the x and y axes."""
        return Vector([self.y, self.x, self.z])

    def __repr__(self) -> str:
        return '[{},{},{}]'.format(self.x, self.y, self.z)

    def __str__(self) -> str:
        return '[{:.4f}, {:.4f}, {:.4f}]'.format(self.x, self.y, self.z)

    def __lt__(self, other) -> bool:
        return self.x < other.x and self.y < other.y and self.z < other.z

    def __gt__(self, other) -> bool:
        return other < self

    def to_json(self) -> str:
        return '{{"x":{}, "y":{}, "z":{}}}'.format(self.x, self.y, self.z)

    @staticmethod
    def from_json(obj: dict) -> 'Vector':
        return Vector([obj['x'], obj['y'], obj['z']])
