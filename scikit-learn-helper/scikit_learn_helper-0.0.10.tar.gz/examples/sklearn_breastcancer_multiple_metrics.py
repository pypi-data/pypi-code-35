from sklearn import datasets
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, f1_score
from sklearn.metrics import accuracy_score
from sklearn_helper.model.evaluator import Evaluator


if __name__ == "__main__":
    breast_cancer = datasets.load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(breast_cancer.data, breast_cancer.target, random_state=0, test_size=0.3)

    models = {
        "DummyClassifier": {
            "model": DummyClassifier()
        },
        "LogisticRegression": {
            "model": LogisticRegressionCV()
        }
    }
    evaluator = Evaluator(models,
                          main_metric=roc_auc_score,
                          maximize_metric=True,
                          additional_metrics=[f1_score, accuracy_score])

    model = evaluator.evaluate(X_train, y_train)

    print(model)
    print(roc_auc_score(model.predict(X_test), y_test))
