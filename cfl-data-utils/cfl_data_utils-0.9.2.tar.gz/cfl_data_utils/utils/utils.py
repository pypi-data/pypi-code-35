from datetime import datetime, timedelta
from os import get_terminal_size
from platform import system
from typing import Union
from io import BufferedReader, BufferedWriter, TextIOWrapper
from sys import stdout
from time import time

from cfl_data_utils.references.constants import TYPE_TESTS, SQL_TYPE_DICT, WINDOWS

if not system() == WINDOWS:
    from blessings import Terminal


def assert_date_is_yesterday(date: datetime):
    """Checks that a date is yesterday for data validation

    :param date: The date to be validated
    :raises AssertionError: if the date isn't today
    """
    yesterday = datetime.today() - timedelta(days=1)
    assert date.date() == yesterday.date()


def sqlize(string):
    """SQL-izes a string to ensure the characters are all legal

    :param string: The string to be processed
    :return: the processed SQL-friendly string
    """
    return string.upper().replace(' ', '_').replace('-', '_').replace(':', '_')


def get_var_type(value: Union[int, float, str, datetime], sql: bool = False):
    """Gets a Python type from a string variable

    :param value: The variable to be type-checked
    :param sql: Flag to decide if return type should be SQL-ized (e.g. int vs INT)

    :return: Type of value passed in
    """

    for typ, test in TYPE_TESTS:
        try:
            test(value)  # TODO: can probably break this into something like `assert type(value) == value`?
            return SQL_TYPE_DICT[typ] if sql else typ
        except (ValueError, AssertionError, TypeError):
            continue
    return 'TEXT' if sql else str


def increment_progress_display(processed: int = None, goal: int = 100, start_time: float = None,
                               downloaded: Union[int, float] = None, print_line: int = None,
                               terminal_width: int = None):
    """Displays a progress bar to track data processing progress

    :param processed: the amount of processing done so far (e.g. number of iterations)
    :param goal: the total amount of processing to be done
    :param start_time: the time at which the processing was started
    :param downloaded: amount of data downloaded
    :param print_line: the line of the terminal to print the progress bar on
    :param terminal_width: width of terminal used for sizing progress bar
    :return:
    """

    try:
        terminal_width = get_terminal_size()[0] if not terminal_width else terminal_width
    except OSError:
        terminal_width = 100

    def output():
        if processed:
            progressbar_width = 64 if terminal_width > 74 else terminal_width - 10
            progress = int(processed / (goal / progressbar_width))
            stdout.write(
                '|' +
                '#' * progress +
                '-' * (progressbar_width - progress) +
                f'| {(processed / goal) * 100:.2f}%  |  ' +
                f'{processed}/{goal} items  |  '
            )

        if start_time:
            time_elapsed = time() - start_time
            stdout.write(f'Time Elapsed: {timedelta(seconds=int(time_elapsed))}  |  ')
            if processed:
                seconds_remaining = int((time_elapsed / processed) * (goal - processed))
                stdout.write(f'Time remaining: {timedelta(seconds=seconds_remaining)}  |  ')

            if downloaded:
                speed = f'{float((downloaded // (time() - start_time)) / 1000000):.3f}'
                stdout.write(f'Avg Speed: {speed} MB/s  |  ')

        if downloaded:
            stdout.write(f'Data processed: {downloaded / 1000000:.2f} MB')

        stdout.flush()

        return processed + 1 if processed is not None else None

    if not system() == WINDOWS:
        term = Terminal()
        with term.location(0, print_line):
            return output()
    else:
        return output()


