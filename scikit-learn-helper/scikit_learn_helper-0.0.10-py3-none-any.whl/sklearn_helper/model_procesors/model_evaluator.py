from timeit import default_timer


class ModelEvaluator:
    def __init__(self, main_metric, additional_metrics=[], n_jobs=None):
        self.main_metric = main_metric
        self.additional_metrics = additional_metrics
        self.n_jobs = n_jobs

    def test_model(self, model_name, model, data_cleaner, X, y):
        X = data_cleaner.clean_testing_data(X)
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

    @staticmethod
    def __calculate__metric(model, X, y, metric):
        prediction = model.predict(X)
        return metric(prediction, y)
