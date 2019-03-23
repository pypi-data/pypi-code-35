
import numpy as np
from datetime import datetime
from grouplabelencode import grouplabelencode
from .panel_to_datalist import panel_to_datalist
from ctmc import ctmc, datacorrection


def panelctmc(paneldata, mapping, lastdate=None,
              transintv=1.0, toltime=1e-8, debug=True):
    # check if numpy array
    if not isinstance(paneldata, np.ndarray):
        raise Exception("'paneldata' is not a numpy array")

    # force dtype=object
    paneldata = paneldata.astype(dtype=object)

    # convert str to datetime objects
    if isinstance(paneldata[:, 1][0], str):
        paneldata[:, 1] = [datetime.strptime(
            p, "%Y-%m-%d") for p in paneldata[:, 1]]

    # encode state labels
    paneldata[:, 2] = grouplabelencode(paneldata[:, 2], mapping, nastate=True)

    # convert panel data to ctmc-datalist object
    datalist = panel_to_datalist(paneldata, lastdate=lastdate)

    # auto correct datalist
    datalist = datacorrection(datalist)

    # Compute transitition matrix
    transmat, genmat, transcount, statetime = ctmc(
        datalist,
        len(mapping) + 1,
        transintv=transintv,
        toltime=toltime,
        debug=debug)

    # done
    return transmat, genmat, transcount, statetime, datalist
