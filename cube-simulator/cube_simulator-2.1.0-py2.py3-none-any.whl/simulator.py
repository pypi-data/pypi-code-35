__author__ = 'SHASHANK'

from datetime import datetime as dt
from dateutil.parser import parse
from .date_utils import DateUtils
from .flows import *

"""
Assumptions :
    1. PG Transfer Money From midnight to midnight
    2. Timezone is IST
    3. BSE ATIN And BD share same holidays
"""


def setup(transaction_datetime):
    transaction_date = dt.strptime(transaction_datetime, "%Y-%m-%d %H:%M:%S")
    dateutil = DateUtils(transaction_date)
    return dateutil


def setup_for_date(transaction_date):
    dateutil = DateUtils(transaction_date)
    return dateutil

def getdate(mode, transaction_date, scheme_id, gateway=0, toacc=""):

    def cal_trans_latency():
        # NODAL #
        if mode == 0:
            event_list, order_dates = execute_cube_nodal_account_flow(next_date, dateutil)
            return order_dates['bill']['update_in_app_date'] - timedelta(hours=5, minutes=30)

        # MF #
        if mode == 1:
            if toacc != "bank":
                try:
                    event_list, order_dates = execute_cube_iccl_flow(next_date, dateutil)
                    return order_dates[scheme_id]['update_in_app_date'] - timedelta(hours=5, minutes=30, seconds=0)
                except Exception as e:
                    return order_dates['Default']['update_in_app_date'] - timedelta(hours=5, minutes=30, seconds=0)

            else:
                event_list, order_dates = execute_mf_redemption_flow(next_date, dateutil, scheme_id)
                return order_dates['mfr']['credit_date'] - timedelta(hours=5, minutes=30)

        # NEFT #
        if mode == 2:
            event_list, order_dates = execute_cube_current_account_flow(next_date, dateutil)
            return order_dates['neft']['update_in_app_date'] - timedelta(hours=5, minutes=30)

        # GOLD #
        if mode == 3:
            return transaction_date - timedelta(hours=5, minutes=30)

        # PURNARTHA FEES #
        if mode == 5:
            return transaction_date - timedelta(hours=5, minutes=30)

        # P2P #
        if mode in [4, 6, 8, 9]:
            if toacc != "bank":
                event_list, order_dates = execute_p2plending_flow(next_date, dateutil)
                return order_dates['p2plending']['update_in_app_date'] - timedelta(hours=5, minutes=30)
            else:
                event_list, order_dates = execute_p2p_withdraw_flow(next_date, dateutil)
                return order_dates['p2plending']['update_in_app_date'] - timedelta(hours=5, minutes=30)
        raise ValueError("Processor Not Implemented")

    if gateway in [0, 1, 3, 4]:
        date_str = (transaction_date + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
        dateutil = setup(date_str)
        next_date = dateutil.get_next_bank_working_day()
    elif gateway == 2:
        dateutils = setup((transaction_date + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M:%S"))
        debit_date = dateutils.get_next_date_for_nach_file()
        date_str = debit_date.strftime("%Y-%m-%d %H:%M:%S")
        dateutil = setup(date_str)
        next_date = dateutil.get_next_bank_working_day()
    else:
        raise ValueError(" Gateway Not Implemented")
    return cal_trans_latency()

if __name__ == "__main__":
    date = parse("2019-04-04 11:30:29")
    getdate(1, date, 'EDGCGP-GR', 2, None)