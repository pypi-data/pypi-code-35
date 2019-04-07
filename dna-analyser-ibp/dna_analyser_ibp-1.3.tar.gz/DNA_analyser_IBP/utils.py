# utils.py
# !/usr/bin/env python3
"""Library with support functions used in multiple files.
Available functions:
- validate_email: Determine if str is valid email.
- generate_dataframe: Returns valid dataframe from given dictionary.
"""

import pandas as pd
import re


def generate_dataframe(res: dict or list) -> pd.DataFrame:
    """
    Generate dataframe from given dict or list.
    :param res: response dict or list from request
    :return: pandas dataframe
    """
    if isinstance(res, list):
        data = pd.DataFrame().from_records(res, columns=res[0].keys())
        return data
    data = pd.DataFrame(data=[res], columns=list(res.keys()))
    return data


def validate_email(value: str) -> bool:
    """
    Validate email for user account
    :param value: email account string
    :return: boolean TRUE if valid email format
    """

    return bool(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", value))
