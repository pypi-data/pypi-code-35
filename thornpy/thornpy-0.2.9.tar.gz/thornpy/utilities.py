"""Miscellaneous tools.

"""
def num_to_ith(num):
    """Converts an integer to a string containing an ordinal number (1st, 2nd, 3rd, ect.)
    
    Parameters
    ----------
    num : int
        Number
    
    Returns
    -------
    str
        Ordinal number

    """    
    if num == -1:
        return 'last'
    elif num < -1:    
        value = str(num+1).replace('-', '')
    else:
        value = str(num)
    
    last_digit = value[-1]

    if len(value) > 1 and value[-2] == '1':
        suffix = 'th'
    elif last_digit == '1':
        suffix = 'st'
    elif last_digit == '2':
        suffix = 'nd'
    elif last_digit == '3':
        suffix = 'rd'
    else:
        suffix = 'th'

    if num < -1:
        suffix += ' to last'

    return  value + suffix