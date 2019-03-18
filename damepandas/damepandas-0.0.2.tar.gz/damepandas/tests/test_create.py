#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2019  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

from unittest import TestCase

import numpy as np
import pandas as pd

class TestBasics(TestCase):

    def test_series(self):
        s1 = pd.Series(['a', 'b'])
        self.assertEqual(len(s1), 2)

    def test_dataframe(self):
        df2 = pd.DataFrame([['c', 3], ['d', 4]], columns=['letter', 'number'])
        self.assertTrue(len(df2) > 0)
        
    def test_range(self):
        dates = pd.date_range('20130101', periods=6)
        self.assertTrue(len(dates) > 0)

    def test_fill_random(self):
        dates = pd.date_range('20130101', periods=6)
        df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
        self.assertTrue(len(df) > 0)

