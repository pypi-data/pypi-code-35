import numpy as np
from sklearn import datasets
from sklearn import svm
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn_helper.data.data_cleaner import DataCleaner
from sklearn_helper.model.evaluator import Evaluator


class Thresholding(DataCleaner):
    THRESHOLD = 3

    def clean_training_data(self, x, y):
        return self.clean_testing_data(x), y

    def clean_testing_data(self, x):
        _x = np.copy(x)
        _x[_x <= self.THRESHOLD] = 0
        _x[_x > self.THRESHOLD] = 1
        return _x


if __name__ == "__main__":
    digits = datasets.load_digits()
    X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, random_state=0, test_size=0.3)

    models = {
        "DummyClassifier": {
            "model": DummyClassifier()
        },
        "SVC": {
            "model": svm.SVC(C=2, gamma=0.0111)
        }
    }
    model_finder = Evaluator(models, data_cleaners=[Thresholding()], main_metric="accuracy")

    model = model_finder.evaluate(X_train, y_train)

    print(model)
    print(accuracy_score(model.predict(X_test), y_test))
