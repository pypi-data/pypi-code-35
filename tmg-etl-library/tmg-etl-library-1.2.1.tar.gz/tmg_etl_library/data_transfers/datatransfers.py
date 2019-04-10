from tmg_etl_library.data_transfers.transfer import Transfer
from tmg_etl_library.components.configurations import *
from tmg_etl_library.components.buckets import gs
from tmg_etl_library.components.locals import csv

from google.cloud.bigquery.job import CopyJobConfig, ExtractJobConfig, LoadJobConfig, CreateDisposition

import uuid


class BQTOBQ(Transfer):
    def __init__(self, log, source, target, config=BQTOBQConfig()):
        super().__init__(log, source, target, config)
        self.id = uuid.uuid4()
        self.source = source
        self.target = target
        if not isinstance(config, BQTOBQConfig):
            raise TypeError('Config Must be of Type: BQTOBQConfig')
        self.config = config
        self.log = log

    def run(self):
        if self.config.query:
            self.source.client.run_query(query=self.config.query,
                                         query_file_name=self.config.query_file_name,
                                         destination=self.target,
                                         write_disposition=self.config.write_disposition,
                                         use_legacy_sql=self.config.use_legacy_sql,
                                         async_query=self.config.async_query,
                                         query_params=self.config.query_params)
        else:
            copy_job_config = CopyJobConfig()
            if self.config:
                copy_job_config.write_disposition = self.config.write_disposition


            if self.target.expiry or self.target.partitioned_field:
                self.target.create(self.config)
            self.log.info('Copying table %s to %s' % (str(self.source), str(self.target)))
            google_bq_table_source = self.source.client.fetch_table_reference(self.source)
            google_bq_table_target = self.target.client.fetch_table_reference(self.target)
            self.source.client.google_client.copy_table(google_bq_table_source, google_bq_table_target, job_config=copy_job_config)


class BQTOMySQL(Transfer):
    def __init__(self, log, source, target, config=BQTOMySQLConfig()):
        super().__init__(log, source, target, config)
        self.id = uuid.uuid4()
        self.source = source
        self.target = target
        if not isinstance(config, BQTOMySQLConfig):
            raise TypeError('Config Must be of Type: BQTOMySQLConfig')
        self.config = config
        self.log = log

    def run(self):
        if self.config.query:
            self.config.query = 'SELECT * FROM `{full_table}`'
            self.config.query_params = {'full_table': str(self.source)}

        data, _ = self.source.client.run_query(self.config.query)
        self.target.insert_data(data, force_creation=self.config.force_creation)


class BQTOCSV(Transfer):
    # TODO: clean up along with BQTOGS
    def __init__(self, log, BQTable, CSVFile, config=BQTOCSVConfig()):
        super().__init__(log, BQTable, CSVFile, config)
        self.id = uuid.uuid4()
        self.BQTable = BQTable
        self.CSVFile = CSVFile
        if not isinstance(config, BQTOCSVConfig):
            raise TypeError('Config Must be of Type: BQTOCSVConfig')
        self.config = config
        self.log = log

    def run(self):
        if self.config.full_table:
            if not self.config.gs_bucket:
                self.config.gs_bucket = '{project}-tmp-files'.format(project=self.BQTable.project)
            if not self.config.gs_filename:
                self.config.gs_filename = '{table}_*'.format(table=self.BQTable.name)

            gs_client = gs.GSClient(log=self.log,
                                    project=self.BQTable.project,
                                    bucket_name=self.config.gs_bucket)
            storage_file = gs.GSFile(client=gs_client,
                                     project=self.BQTable.project,
                                     bucket_name=self.config.gs_bucket,
                                     file_name=self.config.gs_filename)

            to_storage = BQTOGSConfig()
            to_storage.field_delimiter = self.config.field_delimiter
            to_storage.print_header = self.config.print_header
            to_storage.tmp_bucket = self.config.gs_bucket
            to_storage.tmp_filename = self.config.gs_filename

            transfer = BQTOGS(log=self.log,
                              BQTable=self.BQTable,
                              GSFile=storage_file,
                              config=to_storage)
            transfer.run()

            gs_files = gs_client.list_files(prefix=self.config.gs_filename)

            files_to_merge = []
            for file in gs_files:
                local_file = csv.CSVFile(file.file_name + '.csv', self.CSVFile.path, self.CSVFile.delimiter)
                file.download(local_file)
                files_to_merge.append(local_file)
                file.delete()

            self.CSVFile.client.merge_csv_files(files_to_merge, self.CSVFile)

        elif self.config.query:
            data, headers = self.BQTable.client.run_query(self.config.query, query_params=self.config.query_params)
            self.CSVFile.insert_data(data, headers, write_headers=self.config.print_header)
        else:
            raise TypeError("Either 'full_table' or 'query' must be set in the BQTOCSVConfig class")


