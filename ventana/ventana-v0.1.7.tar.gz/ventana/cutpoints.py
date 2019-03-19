"""
Cutpoints
=============
Defines methods for classifying activity levels based on a second-by-second input.

Provides 3 different methods for validation purposes
"""

import numpy as np
import ventana.settings as settings
from ventana.utils import chunks

def freedson_cut(val):
    if val < settings.FREEDSON_SED:
        return "sedentary"
    elif val < settings.FREEDSON_LIGHT:
        return "light"
    elif val < settings.FREEDSON_MOD:
        return "moderate"
    else:
        return "vigourous"

def freedson(counts, time_freq = 60):
    """
    Freedson second-by-second classification of activity level based on second-by-second vertical counts

    :param counts: Second-by-second vertical counts (numbers)
    :param time_freq: Number of seconds that are grouped together to classify activity level, default 60
    :type counts: list
    :type time_freq: int
    :return: Second-by-second classification of activity levels (strings)
    :rtype: list
    """
    minute_est = [freedson_cut(sum(x)) for x in chunks(counts, time_freq)]
    second_est = []
    length = min(len(counts), time_freq)
    [second_est.extend([x] * length) for x in minute_est]
    return np.array(second_est[:len(counts)])

def sasaki_cut(val):
    if val < settings.SASAKI_LIGHT:
        return "light"
    elif val < settings.SASAKI_MOD:
        return "moderate"
    elif val < settings.SASAKI_VIG:
        return "vigourous"
    else:
        return "very vigourous"

def sasaki(counts, time_freq = 60):
    """
    Sasaki second-by-second classification of activity level based on second-by-second vector magnitude

    :param counts: Second-by-second vertical counts (numbers)
    :param time_freq: Number of seconds that are grouped together to classify activity level, default 60
    :type counts: list
    :type time_freq: int
    :return: Second-by-second classification of activity levels (strings)
    :rtype: list
    """
    minute_est = [sasaki_cut(sum(x)) for x in chunks(counts, time_freq)]
    second_est = []
    length = min(len(counts), time_freq)
    [second_est.extend([x] * length) for x in minute_est]
    return np.array(second_est[:len(counts)])

def nhanes_cut(val):
    if val < settings.NHANES_SED:
        return "sedentary"
    elif val < settings.NHANES_LIGHT:
        return "light"
    elif val < settings.NHANES_MOD:
        return "moderate"
    else:
        return "vigourous"

def nhanes(counts, time_freq = 60):
    """
    Nhanes second-by-second classification of activity level based on second-by-second vertical counts

    :param counts: Second-by-second vertical counts (numbers)
    :param time_freq: Number of seconds that are grouped together to classify activity level, default 60
    :type counts: list
    :type time_freq: int
    :return: Second-by-second classification of activity levels (strings)
    :rtype: list
    """
    minute_est = [nhanes_cut(sum(x)) for x in chunks(counts, time_freq)]
    second_est = []
    length = min(len(counts), time_freq)
    [second_est.extend([x] * length) for x in minute_est]
    return np.array(second_est[:len(counts)])
    
