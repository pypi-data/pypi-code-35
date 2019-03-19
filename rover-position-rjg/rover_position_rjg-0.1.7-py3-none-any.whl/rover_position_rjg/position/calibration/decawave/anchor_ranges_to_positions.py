import math

from rover_position_rjg.data.vector import Vector


class AnchorRangesToPositions:
    """Finds the absolute positions of all 4 anchor tags in their
    own frame of reference. Note the Decawave tags use a right hand
    rule when auto-calibrating. This class does the same so that
    calibrations from this class are directly comparable to the
    Decawave calibration."""

    def __init__(self,
                 distance_1_2: float,
                 distance_2_3: float,
                 distance_3_4: float,
                 distance_4_1: float,
                 distance_1_3: float,
                 distance_2_4: float,
                 height: float,
                 ):
        """
        Creates a new instance from the 6 distances.
        :param distance_1_2: Distance from the initiator anchor to the next anchor going
        anticlockwise. This sets the direction of the x axis.
        :param distance_2_3: Distance from 2nd anchor to 3rd anchor going anticlockwise
        :param distance_3_4: Distance from 3rd anchor to 4th anchor going anticlockwise
        :param distance_4_1: Distance from 4th anchor to initiator anchor going anticlockwise
        :param distance_1_3: Diagonal from the initiator to anchor 3
        :param distance_2_4: Diagonal from the 2nd anchor to the 4th
        :param height: height of the anchors above floor level (they must all be the same)
        """
        self._distance_1_2 = distance_1_2
        self._distance_2_3 = distance_2_3
        self._distance_3_4 = distance_3_4
        self._distance_4_1 = distance_4_1
        self._distance_1_3 = distance_1_3
        self._distance_2_4 = distance_2_4
        self._height = height

    def position_1(self) -> Vector:
        """The co-ordinates of anchor 1 (the initiator)"""
        return Vector([0.0, 0.0, self._height])

    def position_2(self) -> Vector:
        """The co-ordinates of anchor 2. They y co-ordinate is always 0."""
        return Vector([self._distance_1_2, 0.0, self._height])

    def position_3(self) -> Vector:
        """The co-ordinates of anchor 3"""
        angle_at_1 = self._calculate_angle(self._distance_1_2, self._distance_1_3, self._distance_2_3)
        x = math.cos(angle_at_1) * self._distance_1_3
        y = math.sin(angle_at_1) * self._distance_1_3
        return Vector([x, y, self._height])

    def position_4(self) -> Vector:
        """The co-ordinates of anchor 4"""
        angle_at_1 = self._calculate_angle(self._distance_1_2, self._distance_4_1, self._distance_2_4)
        x = math.cos(angle_at_1) * self._distance_4_1
        y = math.sin(angle_at_1) * self._distance_4_1
        return Vector([x, y, self._height])

    @staticmethod
    def _calculate_angle(a: float, b: float, c: float) -> float:
        """
        Calculates an angle in a triangle given the lengths of all three sides
        :param a: side a, adjacent to the angle to be returned
        :param b: side b, also adjacent to the angle to be returned
        :param c: side c, opposite the angle to be returned
        :returns the angle in radians
        """
        # Law of cosines
        cos_theta = ((a**2 + b**2) - c**2) / (2 * a * b)
        return math.acos(cos_theta)

    def error_3_4(self) -> float:
        """Returns the difference between the measured and calculated lengths
        for side 3_4 which wasn't used in any calculations"""
        vector_3_4 = self.position_4() - self.position_3()
        error = vector_3_4.magnitude() - self._distance_3_4
        return error
