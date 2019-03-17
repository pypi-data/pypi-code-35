from timeit import default_timer

from sklearn.metrics import make_scorer
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score


class ModelEvaluator:
    def __init__(self, main_metric, additional_metrics=[], data_splitter=KFold(3), n_jobs=None):
        self.main_metric = main_metric
        self.additional_metrics = additional_metrics
        self.data_splitter = data_splitter
        self.n_jobs = n_jobs

    def test_model(self, model_name, model, data_cleaner, X, y):
        start_time = default_timer()
        result = {"model_name": model_name,
                  "cleaner_name": data_cleaner.get_name(),
                  "cleaner": data_cleaner,
                  "model": model,
                  "metrics": {}
                  }
        result["metrics"][self.main_metric] = self.__calculate__metric(model, X, y, self.main_metric)
        for additional_metric in self.additional_metrics:
            result["metrics"][additional_metric] = self.__calculate__metric(model, X, y, additional_metric)
        result["time"] = default_timer() - start_time
        return result

    def __calculate__metric(self, model, X, y, metric):
        return cross_val_score(model, X, y, cv=self.data_splitter, scoring=make_scorer(metric), n_jobs=self.n_jobs).mean()
