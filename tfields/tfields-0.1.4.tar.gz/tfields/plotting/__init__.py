"""
Core plotting tools for tfields library. Especially PlotOptions class
is basis for many plotting expansions

TODO:
    * add other library backends. Do not restrict to mpl
"""
import warnings
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from .mpl import *
from six import string_types


def set_default(dictionary, attr, value):
    """
    Set defaults to a dictionary
    """
    if attr not in dictionary:
        dictionary[attr] = value


class PlotOptions(object):
    """
    processing kwargs for plotting functions and providing easy
    access to axis, dimension and plotting method as well as indices
    for array choice (x..., y..., zAxis)
    """
    def __init__(self, kwargs):
        kwargs = dict(kwargs)
        self.axis = kwargs.pop('axis', None)
        self.dim = kwargs.pop('dim', None)
        self.method = kwargs.pop('methodName', None)
        self.setXYZAxis(kwargs)
        self.plot_kwargs = kwargs

    @property
    def method(self):
        """
        Method for plotting. Will be callable together with plot_kwargs
        """
        return self._method

    @method.setter
    def method(self, methodName):
        if not isinstance(methodName, str):
            self._method = methodName
        else:
            self._method = getattr(self.axis, methodName)

    @property
    def dim(self):
        """
        axis dimension
        """
        return self._dim

    @dim.setter
    def dim(self, dim):
        if dim is None:
            if self._axis is None:
                dim = 2
            dim = axis_dim(self._axis)
        elif self._axis is not None:
            if not dim == axis_dim(self._axis):
                raise ValueError("Axis and dim argument are in conflict.")
        if dim not in [2, 3]:
            raise NotImplementedError("Dimensions other than 2 or 3 are not supported.")
        self._dim = dim

    @property
    def axis(self):
        """
        The plt.Axis object that belongs to this instance
        """
        if self._axis is None:
            return gca(self._dim)
        else:
            return self._axis

    @axis.setter
    def axis(self, axis):
        self._axis = axis

    def setXYZAxis(self, kwargs):
        self._xAxis = kwargs.pop('xAxis', 0)
        self._yAxis = kwargs.pop('yAxis', 1)
        zAxis = kwargs.pop('zAxis', None)
        if zAxis is None and self.dim == 3:
            indicesUsed = [0, 1, 2]
            indicesUsed.remove(self._xAxis)
            indicesUsed.remove(self._yAxis)
            zAxis = indicesUsed[0]
        self._zAxis = zAxis

    def getXYZAxis(self):
        return self._xAxis, self._yAxis, self._zAxis

    def setVminVmaxAuto(self, vmin, vmax, scalars):
        """
        Automatically set vmin and vmax as min/max of scalars
        but only if vmin or vmax is None
        """
        if scalars is None:
            return
        if len(scalars) < 2:
            warnings.warn("Need at least two scalars to autoset vmin and/or vmax!")
            return
        if vmin is None:
            vmin = min(scalars)
            self.plot_kwargs['vmin'] = vmin
        if vmax is None:
            vmax = max(scalars)
            self.plot_kwargs['vmax'] = vmax

    def getNormArgs(self, vminDefault=0, vmaxDefault=1, cmapDefault=None):
        if cmapDefault is None:
            cmapDefault = plt.rcParams['image.cmap']
        cmap = self.get('cmap', cmapDefault)
        vmin = self.get('vmin', vminDefault)
        vmax = self.get('vmax', vmaxDefault)
        return cmap, vmin, vmax

    def format_colors(self, colors, fmt='rgba', length=None):
        """
        format colors according to fmt argument
        Args:
            colors (list/one value of rgba tuples/int/float/str): This argument will
                be interpreted as color
            fmt (str): rgba | hex | norm
            length (int/None): if not None: correct colors lenght
    
        Returns:
            colors in fmt
        """
        hasIter = True
        if not hasattr(colors, '__iter__') or isinstance(colors, string_types):
            # colors is just one element
            hasIter = False
            colors = [colors]

        if fmt == 'norm':
            if hasattr(colors[0], '__iter__'):
                # rgba given but norm wanted
                cmap, vmin, vmax = self.getNormArgs(cmapDefault='NotSpecified',
                                                    vminDefault=None,
                                                    vmaxDefault=None)
                colors = to_scalars(colors, cmap, vmin, vmax)
                self.plot_kwargs['vmin'] = vmin
                self.plot_kwargs['vmax'] = vmax
                self.plot_kwargs['cmap'] = cmap
        elif fmt == 'rgba':
            if isinstance(colors[0], string_types):
                # string color defined
                colors = [mpl.colors.to_rgba(color) for color in colors]
            else:
                # norm given rgba wanted
                cmap, vmin, vmax = self.getNormArgs(cmapDefault='NotSpecified',
                                                    vminDefault=None,
                                                    vmaxDefault=None)
                self.setVminVmaxAuto(vmin, vmax, colors)
                # update vmin and vmax
                cmap, vmin, vmax = self.getNormArgs()
                colors = to_colors(colors,
                                   vmin=vmin,
                                   vmax=vmax,
                                   cmap=cmap)
        elif fmt == 'hex':
            colors = [mpl.colors.to_hex(color) for color in colors]
        else:
            raise NotImplementedError("Color fmt '{fmt}' not implemented."
                                      .format(**locals()))
    
        if length is not None:
            # just one colors value given
            if len(colors) != length:
                if not len(colors) == 1:
                    raise ValueError("Can not correct color length")
                colors = list(colors)
                colors *= length
        elif not hasIter:
            colors = colors[0]
    
        colors = np.array(colors)
        return colors

    def delNormArgs(self):
        self.plot_kwargs.pop('vmin', None)
        self.plot_kwargs.pop('vmax', None)
        self.plot_kwargs.pop('cmap', None)

    def getSortedLabels(self, labels):
        """
        Returns the labels corresponding to the axes
        """
        return [labels[i] for i in self.getXYZAxis() if i is not None]
        
    def get(self, attr, default=None):
        return self.plot_kwargs.get(attr, default)

    def pop(self, attr, default=None):
        return self.plot_kwargs.pop(attr, default)

    def set(self, attr, value):
        self.plot_kwargs[attr] = value

    def set_default(self, attr, value):
        set_default(self.plot_kwargs, attr, value)

    def retrieve(self, attr, default=None, keep=True):
        if keep:
            return self.get(attr, default)
        else:
            return self.pop(attr, default)

    def retrieve_chain(self, *args, **kwargs):
        default = kwargs.pop('default', None)
        keep = kwargs.pop('keep', True)
        if len(args) > 1:
            return self.retrieve(args[0],
                                 self.retrieve_chain(*args[1:],
                                                    default=default,
                                                    keep=keep),
                                 keep=keep)
        if len(args) != 1:
            raise ValueError("Invalid number of args ({0})".format(len(args)))
        return self.retrieve(args[0], default, keep=keep)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
