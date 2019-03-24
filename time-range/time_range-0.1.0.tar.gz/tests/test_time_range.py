#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `time_range` package."""

import pytest
import pandas as pd

import time_range as tr

def test_working_days():
    assert tr.get_working_days(2017, every_day=True).sum()[0] == 365

    assert tr.get_working_days(2014).sum()[0] == 251

    assert isinstance(tr.get_working_days(2014),
                      pd.core.frame.DataFrame)
    


def test_time_distribution():
    trips = ({'country': 'NL', 'start': (1, 1)},
             {'country': 'ES', 'start': (3, 4, 14, 0)},
             {'country': 'NL', 'start': (4, 11, 19, 50)},
             {'country': 'US', 'start': (5, 22, 12), 'state': 'NJ'},
             {'country': 'US', 'start': (6, 30, 12, 30), 'state': 'TX'},
             {'country': 'US', 'start': (7, 3, 16, 28), 'state': 'NJ'})

    print(tr.time_distribution(trips=trips, year=2004))
    assert tr.time_distribution(trips=trips, year=2004)[('NL', 'NL')] == 73.0
    assert tr.time_distribution(trips=trips, year=2004)['working_day'] == 251    
    assert tr.time_distribution(trips=trips, year=2004)[('US', 'TX')] == 2
