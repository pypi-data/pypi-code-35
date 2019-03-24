# plotting.py
# Author: Joshua Beard
# Created: 2019-01-08

# TODO:
# [ ] Support multiple x arrays
# [ ] ylim for Lines
# [ ] max_val_pad for Lines
# [x] Match API for Bars with Lines
# [ ] Offload common methods to Plot2D superclass
# [ ] Better placement of on-chart text relative to bar height
# [ ] Support for "below"-bar on-chart text
# [x] Test non-scaled bars
# [ ] different logic if labels are numbers as opposed to strings?
# [x] support show=False
# [ ] label_rotation = 45 causes part of long labels to be placed off page. Can I rectify this?
# [x] init of Plot2D should use a kwarg

from matplotlib import pyplot as plt
from . import util
from collections import Iterable
from os.path import join as pathjoin
import numpy as np
import warnings

DEBUG = False


class Plot2D(object):
    def __init__(self, **kwargs):
        # TODO do as much of the init stuff here as possible - reduce the size
        # of the codebase and make it easier to read

        try:
            constraints = {'x': Iterable,
                           'y': Iterable,
                           'labels': Iterable,
                           'figsize': Iterable,
                           'title': str,
                           'ylim': Iterable,
                           'max_val_pad': (int, float, '>=0'),
                           'show_bottom_labels': bool,
                           'show_legend': bool,
                           'show': bool,
                           'save': bool,
                           'save_name': str,
                           'xlabel': str,
                           'ylabel': str,
                           }
            constraints.update(self.constraints)
        except AttributeError:
            pass
        finally:
            self.constraints = constraints

        try:
            defaults = {'x': None,
                        'y': None,
                        'labels': None,
                        'figsize': (12, 8),
                        'title': '',
                        'ylim': None,
                        'max_val_pad': 0,
                        'show_bottom_labels': False,
                        'show_legend': True,
                        'show': True,
                        'save': False,
                        'save_name': None,
                        'xlabel': None,
                        'ylabel': None,
                        }
            defaults.update(self.defaults)
        except AttributeError:
            pass
        finally:
            self.defaults = defaults

        self.params = util.ParameterRegister(self.constraints,
                                             self.defaults,
                                             accept_none=True,
                                             match_all_constraints=False)
        self.params.set(**kwargs)
        self.params.set_uninitialized_params()

        self._fig = plt.figure(figsize=self.params['figsize'])
        self._ax = self._fig.add_subplot(111)
        self._data = []

        self._savename = self.params['save_name']
        if self._savename is None:
            self._savename = 'graph_' + '_'.join(self.params['title'].split(' '))

    def show(self):
        plt.show()

    def save(self, savename=None):
        if savename is not None:
            self._savename = savename

        plt.savefig(pathjoin('figs', self._savename))

    def set_title(self):
        self._fig.suptitle(self.params['title'], fontsize=max(self.params['figsize']))


