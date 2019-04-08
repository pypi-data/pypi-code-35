#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import, compute and plot Power Spectral Densities

Use this tool to quickly compute, or plot PSDs from data contained
in one or multiple files, using parametrized Welch method.

Jean-Baptiste Bayle, APC/CNRS/CNES, 28/06/2018.
"""

import argparse
import numpy as np
import scipy.signal as sg
import matplotlib.pyplot as plt
import h5py as h5


def parse_arguments():
    """Create parser and return parsed arguments."""
    parser = argparse.ArgumentParser(
        description='Plot Power Spectral Densities from data files.',
        epilog='Jean-Baptiste Bayle, APC/CNRS/CNES.')
    parser.add_argument(
        'filenames',
        type=str, nargs='+',
        help='input files containing data')
    parser.add_argument(
        '-c', '--columns',
        type=int, nargs='*',
        help='indices of columns to be computed (default all)')
    parser.add_argument(
        '-s', '--skiprows',
        type=int, default=0,
        help='skip the first rows (default to 0)')
    parser.add_argument(
        '-n', '--nperseg',
        type=int, default=None,
        help='number of points per segment (default length of data)')
    parser.add_argument(
        '-l', '--length',
        type=int, default=None,
        help='number of points to use (default length of data)')
    parser.add_argument(
        '--every',
        type=int, default=1,
        help='use every n points (default to all points)')
    parser.add_argument(
        '--overlap',
        type=float, default=0.5,
        help='overlap ratio between segments (default 0.5)')
    parser.add_argument(
        '--window',
        type=str, default='nuttall4',
        help='windowing function (default to Nuttall4 window)')
    parser.add_argument(
        '-fs', '--sampling',
        type=float, default=None,
        help='sampling frequency in Hz (deduced from data by default)')
    parser.add_argument(
        '--detrend',
        type=str, default='none',
        choices=['none', 'constant', 'linear'],
        help='specifies how to detrend each segment (default to none)')
    parser.add_argument(
        '--no-legend',
        dest='legend', action='store_false',
        help='hide legend (default show)')
    parser.add_argument(
        '--aspect',
        type=str, default=None,
        help='aspect of line and markers with matplotlib conventions'
    )
    parser.add_argument(
        '--time-series',
        action='store_true',
        help='plot time series instead of psd')
    parser.add_argument(
        '--title',
        type=str,
        help='plot title'
    )
    parser.add_argument(
        '-o', '--output',
        type=str, default=None,
        help='output file for PSD data or image file (default show)')
    return parser.parse_args()


class Series():
    """Define a series of data and computed PSD."""

    def __init__(self, times, data, title):
        super().__init__()
        self.times = times
        self.data = data
        self.title = title
        self.sampling_freq = None
        self.frequencies = None
        self.psd = None

    @staticmethod
    def from_files(filenames, columns=None, skiprows=0, length=None, every=1):
        """Load series from multiple files."""
        series = []
        for filename in filenames:
            series += Series.from_file(filename, columns, skiprows, length, every)
        return series

    @staticmethod
    def from_file(filename, columns=None, skiprows=0, length=None, every=1):
        """Load series from a file."""
        split_filename = filename.split(':')
        filename = split_filename[0]
        print('Loading data from ' + filename + '...')

        if filename.endswith('.npy'):
            data_file = Series.from_numpy_file(filename, skiprows, length, every)
        elif filename.endswith('.hdf5'):
            if len(split_filename) < 2:
                raise ValueError("Missing path to dataset in HDF5 file '{}'".format(filename))
            path = split_filename[1]
            data_file = Series.from_hdf5_file(filename, path, skiprows, length, every)
        else:
            data_file = Series.from_other_format(filename, skiprows, length, every)

        column_count = data_file.shape[1]
        titles = Series.extract_titles(filename, column_count)
        columns = columns if columns is not None else range(1, column_count)
        return [Series(data_file[:, 0], data_file[:, col], titles[col]) for col in columns]

    @staticmethod
    def from_numpy_file(filename, skiprows=0, length=None, every=1):
        """Load series from a Numpy binary file."""
        file_data = np.load(filename)
        if skiprows > 0:
            print('Skipping the first', skiprows, 'rows of data...')
        if length is not None:
            print('Using the first', skiprows, 'rows of data...')
        if every > 1:
            print('Skipping every', every, 'row of data...')
        return file_data[skiprows:length:every]

    @staticmethod
    def from_hdf5_file(filename, path, skiprows=0, length=None, every=1):
        """Load series from a HDF5 file."""
        hdf5_file = h5.File(filename, 'r')
        try:
            dataset = hdf5_file[path]
            assert isinstance(dataset, h5.Dataset)
        except (KeyError, AssertionError):
            raise ValueError("Dataset '{}' cannot be found in '{}'".format(path, filename))

        if skiprows > 0:
            print('Skipping the first', skiprows, 'rows of data...')
        if length is not None:
            print('Using the first', skiprows, 'rows of data...')
        if every > 1:
            print('Skipping every', every, 'row of data...')
        return dataset[skiprows:length:every]

    @staticmethod
    def from_other_format(filename, skiprows, length=None, every=1):
        """Load series from a file compatible with `np.load()."""
        if skiprows > 0:
            print('Skipping the first', skiprows, 'rows of data...')
        if length is not None:
            print('Using the first', skiprows, 'rows of data...')
        if every > 1:
            print('Skipping every', every, 'row of data...')
        return np.loadtxt(filename, skiprows=skiprows, max_rows=length)[::every]

    @staticmethod
    def extract_titles(filename, column_count, commentchar='#'):
        """Extract column titles from file."""
        titles = None
        if filename.endswith('.txt'):
            with open(filename) as data_file:
                first = data_file.readline().strip()
                if first.startswith(commentchar):
                    titles = first.replace(commentchar, '').split()
        if titles is None:
            titles = [filename + '-' + str(col) for col in range(column_count)]
        return titles

    def compute(self, nperseg=None, overlap=0.5, window='nuttall4', detrend='none'):
        """Compute series PSD and return a PSD series."""
        if nperseg is None:
            nperseg = len(self.data)
        if detrend == 'none':
            detrend = False
        freq = self.deduced_sampling_freq() if self.sampling_freq is None else self.sampling_freq
        print('Computing PSD for', self.title,
              '(using', nperseg, 'points at', "%.1f" % freq, 'Hz)...')
        estimator = SpectralEstimator(freq, window, nperseg, overlap, detrend)
        self.frequencies, self.psd = estimator.compute(self.data)
        return self

    def deduced_sampling_freq(self):
        """Return sampling frequency from first points."""
        return 1.0 / (self.times[1] - self.times[0])

    def filter_nan(self):
        """Filter out NaN values from series."""
        nans = np.isnan(self.data)
        self.times = self.times[~nans]
        self.data = self.data[~nans]
        self.frequencies = None
        self.psd = None
        return self

    def time_series(self, legend=True, title=None, aspect=None):
        """Plot series data vs. time in linear scale."""
        if aspect is None:
            aspect = '.-'

        plt.plot(self.times, self.data, '.-', label=self.title)
        plt.xlabel('Time [s]')
        plt.grid(True)
        plt.ylabel('Signals')
        if legend:
            plt.legend()
        if title is not None:
            plt.title(title)
        return self

    def plot(self, legend=True, title=None, aspect=None):
        """Plot PSD vs. frequencies in a log-log scale."""
        if aspect is None:
            aspect = '-'

        plt.loglog(self.frequencies, self.psd, aspect, label=self.title)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('PSD [/Hz]')
        plt.grid(True)
        if legend:
            plt.legend()
        if title is not None:
            plt.title(title)
        return self

    @staticmethod
    def save_many(series, filename):
        """Save multiple series to Numpy binary file."""
        psds = []
        for serie in series:
            psds.append(serie.frequencies)
            psds.append(serie.psd)
        data = np.stack(psds, axis=1)
        np.save(filename.strip(), data)

    @staticmethod
    def savetxt_many(series, filename):
        """Save multiple series to text file."""
        psds = []
        header = []
        for serie in series:
            psds.append(serie.frequencies)
            header.append(serie.title + '-freq')
            psds.append(serie.psd)
            header.append(serie.title)
        data = np.stack(psds, axis=1)
        np.savetxt(filename.strip(), data, header=' '.join(header))


class SpectralEstimator():
    """Helper methods for spectral estimation."""

    # pylint: disable=R0913
    def __init__(self, fsampling, window, nperseg, overlap, detrend):
        self.fsampling = fsampling
        self.window = SpectralEstimator.get_window(window, nperseg)
        self.nperseg = nperseg
        self.noverlap = int(nperseg * overlap)
        self.detrend = detrend

    @staticmethod
    def get_window(window, nperseg):
        """Return window of type `window` for a length of `nperseg`."""
        func = None
        if window == 'nuttall3':
            coeffs = [0.375, -0.5, 0.125]
            func = lambda x: SpectralEstimator.nuttall(x, coeffs)
        elif window == 'nuttal3a':
            coeffs = [0.40897, -0.5, 0.09103]
            func = lambda x: SpectralEstimator.nuttall(x, coeffs)
        elif window == 'nuttall3b':
            coeffs = [0.4243801, -0.4973406, 0.0782793]
            func = lambda x: SpectralEstimator.nuttall(x, coeffs)
        elif window == 'nuttall4':
            coeffs = [0.3125, -0.46875, 0.1875, -0.03125]
            func = lambda x: SpectralEstimator.nuttall(x, coeffs)
        elif window == 'nuttall4a':
            coeffs = [0.338946, -0.481973, 0.161054, -0.018027]
            func = lambda x: SpectralEstimator.nuttall(x, coeffs)
        elif window == 'nuttall4b':
            coeffs = [0.355768, -0.487396, 0.144232, -0.012604]
            func = lambda x: SpectralEstimator.nuttall(x, coeffs)
        elif window == 'nuttall4c':
            coeffs = [0.3635819, -0.4891775, 0.1365995, -0.0106411]
            func = lambda x: SpectralEstimator.nuttall(x, coeffs)
        if func is not None:
            bins = np.arange(0.0, 1.0, 1.0 / nperseg)
            return [func(i) for i in bins]
        return sg.get_window(window, nperseg)

    @staticmethod
    def nuttall(point, coeffs):
        """Apply nuttall window at `point` for given coefficients."""
        coeffs = np.array(coeffs)
        args = 2 * np.pi * point * np.arange(0, len(coeffs))
        terms = coeffs * np.cos(args)
        return np.sum(terms)

    def compute(self, data):
        """Return frequencies and psd estimation for data."""
        return sg.welch(
            data,
            fs=self.fsampling,
            window=self.window,
            nperseg=self.nperseg,
            noverlap=self.noverlap,
            detrend=self.detrend
        )


def main():
    """Load data file and parse arguments before computing and plotting PSD."""
    # Set a global default size for figures
    plt.rcParams["figure.figsize"] = (12, 6)

    # Load all data series from files
    args = parse_arguments()
    series = Series.from_files(
        args.filenames, args.columns, args.skiprows, args.length, args.every)
    for serie in series:
        serie.filter_nan()
        if args.sampling is not None:
            serie.sampling_freq = args.sampling

    # Compute psd if needed
    show = args.output is None
    savetxt = not show and args.output.endswith('.txt')
    savefig = not show and args.output.endswith(('.png', '.pdf', '.ps', '.eps', '.svg'))
    savenpy = not show and not savefig and not savetxt
    if not args.time_series or savetxt:
        for serie in series:
            serie.compute(args.nperseg, args.overlap, args.window, args.detrend)

    # Save to file if needed
    if savetxt or savenpy:
        print('Saving results to ' + args.output + '...')
        if savetxt:
            Series.savetxt_many(series, args.output)
        else:
            Series.save_many(series, args.output)
        return

    # Plot time series or psd
    print("Plotting results...")
    if args.time_series:
        for serie in series:
            serie.time_series(legend=args.legend, title=args.title, aspect=args.aspect)
    else:
        for serie in series:
            serie.plot(legend=args.legend, title=args.title, aspect=args.aspect)

    # Save figure if needed
    if savefig:
        print('Saving figure to ' + args.output + '...')
        plt.savefig(args.output, dpi=300)
        return

    # Else, show it
    plt.show()


if __name__ == '__main__':
    main()
