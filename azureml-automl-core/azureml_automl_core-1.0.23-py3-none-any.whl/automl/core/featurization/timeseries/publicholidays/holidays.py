# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods and classes used to get public holidays infomation."""

import pandas as pd
import os.path
from datetime import date
from datetime import timedelta
import datetime
from typing import Union, Dict, Optional
import numpy as np
import pkg_resources


class Holidays:
    """Methods and classes used to get public holidays infomation."""

    def __init__(self):
        """Init the Holidays class to load the holiday data."""
        self.holiday_dataPath = pkg_resources \
            .resource_filename('azureml.automl.core',
                               os.path.join('featurization', 'timeseries', 'publicholidays',
                                            'data', 'holidays.csv'))
        self.df = pd.read_csv(self.holiday_dataPath,
                              parse_dates=['Date'],
                              date_parser=lambda x: pd.datetime.strptime(x, '%m/%d/%Y'))
        self.holidays_dates = None  # type: Optional[Dict[datetime.datetime, None]]
        self.holidays_dates_country = None  # type: Optional[str]

    def update_holidays_by_adding_window(self):
        """Generate the holidays csv with window into name."""
        holiday_origin_dataPath = pkg_resources \
            .resource_filename('azureml.automl.core',
                               'featurization/timeseries/publicholidays/data/holidays_origin.csv')
        window_dataPath = pkg_resources \
            .resource_filename('azureml.automl.core',
                               'featurization/timeseries/publicholidays/data/holidays_window.csv')
        df_origin = pd.read_csv(holiday_origin_dataPath,
                                parse_dates=['Date'],
                                date_parser=lambda x: pd.datetime.strptime(x, '%m/%d/%Y'))
        holiday_window = pd.read_csv(window_dataPath,
                                     parse_dates=['Date'],
                                     date_parser=lambda x: pd.datetime.strptime(x, '%m/%d/%Y'))
        df_com = df_origin.set_index(['Date', 'Name']) \
            .join(holiday_window.set_index(['Date', 'Name']), how='left')
        _holidays = df_com.reset_index()
        temp = _holidays.copy()
        temp.drop(columns=['LowerWindow', 'UpperWindow'], inplace=True)
        temp.reset_index(inplace=True, drop=True)

        # Here is the part to generate holiday window names
        for idx, row in _holidays.iterrows():
            lower = 7 if row['LowerWindow'] == 0 else int(row['LowerWindow'])
            upper = 7 if row['UpperWindow'] == 0 else int(row['UpperWindow'])
            curDate = pd.to_datetime(row['Date'])
            for i in range(1, lower + 1):
                newDate = curDate + timedelta(days=-i)
                if np.datetime64(newDate) not in temp['Date'].values:
                    _name = str(i) + ' days before ' + row['Name']
                    _country = row['Country']
                    temp = temp.append({'Name': _name, 'Date': newDate, 'Country': _country}, ignore_index=True)
            for i in range(1, upper + 1):
                newDate = curDate + timedelta(days=i)
                if np.datetime64(newDate) not in temp['Date'].values:
                    _name = str(i) + ' days after ' + row['Name']
                    _country = row['Country']
                    temp = temp.append({'Name': _name, 'Date': newDate, 'Country': _country}, ignore_index=True)

        temp['_IsPaidTimeOff'] = [1 if not np.isnan(x) and x else 0 for x in temp['IsPaidTimeOff']]
        temp.drop(columns=['IsPaidTimeOff'], inplace=True)
        temp = temp.rename(columns={'_IsPaidTimeOff': 'IsPaidTimeOff'}).sort_values(by=['Date'])
        temp.to_csv(self.holiday_dataPath, index=False, date_format='%m/%d/%Y')

    def get_holidays_dates(self, country_code: str = "US") -> Optional[Dict[datetime.datetime, None]]:
        """
        Get a Dict with Key of the dates of holidays.

        :param country_code: Indicate which country's holiday infomation will be used for the check.
        :return: The dict with dates of holidays as the keys and None as values.
        """
        country_name = self.get_country(country_code)
        if country_name is not None:
            if self.holidays_dates_country != country_name:
                self.holidays_dates = dict.fromkeys(self.df[self.df.Country == country_name]['Date'].tolist(), None)
                self.holidays_dates_country = country_name
            elif self.holidays_dates is None:
                self.holidays_dates = dict.fromkeys(self.df[self.df.Country == country_name]['Date'].tolist(), None)
        else:
            self.holidays_dates_country = None
            self.holidays_dates = None
        return self.holidays_dates

    def is_holiday(self, target_date: date, country_code: str = "US") -> bool:
        """
        Detect a date is a holiday or not.

        :param target_date: The date which needs to be check.
        :param country_code: Indicate which country's holiday infomation will be used for the check.
        :return: Whether the target_date is a holiday or not. True or False.
        """
        temp = self.get_holidays_dates(country_code)
        if temp is not None:
            return (target_date in temp)
        else:
            return False

    def get_holidays_in_range(self, start_date: date, end_date: date, country_code: str = "US") -> pd.DataFrame:
        """
        Get a list of holiday infomation base on the given date range.

        :param start_date: The start date of the date range.
        :param end_date: The end date of the date range.
        :param country_code: Indicate which country's holiday infomation will be used for the check.
        :return: A DataFrame which contains the holidays in the target date range.
        """
        rs = pd.DataFrame(columns=["Name", "Date", "IsPaidTimeOff"])
        rsdf_country = self.df
        country_name = self.get_country(country_code)
        if country_name is not None:
            rsdf_country = self.df[self.df.Country == country_name]
        else:
            return rs
        rs_date = rsdf_country[(rsdf_country.Date >= start_date) & (rsdf_country.Date <= end_date)]
        rs_date.drop(columns=['Country'], inplace=True)
        rs_date.reset_index(inplace=True, drop=True)
        rs = rs_date
        return rs

    def get_country(self, country_code: str = "US") -> Optional[str]:
        """
        Get the country name base on a given country code.

        :param country_code: Indicate which country's holiday infomation will be used for the check.
        :return: The country name in string type.
        """
        if country_code == 'US':
            return "United States"
        else:
            return None
