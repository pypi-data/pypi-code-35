#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: quetran
"""
import unittest

import numpy as np
import pandas as pd
from cognite_ml.timeseries.pattern_search.algorithms.DTW.searcher import DTW


class DTWSearcherTestCase(unittest.TestCase):
    def test_find_similar_patterns(self):
        search_len = 3
        expected_seq = pd.DataFrame([[2, 2], [2, 2], [4, 3], [4, 3], [4, 4], [4, 4]], dtype=np.float64)
        pattern = pd.DataFrame([[2, 2], [4, 3], [4, 4]], dtype=np.float64)
        timeseries = pd.concat([pattern, pattern * 100])

        searcher = DTW(min_range=None, max_range=None, limit=5)

        res = searcher.find_similar_patterns(search_len, expected_seq.values, timeseries.values)
        self.assertEqual(searcher.limit, 5)
        self.assertEqual(searcher.sakoeChibaWidth, 0.1)

        top = sorted(res, key=lambda dict: dict["distance"])[0:2]
        for item in top:
            item["distance"] = round(item["distance"], 3)
        expected_res = [{"distance": 0.0, "stride": 1, "len": 3, "i": 0, "window": slice(0, 3, None)}]
        self.assertCountEqual(top, expected_res)

    def test_search(self):
        timestamp = pd.DataFrame((np.linspace(1000, 6000, 6)).astype(int), columns=["timestamp"])
        expected_seq = pd.DataFrame(
            [[2, 2], [2, 2], [4, 3], [4, 3], [4, 4], [4, 4]], columns=["a", "b"], dtype=np.float64
        ).reset_index(drop=True)
        expected_seq = expected_seq.join(timestamp)
        pattern = pd.DataFrame([[2, 2], [4, 3], [4, 4]], columns=["a", "b"], dtype=np.float64)
        timeseries = pd.concat([pattern, pattern * 100]).reset_index(drop=True)
        timeseries = timeseries.join(timestamp)

        searcher = DTW(min_range="2s", max_range=None, limit=2)
        searcher.filterVariance = False

        matches = searcher.search(timeseries, expected_seq, None)
        for m in matches:
            m["score"] = round(m["score"], 3)

        expected_res = [
            {"from": 1000, "to": 3000, "score": 0.0, "percentage": 100.0},
            {"from": 4000, "to": 6000, "score": 0.0, "percentage": 100.0},
        ]
        self.assertCountEqual(expected_res, matches)

    def test_is_overlapping(self):
        searcher = DTW(min_range=None, max_range=None, limit=5)
        searcher.overlap_th = 0.7
        matches = [{"from": 0, "to": 5, "score": 0}, {"from": 8, "to": 10, "score": 0}]
        self.assertFalse(searcher._is_overlapping(matches, 6, 7))
        self.assertTrue(searcher._is_overlapping(matches, 8, 9))
        self.assertFalse(searcher._is_overlapping(matches, 5, 6))  # 50% overlap should be accepted as not overlapping

    def test_lb_to_dtw_distance(self):
        timestamp = pd.DataFrame((np.linspace(1000, 6000, 6)).astype(int), columns=["timestamp"])
        expected_seq = pd.DataFrame(
            [[2, 2], [2, 2], [4, 3], [4, 3], [4, 4], [4, 4]], columns=["a", "b"], dtype=np.float64
        ).reset_index(drop=True)
        expected_seq = expected_seq.join(timestamp)
        pattern = pd.DataFrame([[2, 2], [4, 3], [4, 4]], columns=["a", "b"], dtype=np.float64)
        timeseries = pd.concat([pattern, pattern * 100]).reset_index(drop=True)
        timeseries = timeseries.join(timestamp)

        searcher = DTW(min_range=None, max_range=None, limit=2)
        searcher.input_ts = timeseries
        searcher.query_seq = expected_seq
        input_ts_cols = ["a", "b"]
        query_seqs_cols = ["a", "b"]
        timestamp = timestamp.reset_index()["timestamp"]

        matches = [{"from": 1000, "to": 6000, "score": 0}]
        dict = {"distance": 3, "stride": 1, "len": 4, "i": 0, "window": slice(0, 4, None)}

        op = searcher._lb_to_dtw_distance(
            dict,
            matches,
            timestamp,
            expected_seq[query_seqs_cols].values,
            timeseries[input_ts_cols].values
        )

        self.assertEqual(op, {"from": 1000, "to": 4000, "score": np.inf})  # Distance should be inf when overlap
        matches = [{"from": 5000, "to": 6000, "score": 0}]

        op = searcher._lb_to_dtw_distance(
            dict,
            matches,
            timestamp,
            expected_seq[query_seqs_cols].values,
            timeseries[input_ts_cols].values
        )

        self.assertCountEqual(op, {"from": 1000, "to": 4000, "score": None})
        self.assertGreaterEqual(op["score"], 0)
        self.assertNotEqual(op["score"], np.inf)  # Distance should not be inf when no overlap
