import matplotlib.pyplot as plt
import numpy as np
from arnica.solvers_2d.radiation import filter_stupid_characters
from matplotlib.colors import LogNorm


def heat_map_mesh(x, y, z, show=False, save=True):
    """ heat map plot of skin """

    plt.rcParams['image.cmap'] = 'Blues'

    def get_bins(x, y):
        """Computes equal bins from aspect ratio"""
        l_y = np.abs(np.max(y) - np.min(x))
        l_x = np.abs(np.max(x) - np.min(x))
        ratio = l_y / l_x
        return 500., 500. * ratio

    def plot_skin(tuple_data, tuple_labels):
        """Plot skin as hist2d"""
        x, y = tuple_data
        x_label, y_label = tuple_labels

        fig = plt.figure()
        ax = fig.add_subplot(111)

        title = "%s, %s" % tuple_labels
        ax.set_title(title)
        ax.hist2d(x, y, bins=get_bins(x, y), norm=LogNorm())
        ax.set_xlabel("%s" % x_label)
        ax.set_ylabel("%s" % y_label)
        ax.set_aspect(aspect=1)
        if save:
            name = filter_stupid_characters(title)
            plt.savefig('%s' % name)

    radius = np.hypot(y, z)
    plot_skin((x, radius), ('$x$', '$r$'))
    plot_skin((x, z), ('$y$', '$z$'))
    plot_skin((x, y), ('$x$', '$y$'))
    plot_skin((z, y), ('$z$', '$y$'))

    if show:
        plt.show()


def scatter_plot_mesh(x, y, z, axisym=False, show=False):
    """ scatter plot of skin """

    if axisym:
        radius = np.sqrt(np.square(x) + np.square(y))
        theta = np.arctan2(z, y)

        plt.figure()
        plt.title(r"x, theta")
        plt.scatter(x, theta, edgecolors='none', alpha=0.25)
        plt.xlabel("x")
        plt.xlabel("theta")

        plt.figure()
        plt.title("x, r")
        plt.scatter(x, radius, edgecolors='none', alpha=0.25)
        plt.xlabel("x")
        plt.xlabel("x")

        plt.figure()
        plt.title("r, theta")
        plt.scatter(radius, theta, edgecolors='none', alpha=0.25)
        plt.xlabel("r")
        plt.xlabel("theta")
    else:
        plt.figure()
        plt.title("z, y")
        plt.scatter(z, y, edgecolors='none', alpha=0.25)
        plt.xlabel("z")
        plt.xlabel("y")

        plt.figure()
        plt.title("x, y")
        plt.scatter(x, y, edgecolors='none', alpha=0.25)
        plt.xlabel("x")
        plt.xlabel("y")

        plt.figure()
        plt.title("x, z")
        plt.scatter(x, z, edgecolors='none', alpha=0.25)
        plt.xlabel("x")
        plt.xlabel("z")

    if show:
        plt.show()
