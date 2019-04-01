import pandas as pd
import numpy as np
import glob
import psycopg2
import MySQLdb
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

########################################################
# Database helpers
########################################################
def get_database_credentials(db='redshift', machine='prod_analytics'):
    if db == 'redshift':
        if machine == 'prod_analytics':
            host='prod-lms.czpazaogwafy.us-east-1.redshift.amazonaws.com'
            port='5439'
        elif machine == 'local':
            host = '127.0.0.1'
            port='36060'
        dbname="lms_transactions"
        user="lms"
    elif db == 'mysql':
        if machine == 'local':
            host = '127.0.0.1'
            port= 31060
        dbname="lms"
        user="lms_dbuser"
    return host, port, dbname, user

def execute_query_in_redshift(query, select_statement=True, password_filepath='data/redshift_password.txt', machine='local'):
    # get password
    with open(password_filepath, "r") as myfile:
        password=myfile.read().rstrip('\n')
    host, port, dbname, user = database_credentials(db = 'redshift', machine = machine)

    # Connect to an existing database
    conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user,                             password=password)
    cur = conn.cursor()
    query = """{}""".format(query)

    # Query the database and obtain data as Python objects
    cur.execute(query)

    if select_statement:
        colnames = [desc[0] for desc in cur.description]
        data = cur.fetchall()
        df = pd.DataFrame(data, columns=colnames)
    else:
        conn.commit()
        df = None
    # Close communication with the database
    cur.close()
    conn.close()

    return df

def execute_query_in_mysql(query, select_statement=True, password_filepath='data/mysql_password.txt', machine='local'):
    # get password
    with open(password_filepath, "r") as myfile:
        password=myfile.read().rstrip('\n')
    host, port, dbname, user = database_credentials(db = 'mysql', machine = machine)

    # db=MySQLdb.connect(passwd="wE7raYut",host = '127.0.0.1', user='lms_dbuser', db='lms',port=31060)
    conn=MySQLdb.connect(passwd=password,host = host, user=user, db=dbname,port=port)
    cur=conn.cursor()

    # Query the database and obtain data as Python objects
    query = """{}""".format(query)
    cur.execute(query)

    if select_statement:
        colnames = [desc[0] for desc in cur.description]
        data = cur.fetchall()
        df = pd.DataFrame(list(data), columns=colnames)
    else:
        conn.commit()
        df = None
    # Close communication with the database
    cur.close()
    conn.close()

    return df
