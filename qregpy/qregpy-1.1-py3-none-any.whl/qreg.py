#!/usr/bin/env python
"""Summary
"""
# coding=utf-8
from __future__ import print_function, division
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime


from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor
from xgboost.sklearn import XGBRegressor as XGBRegressor_sklearn
from xgboost.sklearn import XGBClassifier as XGBClassifier_sklearn

from sklearn.model_selection import train_test_split


class QReg:
    """This is the implementation of query-centric regression, QReg.
    
    Attributes:
        base_models (list,optional): a list of regression model names, example ['linear', "xgboost"]
        b_cross_validation (boolean): whether cross-validation is used to train the base models, including xgboost, gboost, etc.
        n_jobs (int): the maximum cores to be used.
        verbose (boolean): control the logging level
        reg (QReg): the QReg regression model
    """

    def __init__(self, base_models=['linear', "xgboost"], b_cross_validation=True, n_jobs=4, verbose=True):
        """Summary
        
        Args:
            base_models (list, optional): a list of regression model names, example ['linear', "xgboost"]. Currently "linear", "polynomial", "decisiontree", "xgboost", "gboost" are supported.
            b_cross_validation (bool, optional): whether cross-validation is used to train the base models, including xgboost, gboost, etc.
            n_jobs (int, optional): the maximum cores to be used.
            verbose (bool, optional): control the logging level
        """
        self.base_models = base_models
        self.b_cross_validation = b_cross_validation
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.reg = None
        if (len(base_models) == 1):
            self.b_use_classifier = False
        else:
            self.b_use_classifier = True
        self.model_catalog = {}
        self.model_catalog_names = []
        self.classifier = None

    def fit(self, X, y):
        """fit the QReg regression on the training data X andy.
        
        Args:
            X (numpy.ndarray): the independent variables, like [[1,2],[2,4]]
            y (numpy.ndarray): the dependent variables, like [4, 8]
        
        Returns:
            QReg: the regression model
        """
        start = datetime.now()

        seed = 7
        test_size = 0.5
        Xreg, Xcls, yreg, ycls = train_test_split(X, y, test_size=test_size, random_state=seed)

        self.deploy_models(Xreg, yreg)

        if self.b_use_classifier:
            predictions = {}
            for model in self.model_catalog:
                predictions[model] = self.model_catalog[model].predict(Xcls).tolist()
            predictions_list = [[predictions[model][index] for model in self.model_catalog] for index in
                                range(len(ycls))]
            predictions_min = [min(items) for items in predictions_list]
            errors = [[(predictions[model][index] - predictions_min[index]) for model in self.model_catalog] for index
                      in range(len(ycls))]
            best_model_index = [item.index(0.0) for item in errors]

            self.build_classifier_xgboost(Xcls, best_model_index)

        end = datetime.now()
        time_train = (end - start).total_seconds()
        print("Finish training QReg, time cost is {:8.3f} sec".format(time_train))
        print("------------------------------------------------------------------")
        return self

    def predict(self, points):
        """make a prediction for given points
        Args:
            points (numpy.ndarray):  points,  like [[1,2],[2,4]] to predict for point [1,2] and point [2,4]
        
        Returns:
            list: list of predictions
        """
        if self.b_use_classifier:
            return [
                self.model_catalog[self.model_catalog_names[self.classifier.predict(point)[0]]].predict([point]).flat[0]
                for point in points]
        else:
            return self.model_catalog[self.model_catalog_names[0]].predict(points)

    def deploy_sklearn_linear_regression(self, X, y):
        """ train the linear regression
        
        Args:
            X (numpy.ndarray): the independent variables, like [[1,2],[2,4]]
            y (numpy.ndarray): the dependent variables, like [4, 8]
        
        Returns:
            TYPE:  the linear regression model
        """
        from sklearn import linear_model
        if self.verbose:
            print("Start training the linear regression...")

        start = datetime.now()
        reg = linear_model.LinearRegression().fit(X, y)
        end = datetime.now()
        time_train = (end - start).total_seconds()

        if self.verbose:
            print("Finish training the linear regression (time cost is {:6.3f} sec.)".format(time_train))
        return reg, time_train

    def deploy_sklearn_polynomial_regression(self, X, y):
        """ Train the polynomial regression
        
        Args:
            X (numpy.ndarray): the independent variables, like [[1,2],[2,4]]
            y (numpy.ndarray): the dependent variables, like [4, 8]
        
        Returns:
            TYPE: the polynomial regression model
        """
        from sklearn.preprocessing import PolynomialFeatures
        from sklearn.linear_model import Ridge
        from sklearn.pipeline import make_pipeline
        if self.verbose:
            print("Start training the polynomial regression...")

        start = datetime.now()
        reg = make_pipeline(PolynomialFeatures(5), Ridge())
        reg.fit(X, y)
        end = datetime.now()
        time_train = (end - start).total_seconds()

        if self.verbose:
            print("Finish training the polynomial regression (time cost is {:6.3f} sec.)".format(time_train))
        return reg, time_train

    def deploy_model_sklearn_decision_tree_regression(self, X, y):
        """ train the decision tree regression
        
        Args:
            X (numpy.ndarray): the independent variables, like [[1,2],[2,4]]
            y (numpy.ndarray): the dependent variables, like [4, 8]
        
        Returns:
            TYPE: the decision tree regression model
        """
        if self.verbose:
            print("Start training the decision tree regression...")

        start = datetime.now()
        if self.b_cross_validation:
            parameters = {'max_depth': range(3, 20)}
            clf = GridSearchCV(DecisionTreeRegressor(),
                               parameters, n_jobs=self.n_jobs, cv=3)
            clf.fit(X, y)
            reg = clf.best_estimator_
        else:
            reg = DecisionTreeRegressor(max_depth=4)
            reg.fit(X, y)

        end = datetime.now()
        time_train = (end - start).total_seconds()

        if self.verbose:
            print("Finish training the decision tree regression (time cost is {:6.3f} sec.)".format(time_train))
        return reg, time_train

    def deploy_xgboost_regression(self, X, y):
        """ train the XGBoost regression
        
        Args:
            X (numpy.ndarray): the independent variables, like [[1,2],[2,4]]
            y (numpy.ndarray): the dependent variables, like [4, 8]
        
        Returns:
            TYPE: the XGBoost regression model
        """
        from xgboost import XGBRegressor
        if self.verbose:
            print("Start training the xgboost regression...")

        start = datetime.now()
        if self.b_cross_validation:
            parameters = {'max_depth': [1, 8, 12]}
            clf = GridSearchCV(XGBRegressor_sklearn(), parameters, n_jobs=4, verbose=0, cv=3)
            clf.fit(X, y)
            reg = clf.best_estimator_
        else:
            reg = XGBRegressor(max_depth=4)
            reg.fit(X, y)

        end = datetime.now()
        time_train = (end - start).total_seconds()

        if self.verbose:
            print("Finish training the xgboost regression (time cost is {:6.3f} sec.)".format(time_train))
        return reg, time_train

    def deploy_sklearn_gradient_tree_boosting(self, X, y):
        """ train the gradient tree boosting regression
        
        Args:
            X (numpy.ndarray): the independent variables, like [[1,2],[2,4]]
            y (numpy.ndarray): the dependent variables, like [4, 8]
        
        Returns:
            TYPE: the gradient tree boosting regression model
        """
        from sklearn.ensemble import GradientBoostingRegressor
        if self.verbose:
            print("Start training the gradient boosting regression...")

        start = datetime.now()
        if self.b_cross_validation:
            parameters = {'max_depth': [1, 4, 10], 'loss': ['ls'],
                          'n_estimators': [100], 'learning_rate': [0.1],
                          # 'min_impurity_split': [1e-1],
                          'learning_rate': [1e-1],
                          'min_samples_split': [7], 'verbose': [2],
                          'min_samples_leaf': [1], 'subsample': [1.0]}
            clf = GridSearchCV(
                GradientBoostingRegressor(verbose=1), parameters, n_jobs=self.n_jobs, cv=3)
            clf.fit(X, y)
            reg = clf.best_estimator_
        else:
            reg = GradientBoostingRegressor(verbose=1,
                                            n_estimators=1, learning_rate=0.1, max_depth=4, random_state=0, loss='ls')
            reg.fit(X, y)

        end = datetime.now()
        time_train = (end - start).total_seconds()

        if self.verbose:
            print("Finish training the gradient boosting regression (time cost is {:6.3f} sec.)".format(time_train))
        return reg, time_train

    def deploy_models(self, X, y):
        start = datetime.now()
        for model in self.base_models:
            if model == "linear":
                self.model_catalog[model] = self.deploy_sklearn_linear_regression(X, y)[0]
            elif model == "xgboost":
                self.model_catalog[model] = self.deploy_xgboost_regression(X, y)[0]
            elif model == "gboost":
                self.model_catalog[model] = self.deploy_sklearn_gradient_tree_boosting(X, y)[0]
            elif model == "polynomial":
                self.model_catalog[model] = self.deploy_sklearn_polynomial_regression(X, y)[0]
            elif model == "decisiontree":
                self.model_catalog[model] = self.deploy_model_sklearn_decision_tree_regression(X, y)[0]
            else:
                print(model + " is not supported! please check!")
                exit(1)

        self.model_catalog_names = list(self.model_catalog.keys())

        if self.verbose:
            end = datetime.now()
            time_train = (end - start).total_seconds()
            print("Finish training the base models: " + str(list(self.model_catalog.keys())))
            print("Time to train base regression models is {:8.3f} sec.".format(time_train))

    def build_classifier_xgboost(self, X, indexes):
        start = datetime.now()

        if self.b_cross_validation:
            parameters = {'max_depth': [1, 4, 8, 12]}
            clf = GridSearchCV(XGBClassifier_sklearn(),
                               parameters, n_jobs=self.n_jobs, cv=3)
            clf.fit(X, indexes)
            classifier = clf.best_estimator_
        else:
            classifier = XGBRegressor(max_depth=4)
            classifier.fit(X, indexes)

        if self.verbose:
            end = datetime.now()
            time_train = (end - start).total_seconds()
            print("Time to train the XGBoost classifier is {:8.3f} sec.".format(time_train))
        self.classifier = classifier


if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("/data/dbest/data/10k.csv")
    headerX = ["ss_list_price", "ss_wholesale_cost"]
    headerY = "ss_wholesale_cost"

    X = df[headerX].values
    y = df[headerY].values

    reg = QReg(base_models=["linear", "polynomial", "decisiontree", "xgboost", "gboost"], verbose=True).fit(X, y)
    # print(reg.predict([[93.35], [60.84]]))
    print(reg.predict([[93.35, 53.04], [60.84, 41.96]]))
