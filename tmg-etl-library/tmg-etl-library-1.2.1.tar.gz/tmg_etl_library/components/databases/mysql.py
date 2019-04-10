from tmg_etl_library.components.databases.database import Database
from jinja2 import Template
from copy import deepcopy
import sqlalchemy
import re
import sqlalchemy.schema as sch
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import ArgumentError, SQLAlchemyError
import mysql.connector as sql

from mysql.connector import errorcode, FieldType
from mysql.connector.errors import InterfaceError
from jsonschema import validate, ValidationError

Base = declarative_base()

DATAREMAP_TO_SQL = {'integer': 'INTEGER',
                    'string': 'TEXT',
                    'date': 'DATE',
                    'time': 'TIME',
                    'decimal': 'DECIMAL',
                    'datetime': 'DATETIME'}

DATAREMAP_FROM_SQL = {'INTEGER': 'integer',
                      'BIGINT': 'big_int',
                      'DOUBLE': 'double',
                      'DECIMAL': 'decimal',
                      'TEXT': 'string',
                      'VARCHAR': 'string',
                      'DATE': 'date',
                      'TIME': 'time',
                      'DATETIME': 'datetime'}


class MySQLClient(Database):
    def __init__(self, log, hostname, username, password, dataset):
        super().__init__(log)
        self.hostname = hostname
        self.username = username
        self.password = password
        self.dataset = dataset

        self.connection = self._connect_sqlalchemy()
        self._set_metadata_sqlalchemy()
        self.cnx = self._connect_mysql_connector()
        #TODO: Should we create metadata on class initalisation?

    def _connect_sqlalchemy(self):
        """
        Establishes a connection to MySQL using sqlalchemy
        :return: sqlalchemy Connection object outlining the connection to MySQL
        """
        try:
            connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(self.username,
                                                                                                  self.password,
                                                                                                  self.hostname,
                                                                                                  self.dataset
                                                                                                  )
                                                  )
            connected = connection.connect()
            return connected

        except InterfaceError as e:
            self.logger.error('Connection failed. Check credentials.')
            raise e

    def _connect_mysql_connector(self):
        """
        Establishes a connection to MySQL using mysql-connector
        :return: mysql-connectior Connection object outlining the connection to MySQL
        """
        try:
            cnx = sql.connect(host=self.hostname, user=self.username, password=self.password, database=self.dataset)
            return cnx
        except sql.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def _set_metadata_sqlalchemy(self):
        """
        Creates a Metadata object containing the metadata information on the MySQL database
        :return: Metadata object
        """
        meta = sch.MetaData()
        meta.reflect(self.connection)

        self.metadata = meta

    def _get_sqlachemy_table(self, table):
        """
        Creates a MySQLTable object which represents the object on MySQL database
        :param table: MySQL table object (discuss if could be string)
        :return: SQLAlchemy representation of the table
        """
        #TODO: Discuss what should be passed to function/the utility of this function
        metadata = self.metadata
        sql_table = metadata.tables[table.name]
        return sql_table

    def list_tables(self, table_regex=''):
        """
        List the tables in tbe dataset which match the regex if provided
        :param table_regex: regex string to filter table names with
        :return: list of MySQLTable objects for the table names which matcht the regex filter
        """
        metadata = self.metadata

        if table_regex:
            table_names = [self._Alchemy_2_MySQLTable(table) for table in metadata.tables.values() if re.match(table_regex, table.name)]
        else:
            table_names = [self._Alchemy_2_MySQLTable(table) for table in metadata.tables.values()]

        return table_names

    def _Alchemy_2_MySQLTable(self, sqlalchemy_table):
        """
        Finds the SQLAlchemy table for the provided name and converts the table to a MySQLTable object
        :param sqlalchemy_table: SQLAlchemy table to convert
        :return: MySQLTable object
        """

        table = MySQLTable(log=self.logger,
                           database_name='test',
                           dataset=self.dataset,
                           name=sqlalchemy_table.name
                           )

        table.schema = self._convert_sqlalchemy_schema(sqlalchemy_table)

        return table

    def _convert_sqlalchemy_schema(self, sqlalchemy_table):
        """
        Changes the SQLAlchemy table schema into the json format used in the MySQLTable object
        :param sqlalchemy_table: SQLAlchemy Table object
        :return: json style schema used by MySQLTable object
        """

        schema = []

        for column in sqlalchemy_table.columns:
            col_info = {
                'name': column.name,
                'type': DATAREMAP_FROM_SQL[column.type.__visit_name__],
                'mode': 'Nullable'
            }
            schema.append(col_info)

        return schema

    def reflect_table_mysql_connector(self, table_name):
        """
        Creates a MySQLTable object to represent a table on MySQL server using mysql_connector
        :param table_name: Name of the table on the MySQL server to be reflected
        :return: MySQL object of the table
        """
        cnx = self.cnx
        cur = cnx.cursor()

        cur.execute(f'select * from {table_name}')
        table_desc = cur.description

        table = MySQLTable(log=self.logger,
                           database_name='blah',
                           dataset=self.dataset,
                           name=table_name
                           )

        schema = []

        for col in table_desc:

            col_info = {
                'name': col[0],
                'type': FieldType.desc[col[1]],
                'mode': 'Null'
            }
            schema.append(col_info)

        table.schema = schema

        return table

    def create_table_sqlalchemy(self, table):
        """
        Creates a table from the MySQLTable object. Uses SQLAlchemy as base.
        May be unusable. Keeping in case it comes in useful in the future
        :param table: MySQLTable object which represents the table to create
        """
        engine = self.connection
        if table.schema:
            Table = table._createAlchemyTable()

            Table.create(engine)
            self._set_metadata_sqlalchemy()
        else:
            self.logger.error('Table must have a schema to be created')
            raise ArgumentError('Need schema to create table')

    def run_query(self, query, destination=None, force_creation=True):
        """
        Passes a query to MySQL and gathers the results
        :param query: the query as a string to be passed to MySQL
        :param destination: Optional MySQLTable to lead the results into
        :param force_creation: Optional parameter whether a missing destination table should be created if doesn't exist
        :return: data received from query and columns of the data received
        """
        results = self.connection.execute(query)
        columns = results._metadata.keys
        data = [[str(data_point) for data_point in row] for row in results]

        if destination:
            table_exist = destination.table_exists(self)
            if not table_exist:
                if force_creation:
                    self.logger.info('Creating table {}'.format(destination.name))
                    destination.create_table(self)
                else:
                    self.logger.error('Destination table does not exist')
                    raise Exception('Table')
            destination.insert_data(self, data)

        return data, columns

    def query_to_file(self, query, file, config):
        """
        Runs the provided query and loads the returned results into a file
        :param query: string version of the query to be passed to MySQL
        :param file: CSVFile object linked to the file the results a loaded into
        :param config: MySQL_to_CSV_config object outlining the configurations for the pull, uses default if not provided
        """

        data, columns = self.run_query(query)
        file.write_to_file(columns, data, config)

    def update_schema(self, table):
        """
        Updates a table on MySQL server to represent the schema in the table object provided
        :param table: MySQLTable with an updated schema to be updated on MySQL
        """
        connection = self.connection
        if table.table_exists(connection):
            current_table = self._get_sqlachemy_table(table)
            current_columns = [column['name'] for column in current_table.schema]
            new_columns = [column for column in table.schema if column['name'] not in current_columns]

            for column in new_columns:
                column['type'] = DATAREMAP_TO_SQL[column['type']]

            alter = Template('''
                ALTER TABLE {{table_name}} 
                ADD COLUMN
                {% for col in new_columns %}
                    {{col.name}} {{col.type}}
                {% endfor %}
            ''')
            query = alter.render(table_name=table.name, new_columns=new_columns)
            connection.execute(query)
        else:
            self.logger.info('Table does not exist, creating instead')
            table.create_table(connection)
        self._set_metadata_sqlalchemy()


