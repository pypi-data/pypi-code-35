#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: quetran
"""
from unittest import TestCase

import pandas as pd
from cognite_ml.timeseries.pattern_search import \
    pattern_search_base as searcher
from parameterized import parameterized


class SimilaritySearchBaseTestCase(TestCase):
    def test_search_init(self):
        input_df = pd.DataFrame(
            [[None, 1532432275000, 3, 4], [2, 1532432285000, 3, 4]], columns=["a", "timestamp", "b", "c"]
        )
        query_df = pd.DataFrame(
            [[None, 1532432275000, 3, 4], [None, 1532432285000, 3, 4]], columns=["a", "timestamp", "b", "c"]
        )
        s = searcher.PatternSearchBase(min_range=None, max_range=None, limit=2)
        s.search_init(input_df, query_df)
        self.assertFalse(s.input_ts.isna().any().any())
        self.assertFalse(s.query_seq.isna().any().any())
        self.assertEqual(s.granularity_second, 10)

    def test_find_similar_periods(self):
        # Test invalid min/max range
        s = searcher.PatternSearchBase(min_range="10h", max_range="1h", limit=2)
        s.granularity_second = 30 * 60
        self.assertRaises(ValueError, s.find_similar_periods, None, None)

    #
    def test_combine_score_value_error(self):
        s = searcher.PatternSearchBase(min_range=None, max_range=None, limit=2)
        # Test bad result
        score1 = [{"distance": 1, "stride": 3, "len": 5, "i": 7}]
        score2 = [{"distance": 2, "stride": 5, "len": 5, "i": 7}]
        self.assertRaises(ValueError, s.combine_scores, score1, score2)

    combine_score_test_cases = [
        (
            [{"distance": 1, "stride": 3, "len": 5, "i": 9}, {"distance": 2, "stride": 4, "len": 7, "i": 7}],
            [{"distance": 3, "stride": 4, "len": 7, "i": 7}],
            [{"distance": 5, "stride": 4, "len": 7, "i": 7}],
        ),
        (
            [
                {"distance": 1, "stride": 3, "len": 5, "i": 9},
                {"distance": 2, "stride": 4, "len": 7, "i": 7},
                {"distance": 2, "stride": 4, "len": 7, "i": 8},
                {"distance": 1, "stride": 4, "len": 8, "i": 8},
            ],
            [
                {"distance": 1, "stride": 3, "len": 3, "i": 9},
                {"distance": 2, "stride": 4, "len": 7, "i": 5},
                {"distance": 3, "stride": 4, "len": 7, "i": 8},
                {"distance": 2, "stride": 4, "len": 8, "i": 8},
            ],
            [{"distance": 5, "stride": 4, "len": 7, "i": 8}, {"distance": 3, "stride": 4, "len": 8, "i": 8}],
        ),
    ]

    @parameterized.expand(combine_score_test_cases)
    def test_combine_score(self, score1, score2, expected_result):
        s = searcher.PatternSearchBase(min_range=None, max_range=None, limit=2)
        result = s.combine_scores(score1, score2)
        self.assertCountEqual(result, expected_result)
