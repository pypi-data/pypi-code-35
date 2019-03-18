import cocos.device
import cocos.numerics as cn
import numpy as np
import pytest


test_data = [np.array([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 20]],
                      dtype=np.int32),
             np.array([[0.2, 1.0, 0.5],
                       [0.4, 0.5, 0.6],
                       [0.7, 0.2, 0.25]],
                      dtype=np.float32),
             np.array([[0.5, 2.3, 3.1],
                       [4, 5.5, 6],
                       [7 - 9j, 8 + 1j, 2 + 10j]],
                      dtype=np.complex64),
             np.array([[[1.0, 2], [3, 4]],
                       [[5, 6], [7, 8]]],
                      dtype=np.float32)]


@pytest.mark.parametrize("A_numpy", test_data)
def test_roll(A_numpy):
    cocos.device.init()
    A_cocos = cn.array(A_numpy)

    for shift in range(-2, 2):
        for axis in range(2):
            B_numpy = np.roll(A_numpy, shift=shift, axis=axis)
            B_cocos = cn.roll(A_cocos, shift=shift, axis=axis)
            assert np.allclose(B_cocos, B_numpy)
