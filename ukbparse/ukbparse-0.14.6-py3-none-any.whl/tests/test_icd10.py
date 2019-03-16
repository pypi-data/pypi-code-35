#!/usr/bin/env python
#
# test_icd10.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import textwrap as tw
import string
import random

import pytest

import numpy  as np
import pandas as pd

import ukbparse.icd10 as icd10

from . import tempdir


def test_icd10():
    with tempdir():

        data = tw.dedent("""
        coding\tmeaning\tnode_id\tparent_id
        a\ta desc\t5\t0
        b\tb desc\t1\t5
        c\tc desc\t3\t5
        d\td desc\t4\t3
        e\te desc\t2\t1
        """)

        with open('codings.tsv', 'wt') as f:
            f.write(data)

        h = icd10.readICD10CodingFile('codings.tsv')

        assert h.index('a') == 4
        assert h.index('b') == 0
        assert h.index('c') == 2
        assert h.index('d') == 3
        assert h.index('e') == 1
        assert h.coding(0)  == 'b'
        assert h.coding(1)  == 'e'
        assert h.coding(2)  == 'c'
        assert h.coding(3)  == 'd'
        assert h.coding(4)  == 'a'

        assert h.parents('a') == []
        assert h.parents('b') == ['a']
        assert h.parents('c') == ['a']
        assert h.parents('d') == ['c', 'a']
        assert h.parents('e') == ['b', 'a']

        assert h.description('a') == 'a desc'
        assert h.description('b') == 'b desc'
        assert h.description('c') == 'c desc'
        assert h.description('d') == 'd desc'
        assert h.description('e') == 'e desc'

        h.set('a', 'meta', 'aa')
        h.set('b', 'meta', 'bb')
        h.set('c', 'meta', 'cc')
        h.set('d', 'meta', 'dd')
        h.set('e', 'meta', 'ee')

        assert h.get('a', 'meta') == 'aa'
        assert h.get('b', 'meta') == 'bb'
        assert h.get('c', 'meta') == 'cc'
        assert h.get('d', 'meta') == 'dd'
        assert h.get('e', 'meta') == 'ee'


def test_codeToNumeric():
    letters = random.sample(string.ascii_uppercase, 20)
    numbers = np.random.randint(1, 1000, 20)
    codes   = ['{}{}'.format(l, n) for l, n in zip(letters, numbers)] + \
              ['badcode']
    exp     = [(ord(l.lower()) - ord('a') + 11) + n
               for l, n in zip(letters, numbers)] + [np.nan]

    conv = [icd10.codeToNumeric(c) for c in codes]

    exp  = np.array(exp)
    conv = np.array(conv)

    expna  = np.isnan(exp)
    convna = np.isnan(conv)

    assert np.all(     expna  ==       convna)
    assert np.all(exp[~expna] == conv[~convna])


def test_store_saveCodes():

    with tempdir():

        icd10.storeCodes.store = []

        with pytest.raises(ValueError):
            icd10.saveCodes('file', None, ['badfield'])

        codings = tw.dedent("""
        coding\tmeaning\tnode_id\tparent_id
        a10\ta desc\t5\t0
        b20\tb desc\t1\t5
        c30\tc desc\t3\t5
        d40\td desc\t4\t3
        e50\te desc\t2\t1
        f60\tf desc\t9\t9
        """)

        with open('codings.tsv', 'wt') as f:
            f.write(codings)

        codes = ['a10', np.nan, 'b20', 'c30', 'd40', 'e50']

        icd10.storeCodes(codes[:2])
        icd10.storeCodes(codes[2:])

        del codes[1]

        h = icd10.readICD10CodingFile('codings.tsv')

        icd10.saveCodes(
            'mapping.tsv', h,
            fields=['code', 'value', 'description',
                    'parent_codes', 'parent_descs'])

        values = [icd10.codeToNumeric(c) for c in codes]

        mf      = pd.read_csv('mapping.tsv', delimiter='\t', index_col=False)
        descs   = ['a desc', 'b desc', 'c desc', 'd desc', 'e desc']
        pcodes  = [np.nan, 'a10', 'a10', 'a10,c30', 'a10,b20']
        pdescs  = [np.nan, '[a desc]', '[a desc]',
                   '[a desc] [c desc]', '[a desc] [b desc]']

        gotpcodes = mf['parent_codes']
        gotpdescs = mf['parent_descs']

        assert (mf['code']         == codes) .all()
        assert (mf['value']        == values).all()
        assert (mf['description']  == descs) .all()
        assert np.isnan(gotpcodes.iloc[0])
        assert np.isnan(gotpdescs.iloc[0])
        assert (gotpcodes.iloc[1:] == pcodes[1:]).all()
        assert (gotpdescs.iloc[1:] == pdescs[1:]).all()
