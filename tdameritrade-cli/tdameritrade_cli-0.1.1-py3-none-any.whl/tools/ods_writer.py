import functools
import os
from collections import OrderedDict
from datetime import date
from typing import Callable, List

import click
from pyexcel_ods import get_data, save_data

from tdameritrade_cli import __version__


def check_version(func: Callable) -> Callable:
    """Context manager that checks the written spreadsheet has a supported version."""

    @functools.wraps(func)
    def wrapper_check_version(*args, **kwargs):
        try:
            data = args[0].sheet_data
            version = data['Cover Sheet'][0][4]
            maj_min = version.split('.')[:2]
            assert maj_min == __version__.split('.')[:2], f'Passed document version ({version}) at ' \
                f'{args[0].sheet_path} is incompatible with current version of the CLI ({__version__}).'

        except FileNotFoundError:
            pass
        except KeyError:
            raise KeyError('Document at sheetpath is incompatible with current version of the CLI.')
        except IndexError:
            raise IndexError('Document at sheetpath is incompatible with current version of the CLI.')

        value = func(*args, **kwargs)
        return value
    return wrapper_check_version


class ODSWriter(object):
    def __init__(self, sheet_path: str):
        """
        Writes financial data to ods files

        Args:
            sheet_path (str): Path to the ods document to either create or append.

        """

        self.sheet_path = sheet_path
        self._sheet_exists = os.path.isfile(sheet_path)

    def write_positions(self, liq_value: str, positions: List[List[str]]):
        """
        Write positions data to an ods document.

        Args:
            liq_value: The current liquidation value of a TDA portfolio.
            positions: List[List[str]] where each List[str] is [position_id, position_type, position_value].

        """

        if not self._sheet_exists:
            self._write_to_sheet(self._sheet_template)

        current_data = self._update_cover_sheet(liq_value, positions)

        new_ids = [pos[0] for pos in positions]
        existing_ids = [sheet for sheet in current_data][1:]
        for i, new_id in enumerate(new_ids):
            if new_id in existing_ids:
                current_data[new_id] = self.update_position(positions[i], current_data[new_id])
            else:
                current_data.update(self.new_position(positions[i]))
        click.echo(f'Writing positions information to {self.sheet_path}')
        self._write_to_sheet(current_data)

    @check_version
    def _write_to_sheet(self, data: OrderedDict):
        save_data(self.sheet_path, data)

    def _update_cover_sheet(self, liq_value: str, positions: List[List[str]]):
        """
        Update the ods cover sheet.

        Args:
            liq_value: The liquidation value of a TD portfolio
            positions: A list of position lists where each sublist is [position_id, position_type, position_value]

        Returns:
            current_book (OrderedDict): The entire ods document.

        """

        current_book = self.sheet_data
        cover_sheet = current_book['Cover Sheet']

        # Update current month with current portfolio value
        current_month = date.today().strftime('%B')
        for i, month in enumerate(cover_sheet[1]):
            if current_month == month:
                # Write all months after the current as having the present value
                current_liquidation = [liq_value] * (13-i)
                cover_sheet[2][i:] = current_liquidation

        # Update the current positions
        new_cover_sheet = cover_sheet[:5]
        for pos in positions:
            new_cover_sheet.append(pos)

        current_book['Cover Sheet'] = new_cover_sheet
        return current_book

    @property
    def sheet_data(self):
        """
        The data currently in the sheet located at self.sheet_path.

        Returns: OrderedDict of data.

        """

        return get_data(self.sheet_path)

    @property
    def _sheet_template(self):
        months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December']
        sheet_template = OrderedDict()
        sheet_template.update({'Cover Sheet': [['Investments', f'{date.today().strftime("%Y")}', '',
                                                'Version:', f'{__version__}'],
                                               months,
                                               ['Liq Value:', ' ', ' ', ' ', ' ', ' ',
                                                ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                               [],
                                               ['Current Positions:'],
                                               ['ID', 'Type', 'Market Value']]
                               })
        return sheet_template

    @staticmethod
    def update_position(position: List[str], pos_sheet: List[List]) -> List[List]:
        """
        Update an existing position in an ods document

        Args:
            position: List of the form [position_id, position_type, position_value] to update.
            pos_sheet: The sheet in the ods document describing the existing position.

        Returns:
            Updated pos_sheet

        """

        entered_dates = [row[0] for row in pos_sheet][2:]
        today = date.today().strftime('%x')
        if today in entered_dates:  # Don't update more than once per day
            return pos_sheet
        pos_sheet.append([date.today().strftime('%x'), position[2]])
        return pos_sheet

    @staticmethod
    def new_position(position: List[str]) -> OrderedDict:
        """
        Create a sheet with a new position.

        Args:
            position: List of the form [position_id, position_type, position_value] to create.

        Returns:
            template (OrderedDict): The new sheet with the first data point given by position included.

        """

        template = OrderedDict()
        template.update({
            position[0]: [
                [position[0], ' ', 'type:', position[1]],
                [' '],
                [date.today().strftime('%x'), position[2]]
            ]
        })
        return template
