"""This module defines a function to do a likelihood ratio test
for any quality parameters deviating from zero,
in the MEAN for the population from which test subjects were recruited.

* Main Result Class:
LikelihoodRatioResult: tuple (statistic, df, pvalue)

Arne Leijon, 2018-12-06
"""
from scipy.stats import chi2
from collections import namedtuple

import logging
logger = logging.getLogger(__name__)


LikelihoodRatioResult = namedtuple('LikelihoodRatioResult', 'statistic df pvalue')
# storage of result from a Likelihood Ratio test
# statistic = 2 * Log-likelihood difference between tested model and NULL model
# df = number of parameters in the tested model that are forced to zero in the NULL model
# pvalue = approximate significance value
# The test statistic is asymptotically Chi-2-distributed with df degrees of freedom
# according to Wilk's theorem.
# NOTE: the pvalue is approximate


def likelihood_ratio_test(pcr0, pcr1):
    """Likelihood-ratio test
    :param pcr0: PairedCompResultSet instance learned with NULL population quality params
    :param pcr1: PairedCompResultSet instance learned with full freedom
    :return: res = nested dict with elements
        res[group][attribute] = LikelihoodRatioResult instance
        for the NULL hypothesis that
        the mean quality parameters in the population are EQUAL
        for all tested objects in all test conditions.
        p_values smaller than, e.g., 0.05 indicate that pcr1 shows significant differences.

    Method: The lower bounds to the data log-likelihood is used to calculate
        a likelihood-ratio that is asymptotically Chi-2-distributed,
        according to Wilk's theorem.
    """
    res = dict()
    for (g, g_models) in pcr1.models.items():
        res[g]= dict()
        for (a, ga_model) in g_models.items():
            LL_1 = ga_model.LL[-1]
            df = pcr0.models[g][a].population.n_null
            LL_0 = pcr0.models[g][a].LL[-1]
            LLR = 2 * (LL_1 - LL_0)  # Wilk: asymptotically chi2-distributed
            p = chi2.sf(LLR, df=df)
            res[g][a] = LikelihoodRatioResult(LLR, df, p)
    return res


# def llr_test_variables(pcr0, pcr1):
#     """Likelihood-ratio test variable
#     :param pcr0: PairedCompResultSet instance learned with NULL population quality params
#     :param pcr1: PairedCompResultSet instance learned with full freedom
#     :return: llr = nested dict with elements
#         llr[group][attribute] = log-likelihood-ratio test variable for the hypothesis that
#         a model with free mean quality parameters in the population
#         versus the NULL hypothesis that
#         the mean quality parameters are EQUAL for all tested objects in all test conditions.
#         Larger llr values are stronger indication of a real difference.
#         The resulting llr values are asymptotically Chi-2 distributed.
#     """
#     llr = dict()
#     for (g, g_models) in pcr1.models.items():
#         llr[g]= dict()
#         for (a, ga_model) in g_models.items():
#             LL_1 = ga_model.LL[-1]
#             LL_0 = pcr0.models[g][a].LL[-1]
#             llr[g][a] = 2 * (LL_1 - LL_0)  # Wilk: asymptotically chi2-distributed
#     return llr


# def display_lr_result(prc0, prc1):
#     """Show results of likelihood ratio test in logger output
#     :param pcr0: PairedCompResultSet instance learned with NULL population quality params
#     :param pcr1: PairedCompResultSet instance learned with full freedom
#     :return: None
#     """
#     lr_dict = likelihood_ratio_test(prc0, prc1)
#     for (g, g_result) in lr_dict.items():
#         for (a, lr) in g_result.items():
#             ga = f'Group {repr(g)}, Attribute {a}: '
#             if lr.pvalue < 0.001:
#                 p = f'p = {lr.pvalue:.2g}'
#                 s = 'Highly Significant'
#             elif lr.pvalue < 0.05:
#                 p = f'p = {lr.pvalue:.1%}'
#                 s = 'Significant.'
#             else:
#                 p = f'p = {lr.pvalue:.1%}'
#                 s = 'NOT Significant.'
#             logger.info(ga + f'chi2(df={lr.df}) = {lr.statistic:.3f}: ' + p + '. ' + s)
#

