import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge, Lasso

from examples.kaggle_House_Prices_Advanced_Regression.FeatureEngineeringDataCleaner import FeatureEngineeringDataCleaner
from sklearn_helper.model.evaluator import Evaluator


"""
this is a solution for Kaggle's House Prices: Advanced Regression Techniques problem
 https://www.kaggle.com/c/house-prices-advanced-regression-techniques
"""


def main():
    df = pd.read_csv("train.csv")
    sale_price = df["SalePrice"]

    models = {
        "DummyRegressor": {
            "model": DummyRegressor(),
        },
        "Base LinearRegression": {
            "model": linear_model.LinearRegression()
        },
        "Ridge": {
            "model": Ridge(),
            "params": {
                'alpha': np.linspace(0, 30, num=100)
            }
        },
        "Lasso": {
            "model": Lasso(),
            "params": {
                'alpha': np.linspace(0, 30, num=100)
            }
        }
    }
    model_finder = Evaluator(models, data_cleaners=[FeatureEngineeringDataCleaner()], n_jobs=-1)

    model = model_finder.evaluate(df, sale_price)
    print(model)

    df_test = pd.read_csv("test.csv")
    test_indexes = df_test.Id

    predictions = np.exp(model.predict(df_test))

    # Print results into a file
    prediction = pd.DataFrame({"SalePrice": predictions})
    prediction["Id"] = test_indexes
    prediction.to_csv("solution.csv", index=False, columns=["Id", "SalePrice"])
    print(prediction.head())


if __name__ == "__main__":
    main()
