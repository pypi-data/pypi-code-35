# used to have a common interface
import numpy as np

from scipy.interpolate import griddata, Rbf
from sklearn.svm import SVR
from skgstat import Variogram, OrdinaryKriging

from .idw import Idw


def __points(x, y):
    return np.asarray((x, y), dtype=float).T


def __scipy_griddata(x, y, z, grid, method):
    points = __points(x, y)
    values = np.asarray(z)
    return griddata(points, values, grid, method=method)


def nearest(Intp, x, y, z, grid, **settings):
    return __scipy_griddata(x, y, z, grid, 'nearest')


def linear(Intp, x, y, z, grid, **settings):
    return __scipy_griddata(x, y, z, grid, 'linear')


def cubic(Intp, x, y, z, grid, **settings):
    return __scipy_griddata(x, y, z, grid, 'cubic')


def rbf(Intp, x, y, z, grid, **settings):
    # get the settings
    func = settings.get('func', 'thin_plate')
    #epsilon = settings.get('epsilon')
    smooth = settings.get('smooth', 0.0)
    norm = settings.get('norm', 'euclidean') # maybe this works with scipy 1.2

    # create the object
    f = Rbf(x, y, z, function=func, smooth=smooth)
    shape = grid[0].shape

    # apply
    return f(grid[0].flatten(), grid[1].flatten()).reshape(shape)


def idw(Intp, x, y, z, grid, **settings):
    # get settings
    radius = settings.get('radius', 5000)
    minp = settings.get('min_points', 4)
    maxp = settings.get('max_points', 20)
    na = settings.get('fill_na')
    exp = settings.get('exp')

    # create the object
    f = Idw(x, y, z, radius,
            min_points=minp,
            max_points=maxp,
            fill_na=na,
            exp=exp)
    shape = grid[0].shape

    # apply
    return f(grid[0].flatten(), grid[1].flatten()).reshape(shape)


def svm(Intp, x, y, z, grid, **settings):
    # get settings
    gamma = 'scale'
    kernel = settings.get('kernel', 'rbf')
    tol = settings.get('tol', 1e-3)

    # transform x,y and grid
    X = np.concatenate((x, y)).reshape(2, len(x)).T.copy()
    target = np.asarray(z)
    xx, yy = grid
    Xi = np.concatenate((xx.flatten(), yy.flatten()))
    Xi = Xi.reshape(2, len(xx.flatten())).T.copy()

    # create SVC instance and fit
    svr = SVR(gamma=gamma, kernel=kernel, tol=tol).fit(X, target)

    # apply
    return svr.predict(Xi).reshape(xx.shape)

def ordinary_kriging(Intp, x, y, z, grid, **settings):
    # get the settings
    model = settings.get('model', 'gaussian')
    estimator = settings.get('estimator', 'matheron')
    n_lags = settings.get('n_lags', 15)
    maxlag = settings.get('maxlag', 'median')
    minp = settings.get('min_points', 5)
    maxp = settings.get('max_points', 15)
    mode = settings.get('mode', 'estimate')
    precision = settings.get('precision', 1000)

    # build the coordinates
    coords = np.concatenate((x, y)).reshape(2, len(x)).T.copy()

    # create the Variogram
    v = Variogram(coords, z, 
            estimator=estimator, 
            model=model, 
            n_lags=n_lags,
            maxlag=maxlag,
            normalize=False
        )

    # plot the variogram
    fig = v.plot(show=False)
    img = Intp.img_to_base64(fig)
    Intp.report['score'] = dict(plot=img, name='Variogram')
 
    # kriging
    shape = grid[0].shape
    ok = OrdinaryKriging(v, min_points=minp, max_points=maxp, mode=mode, precision=precision)

    return ok.transform(grid[0].flatten(), grid[1].flatten()).reshape(shape)
