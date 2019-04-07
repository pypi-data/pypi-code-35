# -*- coding: utf-8 -*-

"""Top-level package for pretty-table-printer."""

__author__ = """Collin Meyers"""
__email__ = 'cfmeyers@gmail.com'
__version__ = '0.1.0'

from .pretty_table_printer import (
    ColumnSpec,
    RowCollection,
    pretty_date,
    pretty_money,
    pretty_generic_decimal,
    pretty_int,
    guess_row_collection,
    clean_headers,
)
