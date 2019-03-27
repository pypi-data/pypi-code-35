from datetime import datetime
from datetime import timedelta
import json
import pandas as pd
import logging


logging.info('Started')
# Do I have the right or not, if I have right for how long
# Given a date, for how long I stay in Schengen countries?


def transform_data(ref_date, entries, exits):
    logging.info(
        'Control if Reference Date is Null and default to today if so')
    today = datetime.now()
    if ref_date == '':  # or is None
        reference_date = today
    else:
        reference_date = datetime.strptime(ref_date, '%Y-%m-%d')

    logging.info('Control if Reference Date is past date, not interesting')
    if reference_date < today:
        exit()  # need a function generating json response
    logging.info('Create reference date/entries/exists dataframe')
    df_entries = pd.DataFrame.from_dict(entries)
    df_entries['Coef'] = 1
    df_exits = pd.DataFrame.from_dict(exits)
    df_exits['Coef'] = 0
    df_raw_input = df_entries.append(df_exits, ignore_index=True, sort=True)

    df_raw_input.columns = ['Date', 'Coef']
    df_raw_input['Date'] = pd.to_datetime(df_raw_input['Date'])

    data_ref = {'Date': [reference_date], 'Coef': [0]}
    df_reference_date = pd.DataFrame(data=data_ref)
    df_reference_date['Date'] = pd.to_datetime(df_reference_date['Date'])

    df = df_raw_input.append(df_reference_date, ignore_index=True, sort=True)
    df_sorted = df.sort_values(by=['Date'], ascending=False)
    df_sorted = df_sorted.reset_index(drop=True)

    logging.info('Find the number of days stayed according to constraints')
    df_sorted['Previous'] = df_sorted.Date.shift(-1)
    df_sorted['Schengen'] = 0

    logging.info('Making operations on days, to take into account enty date')
    buff = []
    list_days = (1 - df_sorted['Coef']) * \
        (df_sorted['Date'] - df_sorted['Previous'])
    for x in list_days:
        a = x.days
        if a == 0:
            buff.append(a)
        else:
            buff.append(a + 1)

    df_sorted['Schengen'] = buff
    df_sorted.dropna(inplace=True)
    df_sorted['CumSum'] = df_sorted['Schengen'].cumsum()
    return {'df': df_sorted, 'reference_date': reference_date}


def remaining_days(df_sorted, max_period, max_days_to_stay):

    logging.info('Find the number of days stayed within the last 180 days')
    max_back = df_sorted['Date'][0] - timedelta(days=max_period)
    df_final = df_sorted.loc[df_sorted['Date'] >= max_back]
    already_stayed = max(df_final['CumSum'])
    remaining = max_days_to_stay - already_stayed
    return remaining


def analysis(reference_date, entries, exits, remaining):
    logging.info('Verdict')
    departure_date = reference_date + timedelta(remaining)
    ref_date = reference_date.strftime('%Y-%m-%d')
    dep_date = departure_date.strftime('%Y-%m-%d')
    if remaining >= 0:
        print('I m happy to say you that you can stay in Schengen\
         countries!\n ')
        print('Still remains %d day(s)' %
              remaining)  # function generating json
        print('Last day for departure %s' %
              departure_date.strftime('%Y-%m-%d'))
        response = {'Reference Date': ref_date, 'Entries': entries,
                    'Exits': exits, 'Remaining': remaining,
                    'Departure Date': dep_date,
                    'Message': 'I m happy!You can stay in Schengen countries!'}
    else:
        print('I m sorry, I will miss you!')
        print('You exceed your stay by %d day(s)' % -remaining)
        # function generation json
        print('Maybe you forgot enter an exit date!')
        response = {'Reference Date': ref_date, 'Entries': entries,
                    'Exits': exits, 'Exceed': -
                    remaining,
                    'Message': 'You exceed your stay! Maybe you forgot enter an exit date!'}
    return response


def not_accurate_entries_exists(df):
    diff = df['Coef'] - df['Coef'].shift(-1)
    flag = 0 in diff.values
    return flag


def process(data):
    # data = json.load(content)
    transformed = transform_data(
        data['Reference Date'], data['Entries'],
        data['Exits'])
    not_accurate = not_accurate_entries_exists(transformed['df'])
    if not_accurate is False:
        remaining = remaining_days(transformed['df'], 180, 90)
        response = analysis(
            transformed['reference_date'], data['Entries'], data['Exits'], remaining)
    else:
        response = {'data': data,
                    "Error": "Entries or Exits not accurate"}
    json_export = json.dumps(response)
    print(json_export)
    return json_export

