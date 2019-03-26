# system modules
import os
import re
import itertools
import logging
import datetime
import sqlite3

# internal modules
from co2logserver import app
from co2logserver.utils import *

# external modules


def config(k):
    return app.config["CO2LOGSERVER_{}".format(k)]


DATATYPES = {
    None: "NULL",
    datetime.datetime: "DATETIME",
    float: "REAL",
    int: "INTEGER",
    str: "TEXT",
}
DATA_TABLE = "data"
MINIMAL_DATA_TABLE_FIELDS = {
    config("UPLOAD_TIME_COL"): DATATYPES.get(datetime.datetime),
    config("MATCHED_CHECKSUMS_COL"): DATATYPES.get(str),
    config("FAILED_CHECKSUMS_COL"): DATATYPES.get(str),
}


class DataBaseHandler(object):
    def __init__(self, dbfile):
        self.dbfile = dbfile

    @property
    def connection(self):
        try:
            return self._connection
        except AttributeError:
            app.logger.debug("opening database '{}'...".format(self.dbfile))
            conn = sqlite3.connect(self.dbfile)
            app.logger.debug("database '{}' opened".format(self.dbfile))
            self._connection = conn
        return self._connection

    @property
    def tablecursor(self):
        try:
            return self(
                "SELECT * FROM {} "
                "ORDER BY '{}' "
                "LIMIT {}".format(
                    DATA_TABLE,
                    config("UPLOAD_TIME_COL"),
                    config("MAX_LIMIT_OF_ROWS"),
                )
            )
        except sqlite3.OperationalError:
            self.create_table(
                name=DATA_TABLE, fields=MINIMAL_DATA_TABLE_FIELDS
            )
            return self.tablecursor

    @property
    def count(self):
        """
        The total number of data record rows
        """
        self.tablecursor  # make sure table exists
        c = self(
            "select count({}) from {};".format(
                config("UPLOAD_TIME_COL"), config("DATA_TABLE_NAME")
            )
        )
        return c.fetchone()[0]

    @property
    def header(self):
        try:
            return self._header
        except AttributeError:
            self._header = header_from_cursor(self.tablecursor)
        return self._header

    def save_records(self, records):
        rowcount = 0
        for vals in itertools.zip_longest(*records.values()):
            recordrow = {k.lower(): v for k, v in zip(records.keys(), vals)}
            recordrow.update(
                {
                    config(
                        "UPLOAD_TIME_COL"
                    ): datetime.datetime.utcnow().replace(
                        tzinfo=datetime.timezone.utc
                    )
                }
            )
            c = self.insert_into_table(
                table=DATA_TABLE,
                columns=recordrow.keys(),
                values=recordrow.values(),
            )
            rowcount += c.rowcount
        return rowcount

    def create_table(self, name, fields):
        f = ",".join(
            [
                "{} {}".format(sanitize(k), sanitize(v))
                for k, v in fields.items()
            ]
        )
        sql = "CREATE TABLE {name} ({fields})".format(
            name=sanitize(name), fields=f
        )
        c = self(sql)
        if hasattr(self, "_header"):
            del self._header
        return c

    def add_column(self, table, column, datatype):
        sql = "ALTER TABLE {table} ADD {column} {datatype}".format(
            table=sanitize(table),
            column=sanitize(column.lower()),
            datatype=sanitize(datatype),
        )
        c = self(sql)
        if hasattr(self, "_header"):
            del self._header
        return c

    def insert_into_table(self, columns, values, table=DATA_TABLE):
        columns = [sanitize(col.lower()) for col in columns]
        values = list(values)
        # add new columns
        new_columns = set(columns) - set(self.header)
        for new_column in new_columns:
            datatype = DATATYPES.get(type(values[columns.index(new_column)]))
            self.add_column(
                table=sanitize(table),
                column=sanitize(new_column),
                datatype=sanitize(datatype),
            )
        sql = "INSERT INTO {table} ({columns}) VALUES ({params})".format(
            table=sanitize(table),
            columns=sqlsep(columns),
            params=",".join("?" for v in values),
        )
        return self(sql, values)

    def select_from_table(self, table=DATA_TABLE, columns="*", cond=""):
        sql = "SELECT {columns} FROM {table} {cond}".format(
            table=sanitize(table),
            columns=",".join(map(sanitize, columns)),
            cond=cond,
        )
        cursor = self(sql)
        return header_from_cursor(cursor), cursor

    def select_from_table_with_conditions(
        self,
        columnsList="*",
        sql_condition="",
        orderByExpression="",
        parameter=None,
        tableData=DATA_TABLE,
    ):
        sql = (
            "SELECT {columns} FROM {table} " "{condition} {order} {limit}"
        ).format(
            columns=",".join(columnsList),  # safe Liste aus den `args`
            table=sanitize(tableData),  # Tabelle ist fest konfiguriert
            condition=sql_condition,
            order=orderByExpression,
            limit="LIMIT :limitValue",
        )
        cursor = self(sql, parameter)
        return cursor
        # return header_from_cursor(cursor), cursor

    def __call__(self, cmd, parameter=None):
        if parameter is None:
            with self.connection as conn:
                app.logger.debug("Executing >>>{}<<<".format(cmd))
                return conn.execute(cmd)
        else:
            with self.connection as conn:
                app.logger.debug(
                    "Executing >>>{}<<< with parameters {}".format(
                        cmd, parameter
                    )
                )
                return conn.execute(cmd, parameter)

    def __del__(self):
        if hasattr(self, "_connection"):
            app.logger.debug("closing database connection...")
            try:
                self.connection.close()
            except sqlite3.ProgrammingError as e:
                pass
            app.logger.debug("database connection closed.")
            del self._connection
