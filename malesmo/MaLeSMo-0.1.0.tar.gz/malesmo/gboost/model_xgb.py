import os
import dill
from copy import deepcopy

from malemba import ArrayModelBase
import numpy as np
import pandas as pd
import xgboost as xgb


NUM_THREADS = 4


class ModelXGB(ArrayModelBase):

    def __init__(self, params=None, **kwargs):
        self.model = None
        super(ModelXGB, self).__init__(params=params, **kwargs)

    def fit(self, X, Y):
        """
        :param X: list or iterator of dicts with features {feat1: v1, feat2: v2, ...}
        :param Y: list of labels
        """
        X, Y, data_shape = super(ModelXGB, self).fit(X=X, Y=Y)
        data = self.np_array(X, data_shape, low_memory=self.low_memory)
        dtrain = xgb.DMatrix(data=pd.DataFrame(data).values, label=np.array(list(Y)), missing=np.nan)
        self.model = xgb.train(params=self.params, dtrain=dtrain)

    def predict(self, X):
        """
        :param X: list or iterator of dicts with features {feat1: v1, feat2: v2, ...}
        :return: list of dicts with labels scores
        """
        X, data_shape = super(ModelXGB, self).predict(X=X)
        data = self.np_array(X, data_shape)
        dpred = xgb.DMatrix(data=pd.DataFrame(data).values, missing=np.nan)
        return list(map(lambda p: dict((self.labels[i], p[i]) for i in range(len(p))),
                        self.model.predict(dpred, output_margin=True)))

    def dump(self, scheme_path, **kwargs):
        if not os.path.exists(scheme_path):
            os.makedirs(scheme_path)
        meta_dict = deepcopy(self.__dict__)
        del meta_dict["model"]
        meta_f = open(os.path.join(scheme_path, "meta.m"), "wb")
        dill.dump(meta_dict, meta_f)
        meta_f.close()

        self.model.save_model(fname=os.path.join(scheme_path, "model.m"))

    @classmethod
    def load(cls, scheme_path, params=None, **kwargs):
        model_xgb = cls(params=params, **kwargs)
        with open(os.path.join(scheme_path, "meta.m"), "rb") as meta_f:
            model_xgb.__dict__ = dill.load(meta_f)
        if params is not None:
            if model_xgb.params is not None:
                model_xgb.params.update(params)
            else:
                model_xgb.params = params
        model_xgb.model = xgb.Booster(params=model_xgb.params)
        model_xgb.model.load_model(fname=os.path.join(scheme_path, "model.m"))
        return model_xgb

    @staticmethod
    def _convert_str_to_factors():
        return True

    @property
    def num_threads(self):
        return self.params.get("nthread", NUM_THREADS)
