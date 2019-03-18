#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: quetran
"""
import unittest

import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal

from cognite_ml.timeseries.pattern_search import auxiliary
from parameterized import parameterized


class AuxTestCase(unittest.TestCase):
    fill_nan_testcases = [
        # Test ffill
        (pd.DataFrame([[None, 2, 3, 4], [2, 2, 3, 4]]), 0),
        # Test bfill
        (pd.DataFrame([[2, 2, 3, 4], [None, 2, 3, 4]]), 0),
        # Test default values
        (pd.DataFrame([[None, 2, 3, 4], [None, 2, 3, 4]]), 2.0),
    ]

    @parameterized.expand(fill_nan_testcases)
    def test_fill_nan(self, df, default_value):
        expected_output = pd.DataFrame([[2.0, 2, 3, 4], [2.0, 2, 3, 4]])
        result = auxiliary.fill_nan(df, default_value)
        assert_frame_equal(expected_output, result)

    def test_convert_time_delta_to_num_points(self):
        granularity = 10 * 60
        time_delta = "1h"
        assert auxiliary.convert_time_delta_to_num_points(granularity, time_delta) == 7

    def test_convert_index(self):
        stride = 3
        ts_indices = np.array([0, 3, 6, 9, 12])
        word_indices = np.array([0, 1, 2, 3, 4])
        assert np.array_equal(auxiliary.convert_index(stride=stride, word_indices=word_indices), ts_indices)
        assert np.array_equal(auxiliary.convert_index(stride=stride, ts_indices=ts_indices), word_indices)
        self.assertRaises(ValueError, auxiliary.convert_index, stride)

    def mapping_timeseries(self, common_aggregates_input, common_aggregates_query):
        input_timeseries = {
            "timeSeries": [
                {"name": "ts1", "missingDataStrategy": "ffill"},
                {"name": "ts2", "aggregates": ["step"], "missingDataStrategy": "ffill"},
            ],
            "aggregates": common_aggregates_input,
        }

        query_timeseries = {
            "timeSeries": [
                {"name": "ts1", "aggregates": ["cv", "dv"], "missingDataStrategy": "ffill"},
                {"name": "ts2", "aggregates": ["step"], "missingDataStrategy": "ffill"},
            ],
            "aggregates": common_aggregates_query,
        }

        return input_timeseries, query_timeseries

    def test_whiten_univariate(self):
        window_signal = [1, 1, 1, 1, 1]
        self.assertTrue(np.array_equal(auxiliary.whiten_univariate(window_signal), np.array([0, 0, 0, 0, 0])))

    # TODO: Should we add test for find_variance_thresholds?

    calculate_overlap_testcases = [
        # Test not overlap
        (5, 10, 1, 4, 0.0),
        # Test not overlap
        (5, 10, 12, 15, 0.0),
        # Test overlap left side
        (5, 10, 1, 5, 0.2),
        # Test overlap right side
        (5, 10, 8, 13, 0.5),
        # Test new period inside old period
        (5, 10, 6, 9, 1),
        # Test old period inside new period
        (5, 10, 3, 10, 0.75),
    ]

    @parameterized.expand(calculate_overlap_testcases)
    def test_calculate_overlap(self, start_old, end_old, start_new, end_new, expected_result):
        self.assertEqual(auxiliary.calculate_overlap(start_old, end_old, start_new, end_new), expected_result)

    extact_matches_testcases = [
        # Test without overlapping
        (None, [{"from": 3, "to": 7, "score": 1}, {"from": 6, "to": 8, "score": 2}, {"from": 2, "to": 5, "score": 3}]),
        # Test with overlapping
        (0.7, [{"from": 3, "to": 7, "score": 1}, {"from": 6, "to": 8, "score": 2}]),
    ]

    @parameterized.expand(extact_matches_testcases)
    def test_extact_matches(self, overlap_ratio, expected_matches):
        timestamp_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        sorted_distance = [
            {"distance": 1, "stride": 3, "len": 5, "i": 1},
            {"distance": 2, "stride": 1, "len": 3, "i": 6},
            {"distance": 3, "stride": 2, "len": 4, "i": 1},
        ]
        matches = auxiliary.extract_matches(sorted_distance, timestamp_list, overlap_ratio, 3)
        self.assertCountEqual(expected_matches, matches)
