import pandas as pd
import numpy as np

def date_as_yyyyqq(date_series, return_int_repr = False):
    '''Convert date series into yyyyqq
    params:
    '''
    date_series_datetime = pd.to_datetime(date_series, format='%Y-%m-%d', errors='coerce')
    year_quarter_series = date_series_datetime.dt.year.astype('str')+'Q'+ \
                    date_series_datetime.dt.quarter.astype('str')
    year_quarter_as_int_series = date_series_datetime.dt.year*100 + \
                    date_series_datetime.dt.quarter
    if return_int_repr:
        return year_quarter_series, year_quarter_as_int_series
    else:
        return year_quarter_series


def import_clients_table(clients_filepath = 'data/CLIENTS.csv'):
    clients = pd.read_csv(clients_filepath, header=None)
    clients = clients.iloc[:, :4]
    clients.columns = ['client_id', 'client_name', 'client_abbrev', 'new_client']
    return clients


def update_quarter_str(quarter = '2017 Q4', quarter_change = 1):
    year, quarter = quarter.split(' ')
    year_num = int(year)
    quarter_num = int(quarter[-1])
    year_q_as_int = year_num*4 + quarter_num
    year_q_as_int_updated = year_q_as_int + quarter_change
    y, q = divmod(year_q_as_int_updated, 4) # for 2017Q4 this will result in year =2018, quarter = 0
    if q == 0:
        y = y-1
        q = 4
    new_quarter = '{} Q{}'.format(y,q)
    return new_quarter

def get_new_year_quarter_given_quarter_change(year=2010, quarter=4, quarter_change = 1):
    year_q_as_int = year*4 + quarter
    year_q_as_int_updated = year_q_as_int + quarter_change
    new_year, new_quarter = divmod(year_q_as_int_updated, 4) # for 2017Q4 this will result in year =2018, quarter = 0
    if new_quarter == 0:
        new_year = new_year-1
        new_quarter = 4
    return new_year, new_quarter

def convert_quarter_str_to_quarter_year(df, quarter_str_header='quarter'):
    '''
    Change field name of quarter to quarter string and then convert the quarter string to int representations of
    year and quarter. Put those into new columns, 'year' and 'quarter'
    :param df: DataFrame with 'quarter' field in format YYYYQQ like 2018Q1
    :param quarter_str_header: name of field with quarter string in it. default is 'quarter'
    :return: dataframe with 'quarter' renamed 'quarter_string' and two new int columns 'quarter' and 'year'
    '''
    df = df.rename({quarter_str_header:'quarter_string'},axis=1)
    yq = pd.DataFrame(df['quarter_string'].str.split('Q').tolist(), columns=['year','quarter'], index=df.index)
    yq['year'] = yq['year'].astype('int')
    yq['quarter'] = yq['quarter'].astype('int')

    df = pd.concat([df,yq], axis=1)

    return df

def convert_date_to_year_quarter_month_columns(df, date_col='date',suffix_for_new_cols=''):
    '''
    Take date columns in the format YYYY-MM-DD and make 3 new columns: year, quarter, month
    :param df: whatever dataframe you want to add these columns to
    :param date_col: column in the format YYYY-MM-DD
    :param suffix_for_new_cols: suffix to put at the end of the newly generated columns year, quarter, month
    :return: df with 3 new columns to represent the date field: year, quarter, month
    '''

    df[date_col] = pd.to_datetime(df[date_col], format='%Y-%m-%d', errors='coerce' )
    df['year{}'.format(suffix_for_new_cols)] = df[date_col].dt.year
    df['quarter{}'.format(suffix_for_new_cols)] = df[date_col].dt.quarter
    df['month{}'.format(suffix_for_new_cols)] = df[date_col].dt.month

    return df
