import datetime as dt
import re
import time
from collections import namedtuple

from google.api_core.exceptions import NotFound
from google.cloud import bigquery
from google.cloud.bigquery import TimePartitioning, TimePartitioningType, QueryJob
from jsonschema import validate, ValidationError

from tmg_etl_library.components.databases.database import Database

JSON_SCHEMA_STRUCTURE = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "mode": {"type": "string"},
            "type": {"type": "string"}
        },
        'required': ["name", "type"]
    }
}
PARTITION_DATE_FORMAT = '%Y%m%d'

QueryResult = namedtuple('QueryResult', 'data header')


class _DriveEnabledGoogleClient(bigquery.Client):
    """
    This client adds the Google Drive scope to bigquery.Client
    """
    SCOPE = (
        'https://www.googleapis.com/auth/bigquery',
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/drive'
    )


class BQClient(Database):
    def __init__(self, log, project, with_drive_scope=False):

        super().__init__(log)
        self.project = project
        if with_drive_scope:
            self.google_client = _DriveEnabledGoogleClient(project=project)
        else:
            self.google_client = bigquery.Client(project=project)

    def list_tables(self, dataset, table_regex=''):
        """
        return list of table names in dataset given a regular expression
        :param dataset:
        :param table_regex:
        :return:
        """

        project = self.project
        google_bq_dataset = self.fetch_dataset(project, dataset)
        google_bq_table_items = self.google_client.list_tables(google_bq_dataset)

        list_of_table_names = [table.table_id for table in google_bq_table_items]

        if table_regex:
            list_of_table_names = [table_name for table_name in list_of_table_names if re.match(table_regex, table_name)]

        return [
            BQTable(client=self, project=project, dataset=dataset, name=table)
            for table in list_of_table_names
        ]

    def run_query(self, query=None, query_file_name=None, destination=None,
                  write_disposition=None, use_legacy_sql=False, async_query=False, query_params=None,
                  discard_result=False):
        """

        :param query: String Query to be Performed
        :param str query_file_name: file name which contains the query
        :param BQTable destination: BQTable, where write the result
        :param str write_disposition: If the table exists, WRITE_TRUNCATE or WRITE_APPEND, Default: WRITE_EMPTY
        :param boolean use_legacy_sql: Defaults to False - uses Standard SQL
        :param boolean async_query: True if you want to run the query async
        :param dict query_params: dictionary of optional query params
        :param boolean discard_result: if True, no result is returned so no data manipulation in place.

        :return: tuple data, header
        """
        if not (query or query_file_name):
            raise Exception("query or query_file_name should be provided.")

        if query_file_name:
            with open(query_file_name, mode="r") as query_file:
                query = query_file.read()

        query_params = query_params if query_params else {}
        query = query.format(**query_params)

        job_config = bigquery.QueryJobConfig()
        job_config.use_legacy_sql = use_legacy_sql

        if destination:
            self.logger.info('Query Destination: %s' % str(destination))
            if destination.partitioned_field:
                job_config.time_partitioning = TimePartitioning(type_=TimePartitioningType.DAY, field=destination.partitioned_field)
            google_bq_table = self.fetch_table_reference(destination)
            job_config.destination = google_bq_table

        if write_disposition:
            job_config.write_disposition = write_disposition

        self.logger.info('Running Query')
        query_job = self.google_client.query(query, job_config=job_config)  # API request - starts the query asynchronously

        if async_query:
            return query_job

        while True:
            query_job.reload()  # Refreshes the state via a GET request.
            if query_job.state == 'DONE':
                if query_job.error_result:
                    raise RuntimeError(query_job.errors)
                break
            time.sleep(1)

        if discard_result:
            return None

        iterator = query_job.result()

        headers = [col.name for col in iterator.schema]

        data = []
        for row in iterator:
            result_row = []
            for point in row:
                result_row.append(point)
            data.append(result_row)

        return QueryResult(data, headers)

    def wait_for_queries(self, query_jobs):
        """
        :param query_jobs: List of QueryJob type

        :return:
        """
        if not isinstance(query_jobs, list):
            raise TypeError('queries must be of type list')
        else:
            for query_job in query_jobs:
                if not isinstance(query_job, QueryJob):
                    raise TypeError('Values in list must be of type QueryJob')

        for query_job in query_jobs:
            while True:
                query_job.reload()  # Refreshes the state via a GET request.
                if query_job.state == 'DONE':
                    if query_job.error_result:
                        raise RuntimeError(query_job.errors)
                    self.logger.info('Query Job with id "%s" has completed' % query_job.job_id)
                    break
                time.sleep(1)

        return True

    def fetch_table_reference(self, table):
        """
        Retrieves table reference
        :param table: BQTable object
        :return:
        """

        dataset = self.fetch_dataset(table.project, table.dataset)
        if not dataset:
            return None
        return dataset.table(table_id=table.name)

    def fetch_dataset(self, project, dataset_id, location='EU', force_dataset_creation=False):
        """
        Create or get the dataset in GC
        :param project: project name
        :param dataset_id: dataset name
        :param location: dataset location name: EU or US
        :param force_dataset_creation: If True creates a dataset if doesn't exists
        :return: dataset
        """

        dataset_ref = self.google_client.dataset(dataset_id, project)
        try:
            dataset = self.google_client.get_dataset(dataset_ref=dataset_ref)
            self.logger.info('Dataset {0} is reached.'.format(dataset_id))
            return dataset
        except NotFound:
            if force_dataset_creation:
                dataset = bigquery.Dataset(dataset_ref=dataset_ref)
                dataset.location = location
                self.google_client.create_dataset(dataset)
                self.logger.info('Dataset {0} is created.'.format(dataset_id))
                return dataset
            else:
                return None


