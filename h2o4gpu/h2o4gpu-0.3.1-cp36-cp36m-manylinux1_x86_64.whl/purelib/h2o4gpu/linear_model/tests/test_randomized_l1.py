# Authors: Alexandre Gramfort <alexandre.gramfort@inria.fr>
# License: BSD 3 clause

from tempfile import mkdtemp
import shutil

import numpy as np
from scipy import sparse

from h2o4gpu.utils.testing import assert_equal
from h2o4gpu.utils.testing import assert_array_equal
from h2o4gpu.utils.testing import assert_raises
from h2o4gpu.utils.testing import assert_raises_regex
from h2o4gpu.utils.testing import assert_allclose
from h2o4gpu.utils.testing import ignore_warnings
from h2o4gpu.utils.testing import assert_warns_message

from h2o4gpu.linear_model.randomized_l1 import(lasso_stability_path,
                                               RandomizedLassoSklearn,
                                               RandomizedLogisticRegressionSklearn)

from h2o4gpu.datasets import load_diabetes, load_iris
from h2o4gpu.feature_selection import f_regression, f_classif
from h2o4gpu.preprocessing import StandardScaler
from h2o4gpu.linear_model.base import _preprocess_data

diabetes = load_diabetes()
X = diabetes.data
y = diabetes.target
X = StandardScaler().fit_transform(X)
X = X[:, [2, 3, 6, 7, 8]]

# test that the feature score of the best features
F, _ = f_regression(X, y)


@ignore_warnings(category=DeprecationWarning)
def test_lasso_stability_path():
    # Check lasso stability path
    # Load diabetes data and add noisy features
    scaling = 0.3
    coef_grid, scores_path = lasso_stability_path(X, y, scaling=scaling,
                                                  random_state=42,
                                                  n_resampling=30)

    assert_array_equal(np.argsort(F)[-3:],
                       np.argsort(np.sum(scores_path, axis=1))[-3:])


@ignore_warnings(category=DeprecationWarning)
def test_randomized_lasso_error_memory():
    scaling = 0.3
    selection_threshold = 0.5
    tempdir = 5
    clf = RandomizedLassoSklearn(verbose=False, alpha=[1, 0.8], random_state=42,
                          scaling=scaling,
                          selection_threshold=selection_threshold,
                          memory=tempdir)
    assert_raises_regex(ValueError, "'memory' should either be a string or"
                        " a h2o4gpu.utils.Memory instance",
                        clf.fit, X, y)


@ignore_warnings(category=DeprecationWarning)
def test_randomized_lasso():
    # Check randomized lasso
    scaling = 0.3
    selection_threshold = 0.5
    n_resampling = 20

    # or with 1 alpha
    clf = RandomizedLassoSklearn(verbose=False, alpha=1, random_state=42,
                          scaling=scaling, n_resampling=n_resampling,
                          selection_threshold=selection_threshold)
    feature_scores = clf.fit(X, y).scores_
    assert_array_equal(np.argsort(F)[-3:], np.argsort(feature_scores)[-3:])

    # or with many alphas
    clf = RandomizedLassoSklearn(verbose=False, alpha=[1, 0.8], random_state=42,
                          scaling=scaling, n_resampling=n_resampling,
                          selection_threshold=selection_threshold)
    feature_scores = clf.fit(X, y).scores_
    assert_equal(clf.all_scores_.shape, (X.shape[1], 2))
    assert_array_equal(np.argsort(F)[-3:], np.argsort(feature_scores)[-3:])
    # test caching
    try:
        tempdir = mkdtemp()
        clf = RandomizedLassoSklearn(verbose=False, alpha=[1, 0.8], random_state=42,
                              scaling=scaling,
                              selection_threshold=selection_threshold,
                              memory=tempdir)
        feature_scores = clf.fit(X, y).scores_
        assert_equal(clf.all_scores_.shape, (X.shape[1], 2))
        assert_array_equal(np.argsort(F)[-3:], np.argsort(feature_scores)[-3:])
    finally:
        shutil.rmtree(tempdir)

    X_r = clf.transform(X)
    X_full = clf.inverse_transform(X_r)
    assert_equal(X_r.shape[1], np.sum(feature_scores > selection_threshold))
    assert_equal(X_full.shape, X.shape)

    clf = RandomizedLassoSklearn(verbose=False, alpha='aic', random_state=42,
                          scaling=scaling, n_resampling=100)
    feature_scores = clf.fit(X, y).scores_
    assert_allclose(feature_scores, [1., 1., 1., 0.225, 1.], rtol=0.2)

    clf = RandomizedLassoSklearn(verbose=False, scaling=-0.1)
    assert_raises(ValueError, clf.fit, X, y)

    clf = RandomizedLassoSklearn(verbose=False, scaling=1.1)
    assert_raises(ValueError, clf.fit, X, y)


