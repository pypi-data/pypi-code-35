import math
import unittest

from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.calibration.decawave.anchor_ranges_to_positions import AnchorRangesToPositions


class TestAnchorRangesToPositions(unittest.TestCase):
    def test_calculate_angle_1(self):
        self.assertEqual(90, math.degrees(AnchorRangesToPositions._calculate_angle(3, 4, 5)))
        self.assertAlmostEqual(36.8699, math.degrees(AnchorRangesToPositions._calculate_angle(4, 5, 3)), 4)
        self.assertAlmostEqual(53.1301, math.degrees(AnchorRangesToPositions._calculate_angle(3, 5, 4)), 4)

    def test_living_room(self):
        result = AnchorRangesToPositions(
            3.880, 3.650, 3.710, 4.975,
            5.040, 6.280, 0.070
        )
        self.assertEqual(Vector([0.0, 0.0, 0.07]), result.position_1())
        self.assertEqual(Vector([3.880, 0.0, 0.07]), result.position_2())
        self.assertEqual(Vector([3.496585052, 3.62980619, 0.07]), result.position_3())
        self.assertEqual(Vector([0.047245490, 4.97477566, 0.07]), result.position_4())

    def test_error(self):
        result = AnchorRangesToPositions(
            3.880, 3.650, 3.710, 4.975,
            5.040, 6.280, 0.070
        )
        self.assertAlmostEqual(result.error_3_4(), -0.00771877)

    def test_wider_at_the_top(self):
        result = AnchorRangesToPositions(
            2.7, 3.8, 6.9, 3.3,
            5.3, 5.8, 0.0
        )
        self.assertEqual(Vector([0.0, 0.0, 0.0]), result.position_1())
        self.assertEqual(Vector([2.7, 0.0, 0.0]), result.position_2())
        self.assertEqual(Vector([3.8777777, 3.6128713, 0.0]), result.position_3())
        self.assertEqual(Vector([-2.8629629, 1.6411712, 0.0]), result.position_4())
        self.assertAlmostEqual(result.error_3_4(), 0.1231892)
