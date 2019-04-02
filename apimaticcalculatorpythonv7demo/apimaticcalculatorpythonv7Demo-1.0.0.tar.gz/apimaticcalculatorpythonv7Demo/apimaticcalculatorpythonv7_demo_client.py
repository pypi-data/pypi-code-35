# -*- coding: utf-8 -*-

"""
    apimaticcalculatorpythonv7Demo

    This file was automatically generated for testing by APIMATIC v2.0 ( https://apimatic.io ).
"""

from apimaticcalculatorpythonv7Demo.decorators import lazy_property
from apimaticcalculatorpythonv7Demo.configuration import Configuration
from apimaticcalculatorpythonv7Demo.controllers.calculator_dev_ops_conf import CalculatorDevOpsConf


class Apimaticcalculatorpythonv7DemoClient(object):

    config = Configuration

    @lazy_property
    def calculator_dev_ops_conf(self):
        return CalculatorDevOpsConf()



