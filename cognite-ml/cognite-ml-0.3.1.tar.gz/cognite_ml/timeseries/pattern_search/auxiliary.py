#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: quetran
"""

import math
from functools import reduce

import numpy as np
import pandas as pd


def fill_nan(dataframe, default_value=0.0):
    dataframe.fillna(method="ffill", inplace=True)
    dataframe.fillna(method="bfill", inplace=True)
    dataframe.fillna(value=default_value, inplace=True)
    return dataframe


def convert_time_delta_to_num_points(granularity, time_delta):
    try:
        time_in_second = pd.to_timedelta(time_delta).total_seconds()
        time_in_datapoints = int(time_in_second / granularity) + 1
        return time_in_datapoints
    except Exception as e:
        raise e


def convert_index(stride, word_indices: np.ndarray = None, ts_indices: np.ndarray = None):
    """
    if word_index is not None, convert word (sliding window) index to time series index
    otherwise convert ts_index to word_index
    """
    if word_indices is not None:
        return word_indices * stride
    elif ts_indices is not None:
        return ts_indices / stride
    else:
        raise ValueError("either word_index or ts_index needs to be specified")


def make_index_even(dataframe):
    "Creates time index with evenly spaced intervals. Adds NaN to timestamps with missing values.\n\n    Args:\n        dataframe (pandas.DataFrame):  Input dataframe.\n\n    Returns:\n        pandas.DataFrame: Input dataframe with evenly spaced intervals.\n    "
    timestamps = dataframe.timestamp.values
    start_time = timestamps[0]
    end_time = timestamps[(-1)]
    deltas = np.diff(timestamps, 1)
    delta = reduce((lambda x, y: math.gcd(x, y)), deltas)
    t_new = np.arange(start_time, (end_time + delta), delta)
    new_df = pd.DataFrame(t_new, columns=["timestamp"])
    dataframe.timestamp = dataframe.timestamp.apply(lambda x: np.int64(x))
    new_df.timestamp = new_df.timestamp.apply(lambda x: np.int64(x))
    return new_df.merge(dataframe, on="timestamp", how="outer").sort_values(by="timestamp").reset_index(drop=True)


def whiten_univariate(window_signal):
    """
    Perform whitening on signal window - it should be local to a sliding window
    """
    s = np.asarray(window_signal)
    mu, sd = np.mean(s), np.std(s)
    return (s - mu) / (sd + 1e-10)


def find_variance_thresholds_univariate(expected_seq):
    """
    Find variance thresholds to prune out noise
    """
    var = expected_seq.var()
    return {"lower": 0 if 0.01 * var < 1 else 0.01 * var, "upper": max(100 * var, 1)}


def find_variance_thresholds_multivariate(expected_seq):
    """
    Find variance thresholds to prune out noise
    """
    var = expected_seq.var(0)
    thresholds = {"lower": [], "upper": []}
    for variance in var:
        thresholds["lower"].append(0 if 0.01 * variance < 1 else 0.01 * variance)
        thresholds["upper"].append(max(100 * variance, 1))
    return thresholds


def calculate_overlap(start_old, end_old, start_new, end_new):
    # returns how much of the new pattern is already covered by the old
    if start_new >= start_old and start_new <= end_old:
        ol = min(end_old, end_new) - start_new + 1
    elif end_new > start_old and end_new <= end_old:
        ol = end_new - max(start_old, start_new) + 1
    else:
        ol = max(0, min(end_new, end_old) - max(start_new, start_old) + 1)
    return ol / (end_new - start_new + 1)


def extract_matches(sorted_distances, timestamp_list, overlap_ratio, n_top):
    matches = []

    for dict in sorted_distances:
        ts_indices = convert_index(
            dict["stride"], word_indices=np.arange(int(len(timestamp_list) / dict["stride"]) + 1)
        )
        start_pattern = int(timestamp_list[ts_indices[dict["i"]]])
        end_pattern = int(timestamp_list[ts_indices[dict["i"]] + dict["len"] - 1])
        if overlap_ratio:
            for match in matches:
                if calculate_overlap(match["from"], match["to"], start_pattern, end_pattern) > overlap_ratio:
                    break
            # Only add match if overlap with better matches is less than threshold
            else:
                matches.append({"from": start_pattern, "to": end_pattern, "score": dict["distance"]})

        else:
            matches.append({"from": start_pattern, "to": end_pattern, "score": dict["distance"]})
        if len(matches) == n_top:
            break
    return matches


def convert_scores_to_percentages(matches, max_length):
    distance = max_length * 1  # 1 std away
    for m in matches:
        m["percentage"] = (1 - min(1, round(m["score"] / distance, 2))) * 100

    return matches
