# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 20:55:26 2017

@author: Young Ju Kim
"""


import pandas as pd
import psycopg2 as pg
import sqlalchemy as sa
# import ibm_db_sa

from unipy.utils.decorator import profiler


__all__ = [
    'insert_mysql',
    'insert_mariadb',
]


@profiler(type='printing')
def _insert_mysql_printer(
    data_frame,
    db=None,
    table=None,
    h=None,
    port=3306,
    u=None,
    p=None,
    if_exists='append',
        ):

    print('Using MariaDB')

    # DB Connection
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'
    engine = sa.create_engine(conn_str.format(u, p, h, str(port), db))

    # Get a DataFrame
    data_frame.to_sql(
        con=engine,
        name=table,
        if_exists=if_exists,
        index=False,
        chunksize=None,
    )


@profiler(type='logging')
def _insert_mysql_logger(
    data_frame,
    db=None,
    table=None,
    h=None,
    port=3306,
    u=None,
    p=None,
    if_exists='append',
        ):

    print('Using MariaDB')

    # DB Connection
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'
    engine = sa.create_engine(conn_str.format(u, p, h, str(port), db))

    # Get a DataFrame
    data_frame.to_sql(
        con=engine,
        name=table,
        if_exists=if_exists,
        index=False,
        chunksize=None,
    )


def insert_mysql(
    data_frame,
    db=None,
    table=None,
    h=None,
    port=3306,
    u=None,
    p=None,
    if_exists='append',
    logging=True,
        ):

    if logging:
        return _insert_mysql_logger(
            data_frame,
            db=db,
            table=table,
            h=h,
            port=port,
            u=u,
            p=p,
            if_exists=if_exists,
        )
    else:
        return _insert_mysql_printer(
            data_frame,
            db=db,
            table=table,
            h=h,
            port=port,
            u=u,
            p=p,
            if_exists=if_exists,
        )


insert_mariadb = insert_mysql
