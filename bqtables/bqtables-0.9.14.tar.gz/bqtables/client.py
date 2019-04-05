import logging
import os
from datetime import datetime, date
from typing import List, Sequence, Mapping

from google.cloud import bigquery

MODULE_NAME = __name__


class BQProject(object):
    def __init__(self):
        self.project_name = os.environ.get('GCP_PROJECT')
        self.client = bigquery.Client()


class BQTable(object):
    def __init__(
            self, project: BQProject,
            dataset_name: str,
            table_name: str,
            date_column_name: str,
            date_column_type: str = 'TIMESTAMP',
            id_column_name: str = 'id',
            checksum_column_name: str = None,
            logger_name: str = MODULE_NAME,
    ):
        self.project = project
        self.dataset_name = dataset_name
        self.table_name = table_name
        self.date_column_name = date_column_name
        self.date_column_type = date_column_type
        self.id_column_name = id_column_name
        self.checksum_column_name = checksum_column_name

        self.dataset_ref = self.project.client.dataset(self.dataset_name)
        self.table_ref = self.dataset_ref.table(self.table_name)

        self.fqtable_name = '.'.join(
            [self.project.project_name, self.dataset_name, self.table_name])

        self.logger = logging.getLogger(logger_name)

    def clear(self):
        try:
            query = f'DELETE FROM `{self.fqtable_name}` WHERE TRUE'
            job: bigquery.job.QueryJob = self.project.client.query(query)
            results = job.result()
        except Exception as ex:
            self.logger.exception(f'BQTable.update.failed: {str(ex)}')
            raise


    def fetch(
            self,
            start_date: [str, datetime],
            end_date: [str, datetime]
    ) -> bigquery.table.RowIterator:
        try:
            if type(start_date) != str:
                start_date = start_date.isoformat()
            if type(end_date) != str:
                end_date = end_date.isoformat()

            query = f"""
                SELECT * from `{self.fqtable_name}`
                WHERE `{self.date_column_name}` BETWEEN
                    {self.date_column_type}('{start_date}') AND 
                    {self.date_column_type}('{end_date}')
                ORDER BY `{self.date_column_name}`"""
            job: bigquery.job.QueryJob = self.project.client.query(query)
            results = job.result()

            return results

        except Exception as ex:
            self.logger.exception(f'BQTable.fetch.failed: {str(ex)}')
            raise

    def stream(self, data: List[dict]) -> List[Sequence[Mapping]]:
        try:
            mappings = []
            table = self.project.client.get_table(self.table_ref)
            chunks = [data[i:i + 1000] for i in range(0, len(data), 1000)]
            for chunk in chunks:
                result = self.project.client.insert_rows(table, chunk)
                mappings.append(result)
            mappings = [error for sublist in mappings for error in sublist]
            if mappings:
                raise ValueError(str(mappings))
            return mappings
        except Exception as ex:
            self.logger.exception(f'BQTable.stream.failed: {str(ex)}')
            raise

    def sync(
            self,
            existing_rows: bigquery.table.RowIterator,
            new_rows: List[dict],
    ):
        to_ignore = []
        to_update = []

        for existing_row in existing_rows:
            id = existing_row[self.id_column_name]
            new_row = next(
                (row for row in new_rows if row[self.id_column_name] == id),
                None)

            if not new_row:
                continue
            if self.checksum_column_name:
                if existing_row[self.checksum_column_name] == \
                        new_row[self.checksum_column_name]:
                    to_ignore.append(new_row)
                    continue

            to_update.append(new_row)

        to_insert = [row for row in new_rows if
                     (row not in to_ignore and row not in to_update)]

        self.logger.info('bqtables.sync.sending_to_bigquery: %d inserts, %d updates',
                          len(to_insert), len(to_update))
        self.stream(to_insert)
        self.update(to_update)

    def update(self, data: List[dict]):
        for item in data:
            try:
                on_value = self._as_query_value(item[self.id_column_name])
                set_operations = self._as_set_operations(item)
                query = f"""
                    UPDATE `{self.fqtable_name}`
                    SET {set_operations}
                    WHERE `{self.id_column_name}` = {on_value}"""
                job: bigquery.job.QueryJob = self.project.client.query(query)
                results = job.result()
            except Exception as ex:
                self.logger.exception(f'BQTable.update.failed: {str(ex)}')
                raise

    def _as_query_value(self, value) -> str:
        if value is None:
            return 'NULL'

        vtype = type(value)
        if vtype == str:
            return f'"{value}"'
        if vtype == datetime or vtype == date:
            return f'{self.date_column_type}("{value.isoformat()}")'

        return str(value)

    def _as_set_operations(self, d: dict) -> str:
        sets = [f'`{k}` = {self._as_query_value(v)}' for k, v in d.items()]
        return ','.join(sets)
