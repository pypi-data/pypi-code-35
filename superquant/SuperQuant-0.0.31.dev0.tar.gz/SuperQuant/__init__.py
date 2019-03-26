#coding :utf-8

__version__ = '0.0.30.dev0'
__author__ = 'junfeng li'
logo = ''
# import sys
# import os
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(BASE_DIR)

# fetch methods
# from SuperQuant.SQFetch.Fetcher import SQ_quotation  # 统一的获取接口
#
# from SuperQuant.SQFetch import (SQ_fetch_get_stock_day, SQ_fetch_get_trade_date, SQ_fetch_get_stock_min, SQ_fetch_get_stock_xdxr,
#                                SQ_fetch_get_stock_indicator, SQ_fetch_get_stock_realtime, SQ_fetch_get_stock_transaction,
#                                SQ_fetch_get_index_day, SQ_fetch_get_index_min, SQ_fetch_get_stock_list, SQ_fetch_get_stock_info,
#                                SQ_fetch_get_stock_block, SQ_fetch_get_stock_transaction_realtime, SQ_fetch_get_security_bars,
#                                SQ_fetch_get_future_day, SQ_fetch_get_future_min, SQ_fetch_get_future_list, SQ_fetch_get_future_transaction,
#                                SQ_fetch_get_future_transaction_realtime, SQ_fetch_get_future_realtime, SQ_fetch_get_bond_list, SQ_fetch_get_index_list,
#                                SQ_fetch_get_hkfund_list, SQ_fetch_get_hkfund_day, SQ_fetch_get_hkfund_min,
#                                SQ_fetch_get_hkindex_list, SQ_fetch_get_hkindex_day, SQ_fetch_get_hkindex_min,
#                                SQ_fetch_get_hkstock_list, SQ_fetch_get_hkstock_day, SQ_fetch_get_hkstock_min,
#                                SQ_fetch_get_usstock_list, SQ_fetch_get_usstock_day, SQ_fetch_get_usstock_min,
#                                SQ_fetch_get_option_list, SQ_fetch_get_option_day, SQ_fetch_get_option_min,
#                                SQ_fetch_get_globalindex_day, SQ_fetch_get_globalindex_min, SQ_fetch_get_globalindex_list,
#                                SQ_fetch_get_macroindex_list, SQ_fetch_get_macroindex_day, SQ_fetch_get_macroindex_min,
#                                SQ_fetch_get_exchangerate_list, SQ_fetch_get_exchangerate_day, SQ_fetch_get_exchangerate_min,
#                                SQ_fetch_get_globalfuture_list, SQ_fetch_get_globalfuture_day, SQ_fetch_get_globalfuture_min)
# from SuperQuant.SQFetch.SQQuery import (SQ_fetch_trade_date, SQ_fetch_account, SQ_fetch_financial_report,
#                                        SQ_fetch_stock_day, SQ_fetch_stock_min, SQ_fetch_ctp_tick,
#                                        SQ_fetch_index_day, SQ_fetch_index_min, SQ_fetch_index_list,
#                                        SQ_fetch_future_min, SQ_fetch_future_day, SQ_fetch_future_list,
#                                        SQ_fetch_future_tick, SQ_fetch_stock_list, SQ_fetch_stock_full, SQ_fetch_stock_xdxr,
#                                        SQ_fetch_backtest_info, SQ_fetch_backtest_history, SQ_fetch_stock_block, SQ_fetch_stock_info,
#                                        SQ_fetch_stock_name, SQ_fetch_quotation, SQ_fetch_quotations)
# from SuperQuant.SQFetch.SQCrawler import SQ_fetch_get_sh_margin, SQ_fetch_get_sz_margin
#
# from SuperQuant.SQFetch.SQQuery_Advance import *
#
# # save
# from SuperQuant.SQSU.main import (SQ_SU_save_stock_list, SQ_SU_save_stock_day, SQ_SU_save_index_day, SQ_SU_save_index_min, SQ_SU_save_stock_info_tushare,
#                                  SQ_SU_save_stock_min, SQ_SU_save_stock_xdxr, SQ_SU_save_stock_info, SQ_SU_save_stock_min_5, SQ_SU_save_index_list, SQ_SU_save_future_list,
#                                  SQ_SU_save_stock_block, SQ_SU_save_etf_day, SQ_SU_save_etf_min, SQ_SU_save_financialfiles)
#
# from SuperQuant.SQSU.user import (SQ_user_sign_in, SQ_user_sign_up)
# from SuperQuant.SQSU.save_strategy import SQ_SU_save_strategy
#
# # Data
# from SuperQuant.SQData import (SQ_data_tick_resample_1min, SQ_data_tick_resample, SQ_data_day_resample, SQ_data_min_resample, SQ_data_ctptick_resample,
#                               SQ_data_calc_marketvalue, SQ_data_marketvalue,
#                               SQ_data_stock_to_fq,
#                               SQ_DataStruct_Stock_day, SQ_DataStruct_Stock_min,
#                               SQ_DataStruct_Day, SQ_DataStruct_Min,
#                               SQ_DataStruct_Future_day, SQ_DataStruct_Future_min,
#                               SQ_DataStruct_Index_day, SQ_DataStruct_Index_min, SQ_DataStruct_Indicators, SQ_DataStruct_Stock_realtime,
#                               SQ_DataStruct_Stock_transaction, SQ_DataStruct_Stock_block, SQ_DataStruct_Series, SQ_DataStruct_Financial,
#                               from_tushare, QDS_StockMinWarpper, QDS_StockDayWarpper, QDS_IndexDayWarpper, QDS_IndexMinWarpper)
# from SuperQuant.SQData.dsmethods import *
# # Setting
# from SuperQuant.SQSetting.SQLocalize import SQ_path, setting_path, cache_path, download_path, log_path
#
# # Util
# from SuperQuant.SQUtil import (SQ_util_date_stamp, SQ_util_time_stamp, SQ_util_ms_stamp, SQ_util_date_valid, SQ_util_calc_time,
#                               SQ_util_realtime, SQ_util_id2date, SQ_util_is_trade, SQ_util_get_date_index, SQ_util_get_last_day, SQ_util_get_next_day, SQ_util_get_order_datetime, SQ_util_get_trade_datetime,
#                               SQ_util_get_index_date, SQ_util_select_hours, SQ_util_date_gap, SQ_util_time_gap, SQ_util_get_last_datetime, SQ_util_get_next_datetime,
#                               SQ_util_select_min, SQ_util_time_delay, SQ_util_time_now, SQ_util_date_str2int,
#                               SQ_util_date_int2str, SQ_util_date_today, SQ_util_to_datetime,
#                               SQ_util_mongo_setting, SQ_util_async_mongo_setting, SQ_util_mongo_sort_ASCENDING, SQ_util_mongo_sort_DESCENDING,
#                               SQ_util_log_debug, SQ_util_log_expection, SQ_util_log_info,
#                               SQ_util_cfg_initial, SQ_util_get_cfg,
#                               SQ_Setting, DATABASE, info_ip_list, stock_ip_list, future_ip_list,
#                               SQ_util_web_ping, SQ_util_send_mail,
#                               trade_date_sse, SQ_util_if_trade, SQ_util_if_tradetime,
#                               SQ_util_get_real_datelist, SQ_util_get_real_date,
#                               SQ_util_get_trade_range, SQ_util_get_trade_gap,
#                               SQ_util_save_csv, SQ_util_code_tostr, SQ_util_code_tolist,
#                               SQ_util_dict_remove_key,
#                               SQ_util_multi_demension_list, SQ_util_diff_list,
#                               SQ_util_to_json_from_pandas, SQ_util_to_list_from_numpy, SQ_util_to_list_from_pandas, SQ_util_to_pandas_from_json, SQ_util_to_pandas_from_list,
#                               SQ_util_mongo_initial,  SQ_util_mongo_status, SQ_util_mongo_infos,
#                               SQ_util_make_min_index, SQ_util_make_hour_index,
#                               SQ_util_random_with_topic, SQ_util_file_md5,
#                               MARKET_TYPE, ORDER_STATUS, TRADE_STATUS, MARKET_ERROR, AMOUNT_MODEL, ORDER_DIRECTION, ORDER_MODEL, ORDER_EVENT,
#                               MARKET_EVENT, ENGINE_EVENT, RUNNING_ENVIRONMENT, FREQUENCE, BROKER_EVENT, BROKER_TYPE, DATASOURCE, OUTPUT_FORMAT)  # SQPARAMETER
#
# import argparse