class BQTOGS(Transfer):
    # TODO: clean up with BQTOCSV
    def __init__(self, log, BQTable, GSFile, config=BQTOGSConfig()):
        super().__init__(log, BQTable, GSFile, config)
        self.id = uuid.uuid4()
        self.BQTable = BQTable
        self.GSFile = GSFile
        if not isinstance(config, BQTOGSConfig):
            raise TypeError('Config Must be of Type: BQTOGSConfig')
        self.config = config
        self.log = log

    def run(self):
        job_config = ExtractJobConfig()
        job_config.print_header = self.config.print_header
        job_config.field_delimiter = self.config.field_delimiter

        if not self.config.tmp_bucket:
            self.config.tmp_bucket = self.GSFile.bucket_name
        if not self.config.tmp_filename:
            self.config.tmp_filename = self.GSFile.file_name

        destination_uri = 'gs://{}/{}'.format(self.config.tmp_bucket, self.config.tmp_filename)
        table_ref = self.BQTable.client.fetch_table_reference(self.BQTable)

        self.log.info('Exporting {project}:{dataset}.{table} to {destination}'.format(
            project=self.BQTable.project,
            dataset=self.BQTable.dataset,
            table=self.BQTable.name,
            destination=destination_uri
        ))

        extract_job = self.BQTable.client.google_client.extract_table(
            source=table_ref,
            destination_uris=[destination_uri],
            job_config=job_config
        )
        # API request
        extract_job.result()


class BQTOS3(Transfer):
    def __init__(self, log, BQTable, S3File, config=BQTOS3Config()):
        super().__init__(log, BQTable, S3File, config)
        self.id = uuid.uuid4()
        self.BQTable = BQTable
        self.S3File = S3File
        if not isinstance(config, BQTOS3Config):
            raise TypeError('Config Must be of Type: BQtoS3Config')
        self.config = config
        self.log = log

    def run(self):
        tmp_csv = csv.CSVFile(name=self.config.tmp_filename,
                              path=self.config.tmp_local_path,
                              delimiter=self.config.delimiter,
                              quote_char=self.config.quote_char)

        to_local_config = BQTOCSVConfig()
        to_local_config.field_delimiter = self.config.delimiter
        to_local_config.quote_character = self.config.quote_char
        to_local_config.use_legacy_sql = self.config.use_legacy_sql
        to_local_config.print_header = self.config.include_headers
        to_local_config.query = self.config.query
        to_local_config.query_file_path = self.config.query_file_path
        to_local_config.query_params = self.config.query_params

        to_local = BQTOCSV(log=self.log,
                           BQTable=self.BQTable,
                           CSVFile=tmp_csv,
                           config=to_local_config
                           )
        to_local.run()

        from_local_config = CSVTOS3Config()

        from_local = CSVTOS3(log=self.log,
                             CSVFile=tmp_csv,
                             S3File=self.S3File,
                             config=from_local_config
                             )
        from_local.run()

        if not self.config.retain_local:
            tmp_csv.delete_file()


class BQTOFTP(Transfer):
    def __init__(self, log, BQTable, FTPFile, config=BQTOFTPConfig()):
        super().__init__(log, BQTable, FTPFile, config)
        self.id = uuid.uuid4()
        self.BQTable = BQTable
        self.FTPFile = FTPFile
        if not isinstance(config, BQTOFTPConfig):
            raise TypeError('Config Must be of Type: BQTOFTPConfig')
        self.config = config
        self.log = log

    def run(self):
        tmp_csv = csv.CSVFile(name=self.config.tmp_filename,
                              path=self.config.tmp_local_path,
                              delimiter=self.config.delimiter,
                              quote_char=self.config.quote_char)

        to_local_config = BQTOCSVConfig()
        to_local_config.field_delimiter = self.config.delimiter
        to_local_config.quote_character = self.config.quote_char
        to_local_config.use_legacy_sql = self.config.use_legacy_sql
        to_local_config.print_header = self.config.include_headers
        to_local_config.query = self.config.query
        to_local_config.query_file_path = self.config.query_file_path
        to_local_config.query_params = self.config.query_params

        to_local = BQTOCSV(log=self.log,
                           BQTable=self.BQTable,
                           CSVFile=tmp_csv,
                           config=to_local_config
                           )
        to_local.run()

        from_local_config = CSVTOFTPConfig()

        from_local = CSVTOFTP(log=self.log,
                              CSVFile=tmp_csv,
                              FTPFile=self.FTPFile,
                              config=from_local_config
                              )
        from_local.run()

        if not self.config.retain_local:
            tmp_csv.delete_file()


