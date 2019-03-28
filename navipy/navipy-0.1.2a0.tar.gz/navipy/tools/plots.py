"""
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import numpy as np
import pandas as pd


def get_color_frame_dataframe(frame_range=[0, 100], cmap=plt.get_cmap('jet')):
    """

Get a colorframe from a range


Return a pandas dataframe indexed by frame number,here colors are \
calculated from a matplotlib cmap generates a pandas data frame \
representing the data frames specified in frame_range, where all \
frames with an index between the maximum and minimum number given \
in frame_range is considered. This pandas data frame is then used \
to call get_color_dataframe()

calls get_color_dataframe()

Arguments

        - Input:
                - frame_range: (default: 0 to 100), 1 dimensional \
array of integers
                - cmap: (default: jet colormap) colormap to be used

        - Output:
                - a color dataframe (pandas table) and the \
corresponding color-map (scalar mappable)
    """

    frame_series = pd.Series(index=np.arange(
        min(frame_range), max(frame_range) + 1))  # +1 include the last frame
    frame_series[:] = np.linspace(0, 1, frame_series.shape[0])
    return get_color_dataframe(frame_series, cmap=cmap)


def get_color_dataframe(series, cmap=plt.get_cmap('jet')):
    """
Get a color Frame from a series

Return a color dataframe from a series. Each value in the series \
table gets a corresponding rbga color value in the returned color \
dataframe with the same index.

>>> df_colors,sm = get_color_dataframe(series,cmap=plt.get_cmap('jet'))

Arguments
---------

Input:
        - series: pandas frame that contains indexed values; \
indices do not need to be in order values in in series is used \
to generate the color map
Output:
        - df_colors: pandas data-frame that contains the colormap; \
the color that corresponds to the value in series has the same \
index as in series.
        - sm: the actual color map
    """

    # The values in the serie need to be normalized between 0 and 1 first
    # We do not want to affect the series
    normalised_values = series.values.copy()
    # substract offset from values, so the smalles one is zero
    normalised_values -= normalised_values.min()
    # all values are zero and have the same value
    if normalised_values.max() == 0:
        raise ValueError('series.values are constant')
    # actually normalize the values
    normalised_values = normalised_values / normalised_values.max()
    colors = cmap(normalised_values)
    # create the dataframe from color
    df_colors = pd.DataFrame(
        data=colors, index=series.index, columns=['r', 'g', 'b', 'a'])

    # Create data for colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap,
                               norm=plt.Normalize(
                                   vmin=series.values.min(),
                                   vmax=series.values.max()))
    # fake up the array of the scalar mappable. Urgh...
    sm._A = []

    return df_colors, sm


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)


def draw_frame(frame,
               ax=plt.gca(),
               mutation_scale=20, lw=3,
               arrowstyle="-|>", colors=['r', 'g', 'b']):
    if not isinstance(frame, (np.ndarray, np.generic)):
        raise TypeError('frame should be a numpy array')
    if len(frame.shape) != 2:
        raise TypeError('frame should have 2 dimensions')
    if not np.all(frame.shape == [4, 4]):
        frame = frame[:3, :]
    if not np.all(frame.shape != [3, 4]):
        raise TypeError('frame should be a 3x4 or 4x4 matrix')

    origin = frame[:, 3]
    for (i, color) in enumerate(colors):
        v = frame[:, i]
        xs = [origin[0], origin[0] + v[0]]
        ys = [origin[1], origin[1] + v[1]]
        zs = [origin[2], origin[2] + v[2]]
        a = Arrow3D(xs, ys, zs,
                    mutation_scale=mutation_scale,
                    lw=lw,
                    arrowstyle=arrowstyle,
                    color=color)
        ax.add_artist(a)