class Bars(Plot2D):
    """
        Plots separate bars as independent categories, coloring them differently
        Parameters:
            data: <list>, <tuple>, or <np.ndarray> of the bar heights
            labels: <list>, <tuple>, or <np.ndarray> of labels for the different bars (optionally displayed)
            bar_width: <int> or <float> defining bar width
            figsize: <list>, <tuple>, or <np.ndarray> of figure size
            title: <str> defining the graph title, which is scaled based on figure size. If save_name is not defined, but save==True, this is also the save name
            ylim: <list>, <tuple>, or <np.ndarray> of y limits, None does autoscaling
            max_val_pad: <int> or <float> defining the proportional padding above the max value. Autoscaling uses 0.1
            sort_by: <str>, <tuple>, <list>, <np.ndarray> defining order of data displayed ('ascending' or 'descending', or some canonical ordering). None does no sorting
            show_bottom_labels: <bool> switch for displaying labels at the bottom
            show_legend: <bool> switch for displaying legend
            show_max_val: <bool> switch for displaying dashed line at maximum value
            show: <bool> whether to show the plot NOTE: as of version 0.1.2, setting this to False does nothing
            save: <bool> whether to save the plot
            scale_by: <int>, <float>, <tuple>, <list>, <np.ndarray> the factor by which to scale the data. Note this must be broadcastable to the data
            show_bar_labels: <bool> switch for displaying labels at top of each bar
            bar_label_format: function format for bars label. If None, displays raw data
            show_as_percent: <bool> scales everything as percentages
        Returns: Nothing
    """

    # Bars-specific constraints and defaults - some of these are duplicated,
    # but kept because I may phase them out in the superclass
    constraints = {'bar_width': util.isnumeric,
                   'max_val_pad': util.isnumeric,
                   'sort_by': ('ascending', 'descending', Iterable),
                   'show_bottom_labels': bool,
                   'show_legend': bool,
                   'show_max_val': bool,
                   'scale_by': (util.isnumeric, Iterable),
                   'show_bar_labels': bool,
                   'bar_label_format': (lambda x: x),
                   'multicolor': bool,
                   'show_as_percent': bool,
                   }
    defaults = {'bar_width': 0.75,
                'max_val_pad': 0.1,
                'sort_by': None,
                'show_bottom_labels': True,
                'show_legend': False,
                'show_max_val': False,
                'scale_by': None,
                'show_bar_labels': False,
                'bar_label_format': None,
                'multicolor': True,
                'show_as_percent': False,
                }

    def __init__(self, **kwargs):
        # Super has a number of kwarg constraints and defaults
        super().__init__(**kwargs)

        try:
            # TODO this is deprecated
            y_vals = self.params['data']
            warnings.warn("using 'data' to pass bar height to plotting object is deprecated. Use 'y' instead")

        except KeyError:
            # NOTE this is the preferred keyword argument, as it more closely follows the API for Lines
            y_vals = self.params['y']
        finally:
            y_vals = np.array(y_vals)

        labels = np.array(self.params['labels']) if self.params['labels'] is not None else None

        # Sort the data and labels by ascending, descending, or the user-defined order
        if self.params['sort_by'] is not None:
            if isinstance(self.params['sort_by'], str):
                order = np.argsort(y_vals)
                if self.params['sort_by'].lower() == 'descending':
                    order = order[::-1]
            else:
                order = np.array(self.params['sort_by'])
            y_vals = y_vals[order]
            labels = labels[order] if labels is not None else None

        # If user wants labels shown at the bottom of the plot
        if self.params['show_bottom_labels'] and labels is not None:
            if len(labels) != len(y_vals):
                raise ValueError('len(labels) = {} but len(y_vals) = {}'.format(len(labels), len(y_vals)))

            bottom_labels = [labels[i] + '\nN = {}'.format(y_vals[i])
                             for i in range(len(labels))]

            # If there are lots of items, rotate the labels
            # TODO this is a little buggy - long labels get pushed off plot
            if len(labels) > 7:
                label_rotation = 45
            else:
                label_rotation = 0

        else:
            bottom_labels = None

        scale_factor = np.array(self.params['scale_by']) if self.params['scale_by'] is not None else None
        if scale_factor is not None:
            if scale_factor.size != len(labels) and scale_factor.size > 1:
                raise ValueError('scale_by (with shape {}) must be broadcastable to y_vals (with shape {})'.format(scale_factor.shape, y_vals.shape))

            y_vals = y_vals / scale_factor
            max_val = 1
        else:
            max_val = y_vals.max()

        # If we're displaying percentages, scale the y-axis accordingly
        ylim = self.params['ylim']
        if self.params['show_as_percent']:
            y_vals *= 100
            if ylim is not None:
                ylim = (ylim[0] * 100, ylim[1] * 100)

        # If ylim is not specified, autoscale
        if DEBUG:
            import ipdb
            ipdb.set_trace()

        if ylim is None:
            ylim = (0, max(y_vals) + max(y_vals) * self.params['max_val_pad'])

        # Now let's plot the damn thing
        offsets = list(range(y_vals.size))
        if self.params['multicolor']:
            for i in range(len(labels)):
                self._data.append(self._ax.bar(offsets[i],
                                               y_vals[i],
                                               self.params['bar_width']))
        else:
            self._data = self._ax.bar(offsets, y_vals, self.params['bar_width'])

        # Show a line at the maximum value
        if self.params['show_max_val']:
            max_val = 100 if self.params['show_as_percent'] else max_val
            self._ax.plot([min(offsets) - 1, max(offsets) + 1],
                          [max_val, max_val],
                          '--',
                          color=[0.75, 0.75, 0.75])

        # Text drawn on the graph labeling the bars with their y_vals
        if self.params['show_bar_labels']:

            # bar_label_format should either be None or some function
            if self.params['bar_label_format'] is not None:
                fmt = self.params['bar_label_format']
            else:
                def fmt(x):
                    return '{}'.format(x)

            if scale_factor != np.array(None):
                y_offset = 0.05

            for i in range(y_vals.size):
                self._ax.text(x=offsets[i], y=y_vals[i] + y_offset, s=fmt(y_vals[i]))

        # Limits and tick spacing
        self._ax.set_ylim(ylim)
        self._ax.set_xlim(-self.params['bar_width'], (len(y_vals) - 1) + self.params['bar_width'])
        self._ax.set_xticks(offsets)
        self._ax.tick_params(labelsize=max(self.params['figsize']))

        # If bottom labels were defined
        if bottom_labels is not None:
            xtick_labels = self._ax.set_xticklabels(bottom_labels)
            # TODO I don't like that this doesn't use the Object-Oriented API,
            # so maybe phase this out if I can't find a suitable replacement
            plt.setp(xtick_labels, rotation=label_rotation)
        else:
            xtick_labels = self._ax.set_xticklabels(['' for i in y_vals])

        # Using a legend
        if self.params['show_legend']:
            self._ax.legend(self._data, labels, prop={'size': max(self.params['figsize'])})

        self.set_title()

        # Saving uses title if save_name is not defined
        if self.params['save']:
            self.save()

        if self.params['show']:
            self.show()