class MySQLTOMySQL(Transfer):
    def __init__(self, log, source, target, config=MySQLTOMySQLConfig()):
        super().__init__(log, source, target, config)
        self.id = uuid.uuid4()
        self.source = source
        self.target = target
        if not isinstance(config, MySQLTOMySQLConfig):
            raise TypeError('Config Must be of Type: MySQLTOMySQLConfig')
        self.config = config
        self.log = log

    def run(self):
        if not self.target.exists():
            if self.config.force_creation:
                self.target.create_table()
            else:
                self.log.error('Table does not exist and force_creation is set to False')
                raise RuntimeError('TableDoesNotExist')

        if self.config.query_file_path:
            with open(self.config.query_file_path, 'rt') as f:
                query = f.read()
        else:
            query = self.config.query

        if query:
            query = query.format(**self.config.query_params)

        if self.config.insert_query:
            self.source.client.run_query(query)
        elif query:
            results, _ = self.source.client.run_query(query)
            self.target.insert_data(results)
        else:
            # TODO: Decide how to implement
            pass


class MySQLTOBQ(Transfer):
    def __init__(self, log, MySQLTable, BQTable, config=MySQLTOBQConfig()):
        super().__init__(log, MySQLTable, BQTable, config)
        self.id = uuid.uuid4()
        self.MySQLTable = MySQLTable
        self.BQTable = BQTable
        if not isinstance(config, MySQLTOBQConfig):
            raise TypeError('Config Must be of Type: MySQLTOBQConfig')
        self.config = config
        self.log = log

    def run(self):
        tmp_csv = csv.CSVFile(name=self.config.tmp_filename,
                              path=self.config.tmp_local_path,
                              delimiter=self.config.delimiter,
                              quote_char=self.config.quote_char)

        to_local_config = MySQLTOCSVConfig()
        to_local_config.field_delimiter = self.config.delimiter
        to_local_config.quote_character = self.config.quote_char
        to_local_config.use_legacy_sql = self.config.use_legacy_sql
        to_local_config.print_header = self.config.include_headers
        to_local_config.query = self.config.query
        to_local_config.query_file_path = self.config.query_file_path
        to_local_config.query_params = self.config.query_params

        to_local = MySQLTOCSV(log=self.log,
                              MySQLTable=self.MySQLTable,
                              CSVFile=tmp_csv,
                              config=to_local_config
                              )
        to_local.run()

        from_local_config = CSVTOBQConfig()

        from_local = CSVTOBQ(log=self.log,
                             csv_file=tmp_csv,
                             bq_table=self.BQTable,
                             config=from_local_config
                             )
        from_local.run()



        if not self.config.retain_local:
            tmp_csv.delete_file()


class MySQLTOCSV(Transfer):
    def __init__(self, log, MySQLTable, CSVFile, config=MySQLTOCSVConfig()):
        super().__init__(log, MySQLTable, CSVFile, config)
        self.id = uuid.uuid4()
        self.MySQLTable = MySQLTable
        self.CSVFile = CSVFile
        if not isinstance(config, MySQLTOCSVConfig):
            raise TypeError('Config Must be of Type: MySQLTOCSVConfig')
        self.config = config
        self.log = log

    def run(self):
        if self.MySQLTable.table_exists():
            sql_table = self.MySQLTable.client._get_sqlachemy_table(self)
        else:
            self.log.error('The table {} does not exist in this dataset'.format(self.MySQLTable.name))
            raise Exception("Table doesn't exist")

        if not self.MySQLTable.schema:
            self.MySQLTable.schema = self.MySQLTable.client._convert_sqlalchemy_schema(sql_table)

        if self.config.query:
            run_query = self.config.query.format(**self.config.query_params)
        elif self.config.query_file_path:
            with open(self.config.query_file_path, 'rt') as f:
                run_query = f.read().format(**self.config.query_params)
        elif self.config.full_table:
            run_query = sql_table.select()
        else:
            self.log.error('Neither full table or a query has been provided. Please apply what part of the table should be downloaded.')
            raise RuntimeError('NoTableSelection')

        results = self.MySQLTable.client.connection.execute(run_query)

        columns = [column['name'] for column in self.MySQLTable.schema]
        data = [[str(data_point) for data_point in row] for row in results]

        self.CSVFile.insert_data(columns, data, write_headers=self.config.include_headers)


