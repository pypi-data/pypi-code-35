"""
METs
=============
Defines methods for estimating METs on a second-by-second input.

Provides 4 different methods for validation purposes
"""

import numpy as np
import settings as const
from math import log
from utils import chunks, get_indices

def cr2_mets_est(i, val, agg_vals, agg_sum):
    slicer = get_indices(i, len(agg_sum))
    slice_val = agg_vals[slicer]
    min_val = np.max(slice_val)
    agg_sum_val = agg_sum[i]
    if min_val <= 0:
        return 0.
    elif agg_sum_val <= const.CR2_AGG_SUM_CUT:
        return 1.
    elif min_val <= const.CR2_MIN_VAL_CUT and min_val > 0. and agg_sum_val > const.CR2_AGG_SUM_CUT:
        return const.CR2_INT_A * (const.CR2_SQUARE_A * agg_sum_val) ** 2
    elif min_val > const.CR2_MIN_VAL_CUT and agg_sum_val > const.CR2_AGG_SUM_CUT:
        return const.CR2_INT_B + (const.CR2_LINEAR_B * log(agg_sum_val)) - (const.CR2_SQUARE_B * (log(agg_sum_val) ** 2)) + (const.CR2_CUBE_B * (log(agg_sum_val) ** 3))
    else:
        return 0.

def c_mets_est(i, val, cvs):
    if val > const.C_VAL_CUT and cvs[i] > 0. and cvs[i] < const.C_CVS_CUT:
        return const.C_INT_A * (const.C_SQUARE_A * val) ** 2
    elif val > const.C_VAL_CUT and cvs[i] == 0. or const.C_CVS_CUT:
        return const.C_INT_B + const.C_LINEAR_B * val - (const.C_SQUARE_B * val ** 2) + (const.C_CUBE_B * val ** 3)
    else:
        return 1.

def cr2_mets(counts, chunk_freq = 10, time_freq = 6):
    """
    Crouter2 second-by-second estimation of METs based on second-by-second vertical counts

    :param counts: Second-by-second vertical counts (numbers)
    :type counts: list
    :return: Second-by-second estimation of METs (floats)
    :rtype: list
    """
    tmp_chunks = list(chunks(counts, chunk_freq))
    agg_vals = np.array([const.INITIAL_AGG * np.std(x) / np.mean(x) if np.mean(x) > 0. else 0. for x in tmp_chunks])
    agg_sum = [np.sum(x) for x in tmp_chunks]
    METs = [cr2_mets_est(i, val, agg_vals, agg_sum) for i, val in enumerate(agg_vals)]
    minute_mets = [np.mean(x) for x in chunks(METs, time_freq)]
    second_mets = []
    length = min(len(counts), chunk_freq * time_freq)
    [second_mets.extend([x] * length) for x in minute_mets]
    return np.array(second_mets)

def c_mets(counts, time_freq = 60):
    """
    Original crouter second-by-second estimation of METs based on second-by-second vertical counts

    :param counts: Second-by-second vertical counts (numbers)
    :type counts: list
    :return: Second-by-second estimation of METs (floats)
    :rtype: list
    """
    cpm = list(chunks(counts, time_freq))
    cvs = [const.INITIAL_AGG * np.std(x) / np.mean(x) if np.mean(x) > 0. else 0. for x in cpm]
    METs = [c_mets_est(i, np.sum(val), cvs) for i, val in enumerate(cpm)]
    second_mets = []
    length = min(len(counts), time_freq)
    [second_mets.extend([x] * length) for x in METs]
    return np.array(second_mets)

def sasaki_mets(counts, time_freq = 60):
    """
    Sasaki second-by-second estimation of METs based on second-by-second vector magnitude counts

    :param counts: Second-by-second vector magnitude counts (numbers)
    :type counts: list
    :return: Second-by-second estimation of METs (floats)
    :rtype: list
    """
    METs = [const.SASAKI_INT + const.SASAKI_LINEAR * np.sum(x) for x in chunks(counts, time_freq)]
    second_mets = []
    length = min(len(counts), time_freq)
    [second_mets.extend([x] * length) for x in METs]
    return np.array(second_mets)

def freedson_mets(counts, time_freq = 60):
    """
    Freedson second-by-second estimation of METs based on second-by-second vertical counts

    :param counts: Second-by-second vertical counts (numbers)
    :type counts: list
    :return: Second-by-second estimation of METs (floats)
    :rtype: list
    """
    METs = [const.FREEDSON_INT + const.FREEDSON_LINEAR * np.sum(x) for x in chunks(counts, time_freq)]
    second_mets = []
    length = min(len(counts), time_freq)
    [second_mets.extend([x] * length) for x in METs]
    return np.array(second_mets)



