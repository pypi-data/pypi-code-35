#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: quetran
"""
import unittest

import numpy as np
import pandas as pd
from cognite_ml.timeseries.pattern_search.algorithms.DTW.pydtw import (DTWModel,
                                                                       is_variance_ok,
                                                                       whiten_multivariate)


class DTWTestCase(unittest.TestCase):
    def test_is_variance_ok(self):
        sequence = pd.DataFrame([[2, 2, 3], [2, 3, 5], [2, 4, 7], [2, 5, 9]], dtype=np.float64)
        # Good variance
        variance_thresholds = {"lower": [0] * 4, "upper": [10] * 4}
        lol = sequence.values
        self.assertTrue(is_variance_ok(sequence.values, variance_thresholds))
        # Bad variance
        variance_thresholds = {"lower": [0] * 4, "upper": [4] * 4}
        self.assertFalse(is_variance_ok(sequence.values, variance_thresholds))

    def test_whiten_multivariate(self):
        window_signal = np.array([[1, 2, 3], [1, 2, 5]], dtype=np.float64)
        expected_result = np.array([[0, 0, -1], [0, 0, 1]], dtype=np.float64)
        print(np.round(whiten_multivariate(window_signal), 2))
        self.assertTrue(np.array_equal(np.round(whiten_multivariate(window_signal), 2), expected_result))

    def test_distance_static(self):
        # TODO: write test
        pass

    def test_lb_keogh_dist(self):
        # TODO: write test
        pass

    def test_make_envelope_keogh(self):
        seq = [0, 1, 2]
        sz2 = 7
        radius = 1
        expected_res = [(1, 0), (1, 0), (1, 0), (2, 0), (2, 1), (2, 1), (2, 1)]
        dtw = DTWModel(3, 1, 7, 0.1)
        result = dtw.make_envelope_keogh(seq, sz2, radius)
        self.assertEqual(expected_res, result)

    def test_make_envelope_index_keogh(self):
        sz1 = 7
        sz2 = 3
        radius = 1
        expected_res = [(0, 2), (0, 2), (0, 2), (0, 3), (1, 3), (1, 3), (1, 4)]
        result = DTWModel.make_envelope_index_keogh(sz1, sz2, radius)
        self.assertEqual(expected_res, result)
