"""
Modules for common GP visualizations.
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

def plot_covariance():
    """
    Plot a heatmap of a covariance matrix.
    """
    raise NotImplementedError()
