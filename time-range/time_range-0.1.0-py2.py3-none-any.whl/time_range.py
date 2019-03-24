# -*- coding: utf-8 -*-

"""Main module."""
import pandas as pd
import copy
from datetime import datetime, timedelta
from workalendar.usa import UnitedStates

def get_working_days(year, every_day=False,
                     holidays=UnitedStates(),
                     resolution = timedelta(days=1)):
    """Determine working days in a year

    """
    year_start = datetime(year, 1, 1)
    year_end = datetime(year+1, 1, 1)

    working_days = pd.date_range(year_start, year_end,
                                 freq=resolution,
                                 closed='left')

    df_calendar = pd.DataFrame(index=working_days)

    working_day_key = 'working_day'
    if every_day:
        df_calendar[working_day_key] = 1
    else:
        df_calendar[working_day_key] = [holidays.is_working_day(date.date()) for date in df_calendar.index]

    return df_calendar

def my_location(trips, year):
    """Details of location throughout year

    Must add up to a year.  Defaults to last year.
    """
    trips = copy.deepcopy(trips)
    for i, trip in enumerate(trips):
        trip['start'] = datetime(year, *trip['start'])
        if 'stop' not in trip:
            if i == len(trips) - 1:
                trip['stop'] = datetime(year+1, 1, 1)
            else:
                trip['stop'] = datetime(year, *trips[i+1]['start'])

        trip['dt'] = trip['stop'] - trip['start']
        if 'state' not in trip:
            trip['state'] = trip['country']

    df = pd.DataFrame.from_records(trips)
    df = df.set_index(['country', 'state'])

    # Check that it's the location for the year (possibly leap year)
    if df['dt'].sum() == 365 or df['dt'].sum() == 366:
        raise ValueError("Location must be for whole year")

    return df

def time_distribution_raw(trips, year=datetime.now().year):
    # Get working days in year
    df_wd = get_working_days(year=year)

    # Make DataFrame of trips
    df = my_location(trips, year=year)

    # Default is each day isn't at location
    for key, value in df.iterrows():
        df_wd[key] = 0

    # For each trip, set days to True for that location
    for key, value in df.iterrows():
        df_wd[key] += (value['start'] <= df_wd.index) & \
            (df_wd.index < value['stop']) & \
            df_wd['working_day']

    return df_wd

def form_2555_data(working_day_rate, country_code = 'US', **kwargs):
    df = time_distribution_raw(**kwargs)
    df = df[df['working_day']]
    
    index_selection = [x for x in df.columns if len(x) > 1 and x[0] == country_code]
    df[country_code] = df[index_selection].sum(axis=1)
    
    group_key = (df[country_code] - df[country_code].shift(1)).ne(0).cumsum()

    form_data = []
    for k, v in df[country_code].groupby(group_key):
        days = v.sum()
        if days == 0:
            continue
        trip_total = (v.sum() * working_day_rate).round()
        form_data.append((v.index[0].date(),
                          v.index[-1].date(),
                          v.sum(),
                          trip_total))

    return pd.DataFrame(data=form_data,
                        columns=['Start', 'End', 'Days', 'Salary [USD]'])

def time_distribution(**kwargs):
    return time_distribution_raw(**kwargs).sum(axis=0)


def fraction_of_year(trips,
                     year=datetime.now().year,
                     income=None):
    series = time_distribution(trips=trips, year=year)
    df = pd.DataFrame.from_dict({'days' : series,
                                 'fraction_of_year' : series/series['working_day']})
    
    if income:
        df['income'] = income * df['fraction_of_year']

    return df


