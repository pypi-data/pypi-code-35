# -*- coding: utf-8 -*-

"""
Core of ip2loc
Notice: no connection pool for the reason that tornado is signle thread
"""

import ipaddress
import math
import logging
import sqlite3
import time

total_len = 0
max_loops = 0
total_len_update_time = 0
TOTAL_LEN_UPDATE_INTERVAL = 5 * 60  # 5 min


def ip2int(ip: str) -> int:
    return int(ipaddress.IPv4Address(ip))


def update_data_length(conn: sqlite3.Connection) -> None:
    global total_len, max_loops, total_len_update_time

    if total_len and total_len_update_time and \
            time.time() - total_len_update_time <= TOTAL_LEN_UPDATE_INTERVAL:
        return  # use cache

    cursor = None
    # noinspection PyBroadException
    try:
        cursor = conn.cursor()
        sql = 'SELECT MAX(id) FROM ip2location'
        cursor.execute(sql)
        total_len = cursor.fetchone()[0] + 1
        max_loops = round(math.log2(total_len)) + 1
        total_len_update_time = time.time()
        logging.debug(f'update_data_length success, total_len: {total_len}, max_loops: {max_loops}')
    except Exception as e:
        logging.error(f'update_data_length error: {e}', exc_info=True)
        if not total_len:
            raise e
    finally:
        if cursor:
            cursor.close()


def ip2loc(conn: sqlite3.Connection, ip: str) -> dict:
    """ IPV4 to geo location implementation
    Using binary search
    """
    update_data_length(conn)
    int_ip = ip2int(ip)
    cursor = None
    # noinspection PyBroadException
    try:
        cursor = conn.cursor()
        start, end = 0, total_len

        for _ in range(max_loops):
            idx = (start + end) // 2
            sql = f'SELECT id, ip_from, ip_to, country_code, country_name, region_name, city_name, latitude, longitude'\
                  f' FROM ip2location WHERE id={idx}'
            cursor.execute(sql)
            ret = cursor.fetchone()
            ip_from, ip_to = ret[1], ret[2]
            if ip_from <= int_ip <= ip_to:
                return {
                    'ip': ip,
                    'country_code': ret[3],
                    'country_name': ret[4],
                    'region_name': ret[5],
                    'city_name': ret[6],
                    'latitude': ret[7],
                    'longitude': ret[8],
                }
            if int_ip < ip_from:
                end = idx - 1
                continue
            elif int_ip > ip_to:
                start = idx + 1
        else:
            # Though I think this would never happen here,
            # carefully using 'max_loops' is better here than just 'while True'
            raise Exception(f"'{ip}' exceeds max loops {max_loops}!")
    except Exception as e:
        logging.error(f'ip2loc error: {e}, ip: {ip}', exc_info=True)
        return {}
    finally:
        if cursor:
            cursor.close()
