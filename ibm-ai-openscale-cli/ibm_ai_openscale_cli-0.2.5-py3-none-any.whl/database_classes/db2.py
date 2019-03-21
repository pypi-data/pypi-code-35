# coding=utf-8
import os
import site
import logging
from sys import platform

logger = logging.getLogger(__name__)

def _get_clidriver_location():
    clidriver_location = None
    for location in site.getsitepackages():
        if os.path.exists(location + '/clidriver/lib'):
            clidriver_location = location + '/clidriver/lib'
            break
    return clidriver_location

try:
    import ibm_db
except Exception as e:
    if platform == "darwin" and ('Library not loaded' in str(e) or 'SQL1042C' in str(e)):
        logger.error('ERROR: Unable to import module "ibm_db"')
        logger.error('Environment variable "DYLD_LIBRARY_PATH" needs to set to use the ibm_db driver. This can be set using:')
        clidriver_location = _get_clidriver_location()
        if clidriver_location is not None:
            logger.info('"export DYLD_LIBRARY_PATH={}:{}/icc"'.format(clidriver_location, clidriver_location))
        else:
            clidriver_location = '</path/to>/clidriver/lib'
            logger.info('"export DYLD_LIBRARY_PATH={}:{}/icc"'.format(clidriver_location, clidriver_location))
        logger.info('Please retry with the above setting.')
        exit(1) # retry will not help
    else:
        raise e

DROP_SCHEMA = u'DROP SCHEMA {} RESTRICT'
CREATE_SCHEMA = u'CREATE SCHEMA {}'
DROP_TABLE = u'DROP {} {}."{}"'
DELETE_TABLE_ROWS = u'DELETE FROM {}."{}"'
PROC_NAME = u'AIOSFASTPATHPROC.DELETESCHEMA{}'
CALL_PROC = u'CALL {}'
DROP_SCHEMA_PROC = u'''CREATE OR REPLACE PROCEDURE {} BEGIN
    DECLARE varErrSchema varchar(128) default '{}ERRORSCHEMA';
    DECLARE varErrTable varchar(128) default '{}ERRORTAB';
    CALL SYSPROC.ADMIN_DROP_SCHEMA('{}', NULL, varErrSchema, varErrTable);
END'''

def validate_db2_credentials(credentials):
    if 'db2' in credentials: # PrimaryStorageCredentialsShort format
        hostname = credentials['db2'].split(':')[2].split('@')[1]
        port = credentials['db2'].split(':')[3].split('/')[0]
        db = credentials['db2'].split(':')[3].split('/')[1]
        username = credentials['db2'].split(':')[1].split('//')[1]
        password = credentials['db2'].split(':')[2].split('@')[0]
        uri = 'db2://{}:{}@{}:{}/{}'.format(username, password, hostname, port, db)
        dsn = 'DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;UID={};PWD={};'.format(db, hostname, port, username, password)
        credentials = {
            "db_type": "db2",
            "hostname": hostname,
            "port": port,
            "db": db,
            "username": username,
            "password": password,
            "uri": uri,
            "dsn": dsn
        }
    elif 'username' not in credentials or 'password' not in credentials or 'hostname' not in credentials or 'db' not in credentials:
        logger.error('Invalid DB2 credentials supplied: values for username, password, hostname, and db are all required')
        exit(1)
    else: # PrimaryStorageCredentialsLong format or DB2 Warehouse on Cloud format
        if 'port' not in credentials:
            credentials['port'] = 50000
        credentials['uri'] = 'db2://{}:{}@{}:{}/{}'.format(credentials['username'], credentials['password'], credentials['hostname'], credentials['port'], credentials['db'])
        if 'dsn' not in credentials:
            credentials['dsn'] = 'DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;UID={};PWD={};'.format(credentials['db'], credentials['hostname'], credentials['port'], credentials['username'], credentials['password'])
    return credentials

class DB2():

    def __init__(self, credentials):
        if 'ssldsn' in credentials:
            conn_string = credentials['ssldsn']
        elif 'dsn' in credentials:
            conn_string = credentials['dsn']
        logger.debug('Connecting to DB2 ...')
        self._connection = ibm_db.connect(conn_string, '', '')

    def _execute(self, statement_str):
        ibm_db.exec_immediate(self._connection, statement_str)

    def _fetch_results(self, command):
        results = []
        result = ibm_db.fetch_assoc(command)
        while result:
            results.append(result)
            result = ibm_db.fetch_assoc(command)
        return results

    def _get_tables_in_schema(self, schema_name):
        schema_name = schema_name.upper()
        results = self._fetch_results(ibm_db.tables(self._connection, None, schema_name))
        return results

    def _drop_tables_in_schema(self, schema_name):
        schema_name = schema_name.upper()
        tables = self._get_tables_in_schema(schema_name)
        for table in tables:
            self._execute(DROP_TABLE.format(table['TABLE_TYPE'], table['TABLE_SCHEM'], table['TABLE_NAME']))

    def _restrict_drop_existing_schema(self, schema_name):
        schema_name = schema_name.upper()
        self._execute(DROP_SCHEMA.format(schema_name))

    def _admin_drop_existing_schema(self, schema_name):
        schema_name = schema_name.upper()
        # drop existing error table
        error_schema_name = '{}ERRORSCHEMA'.format(schema_name)
        self._drop_tables_in_schema(error_schema_name)
        # drop schema
        proc_name = PROC_NAME.format(schema_name)
        self._execute(DROP_SCHEMA_PROC.format(proc_name, schema_name, schema_name, schema_name))
        self._execute(CALL_PROC.format(proc_name))

    def drop_existing_schema(self, schema_name, keep_schema):
        schema_name = schema_name.upper()
        logger.debug('Dropping tables from schema {}'.format(schema_name))
        self._drop_tables_in_schema(schema_name)
        if keep_schema:
            return
        logger.debug('Dropping schema {}'.format(schema_name))
        self._admin_drop_existing_schema(schema_name)

    def create_new_schema(self, schema_name, keep_schema):
        if keep_schema:
            return
        schema_name = schema_name.upper()
        logger.debug('Creating schema {}'.format(schema_name))
        self._execute(CREATE_SCHEMA.format(schema_name))

    def reset_metrics_tables(self, schema_name):
        schema_name = schema_name.upper()
        tables = self._get_tables_in_schema(schema_name)
        for table in tables:
            if table['TABLE_NAME'] == 'MeasurementFacts' or table['TABLE_NAME'] == 'Explanations' or table['TABLE_NAME'].startswith('Payload_') or table['TABLE_NAME'].startswith('Feedback_') or table['TABLE_NAME'].startswith('Manual_Labeling_'):
                self._execute(DELETE_TABLE_ROWS.format(table['TABLE_SCHEM'], table['TABLE_NAME']))

    def drop_metrics_tables(self, schema_name):
        schema_name = schema_name.upper()
        tables = self._get_tables_in_schema(schema_name)
        for table in tables:
            if table['TABLE_NAME'].startswith('Payload_') or table['TABLE_NAME'].startswith('Feedback_') or table['TABLE_NAME'].startswith('Manual_Labeling_'):
                self._execute(DROP_TABLE.format(table['TABLE_TYPE'], table['TABLE_SCHEM'], table['TABLE_NAME']))

    def __exit__(self):
        try:
            if self._connection:
                if ibm_db.close(self._connection):
                    logger.debug('Successfully closed the DB2 connection')
                else:
                    logger.debug('Unable to close the DB2 connection')
        except Exception as e:
            logger.debug('Unable to close the DB2 connection: {}'.format(str(e)))
