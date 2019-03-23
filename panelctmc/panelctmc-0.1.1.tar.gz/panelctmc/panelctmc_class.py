
from sklearn.base import BaseEstimator
from .panelctmc_func import panelctmc
from ctmc import simulate


class PanelCtmc(BaseEstimator):
    """Continous Time Markov Chain for Panel Data, sklearn API class"""

    def __init__(self, mapping=None, lastdate=None,
                 transintv=1.0, toltime=1e-8, debug=False):
        self.mapping = mapping
        self.lastdate = lastdate
        self.transintv = transintv
        self.toltime = toltime
        self.debug = debug
        self.transmat = None
        self.genmat = None
        self.transcount = None
        self.statetime = None
        self.datalist = None

    def fit(self, X, y=None):
        (
            self.transmat,
            self.genmat,
            self.transcount,
            self.statetime,
            self.datalist
        ) = panelctmc(
            X, self.mapping,
            lastdate=self.lastdate,
            transintv=self.transintv,
            toltime=self.toltime,
            debug=self.debug)
        return self

    def predict(self, X, steps=1):
        return simulate(X, self.transmat, steps)
