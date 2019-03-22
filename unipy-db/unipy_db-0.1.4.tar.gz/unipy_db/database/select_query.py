# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 20:55:26 2017

@author: Young Ju Kim
"""


import pandas as pd
import pymysql
import psycopg2 as pg
import sqlalchemy as sa
# import ibm_db
import ibm_db_sa
# import cx_Oracle as co

from unipy.utils.decorator import profiler


__all__ = [
    'from_postgresql',
    'from_PostgreSQL',
    'from_mysql',
    'from_mariadb',
    'from_MariaDB',
    'from_mariadb_async',
    'from_MariaDB_async',
    'from_db2',
    'from_DB2',
]


@profiler(type='printing')
def from_postgresql(query, h=None, port=5432, db=None, u=None, p=None):

    print('Using PostgreSQL')

    # DB Connection
    conn = pg.connect(host=h, port=str(port), user=u, password=p)

    # Get a DataFrame
    query_result = pd.read_sql(query, conn)

    # Cloase Connection
    conn.close()

    return query_result


from_PostgreSQL = from_postgresql


@profiler(type='printing')
def from_db2(query, h=None, port=50000, db=None, u=None, p=None):

    print('Using IBM DB2')

    # DB Connection
    connStr = 'ibm_db_sa://{}:{}@{}:{}/{}'
    engine = sa.create_engine(connStr.format(u, p, h, str(port), db))
    conn = engine.connect()

    # Get a DataFrame
    execonn = engine.execute(query)

    query_result = pd.DataFrame(execonn.fetchall())
    query_result.columns = execonn.keys()

    # Close Connection
    conn.close()

    return query_result


from_DB2 = from_db2


@profiler(type='printing')
def from_mysql(query, h=None, port=3306, db=None, u=None, p=None):

    print('Using MariaDB')

    # DB Connection
    conn = pymysql.connect(host=h, port=port, user=u, password=p, database=db)

    # Get a DataFrame
    query_result = pd.read_sql(query, conn)

    # Close Connection
    conn.close()

    return query_result


from_mariadb = from_MariaDB = from_mysql


@profiler(type='printing')
async def from_mysql_async(query, h=None, port=3306, db=None, u=None, p=None):

    print('Using MariaDB')

    # DB Connection
    conn = pymysql.connect(host=h, port=port, user=u, password=p, database=db)

    # Get a DataFrame
    await  pd.read_sql(query, conn)

    # Close Connection
    conn.close()


from_mariadb_async = from_MariaDB_async = from_mysql_async
