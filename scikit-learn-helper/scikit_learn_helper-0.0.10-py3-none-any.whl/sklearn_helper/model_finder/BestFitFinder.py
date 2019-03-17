from sklearn.model_selection import KFold

from sklearn_helper.data.dummy_cleaner import DummyCleaner
from sklearn_helper.model_procesors.model_evaluator import ModelEvaluator
from sklearn_helper.model_procesors.model_optimizer import ModelOptimizer
from sklearn_helper.output_processor.standard_output_printer import StandardOutputPrinter
from sklearn.metrics import mean_squared_error


class BestFitFinder:
    def __init__(self, models, data_cleaners=[DummyCleaner()],
                 main_metric=mean_squared_error, additional_metrics=[],
                 data_splitter=KFold(3), maximize_metric=False, n_jobs=None):
        self.models = models
        self.data_cleaners = data_cleaners
        self.models = models
        self.data_splitter = data_splitter
        self.n_jobs = n_jobs
        self.maximize_metric = maximize_metric
        self.main_metric = main_metric
        self.additional_metrics = additional_metrics
        self.model_optimizer = ModelOptimizer(main_metric, data_splitter, n_jobs)
        self.model_evaluator = ModelEvaluator(main_metric, additional_metrics, data_splitter, n_jobs)

    def evaluate(self, X, y, print_result=True):
        results = []
        for data_cleaner in self.data_cleaners:
            _X, _y = data_cleaner.clean_training_data(X, y)
            _result = self.__test_models(_X, _y, data_cleaner)
            results += _result

        if print_result:
            StandardOutputPrinter().print_results(results, self.main_metric, self.maximize_metric)

        return self.__train_best_model(X, y, *self.__best_model(results))

    def __test_models(self, X, y, data_cleaner):
        results = []
        for model_name, model_data in self.models.items():
            model = self.model_optimizer.optimize_model(model_data["model"], X, y, model_data.get("params"))
            results.append(
                self.model_evaluator.test_model(model_name, model, data_cleaner, X, y))

        return results

    def __best_model(self, results):
        best_model = sorted(results, key=lambda x: x["metrics"][self.main_metric], reverse=self.maximize_metric)[0]
        return best_model["model"], best_model["cleaner"]

    @staticmethod
    def __train_best_model(X, y, model, data_cleaner):
        X, y = data_cleaner.clean_training_data(X, y)
        model.fit(X, y)

        original_predict = model.predict
        model.predict = lambda _x: original_predict(data_cleaner.clean_testing_data(_x))

        return model
