"""
Utilities for converting EIA dataset codes into meaningful information.

Functions
–––––––––
name_to_code
    Converts energy names into EIA energy codes.
date_to_code
    Converts date string into EIA data code.
"""
import datetime
import pandas as pd

EIA_CODES = {1: 'coal',
             2: 'natural gas',
             3: 'petroleum',
             4: 'fossil fuel',
             5: 'nuclear',
             6: 'hydro',
             7: 'geothermal',
             8: 'solar',
             9: 'wind',
             10: 'biomass',
             11: 'renewable',
             12: 'primary'}

def code_to_name(code):
    """
    Convert an EIA dataset numeric code to its corresponding energy source name.

    Parameters
    ––––––––––
    code : int
        The code corresponding to a specific energy source.;

    Returns
    –––––––
    name : str
        The name of an EIA energy or energy group.
    """
    if code not in EIA_CODES:
        raise KeyError(f"Code '{code}' does not correspond to an EIA energy "
                          "code.")
    else:
        name = EIA_CODES[code]
    return name

def code_to_period(code):
    """
    Convert an EIA date code (YYYYMM) into a pandas period.

    EIA date codes are given as 'YYYYMM'. The month value can be either 1-12
    for the standard months, or 13 for a yearly total. This function processes
    the date code and outputs a pandas period object matching the date code.

    Parameters
    ––––––––––
    code : str
        The six digit date code to be converted into a pandas period.

    Returns
    –––––––
    period : Period object
        The pandas period object corresponding to the given date code.
    """
    month_code = int(code[-2:])
    if month_code == 13:
        period = pd.Period(code[:-2], 'Y')
    elif month_code in range(1,13):
        period = pd.Period(code, 'M')
    else:
        raise ValueError(f"Date code '{code}' is not a valid date.")
    return period

def parse_input_date(date):
    """
    Process an input date to a format that can be compared with the data.

    Parses a date given in a variety of string formats by a user into a pandas
    period object. This period object can be compared easily against the period
    objects of the dataset.

    Parameters
    ––––––––––
    date : str
        A date, given in the format 'YYYY','YYYYMM', 'YYYY-MM', or 'MM-YYYY'.
        Dashes can be substituted for periods, underscores, or forward slashes.

    Returns
    –––––––
    period : Period object
        The pandas period object corresponding to the input energy.
    """
    bad_format_err_msg = (f'Date "{date}" was not given in an acceptable '
                           'format; try formatting date as "YYYYMM".')
    acceptable_separators = ['-', '.', '/', '_']

    # Convert date to code
    if len(date) == 4:
        # Only a year was given, consider the whole year
        date += '13'
    elif len(date) == 7:
        for separator in acceptable_separators[1:]:
            date = date.replace(separator, acceptable_separators[0])
        date_list = date.split(acceptable_separators[0])
        if len(date_list) != 2:
            raise ValueError(bad_format_err_msg.format(date))
        # Check whether the first or second entry is the year
        if len(date_list[0]) == 4:
            date = ''.join(date_list)
        elif len(date_list[1]) == 4:
            date = ''.join(date_list[::-1])
        else:
            raise ValueError(bad_format_err_msg.format(date))
    elif len(date) != 6:
        raise ValueError(bad_format_err_msg.format(date))

    # Check reasonability of date provided
    try:
        # The date must be able to be expressed numerically
        int(date)
    except:
        raise ValueError(bad_format_err_msg.format(date))
    year = int(date[:4])
    month = int(date[4:])
    if year < 1900 or year > datetime.datetime.now().year:
        raise ValueError('Data only exists from the middle of the 20th '
                         'century to the present.')
    if month > 13 or month < 1:  # 13 denotes full year sum
        raise ValueError('A month must be given as a number 1-12 (or use 13 '
                         'to denote a full year.')
    period = code_to_period(date)
    return period
