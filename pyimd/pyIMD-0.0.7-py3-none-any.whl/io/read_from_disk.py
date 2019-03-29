# /********************************************************************************
# * Copyright © 2018-2019, ETH Zurich, D-BSSE, Andreas P. Cuny & Gotthold Fläschner
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the GNU Public License v3.0
# * which accompanies this distribution, and is available at
# * http://www.gnu.org/licenses/gpl
# *
# * Contributors:
# *     Andreas P. Cuny - initial API and implementation
# *******************************************************************************/

from numpy import nan
from nptdms import TdmsFile
from pandas import read_csv, DataFrame
import pathlib

__author__ = 'Andreas P. Cuny'


def read_from_tdms(file):
    """Method to read data from National Instruments technical data management streaming files (TDMS).

    Args:
        file (`str`):              File path + file name string.

    Returns:
        data (`pandas data frame`):  Returns data structured in a pandas data frame.
    """
    tdms_file = TdmsFile(file)
    data = tdms_file.as_dataframe(time_index=False, absolute_time=False)
    return data


def read_from_text(file, delimiter, read_from_row):
    """Method to read data from text files.

    Args:
        file (`str`):               File path + file name.
        delimiter (`str`):          Delimiter used in the data file to separate columns
        read_from_row (`int`):      Row number from where to start reading data to be able \
                                    to skip heading text rows. Make sure that you keep the \
                                    Frequency, Amplitude and Phase headers.

    Returns:
        data (`pandas data frame`):  Returns data structured in a pandas data frame.
    """
    data = read_csv(file, sep=delimiter, skiprows=read_from_row)
    return data


def read_from_file(file, delimiter):
    """Method to read data from a file.

    Args:
        file (`str`):               File path + file name to a .TDMS or .txt file.
        delimiter (`str`):          Delimiter used in the data file to separate columns

    Returns:
        data (`pandas data frame`):  Returns data structured in a pandas data frame.
    """
    p = pathlib.Path(file)
    if p.suffix == '.tdms':
        data = read_from_tdms(file)
        return data
    elif p.suffix == '.txt':
        data = read_from_text(file, delimiter, 0)
    elif p.suffix == '':
        data = read_from_text(file, delimiter, 0)
    elif p.suffix == '.csv':
        data = read_from_text(file, delimiter, 0)

    # Check how many columns we have. For PLL we expect only 2 (minimal) or 7 (default TDMS file). For Cont.Sweep we
    # expect 256 columns. Reshape to correct format if needed.
    if data.shape[1] == 2:
        df = DataFrame(nan, index=range(data.shape[0]), columns=range(7))
        df.iloc[:, 0] = data.iloc[:, 0]
        df.iloc[:, 6] = data.iloc[:, 1]
        data = df

    return data
