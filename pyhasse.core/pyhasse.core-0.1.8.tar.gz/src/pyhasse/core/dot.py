""" Export dot-file

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from pyhasse.core.hddata import HDData


def export_graphviz(csv):
    """ stores the cover matrix in graphviz format

   :param: **csv** dataset
   :return: **txt** content of a graphviz definition as text

   """
    hd = HDData(csv=csv)
    jd = hd.jsondata()
    txt = "\n"
    txt += "graph " + " {\n"
    for i in range(0, csv.redrows):
        txt += " {}".format(csv.objred[i])
    txt += "\n"
    for idxrow, row in enumerate(jd['mx_cover']):
        obj_above = jd['lst_obj_red'][idxrow]
        for idxcol, col in enumerate(row):
            if row[idxcol] == 1:
                obj_below = jd['lst_obj_red'][idxcol]
                txt += "{} -- {};\n".format(obj_above, obj_below)

    txt += "}"
    # Note the rows of an (evtl) reduced zetamatrix
    return txt
