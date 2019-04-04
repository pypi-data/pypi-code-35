"""
This script contains function to properly visualize matrices
"""

import numpy as np


def show_mat(matrix, title, show=False, save=False):
    """
    Show and/or save a matrix visualization.

    Parameters
    ----------
    matrix: 2d matrix
    title: Title of the plot
    show: Boolean to show the plot or not
    save: Boolean to save the plot or nor (automatic name from title)

    Returns
    -------
    None
    """
    import matplotlib.pyplot as plt

    try:
        # If matrix is a csr then take it back to numpy array
        data = matrix.toarray()
    except AttributeError:
        data = np.array(matrix)

    fig = plt.figure()
    plt.title(title)
    axes = fig.add_subplot(111)
    axes.set_xlabel(r"$j_{\rm NS}$")
    axes.set_ylabel(r"$i_{\rm WE}$")
    cax = axes.matshow(data)
    fig.colorbar(cax)
    plt.tight_layout()

    if save:
        name = filter_stupid_characters(title)
        plt.savefig('%s' % name)

    if show:
        plt.show()


def filter_stupid_characters(string):
    """
    Delete and replace stupid characters to save the figure

    Parameters
    ----------
    string: title of the plot to be changed into the filename

    Returns
    -------
    cleaned string
    """
    for char in [",", "$", "\\", " ", "__", "___"]:
        string = string.replace(char, "")

    if string.startswith("_"):
        string = string[1:-1]

    return string
