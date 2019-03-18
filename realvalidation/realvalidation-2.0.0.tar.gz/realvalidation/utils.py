from openpyxl import Workbook as OpenPyxlWorkbook

from .constants import PHONE_COLUMN_REGEX, PHONE_DIGIT_REGEX

from .errors import (
    ResponseCodeNotOkError, MissingPhoneNumberError, InsufficientBalanceError,
    InvalidCustomerError, InvalidPhoneFormatError, InvalidPhoneError
)

import logging
import os
import re

log = logging.getLogger(__name__)


def is_dnc_json_response_on_dnc(response):
    """Determines if json response from DNC API is on dnc

    Parameters
    ----------
    response : dict
        dictionary response from RealValidation DNC API

    Returns
    -------
    bool
        True/False value whether response is on DNC or not

    """
    on_dnc = False

    # put response code/msg into variables
    response_code = response.get('RESPONSECODE')
    response_msg = response.get('RESPONSEMSG')

    # raise for status
    response_raise_for_status(response_code, response_msg)

    if response.get('national_dnc') != 'N':
        on_dnc = True

    if response.get('state_dnc') != 'N':
        on_dnc = True

    if response.get('dma') != 'N':
        on_dnc = True

    if response.get('litigator') != 'N':
        on_dnc = True

    log.debug('is_dnc_json_on_dnc: {} {}'.format(on_dnc, response))

    return on_dnc


def response_raise_for_status(response_code, response_msg):
    # raise for status
    if response_code != 'OK' or response_msg != '':
        # missing phone number in request
        if (
            response_code == '-1'
            and response_msg == 'Missing Phone Number'
        ):
            raise MissingPhoneNumberError

        # customer not authorized to use api
        elif (
            response_code == '102'
            and 'Invalid Customer' in response_msg
        ):
            raise InvalidCustomerError

        # insufficient balance in account
        elif (
            response_code == '102'
            and 'Insufficient Balance' in response_msg
        ):
            raise InsufficientBalanceError

        # invalid phone
        elif (
            response_code == 'invalid-phone'
            and response_msg == 'Phone Number does not exist'
        ):
            raise InvalidPhoneError

        # unknown error
        else:
            raise ResponseCodeNotOkError


def write_rows_to_workbook(rows, workbook_path, workbook_name):
    """Writes row to workbook

    Parameters
    ----------
    rows : list
        list of rows to write to workbook
    workbook_path : str
        Path to write workbook to
    workbook_name : str
        Name of the workbook

    """
    wb = OpenPyxlWorkbook()

    ws = wb.active
    ws.title = workbook_name

    for row in rows:
        ws.append(row)

    file_path = os.path.join(workbook_path, "{}.xlsx".format(workbook_name))

    wb.save(file_path)


def sanitize_phone(phone, regex=r'[^0-9]'):
    """Uses regex sub to sanitize characters from phone

    Parameters
    ----------
    phone : str
        Phone string to sanitize

    regex:  regex
        Regex to use to sub characters from string. Defaults to ``r'[^0-9]'``

    Returns
    -------
    str
        sanitized phone string

    """
    return re.sub(regex, '', phone)


def is_value_phone_identifier(value):
    """Returns True/False whether value is [Pp]hone or 10 numerical digits only

    Parameters
    ----------
    value : str
        Value to determine if phone identifier

    Returns
    -------
    bool
        True/False value whether phone is a valid identifier

    """
    return any(re.match(regex, value, re.IGNORECASE)
               for regex in [PHONE_DIGIT_REGEX, PHONE_COLUMN_REGEX])


def get_cell_values_from_row(row):
    """Returns string representation of cell values from row in a list

    Parameters
    ----------
    row : list
        list of values

    Returns
    -------
    list
        string representation of cell values from row in a list

    """
    return [str(cell.value) for cell in row]


def enumerate_phone_column_index_from_row(row):
    """Enumerates the phone column from a given row. Uses Regexs

    Parameters
    ----------
    row : list
        list of cell values from row

    Returns
    -------
    int
        phone column index enumerated from row

    """
    # initial phone_column_index value
    phone_column_index = -1

    # generate cell values from row
    cell_values = get_cell_values_from_row(row)

    # iterate through cell values
    for i in range(len(cell_values)):
        value = cell_values[i]

        # Check if value matches "[Pp]hone || 0000000000"
        if is_value_phone_identifier(value):
            phone_column_index = i
            break

    return phone_column_index


def verify_phone_format(phone):
    """Verifies a phone using PHONE_REGEX

    Parameters
    ----------
    phone : str
        Phone to be verified.

    Returns
    -------
    bool
        True if successful, otherwise method raises exception (see below)

    Raises
    ------
    InvalidPhoneFormatException
        If the phone couldn't be verified using PHONE_REGEX

    """
    if re.match(PHONE_DIGIT_REGEX, phone):
        return True

    raise InvalidPhoneFormatError
