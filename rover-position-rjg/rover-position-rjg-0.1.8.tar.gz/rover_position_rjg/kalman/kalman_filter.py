import numpy as np
import numpy.linalg as lin


# noinspection PyPep8Naming
class KalmanFilter:
    """
    A general purpose Kalman filter implementation based on
    Based on "An Introduction to the Kalman Filter" by Welch and Bishop
    https://www.cs.unc.edu/~welch/media/pdf/kalman_intro.pdf
    Additional inspiration from
    https://towardsdatascience.com/wtf-is-sensor-fusion-part-2-the-good-old-kalman-filter-3642f321440

    Process Model
    x = Ax + Bu + w
    x - system state vector at time k
    A - function giving the new state after time T assuming no noise or control input
    w - process noise where w approx = N(0, R)
    R - the variance of w

    Measurement Model
    z = Hx + v
    z - the measurements at time k
    H - a function predicting the measurement
    v - measurement noise where v approx = N(0, Q)
    Q - the variance of v
    """

    def __init__(self,
                 x0: np.ndarray,
                 P0: np.ndarray,
                 A: np.ndarray,
                 B: np.ndarray or None,
                 H: np.ndarray,
                 R: np.ndarray,
                 Q: np.ndarray):
        """
        :param x0:  initial state vector
        :param P0:  initial covariance matrix
        :param A:   matrix that updates the next state from the previous state (AKA F)
        :param B:   matrix that adjusts the next state by the control inputs u
        :param H:   matrix that converts the current state into an expected measurement
        :param R:   measurement noise matrix
        :param Q:   process noise matrix
        """
        # Key dimensions
        self.n = np.shape(x0)[0]    # number of dimensions in state vector
        self.m = np.shape(R)[1]     # number of sensor inputs

        # Control inputs are optional
        self.B = None
        self.l = 0                  # number of control inputs
        if B is not None:
            self.l = np.shape(B)[1]
            self.B = np.array(B)
            self.assert_shape(self.B, 'B', self.n, self.l)

        self.x = np.array(x0)
        self.assert_shape(self.x, 'x', self.n, 1)
        self.P = np.array(P0)
        self.assert_shape(self.P, 'P', self.n, self.n)
        self.A = np.array(A)
        self.assert_shape(self.A, 'A', self.n, self.n)
        self.H = np.array(H)
        self.assert_shape(self.H, 'H', self.m, self.n)
        self.R = np.array(R)
        self.assert_shape(self.R, 'R', self.m, self.m)
        self.Q = np.array(Q)
        self.assert_shape(self.Q, 'Q', self.n, self.n)

    def step(self, z: np.ndarray, u: np.ndarray = None) -> np.ndarray:
        """
        Updates the filter from the supplied measurement and control inputs.
        Before calling this method, you should update self.A with the time
        since the last call to step unless the time interval is fixed.
        You should adjust the observation matrix, self.H, unless the same
        number of observations are present in every call.
        You should adjust the control matrix, self.B, unless the same number
        of control inputs are present in every call.
        :param z: The measured state of the system
        :param u: Control input. None if the control input is unavailable
        :return: The new state (x)
        """
        self.assert_shape(z, 'z', self.m, 1)
        if self.B is not None:
            self.assert_shape(u, 'u', self.l, 1)

        # Predict phase
        if self.B is not None:
            self.x = (self.A @ self.x) + (self.B @ u)
        else:
            self.x = self.A @ self.x
        self.P = (self.A @ self.P @ self.A.T) + self.Q

        # Update phase
        HT = self.H.T
        S = self.H @ self.P @ HT + self.R
        self.assert_shape(S, 'S', self.m, self.m)
        K = self.P @ HT @ lin.inv(S)
        self.assert_shape(K, 'K', self.n, self.m)
        v = z - (self.H @ self.x)
        self.assert_shape(v, 'v', self.m, 1)
        self.x = self.x + (K @ v)
        self.assert_shape(self.x, 'x', self.n, 1)
        self.P = self.P - ((K @ S) @ K.T)
        self.assert_shape(self.P, 'P', self.n, self.n)

        return self.x

    @staticmethod
    def assert_shape(matrix: np.ndarray, name: str, expected_rows: int, expected_columns: int):
        shape = np.shape(matrix)
        if len(shape) != 2:
            raise Exception('{} matrix should have 2 dimensions but got {}'.format(name, len(shape)))
        if (expected_rows is not None) and (shape[0] != expected_rows):
            raise Exception('{} matrix should have {} rows but got {}'.format(name, expected_rows, shape[0]))
        if (expected_columns is not None) and (shape[1] != expected_columns):
            raise Exception('{} matrix should have {} columns but got {}'.format(name, expected_columns, shape[1]))
