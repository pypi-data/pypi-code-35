"""
Sojourn
=============
Defines methods for classifying activity levels based on a second-by-second input using sojourn methods.

Provides 1x and a method that outputs that list of clumped data
"""

import numpy as np
import ventana.settings as const
from ventana.METs import cr2_mets

def yield_sojourns(values):
    running = []
    flag = True if values[0] > 0. else False
    for value in values:
        if (value > 0) == flag:
            running.append(value)
        else:
            yield running
            running = [value]
            flag = not flag
    yield(running)

def is_too_short_undet(ident, length):
    return (ident == "undetermined") and (length < const.ACTIVITY_CUT)

def combine_sojourns(clean_s, clean_id):
    skip = False
    fin = []
    for i, soj in enumerate(clean_s):
        if skip:
            skip = False
            continue
        if is_too_short_undet(clean_id[i], len(soj)):
            if (i == 0) or (i + 1 == len(clean_id)):
                fin.append((soj, "undetermined"))
            elif clean_id[i - 1] == clean_id[i + 1]:
                fin[-1] = (fin[-1][0] + soj + clean_s[i + 1], clean_id[i - 1])
                skip = True
            else:
                fin[-1] = (fin[-1][0] + soj, clean_id[i - 1])
        else:
            fin.append((soj, clean_id[i]))
    return fin



def clean_sojourns(sojourns, identity):
    j = 0
    clean_s = []
    clean_id = []
    for i in range(len((identity))):
        if j > 0:
            j -= 1
            continue
        if (i + 1 < len(identity)) and (identity[i] == identity[i + 1]):
            x = sojourns[i]
            j = 0
            while (i + j + 1 < len(identity)) and (identity[i + j] == identity[i + j + 1]):
                x.extend(sojourns[i + j + 1])
                j += 1
            clean_s.append(x)
            clean_id.append(identity[i])
        else:
            clean_s.append(sojourns[i])
            clean_id.append(identity[i])
    return combine_sojourns(clean_s, clean_id)

def get_clumps(counts):
    """
    Sojourn second-by-second estimation of METs based on second-by-second vertical counts

    :param counts: Second-by-second vertical counts (numbers)
    :type counts: list
    :return: List of tuples that can contains (sojourn, identity) where sojourn is a second-by-second list of vertical counts and identity is a string in ("undetermined", "sedentary", "activity")
    :rtype: list
    """
    base_identity = []
    sojourns = []
    for sojourn in yield_sojourns(counts):
        if (sojourn[0] == 0) and (len(sojourn) > const.SIT_CUT):
            base_identity.append("sedentary")
        elif (sojourn[0] != 0) and (len(sojourn) > const.ACTIVITY_CUT):
            base_identity.append("activity")
        else:
            base_identity.append("undetermined")
        sojourns.append(sojourn)
    return clean_sojourns(sojourns, base_identity)

def sojourn_1x(counts, met_method = cr2_mets):
    """
    Sojourn second-by-second estimation of METs based on second-by-second vertical counts

    :param counts: Second-by-second vertical counts (numbers)
    :param met_method: name of function used to estimate METs
    :type counts: list
    :type met_method: func
    :return: Second-by-second estimation of METs (floats)
    :rtype: list
    """

    clumps = get_clumps(counts)
    pred = []
    for (sojourn, level) in clumps:
        mets = []
        if level == "activity":
            mets = met_method(sojourn)
        else:
            val_cut = np.mean(sojourn)
            if val_cut > const.CUT_HIGH:
                mets = met_method(sojourn)
            elif (val_cut > const.CUT_MIN) and (val_cut <= const.CUT_MED) and (len(sojourn) > const.SIT_CUT):
                mets = [const.SOJ_METS_MED] * len(sojourn)
            elif (val_cut > const.CUT_MIN) and (val_cut <= const.CUT_MED) and (len(sojourn) <= const.SIT_CUT):
                mets = [const.SOJ_METS_HIGH] * len(sojourn)
            elif (val_cut > const.CUT_MED) and (val_cut <= const.CUT_HIGH):
                mets = [const.SOJ_METS_VIG] * len(sojourn)
            else:
                mets = [const.SOJ_METS_MIN] * len(sojourn)
        pred.extend(mets)
    return pred