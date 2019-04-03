"""
Matplotlib specific plotting
"""
import tfields

import numpy as np
import warnings
import os
import matplotlib as mpl
import matplotlib.ticker
from matplotlib import style
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d as plt3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.dates as dates
from matplotlib.patches import Rectangle
from itertools import cycle
from functools import partial
import logging


def show():
    plt.show()


def gca(dim=None, **kwargs):
    """
    Forwarding to plt.gca but translating the dimension to projection
    correct dimension
    """
    if dim == 3:
        axis = plt.gca(projection='3d', **kwargs)
    else:
        axis = plt.gca(**kwargs)
        if dim != axis_dim(axis):
            if dim is not None:
                warnings.warn("You have another dimension set as gca."
                              "I will force the new dimension to return.")
                axis = plt.gcf().add_subplot(1, 1, 1, **kwargs)
    return axis


def upgrade_style(style, source, dest=None):
    """
    Copy a style file at <origionalFilePath> to the <dest> which is the foreseen
    local matplotlib rc dir by default
    The style will be name <style>.mplstyle
    Args:
        style (str): name of style
        source (str): full path to mplstyle file to use
        dest (str): local directory to copy the file to. Matpotlib has to
            search this directory for mplstyle files!
    Examples:
        >>> import tfields
        >>> import os
        >>> tfields.plotting.upgrade_style(
        ...     'tfields',
        ...     os.path.join(os.path.dirname(tfields.plotting.__file__),
        ...                  'tfields.mplstyle'))

    """
    if dest is None:
        dest = mpl.get_configdir()
    style_extension = 'mplstyle'
    path = tfields.lib.in_out.resolve(os.path.join(dest, style + '.' +
                                                   style_extension))
    source = tfields.lib.in_out.resolve(source)
    tfields.lib.in_out.cp(source, path)


def set_style(style='tfields', dest=None):
    """
    Set the matplotlib style of name
    Important:
        Either you
    Args:
        style (str)
        dest (str): local directory to use file from. if None, use default
            maplotlib destination
    """
    if dest is None:
        dest = mpl.get_configdir()

    style_extension = 'mplstyle'
    path = tfields.lib.in_out.resolve(os.path.join(dest, style + '.' +
                                                   style_extension))
    if style in mpl.style.available:
        plt.style.use(style)
    elif os.path.exists(path):
        plt.style.use(path)
    else:
        log = logging.getLogger()
        if style == 'tfields':
            log.warning("I will copy the default style to {dest}."
                        .format(**locals()))
            source = os.path.join(os.path.dirname(__file__),
                                  style + '.' + style_extension)
            try:
                upgrade_style(style, source, dest)                
                set_style(style)
            except Exception:
                log.error("Could not set style")
        else:
            log.error("Could not set style {path}. Probably you would want to"
                      "call tfields.plotting.upgrade_style(<style>, "
                      "<path to mplstyle file that should be copied>)"
                      "once".format(**locals()))


def save(path, *fmts, **kwargs):
    """
    Args:
        path (str): path without extension to save to
        *fmts (str): format of the figure to save. If multiple are given, create
            that many files
        **kwargs:
            axis
            fig
    """
    log = logging.getLogger()

    # catch figure from axis or fig
    axis = kwargs.get('axis', None)
    if axis is None:
        fig_default = plt.gcf()
        axis = gca()
        if fig_default is None:
            raise ValueError("fig_default may not be None")
    else:
        fig_default = axis.figure
    fig = kwargs.get('fig', fig_default)

    # set current figure
    plt.figure(fig.number)

    # crop the plot down based on the extents of the artists in the plot
    kwargs['bbox_inches'] = kwargs.pop('bbox_inches', 'tight')
    if kwargs['bbox_inches'] == 'tight':
        extra_artists = None
        for ax in fig.get_axes():
            first_label = ax.get_legend_handles_labels()[0] or None
            if first_label:
                if not extra_artists:
                    extra_artists = []
                if isinstance(first_label, list):
                    extra_artists.extend(first_label)
                else:
                    extra_artists.append(first_label)
        kwargs['bbox_extra_artists'] = kwargs.pop('bbox_extra_artists',
                                                  extra_artists)

    if len(fmts) != 0:
        for fmt in fmts:
            if path.endswith('.'):
                new_file_path = path + fmt
            elif '{fmt}' in path:
                new_file_path = path.format(**locals())
            else:
                new_file_path = path + '.' + fmt
            save(new_file_path, **kwargs)
    else:
        path = tfields.lib.in_out.resolve(path)
        log.info("Saving figure as {0}".format(path))
        plt.savefig(path,
                    **kwargs)


