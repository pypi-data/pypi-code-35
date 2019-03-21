# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: db_operators.py
@date: 3/12/2019
@desc:
'''
from configparser import ConfigParser

import psycopg2

from srfnef.utils import main_path


def config(filename = main_path + 'db/db.ini', section = 'postgresql'):
    # create a parser
    parser = ConfigParser()

    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def test_connection():
    """ Connect to the PostgreSQL db server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL db...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL db version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL db server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def create_api_table():
    command = """
        CREATE TABLE api (
            vendor_id SERIAL PRIMARY KEY,
            creation_time TIMESTAMP DEFAULT (now()),
            name VARCHAR (32),
            creator VARCHAR (32),
            creation VARCHAR (255),
            tags VARCHAR (32)[],
            status VARCHAR (32),
            family VARCHAR (32),
            diskSizeBytes INT ,
            sourceDisk VARCHAR (255),
            fingerprint VARCHAR (255),
            dependencies varchar []            
        )
    """

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(command)
        # close communication with the PostgreSQL db server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