class Lines(Plot2D):
    # No Lines-specific constraints or defaults since there's not a lot of
    # customization that I offer yet.

    constraints = {'line_formats': Iterable,
                   }
    defaults = {'line_formats': '-',
                }

    def __init__(self, **kwargs):
        # Super has a number of kwarg constraints and defaults
        super().__init__(**kwargs)

        # Grab all lines given as a list for easier logic later
        try:
            y_vals = [vec for vec in self.params['y']]
        except TypeError:
            y_vals = [self.params['y']]

        # If x is not given, default to nonnegative integers
        if self.params['x'] is None:
            x_vals = np.arange(len(y_vals[0]))
        else:
            x_vals = self.params['x']

        # If labels are not given, set to blank for simpler plotting
        labels = self.params['labels'] if self.params['labels'] is not None else ['' for i in range(len(y_vals))]

        # If only a single label is given, turn it into a list for easier logic
        labels = [labels] if isinstance(labels, str) else labels

        # Get line formats as list
        line_formats = self.params['line_formats']
        line_formats = [line_formats] if isinstance(line_formats, str) else line_formats

        # Do the plotting
        for (y, label, fmt) in zip(y_vals, labels, line_formats):
            self._data.append(self._ax.plot(x_vals, y, fmt, label=label))

        # If user specified labels, display a legend
        if self.params['labels'] is not None:
            plt.legend()

        # x- and y-axis labels
        if self.params['xlabel'] is not None:
            self._ax.set_xlabel(self.params['xlabel'])
        if self.params['ylabel'] is not None:
            self._ax.set_ylabel(self.params['ylabel'])

        self.set_title()

        # Save and show now if needed
        if self.params['save']:
            self.save()

        if self.params['show']:
            self.show()
