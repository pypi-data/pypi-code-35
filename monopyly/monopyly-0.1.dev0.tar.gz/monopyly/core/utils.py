import datetime
import re

now = datetime.datetime.now()

def format_category(category_string):
    """
    Accept a category name and return a label.

    Categories are named in the database without spaces and in all lowercase.
    This function changes labels to title case and exchanges spaces for
    underscores.

    Parameters
    ––––––––––
    category_string : str
        The unformatted category (column) name.

    Returns
    –––––––
    formatted_category : str
        The formatted category name for display.
    """
    formatted_category = category_string.replace('_', ' ').title()
    return formatted_category

def format_date(date_string):
    """
    Accept several types of dates and return a date in YYYY-MM-DD format.

    This function accepts dates in a variety of formats (MM/DD, MM/DD/YY,
    MM/DD/YYYY, or YYYY/MM/DD, using any non-numeric character as the separator)
    and returns a consistent representation of the data as 'YYYY-MM-DD'.

    Parameters
    ––––––––––
    date_string : str
        The incoming string with a date.

    Returns
    –––––––
    formatted_date : str
        A formatted representation of the date (YYYY-MM-YY).
    """
    # Split string by consecutive strings of numbers
    date_list = re.findall('\d+', date_string)
    if len(date_list) == 3:
        # 3 values were given, check the order
        if len(date_list[0]) == 4:
            # First value is the year
            year = date_list.pop(0)
        else:
            # Last value is the year
            year = date_list.pop()
            if len(year) == 2:
                # Only two digits were given, so construct a 4-digit year
                milcen = now.year//100
                prefix = milcen if int(year) <= now.year%100 else milcen-1
                year = f'{prefix}{year}'
    elif len(date_list) == 2:
        # No year given, so use this year
        year = now.year
    else:
        raise ValueError('The date must be given as `YYYY-MM-DD, or another '
                         'conventional format.')
    month, day = date_list
    formatted_date = f'{year}-{month:0>2}-{day:0>2}'
    return formatted_date
