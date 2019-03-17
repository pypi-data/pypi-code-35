from sklearn import datasets
from sklearn import svm
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn_helper.model.evaluator import Evaluator


if __name__ == "__main__":
    digits = datasets.load_digits()
    X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, random_state=0, test_size=0.3)

    models = {
        "DummyClassifier": {
            "model": DummyClassifier()
        },
        "SVC": {
            "model": svm.SVC()
        }
    }
    model_finder = Evaluator(models, main_metric="accuracy")

    model = model_finder.evaluate(X_train, y_train)

    print(model)
    print(accuracy_score(model.predict(X_test), y_test))
