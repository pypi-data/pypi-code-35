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

    def test_concat(self):
        s1 = pd.Series(['a', 'b'])
        s2 = pd.Series(['c', 'd'])
        self.assertEqual(len(pd.concat([s1, s2])), 4)

    def test_shape(self):
        data = pd.read_csv('files/brain_size.csv', sep=';', na_values=".")
        self.assertEqual(data.shape[0], 40)    # 40 rows and 8 columns
        self.assertEqual(data.shape[1], 8)    # 40 rows and 8 columns

        
