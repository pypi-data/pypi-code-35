import unittest
import numpy as np
from navipy.maths import homogeneous_transformations as ht
from navipy.maths import random
from navipy.maths import euler


class TestHT(unittest.TestCase):
    def test_translation_matrix(self):
        vector = np.random.random(3)
        vector -= 0.5
        vector_test = ht.translation_matrix(vector)[:3, 3]
        self.assertTrue(np.allclose(vector,
                                    vector_test))

    def test_translation_from_matrix(self):
        vector = np.random.random(3)
        vector -= 0.5
        matrix = ht.translation_matrix(vector)
        vector_test = ht.translation_from_matrix(matrix)
        self.assertTrue(np.allclose(vector,
                                    vector_test))

    def test_reflection_matrix(self):
        vector_0 = np.random.random(4)
        vector_0 -= 0.5
        vector_0[3] = 1.
        vector_1 = np.random.random(3)
        vector_1 -= 0.5
        reflection = ht.reflection_matrix(vector_0,
                                          vector_1)
        vector_2 = vector_0.copy()
        vector_2[:3] += vector_1
        vector_3 = vector_0.copy()
        vector_3[:3] -= vector_1
        condition_0 = np.allclose(2, np.trace(reflection))
        condition_1 = np.allclose(vector_0,
                                  np.dot(reflection, vector_0))
        condition_2 = np.allclose(vector_2, np.dot(reflection,
                                                   vector_3))
        condition = condition_0 & condition_1 & condition_2
        self.assertTrue(condition)

    def test_reflection_from_matrix(self):
        vector_0 = np.random.random(3) - 0.5
        vector_1 = np.random.random(3) - 0.5
        matrix_0 = ht.reflection_matrix(vector_0, vector_1)
        point, normal = ht.reflection_from_matrix(matrix_0)
        matrix_1 = ht.reflection_matrix(point, normal)
        condition = ht.is_same_transform(matrix_0, matrix_1)
        self.assertTrue(condition)


    def test_scale(self):
        vector = (np.random.rand(4, 5) - 0.5) * 20
        vector[3] = 1
        factor = -1.234
        scale = ht.scale_matrix(factor)
        condition = np.allclose(np.dot(scale, vector)[:3],
                                factor * vector[:3])
        self.assertTrue(condition)

    def test_scale_sametransform(self):
        factor = np.random.random() * 10 - 5
        origin = np.random.random(3) - 0.5
        scale_0 = ht.scale_matrix(factor, origin)
        factor, origin, direction = ht.scale_from_matrix(scale_0)
        scale_1 = ht.scale_matrix(factor, origin, direction)
        self.assertTrue(ht.is_same_transform(scale_0, scale_1))

    def test_scale_from_matrix(self):
        factor = np.random.random() * 10 - 5
        origin = np.random.random(3) - 0.5
        direct = np.random.random(3) - 0.5
        scale_0 = ht.scale_matrix(factor, origin, direct)
        factor, origin, direction = ht.scale_from_matrix(scale_0)
        scale_1 = ht.scale_matrix(factor, origin, direction)
        self.assertTrue(ht.is_same_transform(scale_0, scale_1))

    def test_projection_matrix_example(self):
        projection = ht.projection_matrix([0, 0, 0], [1, 0, 0])
        self.assertTrue(np.allclose(projection[1:, 1:],
                                    np.identity(4)[1:, 1:]))

    def test_projection_matrix(self):
        point = np.random.random(3) - 0.5
        normal = np.random.random(3) - 0.5
        persp = np.random.random(3) - 0.5
        projection_0 = ht.projection_matrix(point, normal)
        projection_2 = ht.projection_matrix(point, normal,
                                            perspective=persp)
        projection_3 = ht.projection_matrix(point, normal,
                                            perspective=persp,
                                            pseudo=True)
        self.assertTrue(ht.is_same_transform(projection_2,
                                             np.dot(projection_0,
                                                    projection_3)))

    def test_projection_from_matrix(self):
        point = np.random.random(3) - 0.5
        normal = np.random.random(3) - 0.5
        projection_0 = ht.projection_matrix(point, normal)
        result = ht.projection_from_matrix(projection_0)
        projection_1 = ht.projection_matrix(*result)
        self.assertTrue(ht.is_same_transform(projection_0,
                                             projection_1))

    def test_projection_from_matrix_direct(self):
        point = np.random.random(3) - 0.5
        normal = np.random.random(3) - 0.5
        direct = np.random.random(3) - 0.5
        projection_0 = ht.projection_matrix(point, normal, direct)
        result = ht.projection_from_matrix(projection_0)
        projection_1 = ht.projection_matrix(*result)
        self.assertTrue(ht.is_same_transform(projection_0,
                                             projection_1))

    def test_projection_from_matrix_persp_pseudo_false(self):
        point = np.random.random(3) - 0.5
        normal = np.random.random(3) - 0.5
        persp = np.random.random(3) - 0.5
        projection_0 = ht.projection_matrix(point, normal, persp,
                                            pseudo=False)
        result = ht.projection_from_matrix(projection_0)
        projection_1 = ht.projection_matrix(*result)
        self.assertTrue(ht.is_same_transform(projection_0,
                                             projection_1))

    def test_projection_from_matrix_persp_pseudo_true(self):
        point = np.random.random(3) - 0.5
        normal = np.random.random(3) - 0.5
        persp = np.random.random(3) - 0.5
        projection_0 = ht.projection_matrix(point, normal, persp,
                                            pseudo=True)
        result = ht.projection_from_matrix(projection_0)
        projection_1 = ht.projection_matrix(*result)
        self.assertTrue(ht.is_same_transform(projection_0,
                                             projection_1))

    def test_shear_matrix(self):
        angle = (np.random.random() - 0.5) * 4 * np.pi
        point = np.random.random(3) - 0.5
        direct, normal = random.orthogonal_vectors()
        scale = ht.shear_matrix(angle, direct, point, normal)
        self.assertTrue(np.allclose(1, np.linalg.det(scale)))

    # Not Working due to unorthogonality of direct and normal
    # from time to time....
    # def test_shear_from_matrix(self):
    #    angle = (np.random.random() - 0.5) * 4 * np.pi
    #    direct, normal = random.orthogonal_vectors()
    #    point = np.random.random(3) - 0.5
    #    scale_0 = ht.shear_matrix(angle, direct, point, normal)
    #    result = ht.shear_from_matrix(scale_0)
    #    scale_1 = ht.shear_matrix(*result)
    #    self.assertTrue(ht.is_same_transform(scale_0, scale_1))

    def test_decompose_matrix_translation(self):
        translation_0 = ht.translation_matrix([1, 2, 3])
        scale, shear, angles, trans, persp = ht.decompose_matrix(translation_0)
        translation_1 = ht.translation_matrix(trans)
        self.assertTrue(np.allclose(translation_0, translation_1))

    def test_decompose_matrix_scale(self):
        factor = np.random.random()
        scale = ht.scale_matrix(factor)
        scale, shear, angles, trans, persp = ht.decompose_matrix(scale)
        self.assertEqual(scale[0], factor)

    def test_decompose_matrix_rotation(self):
        rotation_0 = euler.matrix(1, 2, 3, 'xyz')
        _, _, angles, _, _ = ht.decompose_matrix(rotation_0)
        rotation_1 = euler.matrix(*angles, 'xyz')
        self.assertTrue(np.allclose(rotation_0, rotation_1))

    def test_compose_matrix(self):
        scale = np.random.random(3) - 0.5
        shear = np.random.random(3) - 0.5
        angles = (np.random.random(3) - 0.5) * (2 * np.pi)
        trans = np.random.random(3) - 0.5
        persp = np.random.random(4) - 0.5
        matrix_0 = ht.compose_matrix(scale, shear, angles, trans, persp)
        result = ht.decompose_matrix(matrix_0)
        matrix_1 = ht.compose_matrix(*result)
        self.assertTrue(ht.is_same_transform(matrix_0, matrix_1))

    def test_is_same_transform(self):
        matrix = np.random.rand(4, 4)
        self.assertTrue(ht.is_same_transform(matrix, matrix))

    def test_is_same_transform_rejection(self):
        # The determinant of a rotation matrix is one,
        # Thus we test rejection rotation against scaled identity
        matrix = 2 * np.identity(4)
        rotation = random.rotation_matrix()
        self.assertFalse(ht.is_same_transform(matrix, rotation))

    def test_compose_decompose(self):
        angles_o = [0.123, -1.234, 2.345]
        scale_o = np.random.rand(3)
        translation_o = [1, 2, 3]
        shear_o = [0, np.tan(angles_o[1]), 0]
        axes = 'xyz'
        matrix = ht.compose_matrix(scale_o, shear_o, angles_o,
                                   translation_o, axes=axes)
        scale, shear, angles, trans, persp = ht.decompose_matrix(matrix, axes)
        np.testing.assert_almost_equal(scale, scale_o)
        np.testing.assert_almost_equal(shear, shear_o)
        np.testing.assert_almost_equal(angles, angles_o)
        np.testing.assert_almost_equal(trans, translation_o)

        matrix_1 = ht.compose_matrix(scale, shear, angles,
                                     trans, persp, axes)
        self.assertTrue(ht.is_same_transform(matrix, matrix_1))


if __name__ == '__main__':
    unittest.main()