class MySQLTOGS(Transfer):
    def __init__(self, log, MySQLTable, GSFile, config=MySQLTOGSConfig()):
        super().__init__(log, MySQLTable, GSFile, config)
        self.id = uuid.uuid4()
        self.MySQLTable = MySQLTable
        self.GSFile = GSFile
        if not isinstance(config, MySQLTOGSConfig):
            raise TypeError('Config Must be of Type: MySQLTOGSConfig')
        self.config = config
        self.log = log

    def run(self):
        tmp_csv = csv.CSVFile(name=self.config.tmp_filename,
                              path=self.config.tmp_local_path,
                              delimiter=self.config.delimiter,
                              quote_char=self.config.quote_char)

        to_local_config = MySQLTOCSVConfig()
        to_local_config.field_delimiter = self.config.delimiter
        to_local_config.quote_character = self.config.quote_char
        to_local_config.print_header = self.config.include_headers
        to_local_config.query = self.config.query
        to_local_config.query_file_path = self.config.query_file_path
        to_local_config.query_params = self.config.query_params

        to_local = MySQLTOCSV(log=self.log,
                              MySQLTable=self.MySQLTable,
                              CSVFile=tmp_csv,
                              config=to_local_config
                              )
        to_local.run()

        from_local_config = CSVTOGSConfig()

        from_local = CSVTOGS(log=self.log,
                             CSVFile=tmp_csv,
                             GSFile=self.GSFile,
                             config=from_local_config
                             )
        from_local.run()

        if not self.config.retain_local:
            tmp_csv.delete_file()


class MySQLTOS3(Transfer):
    def __init__(self, log, MySQLTable, S3File, config=MySQLTOS3Config()):
        super().__init__(log, MySQLTable, S3File, config)
        self.id = uuid.uuid4()
        self.MySQLTable = MySQLTable
        self.S3File = S3File
        if not isinstance(config, MySQLTOS3Config):
            raise TypeError('Config Must be of Type: MySQLTOS3Config')
        self.config = config
        self.log = log

    def run(self):
        tmp_csv = csv.CSVFile(name=self.config.tmp_filename,
                              path=self.config.tmp_local_path,
                              delimiter=self.config.delimiter,
                              quote_char=self.config.quote_char)

        to_local_config = MySQLTOCSVConfig()
        to_local_config.field_delimiter = self.config.delimiter
        to_local_config.quote_character = self.config.quote_char
        to_local_config.print_header = self.config.include_headers
        to_local_config.query = self.config.query
        to_local_config.query_file_path = self.config.query_file_path
        to_local_config.query_params = self.config.query_params

        to_local = MySQLTOCSV(log=self.log,
                              MySQLTable=self.MySQLTable,
                              CSVFile=tmp_csv,
                              config=to_local_config
                              )
        to_local.run()

        from_local_config = CSVTOS3Config()

        from_local = CSVTOS3(log=self.log,
                             CSVFile=tmp_csv,
                             S3File=self.S3File,
                             config=from_local_config
                             )
        from_local.run()

        if not self.config.retain_local:
            tmp_csv.delete_file()


class MySQLTOFTP(Transfer):
    def __init__(self, log, MySQLTable, FTPFile, config=MySQLTOFTPConfig()):
        super().__init__(log, MySQLTable, FTPFile, config)
        self.id = uuid.uuid4()
        self.MySQLTable = MySQLTable
        self.FTPFile = FTPFile
        if not isinstance(config, MySQLTOFTPConfig):
            raise TypeError('Config Must be of Type: MySQLTOFTPConfig')
        self.config = config
        self.log = log

    def run(self):
        tmp_csv = csv.CSVFile(name=self.config.tmp_filename,
                              path=self.config.tmp_local_path,
                              delimiter=self.config.delimiter,
                              quote_char=self.config.quote_char)

        to_local_config = MySQLTOCSVConfig()
        to_local_config.field_delimiter = self.config.delimiter
        to_local_config.quote_character = self.config.quote_char
        to_local_config.print_header = self.config.include_headers
        to_local_config.query = self.config.query
        to_local_config.query_file_path = self.config.query_file_path
        to_local_config.query_params = self.config.query_params

        to_local = MySQLTOCSV(log=self.log,
                              MySQLTable=self.MySQLTable,
                              CSVFile=tmp_csv,
                              config=to_local_config
                              )
        to_local.run()

        from_local_config = CSVTOFTPConfig()

        from_local = CSVTOFTP(log=self.log,
                              CSVFile=tmp_csv,
                              FTPFile=self.FTPFile,
                              config=from_local_config
                              )
        from_local.run()

        if not self.config.retain_local:
            tmp_csv.delete_file()


