import unittest
from mysecondvenv.polynom import solve_polynom

class TestPolynom(unittest.TestCase):
    """
    The class tests the three possible cases.
    Another one is still not tested...
    """

    def test_solve_polynom(self):
        x1, x2 = solve_polynom(1, 0, -4)
        self.assertEqual((x1, x2), (-2, 2))

    def test_solve_polynom_linear(self):
        x1 = solve_polynom(0, 1, -4)
        self.assertEqual(x1, (4,))

    def test_solve_polynom_no_soolution(self):
        x1 = solve_polynom(1, 1, 4)
        self.assertEqual(x1, None)

if __name__ == '__main__':
    unittest.main()