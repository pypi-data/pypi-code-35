#!/usr/bin/env python
"""
Update the pyleiades app data from the EIA website.

All EIA Monthly Energy Review (MER) data can be found on the EIA website,
specifically at 'https://www.eia.gov/totalenergy/data/browser/'. This module
downloads that data and stores it in the project's data directory for access by
the main pyleiades package.

Functions
–––––––––
main :
    Execute the update process.
move_current_data_to_archive :
    Move the existing current data to archival storage.
get_current_data_publication_date :
    Get the publication date for the current data (to use when labeling the
    data in the archive).
generate_filename :
    Generate a filename for a table, given its type and format.
download_eia_data_table :
    Download a data table by type and format from the EIA website.
"""
import os
import datetime
import urllib.request
import pandas as pd
from pyleiades import DATA_DIR, ARCHIVE_DIR

# Define links to the EIA Monthly Energy Review tables
BASE_URL = 'https://www.eia.gov/totalenergy/data/browser'
MER_TABLES = {'overview': 'T01.01',
              'production': 'T01.02',
              'consumption': 'T01.03',
              'imports': 'T01.04A',
              'exports': 'T01.04B'}
OVERVIEW_TABLE = os.path.join(DATA_DIR, 'EIA_MER_overview')
TABLE_FORMATS = {'csv': 'csv',
                 'xls': 'xlsx'}

def generate_filename(table_type, table_format):
    """Generate the table's filename given its type and file format."""
    ext = TABLE_FORMATS[table_format]
    return f'EIA_MER_{table_type}.{ext}'

def get_data_publication_date():
    """Get the date of the current EIA MER."""
    data = pd.read_excel(f'{OVERVIEW_TABLE}.xlsx')
    column = data['U.S. Energy Information Administration'].dropna()
    date_cell = column[column.astype(str).str.contains('Release Date')].iloc[0]
    date_string = date_cell.split(':')[1].strip()
    date = datetime.datetime.strptime(date_string, '%B %d, %Y').date()
    return date

def include_data_in_archive():
    """
    Include the downloaded EIA data in the archive.

    Add a folder with the downloaded EIA dataset to the archive location (files
    are all less than one megabyte, so storing them for the conceivable future
    is not problematic.)
    """
    # The file exists, get the date and format it properly
    date = str(get_data_publication_date()).replace('-', '')
    new_archive_dir = os.path.join(ARCHIVE_DIR, f'EIA_MER_{date}')
    try:
       os.makedirs(new_archive_dir)
    except OSError:
        # Give the user a chance to avoid files being overwritten
        answer = input("It seems as though you already have the most recent "
                       "dataset archived already. Would you like to "
                       "overwrite that information? [y/n] ")
        if answer[0].lower() != 'y':
            return
    # Move the files to the archive
    for table_title in MER_TABLES:
        for table_format in TABLE_FORMATS:
            filename = generate_filename(table_title, table_format)
            current_path = os.path.join(DATA_DIR, filename)
            if os.path.isfile(current_path):
                new_path = os.path.join(new_archive_dir, filename)
                os.rename(current_path, new_path)
    print(f'Created the archive directory:\n\t{new_archive_dir}')



def download_eia_data_table(table_title):
    """
    Downloads an table type from the EIA website.

    Accesses the EIA website and downloads the given table. Tables are
    downloaded as both CSV files and Excel spreadsheets, and saved to the
    `data` directory.

    Parameters
    ––––––––––
    table : str
        The name of the table to be downloaded (e.g. production, consumption,
        imports, exports).
    """
    for table_format in TABLE_FORMATS:
        # URL from https://www.eia.gov/totalenergy/data/browser/ download link
        url = f'{BASE_URL}/{table_format}.php?tbl={MER_TABLES[table_title]}'
        filename = generate_filename(table_title, table_format)
        urllib.request.urlretrieve(url, f'{DATA_DIR}/{filename}')

def main():
    """Update the app's data from the EIA website."""
    print()
    # Download the files, with printed status updates
    print('Downloading the most recent EIA monthly energy review data:')
    for table_title in MER_TABLES:
        print(f'\t-Energy {table_title} table')
        download_eia_data_table(table_title)
    print()
    # Include the data in the archive
    include_data_in_archive()
    print('\nDownload complete.\n')