def time_to_epoch(human_time: str = None, year: int = datetime.now().year, month: int = datetime.now().month,
                  day: int = datetime.now().day, hour: int = datetime.now().hour, minute: int = datetime.now().minute,
                  second: int = datetime.now().second):
    """Converts a time to an epoch timestamp

    :param year: year to be converted
    :param month: month to be converted
    :param day: day to be converted
    :param hour: hour to be converted
    :param minute: minute to be converted
    :param second: second to be converted
    :param human_time: a more human-readable time to allow easier entry
    :return:
    """

    if human_time:
        if type(human_time) == int or get_var_type(human_time) == int:
            human_time_str = str(human_time)
            if len(human_time_str) == 8:  # YYYYMMDD
                time_elem_list = [human_time_str[:4], human_time_str[4:6], human_time_str[6:8], '00', '00', '00']
            elif len(human_time_str) == 12:  # YYYYMMDDHHMM
                time_elem_list = [human_time_str[:4], human_time_str[4:6], human_time_str[6:8], human_time_str[8:10],
                                  human_time_str[10:], '00']
            elif len(human_time_str) == 13:  # Probably passed epoch time by accident
                return human_time
            elif len(human_time_str) == 14:  # YYYYMMDDHHMMSS
                time_elem_list = [human_time_str[:4], human_time_str[4:6], human_time_str[6:8], human_time_str[8:10],
                                  human_time_str[10:12], human_time_str[12:]]
            else:
                raise ValueError(f'Invalid human_time passed: {human_time}\n'
                                 f'Use this format: YYYYMMDDHHMMSS | YYYY-MM-DD HH:MM:SS')
        else:
            time_elem_list = human_time.split('-')[:-1] + human_time.split('-')[-1].split()[:-1] + \
                             human_time.split('-')[-1].split()[-1].split(':')

            # noinspection PyUnboundLocalVariable
            if not len(time_elem_list) == 6:
                raise ValueError(f'Invalid human_time passed: {human_time}\n'
                                 f'Use this format: YYYYMMDDHHMMSS | YYYY-MM-DD HH:MM:SS')

        str_year = time_elem_list[0]
        str_month = time_elem_list[1]
        str_day = time_elem_list[2]
        str_hour = time_elem_list[3]
        str_minute = time_elem_list[4]
        str_second = time_elem_list[5]
    else:
        str_year = str(year)
        str_month = str(month).rjust(2, '0')
        str_day = str(day).rjust(2, '0')
        str_hour = str(hour).rjust(2, '0')
        str_minute = str(minute).rjust(2, '0')
        str_second = str(second).rjust(2, '0')

    try:
        date_time = datetime.strptime(
            f'{str_year} {str_month} {str_day} {str_hour} {str_minute} {str_second}',
            '%Y %m %d %H %M %S'
        ).timestamp()
        return int(date_time) * 1000
    except ValueError:
        raise ValueError(
            f'Invalid arguments passed to time_to_epoch function. Strings: '
            f'{str_year} {str_month} {str_day} {str_hour} {str_minute} {str_second}'
        )


def get_col_types(data: Union[BufferedReader, BufferedWriter, TextIOWrapper, str, dict], sql: bool = False):
    """Returns column headers and their types from a CSV or JSON file

    :param data: the file to be parsed
    :param sql: flag to say whether the types should be in SQL dialect or not
    :return: list of column dictionaries of the form {name: xxx, type: xxx}
    """

    cols = None
    first_rows = []
    try:
        with open(data) as f:
            for i, row in enumerate(f):
                if i == 0:
                    cols = row.rstrip('\n').split(',')
                elif 0 < i < 20:
                    first_rows.append(row.rstrip('\n').split(','))
                else:
                    break
    except TypeError:
        cols = list(data[0].keys())
        first_rows = [None] * 20
        i = 0
        while i < len(first_rows):
            first_rows[i] = list(data[i].values())
            i += 1

    col_type_list = []
    for i, col in enumerate(cols):
        type_found = False
        for j, row in enumerate(first_rows):
            if not (row[i] == '' or row[i] is None):
                type_found = True
                col_type_list.append({'name': col, 'type': get_var_type(row[i], sql)})
                break
        if not type_found:
            col_type_list.append({'name': col, 'type': get_var_type('', sql)})

    return col_type_list