def plot_array(array, **kwargs):
    """
    Points3D plotting method.

    Args:
        array (numpy array)
        axis (matplotlib.Axis) object
        xAxis (int): coordinate index that should be on xAxis
        yAxis (int): coordinate index that should be on yAxis
        zAxis (int or None): coordinate index that should be on zAxis.
            If it evaluates to None, 2D plot will be done.
        methodName (str): method name to use for filling the axis

    Returns:
        Artist or list of Artists (imitating the axis.scatter/plot behaviour).
        Better Artist not list of Artists
    """
    array = np.array(array)
    tfields.plotting.set_default(kwargs, 'methodName', 'scatter')
    po = tfields.plotting.PlotOptions(kwargs)

    labels = po.pop('labels', ['x (m)', 'y (m)', 'z (m)'])
    xAxis, yAxis, zAxis = po.getXYZAxis()
    tfields.plotting.set_labels(po.axis, *po.getSortedLabels(labels))
    if zAxis is None:
        args = [array[:, xAxis],
                array[:, yAxis]]
    else:
        args = [array[:, xAxis],
                array[:, yAxis],
                array[:, zAxis]]
    artist = po.method(*args,
                       **po.plot_kwargs)
    return artist


def plot_mesh(vertices, faces, **kwargs):
    """
    Args:
        axis (matplotlib axis)
        xAxis (int)
        yAxis (int)
        zAxis (int)
        edgecolor (color)
        color (color): if given, use this color for faces in 2D
        cmap
        vmin
        vmax
    """
    vertices = np.array(vertices)
    faces = np.array(faces)
    if faces.shape[0] == 0:
        warnings.warn("No faces to plot")
        return None
    if max(faces.flat) > vertices.shape[0]:
        raise ValueError("Some faces point to non existing vertices.")
    po = tfields.plotting.PlotOptions(kwargs)
    if po.dim == 2:
        full = True
        mesh = tfields.Mesh3D(vertices, faces=faces)
        xAxis, yAxis, zAxis = po.getXYZAxis()
        facecolors = po.retrieve_chain('facecolors', 'color',
                                       default=0,
                                       keep=False)
        if full:
            # implementation that will sort the triangles by zAxis
            centroids = mesh.centroids()
            axesIndices = [0, 1, 2]
            axesIndices.pop(axesIndices.index(xAxis))
            axesIndices.pop(axesIndices.index(yAxis))
            zAxis = axesIndices[0]
            zs = centroids[:, zAxis]
            try:
                iter(facecolors)
                zs, faces, facecolors = tfields.lib.util.multi_sort(zs, faces,
                                                                    facecolors)
            except TypeError:
                zs, faces = tfields.lib.util.multi_sort(zs, faces)
            
            nFacesInitial = len(faces)
        else:
            # cut away "back sides" implementation
            directionVector = np.array([1., 1., 1.])
            directionVector[xAxis] = 0.
            directionVector[yAxis] = 0.
            normVectors = mesh.triangles().norms()
            dotProduct = np.dot(normVectors, directionVector)
            nFacesInitial = len(faces)
            faces = faces[dotProduct > 0]

        vertices = mesh

        po.plot_kwargs['methodName'] = 'tripcolor'
        po.plot_kwargs['triangles'] = faces

        """
        sort out color arguments
        """
        facecolors = po.format_colors(facecolors,
                                      fmt='norm',
                                      length=nFacesInitial)
        if not full:
            facecolors = facecolors[dotProduct > 0]
        po.plot_kwargs['facecolors'] = facecolors

        d = po.plot_kwargs
        d['xAxis'] = xAxis
        d['yAxis'] = yAxis
        artist = plot_array(vertices, **d)
    elif po.dim == 3:
        label = po.pop('label', None)
        color = po.retrieve_chain('color', 'c', 'facecolors',
                                  default='grey',
                                  keep=False)
        color = po.format_colors(color,
                                 fmt='rgba',
                                 length=len(faces))
        nanMask = np.isnan(color)
        if nanMask.any():
            warnings.warn("nan found in colors. Removing the corresponding faces!")
            color = color[~nanMask]
            faces = faces[~nanMask]

        edgecolor = po.pop('edgecolor', None)
        alpha = po.pop('alpha', None)
        po.delNormArgs()

        triangles = np.array([vertices[face] for face in faces])
        artist = plt3D.art3d.Poly3DCollection(triangles, **po.plot_kwargs)
        po.axis.add_collection3d(artist)

        if edgecolor is not None:
            artist.set_edgecolor(edgecolor)
            artist.set_facecolors(color)
        else:
            artist.set_color(color)

        if alpha is not None:
            artist.set_alpha(alpha)

        # for some reason auto-scale does not work
        tfields.plotting.autoscale_3d(po.axis, array=vertices)

        # legend lables do not work at all as an argument
        if label:
            artist.set_label(label)

        # when plotting the legend edgecolors/facecolors2d are needed
        artist._edgecolors2d = None
        artist._facecolors2d = None

        labels = ['x (m)', 'y (m)', 'z (m)']
        tfields.plotting.set_labels(po.axis, *po.getSortedLabels(labels))

    else:
        raise NotImplementedError("Dimension != 2|3")

    return artist


