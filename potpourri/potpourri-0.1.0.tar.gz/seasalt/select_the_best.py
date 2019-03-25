# Interpret CV results - Pick the Best
#    n_best  depends on cv_settings['n_iter']
#    lowest=False  means that max(score) is the "best"
import pandas as pd


def select_the_best(res, n_best=5, lowest=False):
    # copy into dataframe
    res = pd.DataFrame(res.cv_results_)

    # pick the N best
    res = res.sort_values(by='mean_test_score', ascending=lowest)[:n_best]

    # compute CV-ratio depending on the score type
    if lowest:  # small mean(cv), small std(cv)
        res['cvratio'] = -(res['mean_test_score'] * res['std_test_score'])
    else:  # high mean(cv), small std(cv)
        res['cvratio'] = res['mean_test_score'] / res['std_test_score']

    # pick the best CV-Ratio of the N best ("best" must be the highest)
    res = res.sort_values(by='cvratio', ascending=False)

    # prep output args
    bestparams = res['params'][res.index[0]]  # best params
    summary = res[[
        'params', 'cvratio', 'rank_test_score',
        'mean_test_score', 'std_test_score']]
    return bestparams, summary
