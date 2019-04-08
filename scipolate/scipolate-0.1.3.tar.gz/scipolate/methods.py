import numpy as np

from scipy.interpolate import griddata, Rbf
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, \
    AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from skgstat import Variogram, OrdinaryKriging

from .idw import Idw

def __points(x, y):
    return np.asarray((x, y), dtype=float).T


def __point_array(x, y):
    return np.concatenate((x, y)).reshape((2, len(x))).T.copy()


def __scipy_griddata(x, y, z, grid, method):
    points = __points(x, y)
    values = np.asarray(z)
    return griddata(points, values, grid, method=method)


def nearest(x, y, z, grid, **settings):
    return __scipy_griddata(x, y, z, grid, 'nearest')


def linear(x, y, z, grid, **settings):
    return __scipy_griddata(x, y, z, grid, 'linear')


def cubic(x, y, z, grid, **settings):
    return __scipy_griddata(x, y, z, grid, 'cubic')


def rbf(x, y, z, grid, func='thin_plate', epsilon=None, smooth=0.05,
        norm='euclidean', **settings):
    # create the object
    f = Rbf(x, y, z, function=func, epsilon=epsilon, smooth=smooth, norm=norm)

    # get the shape
    shape = grid[0].shape
    return f(grid[0].flatten(), grid[1].flatten()).reshape(shape)


def idw(x, y, z, grid, radius, min_points=3, max_points=15, fill_na=None,
        exp=2., **settings):
    f = Idw(x, y, z, radius,
            min_points=min_points,
            max_points=max_points,
            fill_na=fill_na,
            exp=exp
            )
    shape = grid[0].shape

    return f(grid[0].flatten(), grid[1].flatten()).reshape(shape)


def svm(x, y, z, grid, kernel='rbf', tol=1e-3, **settings):
    # fix gamma settings
    gamma = 'scale'

    # transform input data
    X = __point_array(x, y)
    target = z

    # transform the grid
    xx, yy = grid
    Xi = __point_array(xx.flatten(), yy.flatten())

    # train the model
    svr = SVR(gamma=gamma, kernel=kernel, tol=tol).fit(X, target)

    # apply
    return svr.predict(Xi).reshape(xx.shape)


def random_forest(x, y, z, grid, n_trees=100, max_depth=4, min_samples_split=2,
                  min_samples_leaf=1, **settings):
    # transform input data
    X = __point_array(x, y)
    target = z

    # transform the grid
    xx, yy = grid
    Xi = __point_array(xx.flatten(), yy.flatten())

    # train the model
    f = RandomForestRegressor(n_estimators=n_trees, max_depth=max_depth,
                              min_samples_split=min_samples_split,
                              min_samples_leaf=1).fit(X, target)

    # apply
    return f.predict(Xi).reshape(xx.shape)


def gb(x, y, z, grid, n_trees=100, learning_rate=0.1, max_depth=4,
       min_samples_split=2, min_samples_leaf=1, **settings):
    # transform input data
    X = __point_array(x, y)
    target = z

    # transform the grid
    xx, yy = grid
    Xi = __point_array(xx.flatten(), yy.flatten())

    # train the model
    f = GradientBoostingRegressor(
        n_estimators=n_trees,
        learning_rate=learning_rate,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf
    ).fit(X, target)

    # apply
    return f.predict(Xi).reshape(xx.shape)


def adaboost(x, y, z, grid, estimator='tree', n_estimators=50, learning_rate=1.,
             estimator_kwargs={}, **settings):
    # switch the estimator
    if estimator.lower() == 'tree':
        e = DecisionTreeRegressor(**estimator_kwargs)
    elif estimator.lower() == 'svm':
        estimator_kwargs['gamma'] = 'scale'
        e = SVR(**estimator_kwargs)
    else:
        raise ValueError("estimator has to be one of 'tree', 'svm'")

    # transform input data
    X = __point_array(x, y)
    target = z

    # transform grid
    xx, yy = grid
    Xi = __point_array(xx.flatten(), yy.flatten())

    # train the model
    f = AdaBoostRegressor(base_estimator=e, n_estimators=n_estimators,
                          learning_rate=learning_rate).fit(X, target)

    # apply
    return f.predict(Xi).reshape(xx.shape)


def adasvm(x, y, z, grid, n_estimators=10, learning_rate=0.1, kernel='rbf',
           tol=1e-3, **settings):
    kwargs = dict(kernel=kernel, tol=tol)
    return adaboost(x, y, z, grid, estimator='svm',
                    n_estimators=n_estimators, learning_rate=learning_rate,
                    estimator_kwargs=kwargs, **settings)


def adatree(x, y, z, grid, n_estimators=50, learning_rate=1., max_depth=3,
            min_samples_split=2, min_samples_leaf=1, **settings):
    kwargs = dict(
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf
    )
    return adaboost(x, y, z, grid, estimator='tree',
                    n_estimators=n_estimators, learning_rate=learning_rate,
                    estimator_kwargs=kwargs, **settings)


def ordinary_kriging(x, y, z, grid, model='spherical', estimator='matheron',
                     n_lags=15, maxlag='median', min_points=5, max_points=15,
                     mode='exact', precision=1000, **settings):
    # build coordinates
    coords = __point_array(x, y)

    # fit a Variogram
    V = Variogram(coords, z, model=model, estimator=estimator, n_lags=n_lags,
                  maxlag=maxlag, normalize=False)

    # get the shape and build the Kriging
    shape = grid[0].shape
    ok = OrdinaryKriging(V, min_points=min_points, max_points=max_points,
                         mode=mode, precision=precision)

    # apply
    return ok.transform(grid[0].flatten(), grid[1].flatten()).reshape(shape)
