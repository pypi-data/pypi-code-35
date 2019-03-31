"""
Utilities for converting user inputs into EIA dataset codes.

Functions
–––––––––
name_to_code
    Converts energy names into EIA energy codes.
date_to_code
    Converts date string into EIA data code.
"""
import datetime

def name_to_code(name):
    """
    Convert an energy source name to its corresponding EIA dataset numeric code.

    Parameters
    ––––––––––
    name : str
        The name of an EIA energy or energy group.

    Returns
    –––––––
    name_code : int
        The code corresponding to the energy source provided.
    """
    key_name = name.lower()
    energy_codes = {'coal':1,
                    'natural gas':2,
                    'petroleum':3,
                    'fossil fuel':4,
                    'nuclear':5,
                    'hydro':6,
                    'geothermal':7,
                    'solar':8,
                    'wind':9,
                    'biomass':10,
                    'renewable':11,
                    'primary':12}

    if key_name not in energy_codes:
        raise KeyError(f"Key '{name}' was not found in the EIA dataset; see "
                        "the documentation for implemented energy sources.")
    else:
        name_code = energy_codes[key_name]
    return name_code


def date_to_code(date):
    """
    Convert an input date to its corresponding EIA dataset numeric date code.

    Parameters
    ––––––––––
    date : str
        A date, given in the format 'YYYY','YYYYMM', 'YYYY-MM', or 'MM-YYYY'.
        Dashes can be substituted for periods, underscores, or forward slashes.

    Returns
    –––––––
    date_code : str
        The code corresponding to the energy source provided.
    """
    bad_format_err_msg = (f'Date "{date}" was not given in an acceptable '
                           'format; try formatting date as "YYYYMM".')
    acceptable_separators = ['-', '.', '/', '_']

    # Convert date to code
    if len(date) == 6:
        # A date was given as YYYYMM, the correct format
        date_code = date
    elif len(date) == 4:
        # Only a year was given, set date to January of the given year
        date_code = date + '01'
    elif len(date) == 7:
        for separator in acceptable_separators[1:]:
            date = date.replace(separator, acceptable_separators[0])
        date_list = date.split(acceptable_separators[0])
        if len(date_list) != 2:
            raise ValueError(bad_format_err_msg.format(date))
        # Check whether the first or second entry is the year
        if len(date_list[0]) == 4:
            date_code = ''.join(date_list)
        elif len(date_list[1]) == 4:
            date_code = ''.join(date_list[::-1])
        else:
            raise ValueError(bad_format_err_msg.format(date))
    else:
        raise ValueError(bad_format_err_msg.format(date))

    # Check reasonability of date provided
    try:
        # The date must be able to be expressed numerically
        int(date_code)
    except:
        raise ValueError(bad_format_err_msg.format(date))
    year = int(date_code[:4])
    month = int(date_code[4:])
    if year < 1900 or year > datetime.datetime.now().year:
        raise ValueError('Data only exists from the middle of the 20th '
                         'century to the present.')
    if month > 13 or month < 1:  # 13 denotes full year sum
        raise ValueError('A month must be given as a number 1-12')
    return date_code
