"""

"""
import numpy as np
# For testing whether a number is close to zero or not we use epsilon:
_EPS = np.finfo(float).eps * 4.0

# axis sequences for Euler angles
_NEXT_AXIS = [1, 2, 0, 1]

# map axes strings to/from tuples of inner axis, parity, repetition, frame
_AXES2TUPLE = {
    'xyz': (0, 0, 1, 2), 'xyx': (0, 0, 1, 0), 'xzy': (0, 0, 2, 1),
    'xzx': (0, 0, 2, 0), 'yzx': (0, 1, 2, 0), 'yzy': (0, 1, 2, 1),
    'yxz': (0, 1, 0, 2), 'yxy': (0, 1, 0, 1), 'zxy': (0, 2, 0, 1),
    'zxz': (0, 2, 0, 2), 'zyx': (0, 2, 1, 0), 'zyz': (0, 2, 1, 2)}
