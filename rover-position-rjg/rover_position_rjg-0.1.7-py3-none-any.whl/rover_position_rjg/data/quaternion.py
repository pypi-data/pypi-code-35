import math

from rover_position_rjg.data.vector import Vector
from rover_position_rjg.json_aware.json_aware import *


class Quaternion(JsonAware['Quaternion']):
    """A quaternion with the four values w, i, j and k"""
    _tolerance = 1e-6
    _degreesPerRadian = math.degrees(1)

    @staticmethod
    def identity() -> 'Quaternion':
        return Quaternion(1, 0, 0, 0)

    def __init__(self, w: float, i: float, j: float, k: float):
        self.w = w
        self.i = i
        self.j = j
        self.k = k

    def __matmul__(self, other) -> 'Quaternion':
        """Computes the Hamilton product. If other is a 3D vector then the
        output includes the rotated vector."""
        w = (self.w * other.w) - (self.i * other.i) - (self.j * other.j) - (self.k * other.k)
        i = (self.w * other.i) + (self.i * other.w) + (self.j * other.k) - (self.k * other.j)
        j = (self.w * other.j) - (self.i * other.k) + (self.j * other.w) + (self.k * other.i)
        k = (self.w * other.k) + (self.i * other.j) - (self.j * other.i) + (self.k * other.w)
        return Quaternion(w, i, j, k)

    def rotate(self, vector: Vector) -> Vector:
        v = Quaternion(0, vector.x, vector.y, vector.z)
        inv_self = Quaternion(self.w, -self.i, -self.j, -self.k)    # Assume self is a unit quaternion
        result = self @ v @ inv_self
        return Vector([result.i, result.j, result.k])

    def magnitude(self) -> float:
        return math.sqrt(self.w**2 + self.i**2 + self.j**2 + self.k**2)

    def normalise(self) -> 'Quaternion':
        """Scales the quaternion to have a magnitude of 1"""
        mag = self.magnitude()
        return Quaternion(self.w/mag, self.i/mag, self.j/mag, self.k/mag)

    def __neg__(self):
        """Returns a quaternion which is the inverse of this.
        i.e. a unit quaternion will undo the rotation."""
        mag = self.magnitude()
        return Quaternion(self.w/mag, -self.i/mag, -self.j/mag, -self.k/mag)

    @staticmethod
    # See http://www.sedris.org/wg8home/Documents/WG80485.pdf section 3.4.10
    def from_tait_bryan(tait_bryan_angles: Vector) -> 'Quaternion':
        """Returns a Quaternion representing the given rotation in Tait-Bryan angles.
        AKA Cardan angles, aviation angles. The angles must follow the ZYX convention. AKA 321.
        :param tait_bryan_angles: Tait Bryan angles in degrees where x=roll, y=pitch and z=yaw.
        :return: a unit Quaternion
        """
        return Quaternion.from_tait_bryan_radians(tait_bryan_angles / Quaternion._degreesPerRadian)

    @staticmethod
    # See http://www.sedris.org/wg8home/Documents/WG80485.pdf section 3.4.10
    def from_tait_bryan_radians(tait_bryan_angles: Vector) -> 'Quaternion':
        """Returns a Quaternion representing the given rotation in Tait-Bryan angles.
        AKA Cardan angles, aviation angles. The angles must follow the ZYX convention. AKA 321.
        :param tait_bryan_angles: Tait Bryan angles in degrees where x=roll, y=pitch and z=yaw.
        :return: a unit Quaternion
        """
        roll = tait_bryan_angles.x
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)
        pitch = tait_bryan_angles.y
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        yaw = tait_bryan_angles.z
        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)

        w = cy * cr * cp + sy * sr * sp
        i = cy * sr * cp - sy * cr * sp
        j = cy * cr * sp + sy * sr * cp
        k = sy * cr * cp - cy * sr * sp
        return Quaternion(w, i, j, k)

    # See http://www.sedris.org/wg8home/Documents/WG80485.pdf section 3.4.10
    def to_tait_bryan(self) -> Vector:
        """
        Converts this Quaternion to Tait-Bryan angles. AKA Cardan or aviation angles
        Apply the rotations in the order Yaw, Pitch, Roll to get the correct pose.
        Known as the ZYX or 321 ordering.
        :return: A vector with x=roll, y=pitch and z=yaw
        """
        return self.to_tait_bryan_radians() * Quaternion._degreesPerRadian

    # See http://www.sedris.org/wg8home/Documents/WG80485.pdf section 3.4.10
    def to_tait_bryan_radians(self) -> Vector:
        """
        Converts this Quaternion to Tait-Bryan angles. AKA Cardan or aviation angles
        Apply the rotations in the order Yaw, Pitch, Roll to get the correct pose.
        Known as the ZYX or 321 ordering.
        :return: A vector with x=roll, y=pitch and z=yaw
        """
        # roll (x-axis rotation)
        q = Quaternion(self.w, self.i, self.j, self.k)
        sinr_cosp = +2.0 * (q.w * q.i + q.j * q.k)
        cosr_cosp = +1.0 - 2.0 * (q.i * q.i + q.j * q.j)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # pitch (y-axis rotation)
        sin_p = +2.0 * (q.w * q.j - q.k * q.i)
        if math.fabs(sin_p) >= 1:
            pitch = math.copysign(math.pi / 2, sin_p)  # use 90 degrees if out of range
        else:
            pitch = math.asin(sin_p)

        # yaw (z-axis rotation)
        siny_cosp = +2.0 * (q.w * q.k + q.i * q.j)
        cosy_cosp = +1.0 - 2.0 * (q.j * q.j + q.k * q.k)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        return Vector([roll, pitch, yaw])

    @staticmethod
    def from_euler(e: Vector) -> 'Quaternion':
        """http://www.sedris.org/wg8home/Documents/WG80485.pdf section 3.4.10
        Produces quaternion in the z-x-z orientation from gamma, beta, alpha.
        Angles in vector are in the order alpha, beta, gamma
        This doesn't round trip with the to_euler method. I swapped the x and z
        and negated the signs to make it round trip."""
        alpha = math.radians(e.z)
        cr = math.cos(alpha * 0.5)
        sr = math.sin(alpha * 0.5)
        beta = math.radians(e.y)
        cp = math.cos(beta * 0.5)
        sp = math.sin(beta * 0.5)
        gamma = math.radians(e.x)
        cy = math.cos(gamma * 0.5)
        sy = math.sin(gamma * 0.5)

        w = -(cy*cr - sy*sr) * cp
        i = -(cy*cr + sy*sr) * sp
        j = -(sy*cr - cy*sr) * sp
        k = -(sy*cr + cy*sr) * cp
        return Quaternion(w, i, j, k)

    def to_euler(self) -> Vector:
        """http://www.sedris.org/wg8home/Documents/WG80485.pdf section 3.4.10
        Produces Euler angles of the z-x-z 3-1-3 orientation from gamma, beta, alpha angles.
        This formulation of Euler angles is very rare. The Tait Bryan formulation
        is much more common.
        NOT confirmed to be a valid set of output angles."""
        alpha = math.atan2((self.i*self.k + self.w*self.j), -(self.j*self.k - self.w*self.i))
        beta = math.acos(1 - 2*(self.i**2 + self.j**2))
        gamma = math.atan2((self.i*self.k - self.w*self.j), (self.j*self.k + self.w*self.i))
        return Vector([math.degrees(alpha), math.degrees(beta), math.degrees(gamma)])

    def __eq__(self, other) -> bool:
        if isinstance(other, Quaternion):
            return math.isclose(self.w, other.w, rel_tol=Quaternion._tolerance) and \
                   math.isclose(self.i, other.i, rel_tol=Quaternion._tolerance) and \
                   math.isclose(self.j, other.j, rel_tol=Quaternion._tolerance) and \
                   math.isclose(self.k, other.k, rel_tol=Quaternion._tolerance)
        return False

    def __repr__(self) -> str:
        return '[{},{},{},{}]'.format(self.w, self.i, self.j, self.k)

    def to_json(self) -> str:
        return '{{"w":{}, "i":{}, "j":{}, "k":{}}}'.format(self.w, self.i, self.j, self.k)

    @staticmethod
    def from_json(obj: dict) -> 'Quaternion':
        return Quaternion(obj['w'], obj['i'], obj['j'], obj['k'])