class CSVTOBQ(Transfer):
    def __init__(self, log, csv_file, bq_table, config=None):
        """
        :param Logger log:
        :param CSVFile csv_file:
        :param BQTable bq_table:
        :param CSVTOBQConfig config:
        """
        config = config if config else CSVTOBQConfig()
        super().__init__(log, csv_file, bq_table, config)

        if not isinstance(self.config, CSVTOBQConfig):
            raise TypeError('Config Must be of Type: CSVTOBQConfig')

        self.id = uuid.uuid4()
        self.CSVFile = csv_file
        self.BQTable = bq_table

        self.log = log

    def run(self):
        table_exists = self.BQTable.exists()

        if self.config.create_disposition == CreateDisposition.CREATE_NEVER and not table_exists:
            raise RuntimeError('Table does not exist and config set to not create table')

        elif self.config.create_disposition == CreateDisposition.CREATE_IF_NEEDED and not table_exists:
            self.BQTable.create()

        elif self.config.create_disposition == 'REPLACE_IF_EXISTS':
            if table_exists:
                self.BQTable.delete()
            self.BQTable.create()

        google_bq_table = self.BQTable.client.fetch_table_reference(self.BQTable)

        with open(self.CSVFile.full_path, 'rb') as csv_file_obj:
            job_config = LoadJobConfig()

            job_config.field_delimiter = self.CSVFile.delimiter
            job_config.write_disposition = self.config.write_disposition
            job_config.allow_quoted_newlines = self.config.allow_quoted_newlines
            job_config.skip_leading_rows = 1 if self.config.skip_leading_rows else 0
            job_config.max_bad_records = self.config.max_bad_records
            job_config.allow_jagged_rows = self.config.allow_jagged_rows
            job_config.quote_character = self.CSVFile.quote_char
            job_config.ignore_unknown_values = self.config.ignore_unknown_values
            job_config.schema = self.BQTable.bigquery_schema
            job = self.BQTable.client.google_client.load_table_from_file(
                csv_file_obj, google_bq_table, job_config=job_config)  # API request
            job.result()


class CSVTOMySQL(Transfer):
    def __init__(self, log, CSVFile, MySQLTable, config=CSVTOMySQLConfig()):
        super().__init__(log, CSVFile, MySQLTable, config)
        self.id = uuid.uuid4()
        self.CSVFile = CSVFile
        self.MySQLTable = MySQLTable
        if not isinstance(config, CSVTOMySQLConfig):
            raise TypeError('Config Must be of Type: CSVTOMySQLConfig')
        self.config = config
        self.log = log

    def run(self):
        if not self.MySQLTable.table_exists():
            if self.config.create_disposition:
                self.MySQLTable.create_table()
            else:
                self.log.error('Table does not exist and config set to not create table')
                raise RuntimeError('Table does not exist and config set to not create table')

        data = self.CSVFile.read_data(self.config.skip_leading_rows)
        self.MySQLTable.insert_data(data=data)


class CSVTOGS(Transfer):
    def __init__(self, log, CSVFile, GSFile, config=CSVTOGSConfig()):
        super().__init__(log, CSVFile, GSFile, config)
        self.id = uuid.uuid4()
        self.CSVFile = CSVFile
        self.GSFile = GSFile
        if not isinstance(config, CSVTOGSConfig):
            raise TypeError('Config Must be of Type: CSVTOGSConfig')
        self.config = config
        self.log = log

    def run(self):
        exists = self.GSFile.exists()
        if self.config.write_disposition == 'REPLACE' and exists:
            self.GSFile.upload(self.CSVFile)


class CSVTOS3(Transfer):
    def __init__(self, log, CSVFile, S3File, config=CSVTOS3Config()):
        super().__init__(log, CSVFile, S3File, config)
        self.id = uuid.uuid4()
        self.CSVFile = CSVFile
        self.S3File = S3File
        if not isinstance(config, CSVTOS3Config):
            raise TypeError('Config Must be of Type: CSVTOS3Config')
        self.config = config
        self.log = log

    def run(self):
        exists = self.S3File.exists()
        if self.config.write_disposition == 'REPLACE' and exists:
            self.S3File.upload(self.CSVFile)


