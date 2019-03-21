from .ensemble import TimeSeriesForestClassifier
from ..pipeline import TSPipeline
from ..transformers.series_to_tabular import RandomIntervalFeatureExtractor
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from statsmodels.tsa.stattools import acf


class RiseClassifier(TimeSeriesForestClassifier):

    def __init__(self,
                 n_estimators=500,
                 criterion='gini',
                 max_depth=None,
                 min_samples_split=2,
                 min_samples_leaf=1,
                 min_weight_fraction_leaf=0.,
                 max_features=None,
                 max_leaf_nodes=None,
                 min_impurity_decrease=0.,
                 min_impurity_split=None,
                 bootstrap=False,
                 oob_score=False,
                 n_jobs=None,
                 random_state=None,
                 verbose=0,
                 warm_start=False,
                 class_weight=None,
                 check_input=True):

        features = [np.fft.fft, acf, ar_coefs]
        steps = [('transform', RandomIntervalFeatureExtractor(n_intervals=1,
                                                              features=features)),
                 ('clf', DecisionTreeClassifier())]
        base_estimator = TSPipeline(steps)

        super(RiseClassifier, self).__init__(
            base_estimator=base_estimator,
            n_estimators=n_estimators,
            criterion=criterion,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            min_weight_fraction_leaf=min_weight_fraction_leaf,
            max_features=max_features,
            max_leaf_nodes=max_leaf_nodes,
            min_impurity_decrease=min_impurity_decrease,
            min_impurity_split=min_impurity_split,
            bootstrap=bootstrap,
            oob_score=oob_score,
            n_jobs=n_jobs,
            random_state=random_state,
            verbose=verbose,
            warm_start=warm_start,
            class_weight=class_weight,
            check_input=check_input)

