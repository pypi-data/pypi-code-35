#!/usr/bin/env python

# Copyright 2019 John T. Foster
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import psycopg2
import numpy as np
import pandas as pd

__version__ = "0.1.2"


if "BAZEAN_POSTGRES_USERNAME" in os.environ:
    bazean_postgres_username = os.environ["BAZEAN_POSTGRES_USERNAME"]
else:
    bazean_postgres_username = None

if "BAZEAN_POSTGRES_PASSWORD" in os.environ:
    bazean_postgres_password = os.environ["BAZEAN_POSTGRES_PASSWORD"]
else:
    bazean_postgres_password = None


class PyBD(object):

    """Class for querying Bazean database.
    
    Args:
    
        user (str): Bazean database username, defaults to use the environment variable `BAZEAN_POSTGRES_USERNAME` if assigned
        password (str): Bazean database password, defaults to use the environment variable `BAZEAN_POSTGRES_PASSWORD` if assigned
        subdomain (str): URL subdomain, default is "premium"
        schema (str): Postgres schema, default is "public"
    
    
    """

    def __init__(
        self,
        user=bazean_postgres_username,
        password=bazean_postgres_password,
        subdomain="premium",
        schema="public",
    ):

        url = "postgresql://{}.bazean.com:5432/db?ssl=true".format(subdomain)

        # Create connection to database
        self.__connection = psycopg2.connect(user=user, password=password, dsn=url)
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute("SET search_path TO {}".format(schema))

        self.__default_fetch_size = 50

    def __del__(self):
        """Destructor to close database connection."""

        self.__connection.close()
        self.__cursor.close()

    def __fetch(self, raw_sql_string, number_of_records_to_fetch=None):
        """Fetches records from database
        
        Args:
            raw_sql_string (str): SQL query string
            number_of_records_to_fetch (int or str): limits the length of returned records
            
        Returns:
            (list): A Python list with the records returned by the sql query.
        """

        self.__cursor.execute(raw_sql_string)

        if number_of_records_to_fetch is None:
            return list(
                map(list, self.__cursor.fetchmany(size=self.__default_fetch_size))
            )
        elif isinstance(number_of_records_to_fetch, int):
            return list(
                map(list, self.__cursor.fetchmany(size=number_of_records_to_fetch))
            )
        elif isinstance(number_of_records_to_fetch, str):
            if number_of_records_to_fetch == "all":
                return list(map(list, self.__cursor.fetchall()))

    def __build_query_string(self, table, columns, **kwargs):
        """Builds SQL query string from columns requested and table names

        Args:
            table (str): SQL table name
            columns (tuple of str): A tuple of column names to select
            **kwargs: Arbitrary number of keyword arguments of the form `key=value`. 
                      These would be expected to construct the `WHERE` portion of the SQL statement with a
                      logical `AND` operation.  For example:

                      ```python
                         db = PyBD()
                         db._PyBD__build_query_string('production_all', ('apis',), state='KS', api='15001016610000')
                      ```

                      Would result in the string:

                      ```sql
                        SELECT apis FROM production_all WHERE state='KS' AND api='15001016610000'
                      ```
        Returns:
            (str): The SQL query statement
        """

        if columns != "*" and len(columns) > 1:
            columns = ",".join(columns)
        else:
            columns, = columns

        query_string = "SELECT {} FROM {}".format(columns, table)

        if kwargs is not None:
            for count, items in enumerate(kwargs.items()):
                key, value = items
                if count == 0:
                    query_string += " WHERE {}='{}'".format(key, value)
                else:
                    query_string += " AND {}='{}'".format(key, value)

        return query_string

    def set_fetch_size(self, value):
        """Sets the fetch size for database query methods i.e. `get_` methods
        
        Args:
            value (int or `'all'`): fetch size, default is 50.
        """
        self.__default_fetch_size = value

    def get(self, table, columns, **kwargs):
        """General function to construct SQL query statement and retrieve columns of data

        Args:
            table (str): SQL table name
            columns (tuple of str): A tuple of column names to select
            **kwargs: Arbitrary number of keyword arguments of the form `key=value`. 
                      These would be expected to construct the `WHERE` portion of the SQL statement with a
                      logical `AND` operation.  For example::

                         db = PyBD()
                         db.get('production_all', ('apis',), 
                                state='KS', 
                                api='15001016610000')

                      and would result in the query string::

                         SELECT apis FROM production_all WHERE state='KS' AND api='15001016610000'

                      In this simple case, the function would return a list `[['15001016610000']]`.

        Returns:
            (list): Nested list of returned columns of data from the SQL query.
        """

        query_string = self.__build_query_string(table, columns, **kwargs)

        return self.__fetch(
            query_string, number_of_records_to_fetch=self.__default_fetch_size
        )

    def get_tickers_by_state(self, state):
        """Returns the stock tickers (actual or assigned) of companies that operate/own wells in a given state.

        Args:
            state (str): The two letter postal code of a state, i.e. "TX" or "NM"

        Returns:
            (list of str): A list containing the stock tickers.  Missing entries query entries with `None` are ommitted.

        """

        db_tickers = self.get(table="well_all", columns=("parent_ticker",), state=state)
        unique_tickers = np.unique(np.array(db_tickers, dtype=np.str))
        return unique_tickers[unique_tickers != "None"].tolist()

    def get_well_locations_by_ticker_and_state(self, ticker, state):
        """Returns the latitude, longitude and API number of wells

        Args:
            ticker (str): Company stock ticker, i.e. "XOM"
            state (str): The two letter postal code of a state, i.e. "TX" or "NM"

        Returns:
            (DataFrame): Pandas DataFrame

        """

        latitude, longitude, api = np.array(
            self.get(
                table="well_all",
                columns=("latitude_surface_hole", "longitude_surface_hole", "api"),
                parent_ticker=ticker,
                state=state,
            )
        ).T
        bool_array = latitude != None
        lat_clean = latitude[bool_array].astype(dtype=np.float)
        long_clean = longitude[bool_array].astype(dtype=np.float)
        api_clean = api[bool_array].astype(dtype=np.str)
        # Convert to pandas dataframe
        df = {
            "latitude_surface_hole": lat_clean,
            "longitude_surface_hole": long_clean,
            "api": api_clean,
        }
        return pd.DataFrame(data=df)

    def get_production_from_api(self, api):
        """Returns the total production histories for a given API number

        Args:
            api (str): API number for requested well production histories

        Returns:
            (DataFrame): Pandas DataFrame.

        """

        default_fetch_size = self.__default_fetch_size
        self.set_fetch_size("all")
        request = np.array(
            self.get(
                table="production_all",
                columns=(
                    "date",
                    "volume_oil_formation_bbls",
                    "volume_gas_formation_mcf",
                    "volume_water_formation_bbls",
                ),
                api=api,
            )
        ).T
        self.set_fetch_size(default_fetch_size)
        if request.size != 0:
            date, oil, gas, water = request
            # Convert to pandas dataframe
            df = {
                "volume_oil_formation_bbls": oil.astype("double"),
                "volume_gas_formation_mcf": gas.astype("double"),
                "volume_water_formation_bbls": water.astype("double"),
            }
            return pd.DataFrame(data=df, index=date.astype("datetime64"))
        else:
            return None
