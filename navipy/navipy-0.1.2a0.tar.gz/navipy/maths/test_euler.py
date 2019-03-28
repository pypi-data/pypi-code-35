import numpy as np
from navipy.maths import euler
from navipy.maths.constants import _AXES2TUPLE
import unittest
from navipy.maths.euler import angle_rate_matrix
from navipy.maths.euler import matrix
from navipy.maths.euler import R1, R2, R3


c = np.cos
s = np.sin


class TestEuler(unittest.TestCase):
    # def test_identity(self):
    #    for key in list(_AXES2TUPLE.keys()):
    #        angles = np.zeros(3)
    #        rotation_0 = euler.matrix(angles[0],
    #                                  angles[1],
    #                                  angles[2], key)[:3, :3]
    #        [ai, aj, ak] = euler.from_matrix(rotation_0, key)
    #        np.testing.assert_allclose(angles, np.array([ai, aj, ak]))
    # NOT WORKING DUE TO NUMERICAL APPROX...
    def test_forwardreverse(self):
        """
        tests if the matrix and from_matrix (decompose) function
        from the euler angles works correctly.
        - take some angles
        - build matrix from angles (euler.matrix)
        - decompose obtained matrix to angles (euler.from_matrix)
        - use obtained angles to build euler matrix (euler.matrix)
        - compare old and new euler matrix
        """
        for key in list(_AXES2TUPLE.keys()):
            angles = np.pi * (np.random.rand(3) - 0.5)
            angles[0] *= 2
            angles[2] *= 2
            if np.unique(list(key)).shape[0] < len(list(key)):
                # Repeting axis
                angles[1] += np.pi / 2
            # angles *= 0
            rotation_0 = euler.matrix(angles[0],
                                      angles[1],
                                      angles[2], key)[:3, :3]
            [ai, aj, ak] = euler.from_matrix(rotation_0, key)
            np.testing.assert_allclose(angles, np.array([ai, aj, ak]))

    def test_betweenconvention_new(self):
        """
        Test orientation from one convention to another
        """
        refkey = 'xyz'
        for key in list(_AXES2TUPLE.keys()):
            rotation_0 = euler.matrix(1, 2, 3, refkey)[:3, :3]
            [ai, aj, ak] = euler.from_matrix(rotation_0, key)
            rotation_1 = euler.matrix(ai, aj, ak, key)[:3, :3]
            np.testing.assert_allclose(rotation_0,
                                       rotation_1)

    def test_from_quaternion(self):
        angles = euler.from_quaternion([0.99810947, 0.06146124, 0, 0])
        np.testing.assert_allclose(angles, [0.123, 0, 0])  # 0.123

    def test_from_quaternion_params(self):
        """
        test if errors are raised correctly when parameters of wrong
        type etc are passed to the euler.from_quaternion function
        """
        for a, b, c, d in [(None, 2, 6, 'xyz'), (9.0, 'w', 2, 'xyz'),
                           (5.0, 4.0, None, 'xyz'),
                           (1.0, 2.0, 3.0, 'w')]:
            with self.assertRaises(ValueError):
                euler.from_quaternion([a, b, c, d])
        for c, d in [(3.0,2),([5, 6.0]),([4.0, 2]),(4, 3)]:
            with self.assertRaises(TypeError):
                euler.from_quaternion(c, d)

        with self.assertRaises(Exception):
            euler.from_quaternion([9.0, 8.0, 7.0, 0.3], 'w')

    def test_from_matrix_params(self):
        """
        test if errors are raised correctly if parameters
        of wrong type, value are passed to the euler.from_matrix
        function
        """
        for a, b, c, d in [(None, 2, 6, 'xyz'), (9.0, 'w', 2, 'xyz'),
                           (5.0, 4.0, None, 'xyz'),
                           (1.0, 2.0, 3.0, 'w')]:
            with self.assertRaises(ValueError):
                euler.from_matrix([a, b, c, d])
        for c, d in [(3.0,2),([5, 6.0]),([4.0, 2]),(4, 3)]:
            with self.assertRaises(TypeError):
                euler.from_matrix(c, d)

        with self.assertRaises(Exception):
            euler.from_matrix([9.0, 8],  'w')

    def test_angle_rate_matrix_params(self):
        """
        test if errors are raised correctly if parameters
        of wrong type, value are passed to the
        euler.angle_rate_matrix function
        """
        for a, b, c, d in [(None, None, 6, 'xyz'),
                           (5.0, None, 6, 'xyz'),
                           (5.0, 4.0, None, 'xyx')]:
            with self.assertRaises(TypeError):
                euler.angle_rate_matrix(a, b, c, d)

        # for a, b, c, d in [(9.0, np.nan, 2, 'xyz')]:
        #    with self.assertRaises(ValueError):
        #        euler.angle_rate_matrix(a, b, c, d)

        with self.assertRaises(Exception):
            euler.angle_rate_matrix(9.0, 8.0, 7.0, 'w')

    def test_angular_velocity(self):
        """
        test if errors are raised correctly if parameters
        of wrong type, value are passed to the
        euler.angle_rate_matrix function
        """
        for a, b, c, d, e, f, g in [(None, 2, 6, 8, 7, 8, 'xyz'),
                                    (9.0, 'er', 2, 3, 3, 5, 'xyz'),
                                    (5.0, 4.0, None, 8.0, 8.0, 4.0, 'xyz'),
                                    (np.nan, 8.0, 7.0, '0', 6.0, None, 'xyz'),
                                    (4.0, 2.0, 1.0, 3.0, 'w', 2.0, 'xyz'),
                                    (1.0, 2.0, 3.0, 4.0, 5, 'ab', 'xyz')]:
            with self.assertRaises(TypeError):
                euler.angular_velocity(a, b, c, d, e, f, g)


        with self.assertRaises(ValueError):
            euler.angular_velocity(5.0, 4.0, 3.0, 8.0, 8.0, 4.0, 'l')

        vel = euler.angular_velocity(2.0,3.0,4.0,5.0,6.0,7.0,'xyz')
        self.assertTrue(np.allclose(vel, [ 7.77632637, -0.17571777,  6.29439996]))

    def test_E313(self):
        """
        example from the attitude paper
        """
        ai = 0.10
        aj = 0.20
        ak = 0.70
        # dai = 0
        # daj = 0
        # dak = 1
        E = angle_rate_matrix(ai, aj, ak, 'zxz')
        testE = [[np.sin(aj) * np.sin(ak), np.cos(ak), 0],
                 [-np.sin(aj) * np.cos(ak), np.sin(ak), 0],
                 [np.cos(aj), 0, 1]]
        self.assertTrue(np.allclose(E, testE))

    def test_velocity_paper_example(self):
        c = np.cos
        s = np.sin
        ai = 0.10
        aj = 0.20
        ak = 0
        dai = 0
        daj = 0
        dak = 0.01
        E = [[np.sin(aj) * np.sin(ak), np.cos(ak), 0],
             [-np.sin(aj) * np.cos(ak), np.sin(ak), 0],
             [np.cos(aj), 0, 1]]
        E_p = [[0, np.cos(ai), np.sin(aj) * np.sin(ai)],
               [0, -np.sin(ai), np.sin(aj) * np.cos(ai)],
               [1, 0, np.cos(aj)]]
        E_fkt = angle_rate_matrix(ai, aj, ak, 'zxz')
        self.assertTrue(np.allclose(E, E_fkt))
        w = np.dot(E, [dai, daj, dak])
        w_p = np.dot(E_p, [dai, daj, dak])
        Rijk = [[c(ai) * c(ak) - s(ai) * c(aj) * s(ak),
                 c(ai) * s(ak) + s(ai) * c(aj) * c(ak),
                 s(ai) * s(aj)],
                [-s(ai) * c(ak) - c(ai) * c(aj) * s(ak),
                 -s(ai) * s(ak) + c(ai) * c(aj) * c(ak),
                 c(ai) * s(aj)],
                [s(aj) * s(ak),
                 -s(aj) * c(ak),
                 c(aj)]]
        Rijk_test = np.dot(R3(ai), np.dot(R1(aj), R3(ak)))
        Rijk_fkt = matrix(ai, aj, ak, 'zxz')[:3, :3]
        self.assertTrue(np.allclose(Rijk, Rijk_fkt))
        self.assertTrue(np.allclose(Rijk, Rijk_test))
        new_w_p = np.dot(Rijk, w)
        self.assertTrue(np.allclose(w_p, new_w_p))

    def test_angle_rate(self):
        ea = 0.1
        eb = 0.15
        ec = 0.7
        # da = 0.2
        # db = 0.3
        # dc = 1

        # xyz
        MR3 = np.transpose(R3(ec))
        MR2 = np.transpose(R2(eb))
        e1 = [1, 0, 0]
        e2 = [0, 1, 0]
        e3 = [0, 0, 1]
        p1 = np.dot(MR3, np.dot(MR2, e1))
        p2 = np.dot(MR3, e2)
        rotM = np.column_stack([p1, p2, e3])
        M = angle_rate_matrix(ea, eb, ec, 'xyz')
        self.assertTrue(np.all(rotM == M))

        # yzx
        MRk = np.transpose(R1(ec))
        MRj = np.transpose(R3(eb))
        e1 = [1, 0, 0]
        e2 = [0, 1, 0]
        e3 = [0, 0, 1]
        p1 = np.dot(MRk, np.dot(MRj, e2))
        p2 = np.dot(MRk, e3)
        rotM = np.column_stack([p1, p2, e1])
        M = angle_rate_matrix(ea, eb, ec, 'yzx')
        self.assertTrue(np.allclose(rotM, M))

        # yxz
        MRk = np.transpose(R3(ec))
        MRj = np.transpose(R1(eb))
        e1 = [1, 0, 0]
        e2 = [0, 1, 0]
        e3 = [0, 0, 1]
        p1 = np.dot(MRk, np.dot(MRj, e2))
        p2 = np.dot(MRk, e1)
        rotM = np.column_stack([p1, p2, e3])
        M = angle_rate_matrix(ea, eb, ec, 'yxz')
        self.assertTrue(np.allclose(rotM, M))

        # xzy
        MRk = np.transpose(R2(ec))
        MRj = np.transpose(R3(eb))
        e1 = [1, 0, 0]
        e2 = [0, 1, 0]
        e3 = [0, 0, 1]
        p1 = np.dot(MRk, np.dot(MRj, e1))
        p2 = np.dot(MRk, e3)
        rotM = np.column_stack([p1, p2, e2])
        M = angle_rate_matrix(ea, eb, ec, 'xzy')
        self.assertTrue(np.allclose(rotM, M))

        # zxy
        MRk = np.transpose(R2(ec))
        MRj = np.transpose(R1(eb))
        e1 = [1, 0, 0]
        e2 = [0, 1, 0]
        e3 = [0, 0, 1]
        p1 = np.dot(MRk, np.dot(MRj, e3))
        p2 = np.dot(MRk, e1)
        rotM = np.column_stack([p1, p2, e2])
        M = angle_rate_matrix(ea, eb, ec, 'zxy')
        self.assertTrue(np.allclose(rotM, M))

        # xzx
        MRk = np.transpose(R1(ec))
        MRj = np.transpose(R3(eb))
        e1 = [1, 0, 0]
        e2 = [0, 1, 0]
        e3 = [0, 0, 1]
        p1 = np.dot(MRk, np.dot(MRj, e1))
        p2 = np.dot(MRk, e3)
        rotM = np.column_stack([p1, p2, e1])
        M = angle_rate_matrix(ea, eb, ec, 'xzx')
        self.assertTrue(np.allclose(rotM, M))

        # zxz
        # c = np.cos
        # s = np.sin
        MRk = np.transpose(R3(ec))
        MRj = np.transpose(R1(eb))
        e1 = [1, 0, 0]
        e2 = [0, 1, 0]
        e3 = [0, 0, 1]
        p1 = np.dot(MRk, np.dot(MRj, e3))
        p2 = np.dot(MRk, e1)
        rotM = np.column_stack([p1, p2, e3])
        # Mpaper = [[c(ea)*c(ec)-s(ea)*c(eb)*s(ec),
        #           c(ea)*s(ec)+s(ea)*c(eb)*c(ec),
        #           s(ea)*s(eb)],
        #          [-s(ea)*c(ec)-c(ea)*c(eb)*s(ec),
        #           -s(ea)*s(ec)+c(ea)*c(eb)*c(ec),
        #           c(ea)*s(eb)],
        #          [s(eb)*s(ec), -s(eb)*c(ec), c(eb)]]
        # mfunc = angle_rate_matrix(ea, eb, ec, 'zxz')
        M = angle_rate_matrix(ea, eb, ec, 'zxz')
        self.assertTrue(np.allclose(rotM, M))

        # xyx
        MRk = np.transpose(R1(ec))
        MRj = np.transpose(R2(eb))
        e1 = [1, 0, 0]
        e2 = [0, 1, 0]
        e3 = [0, 0, 1]
        p1 = np.dot(MRk, np.dot(MRj, e1))
        p2 = np.dot(MRk, e2)
        rotM = np.column_stack([p1, p2, e1])
        M = angle_rate_matrix(ea, eb, ec, 'xyx')
        self.assertTrue(np.allclose(rotM, M))

        # yxy
        MRk = np.transpose(R2(ec))
        MRj = np.transpose(R1(eb))
        e1 = [1, 0, 0]
        e2 = [0, 1, 0]
        e3 = [0, 0, 1]
        p1 = np.dot(MRk, np.dot(MRj, e2))
        p2 = np.dot(MRk, e1)
        rotM = np.column_stack([p1, p2, e2])
        M = angle_rate_matrix(ea, eb, ec, 'yxy')
        self.assertTrue(np.allclose(rotM, M))

        # yzy
        MRk = np.transpose(R2(ec))
        MRj = np.transpose(R3(eb))
        e1 = [1, 0, 0]
        e2 = [0, 1, 0]
        e3 = [0, 0, 1]
        p1 = np.dot(MRk, np.dot(MRj, e2))
        p2 = np.dot(MRk, e3)
        rotM = np.column_stack([p1, p2, e2])
        M = angle_rate_matrix(ea, eb, ec, 'yzy')
        self.assertTrue(np.allclose(rotM, M))

        # zyz
        MRk = np.transpose(R3(ec))
        MRj = np.transpose(R2(eb))
        e1 = [1, 0, 0]
        e2 = [0, 1, 0]
        e3 = [0, 0, 1]
        p1 = np.dot(MRk, np.dot(MRj, e3))
        p2 = np.dot(MRk, e2)
        rotM = np.column_stack([p1, p2, e3])
        M = angle_rate_matrix(ea, eb, ec, 'zyz')
        self.assertTrue(np.allclose(rotM, M))

    def test_R1(self):
        for a in [(None), ('w'), ([3,5,2])]:
            with self.assertRaises(TypeError):
                euler.R1(a)

    def test_R2(self):
        for a in [(None), ('q'), ([2, 4,8])]:
            with self.assertRaises(TypeError):
                euler.R2(a)

    def test_R3(self):
        for a in [(None), ('er')]:
            with self.assertRaises(TypeError):
                euler.R3(a)

    def test_matrix(self):
        with self.assertRaises(Exception):
            euler.matrix(9.0, 8.0, 7.0, 'w')


if __name__ == '__main__':
    unittest.main()
