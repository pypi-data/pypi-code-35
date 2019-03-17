from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold


class ModelOptimizer:
    def __init__(self, main_metric, data_splitter=KFold(5), n_jobs=None):
        self.main_metric = main_metric
        self.data_splitter = data_splitter
        self.n_jobs = n_jobs

    def optimize_model(self, model, X, y, param):
        if param is None:
            model.fit(X, y)
            return model
        grid_search_cv = GridSearchCV(model, param, cv=self.data_splitter, scoring=make_scorer(self.main_metric), n_jobs=self.n_jobs)
        grid_search_cv.fit(X, y)
        model = grid_search_cv.best_estimator_
        model.fit(X, y)
        return model
