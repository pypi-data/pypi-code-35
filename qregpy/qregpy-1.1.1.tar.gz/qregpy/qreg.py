#!/usr/bin/env python
# coding=utf-8

"""
.. module:: qregpy
    :platform: Linux, MacOs, Windows
    :synopsis: QReg: Query-centric regression.
 
.. moduleauthor:: Qingzhi Ma <q.ma.2@warwick.ac.uk>
"""


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

__docformat__ = 'reStructuredText'

class QReg:
    """This is the implementation of query-centric regression, QReg.
    
    :param base_models: a list of regression model names, example ['linear', "xgboost"]. Currently "linear", "polynomial", "decisiontree", "xgboost", "gboost" are supported.
    :param b_cross_validation: whether cross-validation is used to train the base models, including xgboost, gboost, etc.
    :param n_jobs: the maximum cores to be used.
    :param verbose: control the logging level
    :type base_models: List of Strings, (Optional)
    :type b_cross_validation: Boolean, (Optional, default True)
    :type n_jobs: int, (Optional, default 4)
    :type verbose: boolean, (Optional, default True)
    """

    def __init__(self, base_models=['linear', "xgboost"], b_cross_validation=True, n_jobs=4, verbose=True):
        """ The constructor for QReg.
        
        :param base_models: a list of regression model names, example ['linear', "xgboost"]. Currently "linear", "polynomial", "decisiontree", "xgboost", "gboost" are supported.
        :param b_cross_validation: whether cross-validation is used to train the base models, including xgboost, gboost, etc.
        :param n_jobs: the maximum cores to be used.
        :param verbose: control the logging level
        :type base_models: List of Strings, (Optional)
        :type b_cross_validation: Boolean, (Optional, default True)
        :type n_jobs: int, (Optional, default 4)
        :type verbose: boolean, (Optional, default True)

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
        """fit the QReg regression on the training data X and y.

        :param X: the independent variables, like [[1,2],[2,4]]
        :param y: the dependent variables, like [4, 8]
        :type X: numpy.ndarray
        :type y: numpy.ndarray
        :returns: the regression model
        :rtype: QReg

        :Example:

        >>> from qregpy import qreg
        >>> import pandas as pd
        >>> 
        >>> # load the files
        >>> df = pd.read_csv("/data/10k.csv")
        >>> headerX = ["ss_list_price", "ss_wholesale_cost"]
        >>> headerY = "ss_wholesale_cost"
        >>> 
        >>> # prepare X and y
        >>> X = df[headerX].values
        >>> y = df[headerY].values
        >>> 
        >>> # train the regression using base models linear regression and XGBoost regression.
        >>> reg = qreg.QReg(base_models=["linear","xgboost"], verbose=True).fit(X, y)
        >>> 
        >>> # make predictions
        >>> reg.predict([[93.35, 53.04], [60.84, 41.96]])
        [23.0, 11.1]

        .. note:: fit() receives X and y
        """
        start = datetime.now()

        if len(y) < 9:
            print("The minimum number of points supported by QReg is 9!!")
            print("Program terminates...")
            exit(1)

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
        """ Make a prediction for given points

                :param points: like [[1,2],[2,4]],  to make predictions for point [1,2] and point [2,4]
                :type points: numpy.ndarray
                :returns: the predictions for points
                :rtype: List of predictions

                :Example:

                >>> from qregpy import qreg
                >>> import pandas as pd
                >>> 
                >>> # load the files
                >>> df = pd.read_csv("/data/10k.csv")
                >>> headerX = ["ss_list_price", "ss_wholesale_cost"]
                >>> headerY = "ss_wholesale_cost"
                >>> 
                >>> # prepare X and y
                >>> X = df[headerX].values
                >>> y = df[headerY].values
                >>> 
                >>> # train the regression using base models linear regression and XGBoost regression.
                >>> reg = qreg.QReg(base_models=["linear","xgboost"], verbose=True).fit(X, y)
                >>> 
                >>> # make predictions
                >>> reg.predict([[93.35, 53.04], [60.84, 41.96]])
                [23.0, 11.1]

                .. note:: The input points should be numpy.ndarray
                """
        if self.b_use_classifier:
            return [
                self.model_catalog[self.model_catalog_names[self.classifier.predict(point)[0]]].predict([point]).flat[0]
                for point in points]
        else:
            return self.model_catalog[self.model_catalog_names[0]].predict(points)

    def deploy_sklearn_linear_regression(self, X, y):
        """ train the linear regression

        :param X: the independent variables, like [[1,2],[2,4]]
        :param y: the dependent variables, like [4, 8]
        :type X: numpy.ndarray
        :type y: numpy.ndarray
        :returns: the linear regression model
        :rtype: LinearRegression
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
        
        :param X: the independent variables, like [[1,2],[2,4]]
        :param y: the dependent variables, like [4, 8]
        :type X: numpy.ndarray
        :type y: numpy.ndarray
        :returns: the polynomial regression model
        :rtype: an polynomial regression object
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
        
        :param X: the independent variables, like [[1,2],[2,4]]
        :param y: the dependent variables, like [4, 8]
        :type X: numpy.ndarray
        :type y: numpy.ndarray
        :returns: the decision tree regression model
        :rtype: DecisionTreeRegressor
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
        
        :param X: the independent variables, like [[1,2],[2,4]]
        :param y: the dependent variables, like [4, 8]
        :type X: numpy.ndarray
        :type y: numpy.ndarray
        :returns: the XGBoost regression model
        :rtype: XGBRegressor
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
        
        :param X: the independent variables, like [[1,2],[2,4]]
        :param y: the dependent variables, like [4, 8]
        :type X: numpy.ndarray
        :type y: numpy.ndarray
        :returns: the gradient tree boosting regression model
        :rtype: GradientBoostingRegressor
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
        """ train the base regression models
        
        :param X: the independent variables, like [[1,2],[2,4]]
        :param y: the dependent variables, like [4, 8]
        :type X: numpy.ndarray
        :type y: numpy.ndarray
        """
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
        """
        Build the XGBoost classifier for QReg.

        :param X: the independent variables, like [[1,2],[2,4]]
        :param indexes: a list of index, showting the best base model
        :type X: numpy.ndarray
        :type indexes: List of int
        """
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

    # example 1
    # import pandas as pd
    # df = pd.read_csv("/data/dbest/data/10k.csv")
    # headerX = ["ss_list_price", "ss_wholesale_cost"]
    # headerY = "ss_wholesale_cost"
    #
    # X = df[headerX].values
    # y = df[headerY].values
    #
    # reg = QReg(base_models=["linear", "polynomial", "decisiontree", "xgboost", "gboost"], verbose=True).fit(X, y)
    # # print(reg.predict([[93.35], [60.84]]))
    # print(reg.predict([[93.35, 53.04], [60.84, 41.96]]))

    # example 2
    import numpy as np
    # The target fitting function is y=x1+2x2
    X = np.array([[1,2],[2,5],[3,7],[4,9],[1,3],[2,4], [3,5], [4,2], [5,1]])
    y= np.array([5.2, 12, 17.5, 21.2,7.2, 11,13, 7.8, 6.9])

    reg = QReg(base_models=["linear", "polynomial"], verbose=True).fit(X, y)

    print(reg.predict([[3,4]]))
