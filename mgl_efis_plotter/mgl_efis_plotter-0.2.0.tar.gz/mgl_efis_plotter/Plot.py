from collections import OrderedDict
from typing import List

import matplotlib.pyplot as plt
from matplotlib import cycler
import pandas as pd

from .Config import Config
from .Flight import Flight


class Plot(object):
    """
    wrapper for plotting with matplotlib pyplot
    """

    flight: Flight
    colors: cycler
    config: Config

    def __init__(self, flight: Flight):
        self.flight = flight
        self.config = self.flight.config
        self.colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    def data(self, attr: str) -> OrderedDict:
        return self.flight.get_plot_data(attr)

    def list_attributes(self) -> None:
        self.flight.list_attributes()

    def plot(self, attr: str, label: str = None, **kwargs) -> 'Plot':
        """
        plot one attribute
        :param attr:
        :param label:
        :param kwargs: xlim, ylim
        :return:
        """
        plt.figure(figsize=self.config.plot_dimensions, dpi=self.config.plot_dpi, constrained_layout=True)
        data = self.data(attr)
        if self._is_scalar(data[0]):
            df = pd.DataFrame(data.values(), columns=[attr])
            df = df.rolling(self.config.rolling_window, min_periods=1).mean()
            y = df[attr]
        else:
            y = data.values()
        if label is None:
            label = attr
        plt.plot(data.keys(), y)
        plt.ylabel(label, fontsize=self.config.plot_font_size)

        values = list(data.values())
        if isinstance(values[0], list):
            self._add_legend(len(values))

        if 'xlim' in kwargs.keys():
            plt.xlim(kwargs['xlim'])
            del kwargs['xlim']
        if 'ylim' in kwargs.keys():
            plt.ylim(kwargs['ylim'])
            del kwargs['ylim']
        if 0 < len(kwargs.keys()):
            raise Exception('Unknown keyword argument: ' + list(kwargs.keys())[0])

        return self

    def plot2(self, attr: List[str], labels: List[str] = None, **kwargs) -> 'Plot':
        """
        Plot several attributes
        :param attr: List of attributes
        :param labels: List of labels
        :param kwargs: xlim, ylim
        :return:
        """
        if labels is None:
            labels = attr

        for i in range(0, len(attr)):
            if 0 == i:
                fig, axis0 = plt.subplots(figsize=self.config.plot_dimensions, dpi=self.config.plot_dpi,
                                          constrained_layout=True)
                axis = axis0
                axis0.set_xlabel('Minutes')
                if 'xlim' in kwargs.keys():
                    plt.xlim(kwargs['xlim'])
                    del kwargs['xlim']
                if 'ylim' in kwargs.keys():
                    plt.ylim(kwargs['ylim'])
                    del kwargs['ylim']
            else:
                axis = axis0.twinx()
                offset = 1 + ((i - 1) * 0.1)
                axis.spines['right'].set_position(('axes', offset))

            axis.set_ylabel(labels[i], color=self.colors[i], fontsize=self.config.plot_font_size)
            data = self.data(attr[i])
            if self._is_scalar(data[0]):
                df = pd.DataFrame(data.values())
                df = df.rolling(self.config.rolling_window, min_periods=1).mean()
                y = df.values.tolist()
            else:
                y = data.values()
            axis.plot(data.keys(), y, color=self.colors[i])

        if 0 < len(kwargs.keys()):
            raise Exception('Unknown keyword argument: ' + list(kwargs.keys())[0])

        return self

    def _is_scalar(self, n) -> bool:
        return not hasattr(n, '__len__')

    def save(self, fname: str, *args, **kwargs) -> None:
        """
        save the figure that has been plotted
        :param fname:
        :param args:
        :param kwargs:
        :return:
        """
        self._add_decorations()
        plt.savefig(fname, *args, **kwargs)

    def show(self) -> None:
        """
        show (display on the sreen) the figure that has been plotted
        :return:
        """
        self._add_decorations()
        plt.show()

    def _add_decorations(self) -> None:
        plt.title(self.flight.title())
        plt.xlabel('Minutes', fontsize=self.config.plot_font_size)

    def _add_legend(self, qty: int):
        labels = ['#{}'.format(n) for n in range(1, qty + 1)]
        plt.legend(labels, loc='best')
