import unittest
from korr import mcc
import numpy as np
import numpy.testing as npt


class Test_mcc(unittest.TestCase):

    def test1(self):
        x = np.array([[0, 1], [0, 0], [0, 0]])
        r, _ = mcc(x)
        print(r)
        npt.assert_array_equal(r, [[1, np.nan], [np.nan, 1]])

    def test2(self):
        x = np.array([[0, 1], [0, 0], [0, 0]], autocorrect=True)
        r, _ = mcc(x)
        print(r)
        npt.assert_array_equal(r, [[1, 0], [0, 1]])


# run
if __name__ == '__main__':
    unittest.main()
