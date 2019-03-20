from drifter_ml import classification_tests
import joblib
import pandas as pd
import numpy as np
import code
from sklearn import metrics

def test():
    df = pd.read_csv("data.csv")
    column_names = ["A", "B", "C"]
    target_name = "target"
    clf = joblib.load("model1.joblib")

    test_suite = classification_tests.ClassificationTests(clf,
                                                          df,
                                                          target_name,
                                                          column_names)
    classes = list(df.target.unique())
    assert test_suite.classifier_testing(
        {klass: 0.9 for klass in classes},
        {klass: 0.9 for klass in classes},
        {klass: 0.9 for klass in classes}
    )
    
def precision_lower_boundary_per_class(clf, X, y, classes, lower_boundary):
    y_pred = clf.predict(X)
    for klass in classes:
        y_pred_class = np.take(y_pred, y[y == klass].index, axis=0)
        y_class = y[y == klass]
        result = metrics.precision_score(y_class, y_pred_class) 
        code.interact(local=locals())

if __name__ == '__main__':    
    df = pd.read_csv("data.csv")
    column_names = ["A", "B", "C"]
    target_name = "target"
    clf = joblib.load("model1.joblib")
    code.interact(local=locals())
    test_suite = classification_tests.ClassificationTests(clf,
                                                          df,
                                                          target_name,
                                                          column_names)
    classes = list(df.target.unique())
    #test_suite.precision_lower_boundary_per_class(
    #    {klass: 0.9 for klass in classes}
    #)
    boundary = {klass: 0.9 for klass in classes}
    precision_lower_boundary_per_class(clf, df[column_names], df[target_name], classes, boundary)
    code.interact(local=locals())