def plot_tensor_field(points, field, **kwargs):
    """
    Args:
        points (array_like): base vectors
        field (): direction field
    """
    po = tfields.plotting.PlotOptions(kwargs)
    field = np.array(field)
    if len(field.shape) == 2 and field.shape[1] == 1:
        # scalar
        field = field.reshape(len(points))
    if len(field.shape) == 1:
        # scalar
        colors = po.format_colors(field)
        po.delNormArgs()
        artists = plot_array(points, c=colors, **po.plot_kwargs)
        artists.set_array(field)
    elif len(field.shape) == 2:
        # vector
        if points is None:
            points = np.full(field.shape, 0.)
        xAxis, yAxis, zAxis = po.getXYZAxis()
        artists = []
        for point, vector in zip(points, field):
            if po.dim == 3:
                artists.append(
                    po.axis.quiver(
                        point[xAxis], point[yAxis], point[zAxis],
                        vector[xAxis], vector[yAxis], vector[zAxis],
                        **po.plot_kwargs))
            elif po.dim == 2:
                artists.append(po.axis.quiver(point[xAxis], point[yAxis],
                                              vector[xAxis], vector[yAxis],
                                              **po.plot_kwargs))
            else:
                raise NotImplementedError("Dimension != 2|3")
    else:
        raise NotImplementedError("Only Scalars and Vectors implemented")
    return artists


def plot_plane(point, normal, **kwargs):

    def plot_vector(fig, orig, v, color='blue'):
        axis = fig.gca(projection='3d')
        orig = np.array(orig)
        v = np.array(v)
        axis.quiver(orig[0], orig[1], orig[2], v[0], v[1], v[2], color=color)
        axis.set_xlim(0, 10)
        axis.set_ylim(0, 10)
        axis.set_zlim(0, 10)
        axis = fig.gca(projection='3d')
        return fig

    def rotation_matrix(d):
        sin_angle = np.linalg.norm(d)
        if sin_angle == 0:
            return np.identity(3)
        d /= sin_angle
        eye = np.eye(3)
        ddt = np.outer(d, d)
        skew = np.array([[0, d[2], -d[1]],
                         [-d[2], 0, d[0]],
                         [d[1], -d[0], 0]],
                        dtype=np.float64)

        M = ddt + np.sqrt(1 - sin_angle**2) * (eye - ddt) + sin_angle * skew
        return M

    def pathpatch_2d_to_3d(pathpatch, z, normal):
        if type(normal) is str:  # Translate strings to normal vectors
            index = "xyz".index(normal)
            normal = np.roll((1.0, 0, 0), index)

        normal /= np.linalg.norm(normal)  # Make sure the vector is normalised
        path = pathpatch.get_path()  # Get the path and the associated transform
        trans = pathpatch.get_patch_transform()

        path = trans.transform_path(path)  # Apply the transform

        pathpatch.__class__ = plt3D.art3d.PathPatch3D  # Change the class
        pathpatch._code3d = path.codes  # Copy the codes
        pathpatch._facecolor3d = pathpatch.get_facecolor  # Get the face color

        verts = path.vertices  # Get the vertices in 2D

        d = np.cross(normal, (0, 0, 1))  # Obtain the rotation vector
        M = rotation_matrix(d)  # Get the rotation matrix

        pathpatch._segment3d = np.array([np.dot(M, (x, y, 0)) + (0, 0, z) for x, y in verts])

    def pathpatch_translate(pathpatch, delta):
        pathpatch._segment3d += delta

    kwargs['alpha'] = kwargs.pop('alpha', 0.5)
    po = tfields.plotting.PlotOptions(kwargs)
    patch = Circle((0, 0), **po.plot_kwargs)
    po.axis.add_patch(patch)
    pathpatch_2d_to_3d(patch, z=0, normal=normal)
    pathpatch_translate(patch, (point[0], point[1], point[2]))