###
# # from SuperQuant import SQApplication
# # from SuperQuant import SQARP
# # from SuperQuant import SQCmd
# from SuperQuant import SQData
# from SuperQuant import SQDatabase
# from SuperQuant import SQEngine
# from SuperQuant import SQFetch
# # from SuperQuant import SQIndicator
# # from SuperQuant import SQMarket
# from SuperQuant import SQSetting
# from SuperQuant import SQSU
# from SuperQuant import SQUtil

# from SuperQuant.SQFetch.SQQuery_Advance import *
# from SuperQuant.SQSU import save_financialfiles
# from SuperQuant.SQUtil import SQAuth
# check
import sys
if sys.version_info.major != 3 or sys.version_info.minor not in [4, 5, 6, 7, 8]:
    print('wrong version, should be 3.4/3.5/3.6/3.7/3.8 version')
    sys.exit()


# import ALL
__all__ = ['SQData','SQDatabase','SQEngine','SQFetch','SQSetting','SQSU','SQUtil']
from SuperQuant import *
## import SQData
from SuperQuant.SQData import base_datastruct
from SuperQuant.SQData import data_fq
from SuperQuant.SQData import data_resample
from SuperQuant.SQData import financial_mean
from SuperQuant.SQData import SQBlockStruct
from SuperQuant.SQData import SQDataStruct
from SuperQuant.SQData import SQFinancialStruct
## import SQDatabase
from SuperQuant.SQDatabase import SQDBSetting
from SuperQuant.SQDatabase import SQMongo
## import SQEngine
from SuperQuant.SQEngine.SQEvent import SQ_Event, SQ_Worker
from SuperQuant.SQEngine.SQTask import SQ_Task
from SuperQuant.SQEngine.SQThreadEngine import SQ_Thread, SQ_Engine
## import SQFetch
from SuperQuant.SQFetch import SQTdx
from SuperQuant.SQFetch import SQfinancial
from SuperQuant.SQFetch import base
from SuperQuant.SQFetch import SQQuery
from SuperQuant.SQFetch import SQQuery_Advance
## import SQSetting
from SuperQuant.SQSetting import host
from SuperQuant.SQSetting import SQSetting
from SuperQuant.SQSetting import SQLocalize
from SuperQuant.SQSetting import SQParameter
## import SQSU
from SuperQuant.SQSU import save_tdx
from SuperQuant.SQSU import save_account
from SuperQuant.SQSU import save_financialfiles
from SuperQuant.SQSU import user
## import SQUtil
from SuperQuant.SQUtil import ParallelSim
from SuperQuant.SQUtil import SQAuth
from SuperQuant.SQUtil import SQBar
from SuperQuant.SQUtil import SQCfg
from SuperQuant.SQUtil import SQCode
from SuperQuant.SQUtil import SQCrawler
from SuperQuant.SQUtil import SQcrypto
from SuperQuant.SQUtil import SQCsv
from SuperQuant.SQUtil import SQDate
from SuperQuant.SQUtil import SQDate_trade
from SuperQuant.SQUtil import SQDateTools
from SuperQuant.SQUtil import SQDict
from SuperQuant.SQUtil import SQError
from SuperQuant.SQUtil import SQFile
from SuperQuant.SQUtil import SQList
from SuperQuant.SQUtil import SQLogs
from SuperQuant.SQUtil import SQMail
from SuperQuant.SQUtil import SQPlot
from SuperQuant.SQUtil import SQRandom
from SuperQuant.SQUtil import SQText
from SuperQuant.SQUtil import SQTransform
from SuperQuant.SQUtil import SQWebutil
# 导入便捷包方便调用
from SuperQuant.SQFetch.SQQuery_Advance import *



# SQ_util_log_info('Welcome to SuperQuant, the Version is {}'.format(__version__))
# SQ_util_log_info(logo)