class CSVTOFTP(Transfer):
    def __init__(self, log, CSVFile, FTPFile, config=CSVTOFTPConfig()):
        super().__init__(log, CSVFile, FTPFile, config)
        self.id = uuid.uuid4()
        self.CSVFile = CSVFile
        self.FTPFile = FTPFile
        if not isinstance(config, CSVTOFTPConfig):
            raise TypeError('Config Must be of Type: CSVTOFTPConfig')
        self.config = config
        self.log = log

    def run(self):
        exists = self.FTPFile.exists()
        if self.config.write_disposition == 'REPLACE' and exists:
            self.FTPFile.upload(self.CSVFile)


class GSTOBQ(Transfer):
    def __init__(self, log, gs_file, bq_table, config=None):
        """

        :param Logger log:
        :param GSFile gs_file:
        :param BQTable bq_table:
        :param GSTOBQConfig config:
        """

        config = config if config else GSTOBQConfig()
        super().__init__(log, gs_file, bq_table, config)

        if not isinstance(config, GSTOBQConfig):
            raise TypeError('Config Must be of Type: GSTOBQConfig')

        self.id = uuid.uuid4()
        self.GSFile = gs_file
        self.BQTable = bq_table

        self.log = log

    def run(self):
        table_exists = self.BQTable.exists()

        if self.config.create_disposition == 'CREATE_NEVER' and not table_exists:
            raise RuntimeError('Table does not exist and config set to not create table')

        elif self.config.create_disposition == 'CREATE_IF_NEEDED' and not table_exists:
            self.BQTable.create()

        google_bq_table = self.BQTable.client.fetch_table_reference(self.BQTable)

        job_config = LoadJobConfig()

        job_config.field_delimiter = self.config.field_delimiter
        job_config.write_disposition = self.config.write_disposition
        job_config.allow_quoted_newlines = self.config.allow_quoted_newlines
        job_config.skip_leading_rows = self.config.skip_leading_rows if self.config.skip_leading_rows else 0
        job_config.max_bad_records = self.config.max_bad_records
        job_config.allow_jagged_rows = self.config.allow_jagged_rows
        job_config.quote_character = self.config.quote_character
        job_config.ignore_unknown_values = self.config.ignore_unknown_values

        job = self.BQTable.client.google_client.load_table_from_uri(
            self.GSFile.full_path, google_bq_table, job_config=job_config)  # API request
        job.result()


class GSTOMySQL(Transfer):
    def __init__(self, log, GSFile, MySQLTable, config=GSTOMySQLConfig()):
        super().__init__(log, GSFile, MySQLTable, config)
        self.id = uuid.uuid4()
        self.GSFile = GSFile
        self.MySQLTable = MySQLTable
        if not isinstance(config, GSTOMySQLConfig):
            raise TypeError('Config Must be of Type: GSTOMySQLConfig')
        self.config = config
        self.log = log

    def run(self):
        tmp_csv = csv.CSVFile(name=self.config.tmp_filename,
                              path=self.config.tmp_local_path,
                              delimiter=self.config.delimiter,
                              quote_char=self.config.quote_char)

        to_local_config = GSTOCSVConfig()
        to_local_config.field_delimiter = self.config.delimiter
        to_local_config.quote_character = self.config.quote_char
        to_local_config.print_header = self.config.include_headers

        to_local = GSTOCSV(log=self.log,
                           GSFile=self.GSFile,
                           CSVFile=tmp_csv,
                           config=to_local_config
                           )
        to_local.run()

        from_local_config = CSVTOMySQLConfig()

        from_local = CSVTOMySQL(log=self.log,
                                CSVFile=tmp_csv,
                                MySQLTable=self.MySQLTable,
                                config=from_local_config
                                )
        from_local.run()

        if not self.config.retain_local:
            tmp_csv.delete_file()


class GSTOCSV(Transfer):
    def __init__(self, log, GSFile, CSVFile, config=GSTOCSVConfig()):
        super().__init__(log, GSFile, CSVFile, config)
        self.id = uuid.uuid4()
        self.GSFile = GSFile
        self.CSVFile = CSVFile
        if not isinstance(config, GSTOCSVConfig):
            raise TypeError('Config Must be of Type: GSTOCSVConfig')
        self.config = config
        self.log = log

    def run(self):
        self.GSFile.download(self.CSVFile)


