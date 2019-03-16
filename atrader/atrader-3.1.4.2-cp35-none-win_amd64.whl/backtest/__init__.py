# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 11:34:37 2018

@author: kunlin.l
"""

import numpy as np
import pandas as pd

# noinspection PyUnresolvedReferences
from collections import Iterable
# noinspection PyUnresolvedReferences
from datetime import datetime
# noinspection PyUnresolvedReferences
import atrader.enums as enums
# noinspection PyUnresolvedReferences
from atrader.tframe import sysclsbase as cnt
# noinspection PyUnresolvedReferences
from atrader.tframe.sysclsbase import smm
# noinspection PyUnresolvedReferences
from atrader.tframe.sysclsbase import gv
from atrader.setting import get_setting, get_support, set_setting, get_version
# noinspection PyUnresolvedReferences
from atrader.tframe.utils.argchecker import apply_rule, verify_that

# noinspection PyUnresolvedReferences
from atrader.api.bpfactor import *
# noinspection PyUnresolvedReferences
from atrader.api.history import *
# noinspection PyUnresolvedReferences
from atrader.api.orders import *
# noinspection PyUnresolvedReferences
from atrader.api.regfuncs import *
# noinspection PyUnresolvedReferences
from atrader.tframe import clear_cache
# noinspection PyUnresolvedReferences
from atrader.tframe.snapshot import *
# noinspection PyUnresolvedReferences
from atrader.tframe.snapshot import ContextBackReal as Context
# noinspection PyUnresolvedReferences
from atrader.api import bpfactor as factors_api, history as history_api, orders as orders_api, regfuncs as reg_api
from atrader.api import fundamental as fundamental_api
# noinspection PyUnresolvedReferences
from atrader.api.fundamental import *

__all__ = [
    'np',
    'pd',
    'set_setting',
    'get_setting',
    'get_version',
    'get_support',
    'clear_cache',
    'set_backtest',
    'run_backtest',
    *factors_api.__all__,
    *history_api.__all__,
    *orders_api.__all__,
    *reg_api.__all__,
    *fundamental_api.__all__,
    'Context',
    'ContextFactor',
    'AccountSnapshot',
    'ExecutionSnapshot',
    'OrderSnapshot',
    'enums',
]


@smm.force_mode(gv.RUNMODE_CONSOLE)
@smm.force_phase(gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('strategy_name').is_instance_of(str),
            verify_that('file_path').is_exist_path(),
            verify_that('target_list').is_instance_of(Iterable),
            verify_that('frequency').is_valid_frequency(),
            verify_that('fre_num').is_instance_of(int).is_greater_than(0),
            verify_that('begin_date').is_instance_of((str, datetime)).is_valid_date(),
            verify_that('end_date').is_instance_of((str, datetime)).is_valid_date(),
            verify_that('fq').is_in((enums.FQ_BACKWARD,
                                     enums.FQ_FORWARD,
                                     enums.FQ_NA)))
def run_backtest(strategy_name='',
                 file_path='.',
                 target_list=(),
                 frequency='day',
                 fre_num=1,
                 begin_date='',
                 end_date=0,
                 fq=0):
    config = {
        'entry': {
            'strategy_name': strategy_name,
            'strategy_path': file_path,
            'targets': list(target_list),
            'frequency': frequency,
            'freq_num': fre_num,
            'begin_date': begin_date,
            'end_date': end_date,
            'fq': fq
        }
    }

    from .main import main_run_back_test
    return str(main_run_back_test(config))


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT)
@smm.force_mode(gv.RUNMODE_BACKTEST)
@apply_rule(verify_that('initial_cash').is_greater_than(0.0),
            verify_that('future_cost_fee').is_greater_than(0.0),
            verify_that('stock_cost_fee').is_greater_than(0.0),
            verify_that('rate').is_greater_than(0.0),
            verify_that('margin_rate').is_greater_than(0.0),
            verify_that('slide_price').is_greater_or_equal_than(0.0),
            verify_that('price_loc').is_instance_of(int).is_greater_or_equal_than(0),
            verify_that('deal_type').is_in((enums.MARKETORDER_DIRECT,
                                            enums.MARKETORDER_NONME_BEST_PRICE,
                                            enums.MARKETORDER_ME_BEST_PRICE)),
            verify_that('limit_type').is_in((enums.LIMITORDER_DIRECT,
                                             enums.LIMITORDER_NOPRICE_CANCEL)))
def set_backtest(initial_cash=1e7,
                 future_cost_fee=1.0,
                 stock_cost_fee=2.5,
                 rate=0.02,
                 margin_rate=1.0,
                 slide_price=0.0,
                 price_loc=1,
                 deal_type=0,
                 limit_type=0):
    return cnt.env.set_back_test(initial_cash, future_cost_fee, stock_cost_fee, rate,
                                 margin_rate, slide_price, price_loc, deal_type, limit_type)
