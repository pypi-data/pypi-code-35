# bar_chart.py
# Author: Joshua Beard
# Created: 2019-01-08

# TODO:
# [ ] Better placement of on-chart text relative to bar height
# [ ] Support for "below"-bar on-chart text
# [ ] Test non-scaled bars
# [ ] different logic if labels are numbers as opposed to strings?
# [ ] support show=False
# [ ] label_rotation = 45 causes part of long labels to be placed off page. Can I rectify this?

import numpy as np
from matplotlib import pyplot as plt
from . import util


def plot_separate(data,
                  labels=None,
                  bar_width=0.75,
                  figsize=(12, 8),
                  title='',
                  ylim=None,
                  max_val_pad=0.1,
                  sort_order=None,
                  use_bottom_labels=False,
                  use_legend=False,
                  show_max_val=False,
                  show=True,
                  save=False,
                  save_name=None,
                  scale_by=None,
                  label_bars=None,
                  label_bars_format='percent',
                  ):
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
            sort_order: <str> defining order of data displayed ('ascending' or 'descending'). None does no sorting
            use_bottom_labels: <bool> switch for displaying labels at the bottom
            use_legend: <bool> switch for displaying legend
            show_max_val: <bool> switch for displaying dashed line at maximum value
            show: <bool> whether to show the plot NOTE: as of version 0.1.2, setting this to False does nothing
            save: <bool> whether to save the plot
            scale_by: <int>, <float>, <tuple>, <list>, <np.ndarray> the factor by which to scale the data. Note this must be broadcastable to the data
            label_bars: <str> location for bar labels. None displays no labels
            label_bars_format: <str> format for bars label. None does nothing fancy, percent displays the bars as percentages of total and scales ylim
        Returns: Nothing
    """

    valid_options = {'data': (list, np.ndarray),
                     'labels': (list, np.ndarray),
                     'bar_width': (float),
                     'figsize': (list, tuple, np.ndarray),
                     'title': (str),
                     'ylim': (list, tuple, np.ndarray, None),
                     'max_val_pad': (int, float, None),
                     'sort_order': (None, 'ascending', 'descending'),
                     'use_bottom_labels': (bool),
                     'use_legend': (bool),
                     'show_max_val': (bool),
                     'show': (bool),
                     'save': (bool),
                     'save_name': (str, None),
                     'scale_by': (list, tuple, int, float, np.ndarray, None),
                     'label_bars': (None, 'above', 'below'),
                     'label_bars_format': (None, 'percent'),
                     'save': (bool),
                     }

    data = np.array(data)
    labels = np.array(labels)

    # Only sort if specified, and do so either ascending or descending
    util.check_parameter(sort_order, 'sort_order', valid_options)
    if sort_order is not None:
        order = np.argsort(data)
        if sort_order.lower() == 'descending':
            order = order[::-1]
        data = [order]
        labels = labels[order]

    # If we're showing labels at the bottom (and they're defined):
    util.check_parameter(labels, 'labels', valid_options)
    if use_bottom_labels and labels is not None:
        if len(labels) != len(data):
            raise ValueError('len(labels) != len(data)')

        bottom_labels = [labels[i] + '\nN = {}'.format(data[i])
                         for i in range(len(labels))]

        # If there are lots of items, rotate the labels
        if len(labels) > 7:
            label_rotation = 45
        else:
            label_rotation = 0
    else:
        bottom_labels = None

    # Used if normalizing
    if scale_by is not None:
        data = data / np.array(scale_by)
        n_total = 1
    else:
        n_total = data.sum()

    # Separation between bars
    #string_dtype = np.dtype('<U1')
    #if labels.dtype == string_dtype:
    #    offsets = list(range(len(labels)))
    #else:
    #    offsets = list(range(len(labels)))
    offsets = list(range(len(labels)))

    # If we're displaying percentages, scale the y-axis accordingly
    util.check_parameter(label_bars_format, 'label_bars_format', valid_options)
    if label_bars_format.lower() == 'percent':
        data *= 100
        if ylim is not None:
            ylim = (ylim[0] * 100, ylim[1] * 100)

    # Now let's plot the damn thing
    bars = []
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    for i in range(len(labels)):
        bars.append(ax.bar(offsets[i], data[i], bar_width))

    # Show a line at the maximum value
    if show_max_val:
        ax.plot([min(offsets) - 1, max(offsets) + 1],
                [n_total, n_total],
                '--',
                color=[0.75, 0.75, 0.75])

    # Text drawn on the graph labeling the bars with their data
    if label_bars is not None:
        if label_bars_format.lower() == 'percent':
            def fmt(x):
                return '{:.1f}%'.format(x)
        else:
            def fmt(x):
                return '{}'.format(x)

        if label_bars.lower() == 'above':
            if scale_by is not None:
                y_offset = 0.05

        for i in range(len(labels)):
            plt.text(x=offsets[i], y=data[i] + y_offset, s=fmt(data[i]))

    # If ylim is not specified, autoscale
    if ylim is None:
        ylim = (0, max(data) + max(data) * max_val_pad)

    # Limits and tick spacing
    ax.set_ylim(ylim)
    ax.set_xlim(-bar_width, (len(data) - 1) + bar_width)
    ax.set_xticks(offsets)
    plt.tick_params(labelsize=max(figsize))

    # If bottom labels were defined
    if bottom_labels is not None:
        xtick_labels = ax.set_xticklabels(bottom_labels)
        plt.setp(xtick_labels, rotation=label_rotation)

    # Using a legend
    if use_legend:
        ax.legend(bars, labels, prop={'size': max(figsize)})

    # Title
    fig.suptitle(title, fontsize=max(figsize) * 2)

    # Saving uses title if save_name is not defined
    if save:
        if save_name is not None:
            plt.savefig(save_name)
        else:
            plt.savefig(title)

    if show:
        plt.show()
