# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods and classes used to get public holidays infomation."""

import pandas as pd

from datetime import date
from datetime import timedelta
from typing import Union
import pkg_resources


class Holidays:
    """Methods and classes used to get public holidays infomation."""

    def __init__(self):
        """Init the Holidays class to load the holiday data."""
        holiday_dataPath = pkg_resources \
            .resource_filename('automl', 'client/core/common/featurization/publicholidays/data/holidays.csv')
        window_dataPath = pkg_resources \
            .resource_filename('automl', 'client/core/common/featurization/publicholidays/data/holidays_window.csv')
        self.holiday_df = pd.read_csv(holiday_dataPath,
                                      parse_dates=['Date', 'StartDate', 'EndDate'],
                                      date_parser=lambda x: pd.datetime.strptime(x, '%m/%d/%Y'))
        self.holiday_window = pd.read_csv(window_dataPath,
                                          parse_dates=['Date'],
                                          date_parser=lambda x: pd.datetime.strptime(x, '%m/%d/%Y'))
        self.df = self.holiday_df.set_index(['Date', 'Name']) \
            .join(self.holiday_window.set_index(['Date', 'Name']), how='left')
        self.df = self.df.reset_index()

    def is_holiday(self, target_date: date, country_code: str = "US") -> bool:
        """
        Detect a date is a holiday or not.

        :param target_date: The date which needs to be check.
        :param country_code: Indicate which country's holiday infomation will be used for the check.
        :return: Whether the target_date is a holiday or not. True or False.
        """
        rsdf_country = self.df
        country_name = self.get_country(country_code)
        if country_name is not None:
            rsdf_country = self.df[self.df.Country == country_name]
        rs_date = rsdf_country[rsdf_country.Date == target_date]
        return not rs_date.empty

    def get_holidays_in_range(self, start_date: date, end_date: date, country_code: str = "US") -> pd.DataFrame:
        """
        Get a list of holiday infomation base on the given date range.

        :param start_date: The start date of the date range.
        :param end_date: The end date of the date range.
        :param country_code: Indicate which country's holiday infomation will be used for the check.
        :return: A DataFrame which contains the holidays in the target date range.
        """
        rs = pd.DataFrame(columns=["Name", "Date", "LowerWindow", "UpperWindow"])
        rsdf_country = self.df
        country_name = self.get_country(country_code)
        if country_name is not None:
            rsdf_country = self.df[self.df.Country == country_name]
        else:
            return rs
        rs_date = rsdf_country[(rsdf_country.Date >= start_date) & (rsdf_country.Date <= end_date)]
        rs_date = rs_date.loc[:, ['Name', 'Date', 'LowerWindow', 'UpperWindow']]
        targetDate = start_date
        while(targetDate <= end_date):
            rs_temp = rs_date[rs_date.Date == targetDate]
            if not rs_temp.empty:
                rs = rs.append(rs_temp, ignore_index=True)
            targetDate = targetDate + timedelta(days=1)
        return rs

    def get_country(self, country_code: str = "US") -> Union[str, None]:
        """
        Get the country name base on a given country code.

        :param country_code: Indicate which country's holiday infomation will be used for the check.
        :return: The country name in string type.
        """
        if country_code == 'US':
            return "United States"
        else:
            return None