@ignore_warnings(category=DeprecationWarning)
def test_randomized_lasso_precompute():
    # Check randomized lasso for different values of precompute
    n_resampling = 20
    alpha = 1
    random_state = 42

    G = np.dot(X.T, X)

    clf = RandomizedLassoSklearn(alpha=alpha, random_state=random_state,
                          precompute=G, n_resampling=n_resampling)
    feature_scores_1 = clf.fit(X, y).scores_

    for precompute in [True, False, None, 'auto']:
        clf = RandomizedLassoSklearn(alpha=alpha, random_state=random_state,
                              precompute=precompute, n_resampling=n_resampling)
        feature_scores_2 = clf.fit(X, y).scores_
        assert_array_equal(feature_scores_1, feature_scores_2)


@ignore_warnings(category=DeprecationWarning)
def test_randomized_logistic():
    # Check randomized sparse logistic regression
    iris = load_iris()
    X = iris.data[:, [0, 2]]
    y = iris.target
    X = X[y != 2]
    y = y[y != 2]

    F, _ = f_classif(X, y)

    scaling = 0.3
    clf = RandomizedLogisticRegressionSklearn(verbose=False, C=1., random_state=42,
                                       scaling=scaling, n_resampling=50,
                                       tol=1e-3)
    X_orig = X.copy()
    feature_scores = clf.fit(X, y).scores_
    assert_array_equal(X, X_orig)   # fit does not modify X
    assert_array_equal(np.argsort(F), np.argsort(feature_scores))

    clf = RandomizedLogisticRegressionSklearn(verbose=False, C=[1., 0.5],
                                       random_state=42, scaling=scaling,
                                       n_resampling=50, tol=1e-3)
    feature_scores = clf.fit(X, y).scores_
    assert_array_equal(np.argsort(F), np.argsort(feature_scores))

    clf = RandomizedLogisticRegressionSklearn(verbose=False, C=[[1., 0.5]])
    assert_raises(ValueError, clf.fit, X, y)


@ignore_warnings(category=DeprecationWarning)
def test_randomized_logistic_sparse():
    # Check randomized sparse logistic regression on sparse data
    iris = load_iris()
    X = iris.data[:, [0, 2]]
    y = iris.target
    X = X[y != 2]
    y = y[y != 2]

    # center here because sparse matrices are usually not centered
    # labels should not be centered
    X, _, _, _, _ = _preprocess_data(X, y, True, True)

    X_sp = sparse.csr_matrix(X)

    F, _ = f_classif(X, y)

    scaling = 0.3
    clf = RandomizedLogisticRegressionSklearn(verbose=False, C=1., random_state=42,
                                       scaling=scaling, n_resampling=50,
                                       tol=1e-3)
    feature_scores = clf.fit(X, y).scores_
    clf = RandomizedLogisticRegressionSklearn(verbose=False, C=1., random_state=42,
                                       scaling=scaling, n_resampling=50,
                                       tol=1e-3)
    feature_scores_sp = clf.fit(X_sp, y).scores_
    assert_array_equal(feature_scores, feature_scores_sp)


def test_warning_raised():

    scaling = 0.3
    selection_threshold = 0.5
    tempdir = 5
    assert_warns_message(DeprecationWarning, "The function"
                         " lasso_stability_path is "
                         "deprecated in 0.19 and will be removed in 0.21.",
                         lasso_stability_path, X, y, scaling=scaling,
                         random_state=42, n_resampling=30)

    assert_warns_message(DeprecationWarning, "Class RandomizedLassoSklearn is"
                         " deprecated; The class RandomizedLassoSklearn is "
                         "deprecated in 0.19 and will be removed in 0.21.",
                         RandomizedLassoSklearn, verbose=False, alpha=[1, 0.8],
                         random_state=42, scaling=scaling,
                         selection_threshold=selection_threshold,
                         memory=tempdir)

    assert_warns_message(DeprecationWarning, "The class"
                         " RandomizedLogisticRegressionSklearn is "
                         "deprecated in 0.19 and will be removed in 0.21.",
                         RandomizedLogisticRegressionSklearn,
                         verbose=False, C=1., random_state=42,
                         scaling=scaling, n_resampling=50,
                         tol=1e-3)
