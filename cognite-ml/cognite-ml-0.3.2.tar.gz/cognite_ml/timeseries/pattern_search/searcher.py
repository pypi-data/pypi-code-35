#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: quetran
"""

import logging

from cognite_ml.timeseries.pattern_search.algorithms.DTW.searcher import DTW

logger = logging.getLogger(__name__)


class PatternSearch:
    def __init__(self, timeout=300):
        self.timeout = timeout

    def search(self, input_timeseries, pattern_timeseries, min_range=None, max_range=None, limit=10):
        searcher = DTW(min_range, max_range, limit)
        matches = searcher.search(input_timeseries, pattern_timeseries, self.timeout)

        result = {"data": {"items": matches}}
        return result
