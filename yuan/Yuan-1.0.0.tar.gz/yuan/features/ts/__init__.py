#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '__init__.py'
__author__ = 'JieYuan'
__mtime__ = '19-3-12'
"""

import pandas as pd

t = pd.Timestamp(pd.datetime.today())


class TimeFeats(object):
    period_dict = dict(
        second=1,
        minute=2,
        hour=3,
        day=4,
        week=5,
        month=6,
        quarter=7,
        year=8
    )

    def __init__(self, max_time_period='year'):
        self.period = self.period_dict.get(max_time_period, 0)

    def feat_base(self, t=pd.Timestamp(pd.datetime.today())):
        ts = []
        if self.period_dict['year'] <= self.period:
            ts.append(t.is_leap_year)
            ts.append(t.year)
            ts.append(t.weekofyear)
            ts.append(t.dayofyear)
        elif self.period_dict['quarter'] <= self.period:
            ts.append(t.quarter)
            ts.append(t.quarter)
            ts.append(t.quarter)