def plot_sphere(point, radius, **kwargs):
    po = tfields.plotting.PlotOptions(kwargs)
    # Make data
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = point[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = point[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = point[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))

    # Plot the surface
    return po.axis.plot_surface(x, y, z, **po.plot_kwargs)


def plot_function(fun, **kwargs):
    """
    Args:
        axis (matplotlib.Axis) object

    Returns:
        Artist or list of Artists (imitating the axis.scatter/plot behaviour).
        Better Artist not list of Artists
    """
    import numpy as np
    labels = ['x', 'f(x)']
    po = tfields.plotting.PlotOptions(kwargs)
    tfields.plotting.set_labels(po.axis, *labels)
    xMin, xMax = po.pop('xMin', 0), po.pop('xMax', 1)
    n = po.pop('n', 100)
    vals = np.linspace(xMin, xMax, n)
    args = (vals, map(fun, vals))
    artist = po.axis.plot(*args,
                          **po.plot_kwargs)
    return artist


def plot_errorbar(points, errors_up, errors_down=None, **kwargs):
    """
    Args:
        axis (matplotlib.Axis) object

    Returns:
        Artist or list of Artists (imitating the axis.scatter/plot behaviour).
        Better Artist not list of Artists
    """
    po = tfields.plotting.PlotOptions(kwargs)
    po.set_default('marker', '_')

    if errors_down is None:
        errors_down = errors_up

    artists = []

    # plot points
    # artists.append(po.axis.plot(points, **po.plot_kwargs))

    # plot errorbars
    for i in range(len(points)):
        artists.append(
            po.axis.plot([points[i, 0] + errors_up[i, 0],
                          points[i, 0] - errors_down[i, 0]],
                         [points[i, 1], points[i, 1]],
                         [points[i, 2], points[i, 2]],
                         **po.plot_kwargs))
        artists.append(
            po.axis.plot([points[i, 0], points[i, 0]],
                         [points[i, 1] + errors_up[i, 1],
                          points[i, 1] - errors_down[i, 1]],
                         [points[i, 2], points[i, 2]],
                         **po.plot_kwargs))
        artists.append(
            po.axis.plot([points[i, 0], points[i, 0]],
                         [points[i, 1], points[i, 1]],
                         [points[i, 2] + errors_up[i, 2],
                          points[i, 2] - errors_down[i, 2]],
                         **po.plot_kwargs))

    return artists


"""
Color section
"""


def to_colors(scalars, cmap=None, vmin=None, vmax=None):
    """
    retrieve the colors for a list of scalars
    """
    if not hasattr(scalars, '__iter__'):
        scalars = [scalars]
    scalars = np.array(scalars)
    if vmin is None:
        vmin = min(scalars.flat)
    if vmax is None:
        vmax = max(scalars.flat)
    color_map = plt.get_cmap(cmap)
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    return color_map([norm(s) for s in scalars])


def to_scalars(colors, cmap, vmin, vmax):
    """
    Inverse 'to_colors'
    Reconstruct the numeric values (0 - 1) of given
    Args:
        colors (list or rgba tuple)
        cmap (matplotlib colormap)
        vmin (float)
        vmax (float)
    """
    # colors = np.array(colors)/255.
    r = np.linspace(vmin, vmax, 256)
    norm = mpl.colors.Normalize(vmin, vmax)
    mapvals = cmap(norm(r))[:, :4]  # there are 4 channels: r,g,b,a
    scalars = []
    for color in colors:
        distance = np.sum((mapvals - color) ** 2, axis=1)
        scalars.append(r[np.argmin(distance)])
    return scalars


def colormap(seq):
    """
    Args:
        seq (iterable): a sequence of floats and RGB-tuples. The floats should be increasing
            and in the interval (0,1).
    Returns:
        LinearSegmentedColormap
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mpl.colors.LinearSegmentedColormap('CustomMap', cdict)


def color_cycle(cmap=None, n=None):
    """
    Args:
        cmap (matplotlib colormap): e.g. plt.cm.coolwarm
        n (int): needed for cmap argument
    """
    if cmap:
        color_rgb = to_colors(np.linspace(0, 1, n), cmap=cmap, vmin=0, vmax=1)
        colors = map(lambda rgb: '#%02x%02x%02x' % (int(rgb[0] * 255),
                                                    int(rgb[1] * 255),
                                                    int(rgb[2] * 255)),
                     tuple(color_rgb[:, 0:-1]))
    else:
        colors = list([color['color'] for color in mpl.rcParams['axes.prop_cycle']])
    return cycle(colors)


"""
Display section
"""


def axis_dim(axis):
    """
    Returns int: axis dimension
    """
    if hasattr(axis, 'get_zlim'):
        return 3
    else:
        return 2


def set_aspect_equal(axis):
    """Fix equal aspect bug for 3D plots."""

    if axis_dim(axis) == 2:
        axis.set_aspect('equal')
        return

    xlim = axis.get_xlim3d()
    ylim = axis.get_ylim3d()
    zlim = axis.get_zlim3d()

    from numpy import mean
    xmean = mean(xlim)
    ymean = mean(ylim)
    zmean = mean(zlim)

    plot_radius = max([abs(lim - mean_)
                       for lims, mean_ in ((xlim, xmean),
                                           (ylim, ymean),
                                           (zlim, zmean))
                       for lim in lims])

    axis.set_xlim3d([xmean - plot_radius, xmean + plot_radius])
    axis.set_ylim3d([ymean - plot_radius, ymean + plot_radius])
    axis.set_zlim3d([zmean - plot_radius, zmean + plot_radius])


def set_axis_off(axis):
    if axis_dim(axis) == 2:
        axis.set_axis_off()
    else:
        axis._axis3don = False


def autoscale_3d(axis, array=None, xLim=None, yLim=None, zLim=None):
    if array is not None:
        xMin, yMin, zMin = array.min(axis=0)
        xMax, yMax, zMax = array.max(axis=0)
        xLim = (xMin, xMax)
        yLim = (yMin, yMax)
        zLim = (zMin, zMax)
    xLimAxis = axis.get_xlim()
    yLimAxis = axis.get_ylim()
    zLimAxis = axis.get_zlim()

    if not False:
        # not empty axis
        xMin = min(xLimAxis[0], xLim[0])
        yMin = min(yLimAxis[0], yLim[0])
        zMin = min(zLimAxis[0], zLim[0])
        xMax = max(xLimAxis[1], xLim[1])
        yMax = max(yLimAxis[1], yLim[1])
        zMax = max(zLimAxis[1], zLim[1])
    axis.set_xlim([xMin, xMax])
    axis.set_ylim([yMin, yMax])
    axis.set_zlim([zMin, zMax])


def set_legend(axis, artists, **kwargs):
    """
    Convenience method to set a legend from multiple artists to an axis.
    Args:
        **kwargs
            table (bool): if True, labels containing ',' will be mapped to table
            table_title (str): value of the table entry top left - only active
                if table
    Examples:
        >> import tfields
        >> import matplotlib.pyplot as plt

        >> fig = plt.figure()
        >> ax = fig.add_subplot(111)

        >> im1 = ax.plot(range(10), pylab.randn(10), "r--", label=(r"$i = 1$,$j = 1$"))
        >> im2 = ax.plot(range(10), pylab.randn(10), "g--", label=(r"$i = 1$,$j = 2$"))
        >> im3 = ax.plot(range(10), pylab.randn(10), "b--", label=(r"$i = 1$,$j = 3$"))
        >> im4 = ax.plot(range(10), pylab.randn(10), "r.",  label=(r"$i = 2$,$j = 1$"))
        >> im5 = ax.plot(range(10), pylab.randn(10), "g.",  label=(r"$i = 2$,$j = 2$"))
        >> im6 = ax.plot(range(10), pylab.randn(10), "b.",  label=(r"$i = 2$,$j = 3$"))
        >> im7 = ax.plot(range(10), pylab.randn(10), "r^",  label=(r"$i = 3$,$j = 1$"))
        >> im8 = ax.plot(range(10), pylab.randn(10), "g^",  label=(r"$i = 3$,$j = 2$"))
        >> im9 = ax.plot(range(10), pylab.randn(10), "b^",  label=(r"$i = 3$,$j = 3$"))
        >> handles = [im1, im2, im3, im4, im5, im6, im7, im8, im9]

        >> tfields.plotting.set_legend(ax, handles, table=True)

        >> plt.show()
    """
    table = kwargs.pop('table', False)
    labels = kwargs.pop('labels', None)
    ncol = kwargs.pop('ncol', None)

    handles = []
    for artist in artists:
        if isinstance(artist, list):
            handles.append(artist[0])
        else:
            handles.append(artist)

    if table and labels is None and ncol is None:
        table_title = kwargs.pop('table_title', '')
        labels = np.array([h.get_label() for h in handles])
        labels = [l.split(',') for l in labels]
        captions_i = []
        captions_j = []
        for l in labels:
            if l[0] not in captions_i:
                captions_i.append(l[0])
            if l[1] not in captions_j:
                captions_j.append(l[1])
                
        shape = (len(captions_i),
                 len(captions_j))
        
        # initialize
        shape = np.array(shape)
        handles = np.array(handles)
        
        # create blank rectangle
        extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
        
        # Create organized list containing all handles for table. Extra represent empty space
        handles_table = np.full(shape + 1, extra)
        for handle, label in zip(handles, labels):
            i = captions_i.index(label[0])
            j = captions_j.index(label[1])
            if handles_table[i + 1, j + 1] != extra:
                raise ValueError("Duplicate label {label}"
                                 .format(**locals()))
            handles_table[i + 1, j + 1] = handle

        # Define the label captions
        labels_table = np.full(shape + 1, '', dtype='S80')
        labels_table[0, 0] = table_title
        labels_table[0, 1:] = captions_j
        labels_table[1:, 0] = captions_i
        labels_table = labels_table.astype(str)
        
        handles = list(handles_table.flat)
        labels = list(labels_table.flat)
        kwargs['ncol'] = shape[0] + 1
        kwargs['handletextpad'] = kwargs.pop('handletextpad', -1.5)  # negative numbers move to the right
        kwargs['columnspacing'] = kwargs.pop('columnspacing', 1.5)

    return axis.legend(handles=handles, labels=labels, **kwargs)


class set_zoomable(object):
    """
    Left click a colorbar and release in order to zoom.
    Upper and lower 5% of the colorbar will zoom out.
    """
    def __init__(self, cbar):
        self._cbar = cbar
        self._v_press = None
        self._v_release = None

        artist = self._cbar.mappable
        self._press_connection_id = artist.axes.figure.canvas.mpl_connect(
            'button_press_event',
            partial(self.on_press))
        self._release_connection_id = artist.axes.figure.canvas.mpl_connect(
            'button_release_event',
            partial(self.on_release))

    def on_press(self, event):
        if event.inaxes is self._cbar.ax:
            self._v_press = event.ydata

    def on_release(self, event):
        if event.inaxes is self._cbar.ax:
            self._v_release = event.ydata
            self.update_v_min_max()

    def update_v_min_max(self):
        # sort press and release event
        if self._v_press > self._v_release:
            x_up = self._v_press
            x_low = self._v_release
        if self._v_press < self._v_release:
            x_up = self._v_release
            x_low = self._v_press

        # zoom out if in 5% margin
        if x_up > 0.95:
            x_up = 1.5
        if x_low < 0.05:
            x_low = -0.5

        artist = self._cbar.mappable
        vmin, vmax = artist.get_clim()
        v_range = vmax - vmin
        vmax = vmin + x_up * v_range
        vmin = vmin + x_low * v_range
        artist.set_clim(vmin, vmax)
        artist.axes.figure.canvas.draw()


def set_colorbar(axis, artist, label=None, divide=True,
                 position='right', size="2%", pad=0.05,
                 labelpad = None, zoom=False,
                 **kwargs):
    """
    Note:
        Bug found in matplotlib:
            when calling axis.clear(), the colorbar has to be removed by hand,
            since it will not be removed by clear.
        >> import tfields
        >> axis = tfields.plotting.gca()
        >> artist = ...
        >> cbar = tfields.plotting.set_colorbar(axis, artist)
        >> tfields.plotting.save(...)
        >> cbar.remove()  # THIS IS IMPORTANT. Otherwise you will have problems
        # at the next call of savefig.
        >> axis.clear()

    """
    ticks_position = 'default'
    label_position = 'bottom'
    labelpad = 30 if labelpad is None else labelpad
    if position == 'right':
        rotation = 270
    elif position == 'left':
        rotation = 90
    elif position == 'top':
        rotation = 0
        ticks_position = 'top'
        label_position = 'top'
        labelpad = 5
    elif position == 'bottom':
        rotation = 0
    # colorbar
    if divide:
        divider = make_axes_locatable(axis)
        axis = divider.append_axes(position, size=size, pad=pad)
    cbar = plt.colorbar(artist, cax=axis, **kwargs)
    cbar.ax.xaxis.set_ticks_position(ticks_position)
    cbar.ax.xaxis.set_label_position(label_position)
    cbar.ax.tick_params(axis='x', which='major', pad=0)

    # label
    if label is None:
        art_label = artist.get_label()
        if art_label:
            label = art_label
    if label is not None:
        cbar.set_label(label, rotation=rotation, labelpad=labelpad)

    if zoom:
        set_zoomable(cbar)

    return cbar


def set_labels(axis, *labels):
    axis.set_xlabel(labels[0])
    axis.set_ylabel(labels[1])
    if axis_dim(axis) == 3:
        axis.set_zlabel(labels[2])


def set_formatter(sub_axis=None, formatter=dates.DateFormatter('%d-%m-%y')):
    if sub_axis is None:
        axis = gca()
        sub_axis = axis.xaxis
    sub_axis.set_major_formatter(formatter)


class ScientificFormatter(mpl.ticker.ScalarFormatter):
    """
    Examples:
        >> cbar = tfields.plotting.set_colorbar(
        ..     axis, artist,
        ..     label=r"$q_c\;(MW/m^2)$",
        ..     format=tfields.plotting.ScientificFormatter(None, useMathText=False))
    """
    def __init__(self, oom=None, **kwargs):
        """
        Args:
            oom (int): order of magnitued on the axis
        """
        self._oom = oom
        super(ScientificFormatter, self).__init__(**kwargs)

    def _set_orderOfMagnitude(self, oom):
        self._exp = int(np.log10(oom))
        if self._oom is not None:
            oom = self._oom
        else:  # Default: -3, 0, 3, 6, ...
            oom = self._exp - (self._exp % 3)
        self.orderOfMagnitude = oom


if __name__ == '__main__':
    m = tfields.Mesh3D.grid((0, 2, 2), (0, 1, 3), (0, 0, 1))
    m.maps[0].fields.append(tfields.Tensors(np.arange(m.faces.shape[0])))
    art1 = m.plot(dim=3, map_index=0, label='twenty')

    m = tfields.Mesh3D.grid((4, 7, 2), (3, 5, 3), (2, 2, 1))
    m.maps[0].fields.append(tfields.Tensors(np.arange(m.faces.shape[0])))
    art = m.plot(dim=3, map_index=0, edgecolor='k', vmin=-1, vmax=1, label="something")

    plot_sphere([7, 0, 1], 3)