class S3TOBQ(Transfer):
    def __init__(self, log, S3File, BQTable, config=S3TOBQConfig()):
        super().__init__(log, S3File, BQTable, config)
        self.id = uuid.uuid4()
        self.S3File = S3File
        self.BQTable = BQTable
        if not isinstance(config, S3TOBQConfig):
            raise TypeError('Config Must be of Type: S3TOBQConfig')
        self.config = config
        self.log = log

    def run(self):
        tmp_csv = csv.CSVFile(name=self.config.tmp_filename,
                              path=self.config.tmp_local_path,
                              delimiter=self.config.delimiter,
                              quote_char=self.config.quote_char)

        to_local_config = S3TOCSVConfig()
        to_local_config.field_delimiter = self.config.delimiter
        to_local_config.quote_character = self.config.quote_char
        to_local_config.print_header = self.config.include_headers

        to_local = S3TOCSV(log=self.log,
                           S3File=self.S3File,
                           CSVFile=tmp_csv,
                           config=to_local_config
                           )
        to_local.run()

        from_local_config = CSVTOBQConfig()

        from_local = CSVTOBQ(log=self.log,
                             csv_file=tmp_csv,
                             bq_table=self.BQTable,
                             config=from_local_config
                             )
        from_local.run()

        if not self.config.retain_local:
            tmp_csv.delete_file()


class S3TOMySQL(Transfer):
    def __init__(self, log, S3File, MySQLTable, config=S3TOMySQLConfig()):
        super().__init__(log, S3File, MySQLTable, config)
        self.id = uuid.uuid4()
        self.S3File = S3File
        self.MySQLTable = MySQLTable
        if not isinstance(config, S3TOMySQLConfig):
            raise TypeError('Config Must be of Type: S3TOMySQLConfig')
        self.config = config
        self.log = log

    def run(self):
        tmp_csv = csv.CSVFile(name=self.config.tmp_filename,
                              path=self.config.tmp_local_path,
                              delimiter=self.config.delimiter,
                              quote_char=self.config.quote_char)

        to_local_config = S3TOCSVConfig()
        to_local_config.field_delimiter = self.config.delimiter
        to_local_config.quote_character = self.config.quote_char
        to_local_config.print_header = self.config.include_headers

        to_local = S3TOCSV(log=self.log,
                           S3File=self.S3File,
                           CSVFile=tmp_csv,
                           config=to_local_config
                           )
        to_local.run()

        from_local_config = CSVTOMySQLConfig()

        from_local = CSVTOMySQL(log=self.log,
                                CSVFile=tmp_csv,
                                MySQLTable=self.MySQLTable,
                                config=from_local_config
                                )
        from_local.run()

        if not self.config.retain_local:
            tmp_csv.delete_file()


class S3TOCSV(Transfer):
    def __init__(self, log, S3File, CSVFile, config=S3TOCSVConfig()):
        super().__init__(log, S3File, CSVFile, config)
        self.id = uuid.uuid4()
        self.S3File = S3File
        self.CSVFile = CSVFile
        if not isinstance(config, S3TOCSVConfig):
            raise TypeError('Config Must be of Type: S3TOCSVConfig')
        self.config = config
        self.log = log

    def run(self):
        self.S3File.download(self.CSVFile)


class S3TOGS(Transfer):
    def __init__(self, log, S3File, GSFile, config=S3TOGSConfig()):
        super().__init__(log, S3File, GSFile, config)
        self.id = uuid.uuid4()
        self.S3File = S3File
        self.GSFile = GSFile
        if not isinstance(config, S3TOGSConfig):
            raise TypeError('Config Must be of Type: S3TOGSConfig')
        self.config = config
        self.log = log

    def run(self):
        tmp_csv = csv.CSVFile(name=self.config.tmp_filename,
                              path=self.config.tmp_local_path,
                              delimiter=self.config.delimiter,
                              quote_char=self.config.quote_char)

        to_local_config = S3TOCSVConfig()
        to_local_config.field_delimiter = self.config.delimiter
        to_local_config.quote_character = self.config.quote_char
        to_local_config.print_header = self.config.include_headers

        to_local = S3TOCSV(log=self.log,
                           S3File=self.S3File,
                           CSVFile=tmp_csv,
                           config=to_local_config
                           )
        to_local.run()

        from_local_config = CSVTOGSConfig()

        from_local = CSVTOGS(log=self.log,
                             CSVFile=tmp_csv,
                             GSFile=self.GSFile,
                             config=from_local_config
                             )
        from_local.run()

        if not self.config.retain_local:
            tmp_csv.delete_file()


