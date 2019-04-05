import os
import dill
from copy import deepcopy

import numpy as np
import pandas as pd
from malemba import ArrayModelBase
from catboost import CatBoost


NUM_THREADS = 4


class ModelCatBoost(ArrayModelBase):

    def __init__(self, params=None, **kwargs):
        self.model = CatBoost(params=params)
        self.cat_features = set()
        super(ModelCatBoost, self).__init__(params=params, **kwargs)

    def fit(self, X, Y):
        X = self.get_cat_features(X=X)
        print("got categorial features")
        X, Y, data_shape = super(ModelCatBoost, self).fit(X=X, Y=Y)
        print("got features array shape")
        data = self.np_array(X, data_shape, low_memory=self.low_memory)
        self.model.fit(X=pd.DataFrame(data).values,
                       y=np.array(list(Y)),
                       cat_features=sorted([self._features[feat] for feat in self.cat_features]))

    def predict(self, X):
        X = self.get_cat_features(X=X)
        print("got categorial features")
        X, data_shape = super(ModelCatBoost, self).predict(X=X)
        print("got features array shape")
        data = self.np_array(X, data_shape)
        # self._labels["diagnosis_source_code"] = 15###
        return list(map(lambda p: dict((self.labels[i],
                                        p[i]**(1.0/self.label_weights[self.labels[i]])) for i in range(len(p))),
                        self.model.predict(data=pd.DataFrame(data).values, prediction_type="Probability")))

    def dump(self, scheme_path, **kwargs):
        if not os.path.exists(scheme_path):
            os.makedirs(scheme_path)
        meta_dict = deepcopy(self.__dict__)
        del meta_dict["model"]
        meta_f = open(os.path.join(scheme_path, "meta.m"), "wb")
        dill.dump(meta_dict, meta_f)
        meta_f.close()

        self.model.save_model(fname=os.path.join(scheme_path, "model.m"), format="cbm")

    @classmethod
    def load(cls, scheme_path, params=None, **kwargs):
        model_catboost = cls(params=params, **kwargs)
        with open(os.path.join(scheme_path, "meta.m"), "rb") as meta_f:
            model_catboost.__dict__ = dill.load(meta_f)
        if params is not None:
            if model_catboost.params is not None:
                model_catboost.params.update(params)
            else:
                model_catboost.params = params
        model_catboost.model = CatBoost(params=model_catboost.params)
        model_catboost.model.load_model(fname=os.path.join(scheme_path, "model.m"), format="cbm")
        return model_catboost

    @staticmethod
    def _convert_str_to_factors():
        return False

    @property
    def num_threads(self):
        return self.params.get("thread_count", NUM_THREADS)

    def get_cat_features(self, X):
        for x in X:
            x_cat = dict()
            for feat in x:
                if type(x[feat]) in (str, np.str, np.str_):
                    self.cat_features.add(feat)
                if type(x[feat]) in (bool, np.bool, np.bool_):
                    x_cat[feat] = int(x[feat])
                else:
                    x_cat[feat] = x[feat]
            yield x_cat
