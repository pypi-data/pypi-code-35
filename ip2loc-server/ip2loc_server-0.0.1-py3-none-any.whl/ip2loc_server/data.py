# -*- coding: utf-8 -*-

"""
- Check data version compare with page: https://lite.ip2location.com/database/ip-country-region-city-latitude-longitude
- Restore csv data to sqlite
"""

import logging
import os
import re

import requests

from .util import unzip as do_unzip

DATA_PAGE_URL = 'https://lite.ip2location.com/database/ip-country-region-city-latitude-longitude'
DATA_DOWNLOAD_URL = 'https://lite.ip2location.com/download?db=db5&type=csv&version=4'

CURRENT_PATH = os.path.split(os.path.realpath(__file__))[0]
VERSION_FILE_PATH_NAME = os.path.join(CURRENT_PATH, 'data/data_version')

# noinspection PyBroadException
try:
    current_version = open(VERSION_FILE_PATH_NAME, 'r').read().strip()
except Exception as re:
    current_version = '???'
    logging.error(
        f"Read version from file '{VERSION_FILE_PATH_NAME}' fail: {re}", exc_info=True)


def check_data_version() -> bool:
    res = requests.get(DATA_PAGE_URL)
    version = re.search(
        r'<strong>Current Version</strong></td>\s*<td.*?>(.*?)</td>', res.text).group(1)
    if version == current_version:
        logging.info(f'Current data version is the latest: {version}')
        return True
    else:
        logging.warning(
            f'\nCurrent data version is not the latest\n'
            f'\tCurrent: {current_version}\n'
            f'\tLatest:  {version}\n'
            f"\tSee 'Track the Latest Data' in README\n"
        )
        return False


def _update_version(specified_version: str=None):
    if specified_version:
        # noinspection PyBroadException
        try:
            specified_version = specified_version.strip('\n ')
            open(VERSION_FILE_PATH_NAME, 'w').write(specified_version)
        except Exception as we:
            logging.error(
                f"Write version 'f{specified_version}' to file '{VERSION_FILE_PATH_NAME}' fail: {we}", exc_info=True)


def load_data(csv_path_name: str, zip_path_name: str, sqlite_path_name: str,
              unzip: bool=False, specified_version: str=None):
    """ Load data from 'data/raw_data/IP2LOCATION-LITE-DB5.CSV' to 'data/data.db'"""
    import sqlite3

    if unzip:
        logging.info(f"Unzip '{zip_path_name}' \nto '{csv_path_name}'")
        do_unzip(zip_path_name, csv_path_name)
        if not os.path.exists(csv_path_name) or not os.path.getsize(csv_path_name) > 0:
            logging.fatal(f"Unzip '{zip_path_name}' to '{csv_path_name}' failed.")
            exit(2)
    sqlite_bak_path_name = f'{sqlite_path_name}.bak'

    # backup old sqlite db and always restore data to an empty sqlite db
    if os.path.exists(sqlite_path_name) and os.path.isfile(sqlite_path_name):
        os.rename(sqlite_path_name, sqlite_bak_path_name)
        logging.debug(f"Backup '{sqlite_path_name} to '{sqlite_bak_path_name}")
    conn = None
    try:
        conn = sqlite3.connect(sqlite_path_name)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE `ip2location`(
            `id` INTEGER PRIMARY KEY,
            `ip_from` INTEGER,
            `ip_to` INTEGER,
            `country_code` CHAR(2),
            `country_name` CHAR(64),
            `region_name` CHAR(128),
            `city_name` CHAR(128),
            `latitude` REAL,
            `longitude` REAL
        );
        """)
        conn.commit()
        with open(csv_path_name, 'r') as csv_file:
            cnt = 0
            while True:
                line = csv_file.readline()
                if not line or not line.strip('\n'):
                    break
                line = line.strip('\n')
                sql = f'INSERT INTO ip2location VALUES ({cnt},{line})'
                cnt += 1
                cursor.execute(sql)
                if cnt % 100000 == 0:
                    conn.commit()
                    logging.info(f"{cnt} items have been stored to sqlite db.")

        conn.commit()
        logging.info(f"{cnt} items have been stored to sqlite db.")
        cursor.close()
    except (KeyboardInterrupt, InterruptedError):  # signal interrupted -> recovery
        if os.path.exists(sqlite_bak_path_name) and os.path.isfile(sqlite_bak_path_name):
            os.rename(sqlite_bak_path_name, sqlite_path_name)
        logging.warning(f"User interrupted during CSV to SQLITE."
                        f"\nSqlite data recovery from backup file '{sqlite_bak_path_name}'")
    except Exception as e:  # exception -> recovery
        if os.path.exists(sqlite_bak_path_name) and os.path.isfile(sqlite_bak_path_name):
            os.rename(sqlite_bak_path_name, sqlite_path_name)
        else:  # no backup file means its the first time loading data
            os.remove(sqlite_path_name)
            logging.fatal(f'First time sqlite db initial from csv error', exc_info=True)
            exit(3)
        logging.error(repr(e), exc_info=True)
    else:  # del backup sqlite db
        logging.info('CSV to SQLITE success.')
        if os.path.exists(sqlite_bak_path_name) and os.path.isfile(sqlite_bak_path_name):
            # noinspection PyBroadException
            try:
                os.remove(sqlite_bak_path_name)
                logging.debug(f"Backup database '{sqlite_bak_path_name} has been deleted.")
            except Exception as e:
                logging.error(f"Try to remove backup database '{sqlite_bak_path_name} error: {e}", exc_info=True)
        _update_version(specified_version=specified_version)
        logging.debug('Version file updated success.')
    finally:
        if conn:
            conn.close()


