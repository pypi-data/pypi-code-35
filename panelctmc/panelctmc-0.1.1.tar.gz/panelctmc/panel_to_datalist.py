
from yearfrac import yearfrac
import numpy as np


def panel_to_datalist(data, lastdate=None):
    """Transforms array/list to ctmc's internal data format

    Parameters:
    -----------
    data : ndarray
        panel data with the following columns

            data[:,0]   ID of example
            data[:,1]   Event dates
            data[:,2]   State labels

    lastdate : datetime
        (Optional, Default: max(data[:,1]))
        The date when the last update of the
        panel data occured, or resp. the date
        when the latest panel data have been
        downloaded.
    """
    if lastdate is None:
        lastdate = np.max(data[:, 1])

    newdata = list()

    for _, exampleid in enumerate(np.unique(data[:, 0])):
        # read all entries for the example
        tmp = data[data[:, 0] == exampleid]

        # sort by date
        idxsorted = tmp[:, 1].argsort()
        dates = tmp[idxsorted, 1]
        states = tmp[idxsorted, 2]

        # filter state changes
        idxunique = np.append([True], states[1:] != states[:-1])

        # year fraction
        dates2 = np.append(dates[idxunique], [lastdate])
        # times = np.vectorize(yearfrac)(dates2[:-1], dates2[1:])
        times = yearfrac(dates2[:-1], dates2[1:])

        # store
        if len(times) > 1:
            newdata.append((list(states[idxunique]), list(times)))

    return newdata