class FTPTOBQ(Transfer):
    def __init__(self, log, S3File, BQTable, config=S3TOBQConfig()):
        super().__init__(log, S3File, BQTable, config)
        self.id = uuid.uuid4()
        self.S3File = S3File
        self.BQTable = BQTable
        if not isinstance(config, S3TOBQConfig):
            raise TypeError('Config Must be of Type: S3TOBQConfig')
        self.config = config
        self.log = log

    def run(self):
        tmp_csv = csv.CSVFile(name=self.config.tmp_filename,
                              path=self.config.tmp_local_path,
                              delimiter=self.config.delimiter,
                              quote_char=self.config.quote_char)

        to_local_config = S3TOCSVConfig()
        to_local_config.field_delimiter = self.config.delimiter
        to_local_config.quote_character = self.config.quote_char
        to_local_config.print_header = self.config.include_headers

        to_local = S3TOCSV(log=self.log,
                           S3File=self.S3File,
                           CSVFile=tmp_csv,
                           config=to_local_config
                           )
        to_local.run()

        from_local_config = CSVTOBQConfig()

        from_local = CSVTOBQ(log=self.log,
                             csv_file=tmp_csv,
                             bq_table=self.BQTable,
                             config=from_local_config
                             )
        from_local.run()

        if not self.config.retain_local:
            tmp_csv.delete_file()


class FTPTOMySQL(Transfer):
    def __init__(self, log, FTPFile, MySQLTable, config=FTPTOMySQLConfig()):
        super().__init__(log, FTPFile, MySQLTable, config)
        self.id = uuid.uuid4()
        self.FTPFile = FTPFile
        self.MySQLTable = MySQLTable
        if not isinstance(config, FTPTOMySQLConfig):
            raise TypeError('Config Must be of Type: FTPTOMySQLConfig')
        self.config = config
        self.log = log

    def run(self):
        tmp_csv = csv.CSVFile(name=self.config.tmp_filename,
                              path=self.config.tmp_local_path,
                              delimiter=self.config.delimiter,
                              quote_char=self.config.quote_char)

        to_local_config = FTPTOCSVConfig()
        to_local_config.field_delimiter = self.config.delimiter
        to_local_config.quote_character = self.config.quote_char
        to_local_config.print_header = self.config.include_headers

        to_local = FTPTOCSV(log=self.log,
                            FTPFile=self.FTPFile,
                            CSVFile=tmp_csv,
                            config=to_local_config
                            )
        to_local.run()

        from_local_config = CSVTOMySQLConfig()

        from_local = CSVTOMySQL(log=self.log,
                                CSVFile=tmp_csv,
                                MySQLTable=self.MySQLTable,
                                config=from_local_config
                                )
        from_local.run()

        if not self.config.retain_local:
            tmp_csv.delete_file()


class FTPTOCSV(Transfer):
    def __init__(self, log, FTPFile, CSVFile, config=FTPTOCSVConfig()):
        super().__init__(log, FTPFile, CSVFile, config)
        self.id = uuid.uuid4()
        self.FTPFile = FTPFile
        self.CSVFile = CSVFile
        if not isinstance(config, FTPTOCSVConfig):
            raise TypeError('Config Must be of Type: FTPTOCSVConfig')
        self.config = config
        self.log = log

    def run(self):
        self.FTPFile.download(self.CSVFile)


class FTPTOGS(Transfer):
    def __init__(self, log, FTPFile, GSFile, config=FTPTOGSConfig()):
        super().__init__(log, FTPFile, GSFile, config)
        self.id = uuid.uuid4()
        self.FTPFile = FTPFile
        self.GSFile = GSFile
        if not isinstance(config, FTPTOGSConfig):
            raise TypeError('Config Must be of Type: FTPTOGSConfig')
        self.config = config
        self.log = log

    def run(self):
        tmp_csv = csv.CSVFile(name=self.config.tmp_filename,
                              path=self.config.tmp_local_path,
                              delimiter=self.config.delimiter,
                              quote_char=self.config.quote_char)

        to_local_config = FTPTOCSVConfig()
        to_local_config.field_delimiter = self.config.delimiter
        to_local_config.quote_character = self.config.quote_char
        to_local_config.print_header = self.config.include_headers

        to_local = FTPTOCSV(log=self.log,
                            FTPFile=self.FTPFile,
                            CSVFile=tmp_csv,
                            config=to_local_config
                            )
        to_local.run()

        from_local_config = CSVTOGSConfig()

        from_local = CSVTOGS(log=self.log,
                             CSVFile=tmp_csv,
                             GSFile=self.GSFile,
                             config=from_local_config
                             )
        from_local.run()

        if not self.config.retain_local:
            tmp_csv.delete_file()
