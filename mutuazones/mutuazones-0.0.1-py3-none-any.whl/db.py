import os
import pandas as pd
import pandas_profiling
import logging

from sqlalchemy import create_engine
from base64 import b64decode

# importante para el tema de acentos y codificación
os.environ['NLS_LANG'] = 'SPANISH_SPAIN.WE8ISO8859P15'


class Zone(object):

    def __init__(self, schemaName):
        self.__con = None
        self.__schema = schemaName
        self.__logger = logging.getLogger(__name__)

    def __connect(self):
        if self.__con is not None:
            return
        user = os.getenv('DB_USER')
        if user is None or user == '':
            #raise ImportError('The DB_USER has not been defined as an environment variable')
            user = self.__schema
        password = os.getenv('DB_PASS')
        if password is None or password == '':
            raise ImportError('The DB_PASS has not been defined as an environment variable')
            #password = 'Sistemas2019'
        password = b64decode(password).decode('utf-8')
        self.__logger.debug(f'Utilizando password {password}')
        url = os.getenv('DB_URL')
        if url is None or url == '':
            url = '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=mtcldb-scan.mutuatfe.local)(PORT=1521))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=DESA)))'

        self.__logger.debug(f'En el esquema "{self.__schema}" realizando conexión a "{url}" utilizando el usuario "{user}"')

        if "DESCRIPTION" in url:  # conexión vía SERVICE
            self.__engine = create_engine('oracle+cx_oracle://{0}:{1}@{2}'.format(user, password, url))
        else:  # conexíon vía SID
            self.__engine = create_engine('oracle://{0}:{1}@{2}'.format(user, password, url))

        self.__logger.debug(f'Conectando a la URL {self.__engine}')
        self.__con = self.__engine.connect()

    @property
    def df_names(self):
        self.__connect()
        return self.__engine.table_names(self.__schema, self.__con)
        
    def load_df(self, name):
        self.__connect()
        return pd.read_sql_table(name, self.__con, schema=self.__schema)

    
    def load_df_sql(self, query):
        self.__connect()
        return pd.read_sql(query, self.__con)
    
    def save_df(self, df, name, if_exists='replace'):
        self.__connect()
        df.to_sql(name, self.__con, schema=self.__schema, if_exists=if_exists)
        
    def generate_profile(self, df):
        self.__connect()
        return pandas_profiling.ProfileReport(df)
    
    def save_profile_to_file(self, pathFile, df=None, profile=None):
        self.__connect()
        if df is None and profile is None:
            raise ValueError('One parameter is missing, df or profile parameter is required')
        if df is not None:
            profile = pandas_profiling.ProfileReport(df)
        profile.to_file(outputfile=pathFile)