class BQTable:
    def __init__(self, client, project, dataset, name):
        """
        Class that contains all the information needed to represent a BQ table

        :param BQClient client:
        :param str project: BQ project name
        :param str dataset: BQ dataset name
        :param str name: BQ table name

        """
        self.project = project
        self.dataset = dataset
        self.name = name
        self._schema = None
        self._expiry = None
        self._partitioned_field = None
        if isinstance(client, BQClient):
            self._client = client
        else:
            raise TypeError('Client should be of BQClient type')

    @property
    def full_table_name(self):

        return f"{self.project}.{self.dataset}.{self.name}"

    @property
    def client(self):
        return self._client

    def __repr__(self):
        return '%s.%s.%s' % (self.project, self.dataset, self.name)

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, value):
        try:
            validate(value, JSON_SCHEMA_STRUCTURE)
            self._schema = value
        except ValidationError as e:
            raise ValidationError('Schema given is not in the correct format. Please check documentation.')

    @property
    def expiry(self):
        return self._expiry

    @expiry.setter
    def expiry(self, value):
        """
        :param value: Time in Minutes for when the table should expire (delete itself)
        :return: Nothing
        """
        if not isinstance(value, int):
            raise TypeError('expiry must be an Integer')

        self._expiry = value

    @property
    def partitioned_field(self):
        return self._partitioned_field

    @partitioned_field.setter
    def partitioned_field(self, value):
        """
        :param value: Field (String) to set as the field to partition the table on
        :return: Nothing
        """
        if not isinstance(value, str):
            raise TypeError('Partitioned Field must be a String')

        self._partitioned_field = value

    def exists(self):
        """
        Checks to see if a big query table exists
        :return: True/False
        """

        google_table_ref = self.client.fetch_table_reference(self)

        try:
            self.client.google_client.get_table(google_table_ref)
            return True
        except NotFound:
            return False

    def delete(self):
        """
        :param client: Client object to interact with BQ
        :return: Nothing
        """

        google_bq_table = self.client.fetch_table_reference(self)
        self.client.logger.info('Deleting Table: %s' % str(self))
        self.client.google_client.delete_table(google_bq_table)

    def create(self, force_dataset_creation=True, force_table_creation=True):
        """
        Creates a new empty table in BQ.
        :param boolean force_dataset_creation: force creation of dataset
        :param boolean force_table_creation: forc table creation
        :return:
        """

        if not self.schema:
            raise Exception('No schema is defined.')

        dataset = self.client.fetch_dataset(self.project, self.dataset, force_dataset_creation=force_dataset_creation)
        if not dataset:
            raise Exception('Dataset {0} not found'.format(self.dataset))

        table_ref = dataset.table(self.name)

        try:
            self.client.google_client.get_table(table_ref)
            self.client.logger.info('Table {0} already exists.'.format(self.name))
            return self
        except NotFound:
            if not force_table_creation:
                raise Exception('Table {0} does not exist and force_table_creation is not set to True.'.format(self.name))
            self.client.logger.info('Table {0} does not exists.'.format(self.name))

        gbq_table = bigquery.Table(table_ref, schema=self.bigquery_schema)

        if self.expiry:
            expiry_datetime = dt.datetime.now() + dt.timedelta(minutes=self.expiry)
            gbq_table.expires = expiry_datetime

        if self.partitioned_field:
            gbq_table.time_partitioning = TimePartitioning(type_=TimePartitioningType.DAY, field=self.partitioned_field)

        self.client.google_client.create_table(gbq_table)
        self.client.logger.info('Table {0} is created.'.format(self.name))

    @property
    def bigquery_schema(self):
        """
        Build a BigQuery schema from a JSONSchema file
        """
        return [
            bigquery.SchemaField(name=column['name'], field_type=column['type'], mode=column.get('mode', 'NULLABLE'))
            for column in self.schema
        ]

    def update_table_schema(self):

        self.client.logger.info('Updating Schema for Table %s' % str(self))

        google_bq_current_table_ref = self.client.fetch_table_reference()
        google_bq_current_table = self.client.google_client.get_table(google_bq_current_table_ref)
        current_field_names = [field.name for field in google_bq_current_table.schema]

        new_schema_field_names = [field['name'] for field in self.schema]
        columns_removed = [field_name for field_name in current_field_names if field_name not in new_schema_field_names]

        if columns_removed:
            raise Exception('New Schema does not have columns which exist in current table - Please Include')

        updated_schema = [bigquery.SchemaField(name=column['name'], field_type=column['type'], mode=column.get('mode', 'NULLABLE'))
                          for column in self.schema]

        google_bq_current_table.schema = updated_schema

        self.client.google_client.update_table(google_bq_current_table, ['schema'])

    def delete_partition_by_name(self, partition_name):
        """
       Delete data for a partition.

       :param str partition_name:
       :return:
        """

        if not self.partitioned_field:
            raise AttributeError("Can't delete a partition if partition field is not set")

        self.client.logger.info(f"Deleting partition {partition_name} from table {self.name}")

        query = f"""
         DELETE FROM `{self.full_table_name}` 
         WHERE {self.partitioned_field} = PARSE_DATE('{PARTITION_DATE_FORMAT}', '{partition_name}')   
        """

        self.client.run_query(query)

    def fetch_partition_list(self):

        """
        Get the list of partitions

        """

        if not self.partitioned_field:
            raise AttributeError("Can't fetch partitions if partition field is not set")

        query = f"""
            SELECT FORMAT_DATE("{PARTITION_DATE_FORMAT}", {self.partitioned_field}) as partition_name
            FROM `{self.full_table_name}`
            GROUP BY partition_name
            ORDER BY partition_name
        """
        data, headers = self.client.run_query(query)

        return [d[0] for d in data]
