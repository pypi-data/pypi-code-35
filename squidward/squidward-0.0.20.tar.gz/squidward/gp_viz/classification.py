"""
Modules for GPC visualizations.
"""

import numpy as np
from mpl_toolkits.mplot3d import axes3d
from squidward.utils import make_grid, exactly_1d

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
except:
    import matplotlib
    matplotlib.use('PS')
    from matplotlib import pyplot as plt
    import seaborn as sns

def plot_contour(model, coordinates=(-1, 1, .1), show_var=False):
    """
    Description
    ----------
    Function to plot a contour plot for a two dimensional guassian process
    classifier.

    Parameters
    ----------
    Model: gaussian process classification model object
        A gaussian process classification (gpc) model object.
    Coordinates: Tuple
        A tuple with the minimum and maximum values of the contour and
        the interval over which to the contour.
        i.e. (min,max,interval)
    Show_var: boolean
        If True, will plot the variance contour. If
        False, will plot the mean contour.

    Returns
    ----------
    Matplotlib plot of mean function or variance of the gaussian process
    model as a contour plot.
    """
    x_test, size = make_grid(coordinates)
    if not show_var:
        mean = model.posterior_predict(x_test)
        predictions = mean.argmax(axis=1)
        zed = predictions.T.reshape(size, size)
    else:
        mean, var = model.posterior_predict(x_test, True)
        zed = np.mean(var, axis=1).T.reshape(size, size)
    alpha, beta = x_test.T.reshape(2, size, size)
    plt.contourf(alpha, beta, zed, 20, cmap='Blues')
    plt.colorbar()
    contours = plt.contour(alpha, beta, zed, 5, colors='black')
    plt.clabel(contours, inline=True, fontsize=8)
    return None
