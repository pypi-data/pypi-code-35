#!/usr/bin/env python
#
# icd10.py - Query the ICD10 disease coding hierarchy.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains the :class:`ICD10Hierarchy` class, which can be used
to query the `ICD10 <https://en.wikipedia.org/wiki/ICD-10>`_ disease coding
hierarcy.


The :func:`readICD10CodingFile` function will read the hierarchy information
from a text file, and return an :class:`ICD10Hierarchy` object.


The :func:`codeToNumeric` function will take an ICD10 coding, and return
a numeric variant of it.


The :func:`storeCodes` function allows sets of ICD10 codes to be stored
so that they can be saved out to a file via the :func:`saveCodes` function, at
a later stage.
"""


import              logging
import functools as ft
import itertools as it

import numpy     as np
import pandas    as pd


log = logging.getLogger(__name__)


@ft.lru_cache()
def readICD10CodingFile(fname):
    """Reads the ICD10 hierarchy information from the given file.

    ``fname`` is assumed to refer to a tab-separated file containing
    the following columns:

      - ``coding``:    The ICD10 code
      - ``meaning``:   Description
      - ``node_id``:   Index in the hierarchy
      - ``parent_id``: Index of this node's parent

    It is assumed that all codes have a sequential ``node_id`` starting from 1,
    and that the parent node(s) have a ``parent_id`` of 0.
    The codes are not assumed to be ordered by their ID.

    :arg fname: File containing ICD10 hierarchy information
    :returns:   An :class:`ICD10Hierarchy` object.
    """

    data      = pd.read_csv(fname, delimiter='\t', index_col=False)
    codings   = data['coding']   .values
    meanings  = data['meaning']  .values
    nodeIds   = data['node_id']  .values
    parentIds = data['parent_id'].values

    order = np.argsort(nodeIds)

    codings   = codings[  order]
    meanings  = meanings[ order]
    nodeIds   = nodeIds[  order] - 1
    parentIds = parentIds[order] - 1

    return ICD10Hierarchy(nodeIds, parentIds, codings, meanings)


class ICD10Hierarchy(object):
    """The ``ICD10Hierarchy`` class allows information in the ICD10 disease
    hierarchy to be queried. The :meth:`parents` method will return all
    parents in the hiearchy for a given code, and the :meth:`description`
    method will return the description for a coding.


    Additional metadata can be added and retrieved for codings via the
    :meth:`set` and :meth:`get` methods.
    """

    def __init__(self, nodes, parents, codings, descs):
        """Create a ``ICD10Hierarchy`` object.

        :arg nodes:   Node IDs. Currently assumed to be equivalent to
                      ``np.arange(len(nodes))``
        :arg parents: Parent IDs for each node.
        :arg codings: ICD10 coding for each node.
        :arg descs:   Description for each node
        """

        self.__nodes    = nodes
        self.__parents  = parents
        self.__codings  = codings
        self.__attrs    = {}
        self.__codeidxs = {}

        self.__attrs['description'] = descs

        for i, c in enumerate(self.__codings):
            self.__codeidxs[c] = i


    def index(self, coding):
        """Return the node ID for the given ``coding``. """
        return self.__codeidxs[coding]


    def coding(self, nodeID):
        """Return the coding for the given ``nodeID``. """
        return self.__codings[nodeID]


    def parents(self, coding):
        """Return all parents of the given coding. """

        parents = []
        cidx    = self.index(coding)
        pidx    = self.__parents[cidx]

        while pidx >= 0:
            parents.append(self.coding(pidx))
            pidx = self.__parents[pidx]

        return parents


    def description(self, coding):
        """Return the description for the given coding. """
        return self.get(coding, 'description')


    def get(self, coding, attr):
        """Get the given attribue for the given coding. """
        idx = self.index(coding)
        return self.__attrs[attr][idx]


    def set(self, coding, attr, value):
        """Set an attribute for the given coding. """

        if attr not in self.__attrs:
            self.__attrs[attr] = [None] * len(self.__nodes)

        idx = self.index(coding)
        self.__attrs[attr][idx] = value


def codeToNumeric(code):
    """Converts an ICD10 code into a numeric version. """
    try:
        if code[0].isalpha() and code[1:].isdecimal():
            prefix = ord(code[0].lower()) - ord('a') + 11
            return prefix + int(code[1:])
        else:
            return np.nan
    except Exception:
        return np.nan


def storeCodes(codes):
    """Stores the given sequence of ICD10 codes, so they can be exported to
    file at a later stage.

    The codes are stored in a list called ``store``, an attribute of this
    function.

    :arg codes: Sequence of ICD10 codes to add to the mapping file
    """
    store = getattr(storeCodes, 'store', [])
    store.append(codes)
    storeCodes.store = store


def saveCodes(fname, hierarchy, fields=None):
    """Saves any codes which have been stored via :func:`storeCodes` out to
    the specified file.

    :arg fname:     File to save the codes to.

    :arg hierarchy: :class:`ICD10Hierarchy` object containing the ICD10
                    hierarchy information.

    :arg fields:    Sequence of fields to include in the ``mapfile``. Defaults
                    to ``['code', 'value', 'description', 'parent_descs]``. May
                    contain any of the following:
                      - ``'code'``
                      - ``'value'``
                      - ``'description'``
                      - ``'parent_codes'``
                      - ``'parent_descs'``
    """

    if fields is None:
        fields = ['code', 'value', 'description', 'parent_descs']

    valid = ['code', 'value', 'description', 'parent_codes', 'parent_descs']
    if not all([f in valid for f in fields]):
        raise ValueError('Invalid field in: {}'.format(fields))

    store = getattr(storeCodes, 'store', [])
    store = pd.Series(list(it.chain(*store)))
    store = store[store.notna()]
    codes = np.sort(store.unique())

    def parent_codes(c):
        return ','.join(reversed(hierarchy.parents(c)))

    def parent_descs(c):
        parents = reversed(hierarchy.parents(c))
        descs   = [hierarchy.description(p) for p in parents]
        return ' '.join(['[{}]'.format(d) for d in descs])

    df = pd.DataFrame({'code' : codes})

    for f in fields:
        if   f == 'code':         continue
        elif f == 'value':        func = codeToNumeric
        elif f == 'description':  func = hierarchy.description
        elif f == 'parent_codes': func = parent_codes
        elif f == 'parent_descs': func = parent_descs

        df[f] = df['code'].apply(func)

    log.debug('Saving %u ICD10 codes to %s', len(df), fname)

    df = df[fields]
    df.to_csv(fname, sep='\t', index=False)
