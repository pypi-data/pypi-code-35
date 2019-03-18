#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: quetran
"""
import collections
import logging
from functools import partial
from multiprocessing import Pool, cpu_count

import numpy as np
from cognite_ml.timeseries.pattern_search import auxiliary as aux
from cognite_ml.timeseries.pattern_search.auxiliary import find_variance_thresholds_multivariate
from cognite_ml.timeseries.pattern_search.pattern_search_base import PatternSearchBase

from . import pydtw
from .pydtw import DTWModel


logger = logging.getLogger(__name__)


class DTW(PatternSearchBase):
    def __init__(self, min_range, max_range, limit):

        PatternSearchBase.__init__(self, min_range, max_range, limit)
        # forcing to use global constraint
        self.sakoeChibaWidth = 0.1

    def _lb_to_dtw_distance(self, dict, matches, timestamp_list, query_array, input_array):
        ts_indices = aux.convert_index(
            dict["stride"], word_indices=np.arange(int(len(self.input_ts) / dict["stride"]) + 1)
        )
        start_pattern = int(timestamp_list[ts_indices[dict["i"]]])
        end_pattern = int(timestamp_list[ts_indices[dict["i"]] + dict["len"] - 1])
        if not self.overlap_th or not self._is_overlapping(matches, start_pattern, end_pattern):
            seq2 = input_array[dict["window"]]
            dtw_distance = DTWModel.distance_static(query_array, seq2, self.sakoeChibaWidth)
            return {"from": start_pattern, "to": end_pattern, "score": dtw_distance}
        return {"from": start_pattern, "to": end_pattern, "score": np.inf}

    def search(self, input_timeseries, pattern_timeseries, timeout=None):
        input_ts_cols = sorted(input_timeseries.columns.values)
        query_seqs_cols = sorted(pattern_timeseries.columns.values)

        if input_ts_cols != query_seqs_cols:
            raise ("Input data and query data must have the same column names.")

        if ("timestamp" not in input_ts_cols) or (collections.Counter(input_ts_cols)["timestamp"] != 1):
            raise ("Data must have one Timestamp column.")

        input_ts_cols.remove("timestamp")
        query_seqs_cols.remove("timestamp")

        PatternSearchBase.search_init(self, input_timeseries, pattern_timeseries, timeout)

        lower_bounds = self.find_similar_periods(
            self.query_seq[query_seqs_cols].values, self.input_ts[input_ts_cols].values
        )
        sorted_lower_bounds = sorted(lower_bounds, key=lambda dict: dict["distance"])  # sort by score

        timestamp_list = self.input_ts.reset_index()["timestamp"]
        matches = []
        dtw_scores = []

        query_array = self.query_seq[query_seqs_cols].values
        input_array = self.input_ts[input_ts_cols].values

        slices = [s for s in range(0, len(sorted_lower_bounds), 3000)]
        slices.append(len(sorted_lower_bounds))

        for i in range(len(slices) - 1):
            num_cpu = cpu_count()
            with Pool(processes=num_cpu) as p:
                results = p.map_async(
                    partial(
                        self._lb_to_dtw_distance,
                        matches=matches,
                        timestamp_list=timestamp_list,
                        query_array=query_array,
                        input_array=input_array,
                    ),
                    sorted_lower_bounds[slices[i] : slices[i + 1]],
                ).get(timeout=self.timeout)
            dtw_scores.extend(results)

            dtw_scores = sorted(dtw_scores, key=lambda k: k["score"])
            min_dtw_distance = dtw_scores[0]["score"]
            if i < len(slices) - 2:
                while min_dtw_distance < sorted_lower_bounds[slices[i + 1]]["distance"]:
                    candidate_match = dtw_scores.pop(0)
                    if not self.overlap_th or not self._is_overlapping(
                        matches, candidate_match["from"], candidate_match["to"]
                    ):
                        logger.info(candidate_match)
                        matches.append(candidate_match)
                    if len(matches) == self.limit:
                        matches = aux.convert_scores_to_percentages(matches, self.max_length)
                        return matches
                    min_dtw_distance = dtw_scores[0]["score"] if dtw_scores else np.inf

        while len(matches) < self.limit:
            if len(dtw_scores) > 0:
                candidate_match = dtw_scores.pop(0)
                if not self.overlap_th or not self._is_overlapping(
                    matches, candidate_match["from"], candidate_match["to"]
                ):
                    matches.append(candidate_match)
                if len(matches) == self.limit:
                    matches = aux.convert_scores_to_percentages(matches, self.max_length)
                    return matches
            else:
                matches = aux.convert_scores_to_percentages(matches, self.max_length)
                return matches

    def _is_overlapping(self, matches, start_candidate_pattern, end_candidate_pattern):
        for match in matches:
            if (
                aux.calculate_overlap(match["from"], match["to"], start_candidate_pattern, end_candidate_pattern)
                > self.overlap_th
            ):
                return True
        return False

    def find_similar_patterns(self, search_len, expected_seq, timeseries):
        stride = int(search_len / 20) + 1
        dtw_model = DTWModel(search_len, stride, len(expected_seq), self.sakoeChibaWidth)
        windows = list(dtw_model.sliding_window_index(len(timeseries)))
        variance_thresholds = find_variance_thresholds_multivariate(expected_seq)
        distances = []
        new_expected_seq = pydtw.whiten_multivariate(expected_seq).transpose()
        envelope = []
        l = len(new_expected_seq)
        for i in range(l):
            envelope.append(
                dtw_model.make_envelope_keogh(
                    new_expected_seq[i], search_len, max(1, self.sakoeChibaWidth * max(len(expected_seq), search_len))
                )
            )
        envelope = np.array(envelope)
        for i in range(len(windows)):
            if not self.filterVariance or pydtw.is_variance_ok(timeseries[windows[i]], variance_thresholds):
                distances.append(
                    {
                        "distance": dtw_model.lb_keogh_dist(expected_seq, timeseries[windows[i]], envelope),
                        "stride": stride,
                        "len": search_len,
                        "i": i,
                        "window": windows[i],
                    }
                )
        return distances
