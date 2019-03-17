from sklearn.base import BaseEstimator, RegressorMixin


class SMRegressor(BaseEstimator, RegressorMixin):
    """Wrapper around a statsmodels linear regressor such as sm.OLS or sm.RLM.
    """

    def __init__(self, model_class, fit_intercept=True):
        self.model_class = model_class
        self.fit_intercept = fit_intercept
        self._fitted = False

    def fit(self, X, y, **kwargs):
        if self.fit_intercept:
            # Do not use sm.add_constant to avoid explicit statsmodels dependency
            X = X.copy()
            X.insert(0, "const", 1)
        self._model = self.model_class(y, X)
        self._results = self._model.fit()
        self._fitted = True
        return self

    def predict(self, X, **kwargs):
        if self.fit_intercept:
            X = X.copy()
            X.insert(0, "const", 1)
        return self._results.predict(X)

    transform = predict

    def summary(self):
        return self._results.summary()

    @property
    def coef_(self):
        start_idx = 1 if self.fit_intercept else 0  # Omit coefficient of added constant
        return self._results.params[start_idx:]

    @property
    def feature_importances_(self):
        start_idx = 1 if self.fit_intercept else 0  # Omit pvalue of added constant
        return 1 / (self._results.pvalues[start_idx:] + 1e-9)  # Avoid numerical problems
