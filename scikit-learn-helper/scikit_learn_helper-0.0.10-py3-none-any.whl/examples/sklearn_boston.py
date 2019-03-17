from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error
from sklearn.dummy import DummyRegressor
from sklearn.model_selection import train_test_split
from sklearn_helper.model.evaluator import Evaluator

if __name__ == "__main__":
    digits = datasets.load_boston()
    X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, random_state=0, test_size=0.3)

    models = {
        "DummyRegressor": {
            "model": DummyRegressor(),
        },
        "Base LinearRegression": {
            "model": linear_model.LinearRegression()
        }
    }
    model_finder = Evaluator(models)

    model = model_finder.evaluate(X_train, y_train)

    print(model)