class MySQLTable:

    def __init__(self, client, log, database_name, dataset, name, schema=[]):
        """
        Class that contains all the information needed to represent a BQ table

        :param database_name: MySQL database name
        :param dataset: MySQL dataset name
        :param name: MySQL table name
        """
        self.logger = log
        self.database_name = database_name # Is this necessary? MySQL doesn't really have database names
        self.dataset = dataset
        self.name = name
        self._schema = schema
        if isinstance(client, MySQLClient):
            self._client = client
        else:
            raise TypeError('Client should be of MySQLClient type')

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        raise RuntimeError('The client should not updated after creation of the MySQLClient')

    @property
    def schema(self):
        """
        getter for schema attribute
        :return: schema of table
        """
        return self._schema

    @schema.setter
    def schema(self, value):
        """
        setter for schema. Validates the schema is in correct format and triggers recreation of SQLAlchemy Table representation
        :param value: json style representation of schema
        """
        if value:
            valid_schema = {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string"}
                    },
                    'required': ["name", "type"],
                    "additionalProperties": True,
                    'max_items': 3
                }
            }

            try:
                validate(value, valid_schema)
                self._schema = value
            except ValidationError as e:
                raise('Schema given is not in the correct format. Please check documentation.')
        else:
            self._schema = None

    def _createAlchemyTable(self):
        """
        Creates and sets the SQLAlchemy Table which reflects the MySQL object.
        Not currently used. Kept for potential future uses
        """
        if not self._schema:
            return None

        attr_dict = {}
        datatype_mapping = {'string': Text, 'integer': Integer}

        attr_dict['__tablename__'] = self.name
        attr_dict['__table_args__'] = {'extend_existing': True}
        for row in self._schema:
            primary_key = True if row.get('primary_key') else False
            attr_dict[row['name']] = Column(datatype_mapping.get(row['type'].lower()), primary_key=primary_key)

        table = type(self.name, (Base,), attr_dict).__table__
        return table

    def __repr__(self):
        return '%s . %s' % (self.dataset, self.name)

    def __str__(self):
        return '%s . %s' % (self.dataset, self.name)

    # def full_table_to_file(self, client, file, config=None):
    #     """
    #     Pulls the entire contents of a table and loads into a delimitered file
    #     :param table: MySQLTable object linked to the table to be downloaded
    #     :param file: CSVFile object linked to the file the data is to be written into
    #     :param config: MySQL_to_CSV_config object outlining the configurations for the pull, uses default if not provided
    #     """
    #     if not config:
    #         config = MySQLToCSVConfig()
    #
    #     if self.table_exists(client):
    #         sql_table = client.get_sqlachemy_table(self)
    #     else:
    #         self.logger.error('The table {} does not exist in this dataset'.format(self.name))
    #         raise Exception("Table doesn't exist")
    #
    #     if not self.schema:
    #         self.schema = client._convert_sqlalchemy_schema(sql_table)
    #
    #     results = client.connection.execute(sql_table.select())
    #     columns = [column['name'] for column in self.schema]
    #     data = [[str(data_point) for data_point in row] for row in results]
    #
    #     file.write_to_file(columns, data, config)

    def insert_data(self, data):
        """
        Pushes data into a table on MySQL database
        :param table: MySQLTable object linked to the table the data is inserted into
        :param data: list of delimited data to be inserted. Each value in list represents a row in the table
        :param delimiter: the delimiter which seperates the fields in the data rows
        """
        if self.schema:
            columns = [column['name'] for column in self.schema]
        else:
            self.logger.error('Table needs a schema to insert into')
            raise Exception('TableSchemaMissing')
        row_num = 1
        if self.table_exists(self.client):
            mysql_table = self.client._get_sqlachemy_table(self)
        else:
            self.logger.error('Table does not exist')
            raise Exception("TableDoesNotExist")

        insert_rows = []

        for row in data:
            row_num += 1
            if len(columns) != len(row):
                self.logger.error('Data missing for row {0}'.format(row_num))
                continue
            data_dict = {k: v for k, v in zip(columns, row)}
            insert_rows.append(data_dict)

        self.client.connection.execute(mysql_table.insert(), insert_rows)
        self.client._set_metadata_sqlalchemy()

    # def insert_csv(self, connection, file, config=None):
    #     """
    #     Inserts data from a csv into table on MySQL database
    #     :param file: CSVFile object linked to the file to be inserted
    #     :param table: MySQLTable object linked to the table the data is to be inserted into
    #     :param config: CSV_to_MySQL_config object outlining configurations for the load. If one is not provided the default object is used.
    #     """
    #     if not config:
    #         config = CSVToMySQLConfig()
    #     lead_row = True if config.skip_leading_rows else False
    #     data = []
    #     with open(file.full_path, 'rt') as f:
    #         for line in f:
    #             if lead_row:
    #                 lead_row = False
    #                 continue
    #             data.append(line.split(file.delimiter))
    #
    #     self.insert_data(connection, data, force_creation=config.force_creation)
    #     connection.set_metadata_sqlalchemy()

    def create_table(self):
        """
        Creates a table from the MySQLTable object. Uses mysql-connector as base.
        :param table: MySQLTable object as basis of table
        """
        if not self.schema:
            self.logger.error('A schema is required to create a table')
            raise ArgumentError('Schema needed')
        if self.table_exists():
            self.logger.error('This table already exists')
            raise SQLAlchemyError('Table exists')

        connection = self.client.connection.connection
        cur = connection.cursor()

        columns = deepcopy(self.schema)

        for col in columns:
            col['type'] = DATAREMAP_TO_SQL[col['type']]

        query = Template('''
        CREATE TABLE {{table_name}}
        (
        {% for col in columns %}
            {{col.name}} {{col.type}} {% if col.mode == 'Nullable' %} NULL {% endif %} {{col.primary_key}}
            {% if not loop.last %},{% endif %}
        {% endfor %}
        )
        ''')

        create = query.render(table_name=self.name, columns=columns)

        cur.execute(create)
        connection.commit()

        self.client._set_metadata_sqlalchemy()

    def table_exists(self):
        """
        Checks the Metadate object which reflects the metadata of the MySQL database for the existance of the table
        :param table: MySQLTable object representing the table to be checked
        :return: bool whether table exists or not
        """

        connection = self.client.connection
        if self.client.dataset != self.dataset:
            self.logger.error("Table's dataset does not match the active dataset in MySQL")
            self.logger.error("Table's dataset: {}".format(self.dataset))
            self.logger.error("Connection's dataset: {}".format(connection.dataset))
            raise ConnectionError('Dataset matching error')
        else:
            tables = self.client.list_tables('^' + self.name + '$')
            return True if tables else False

    def delete_table(self):
        """
        Drops provided tables from MySQL database
        :param tables: List of MySQLTable object to be dropped
        """


        if self.table_exists():
            mysql_table = self.client._get_sqlachemy_table(self)
            mysql_table.drop(self.client.connection)
        else:
            self.logger.error('Table {} does not exist'.format(self.name))
            raise Exception('TableDoesNotExists')
        self.client._set_metadata_sqlalchemy()



