from .db import get_database, File
from .filesystem import (
    DEFAULT_DATA_DIR,
    create_dir,
    sha256,
    load_token,
)
from entsoe import EntsoePandasClient
from peewee import DoesNotExist
import os
import pandas as pd


class CachingDataClient:
    def __init__(self, location=None):
        USER_PATH = os.environ.get('BENTSO_DATA_DIR')
        self.dir = location or USER_PATH or DEFAULT_DATA_DIR
        create_dir(self.dir)
        get_database(self.dir)
        self.data_dir = os.path.join(self.dir, "data")
        create_dir(self.data_dir)
        print("Using data directory {}".format(self.dir))
        self.client = EntsoePandasClient(api_key=load_token())

    def get_trade(self, from_country, to_country, year):
        country_field = "{}-{}".format(from_country, to_country)
        return self._cached_query(
            (from_country, to_country,),
            year,
            'trade',
            country_field,
            self.client.query_crossborder_flows,
        )

    def get_consumption(self, country, year):
        return self._cached_query(
            (country,),
            year,
            'load',
            country,
            self.client.query_load,
        )

    def get_generation(self, country, year):
        return self._cached_query(
            (country,),
            year,
            'generation',
            country,
            self.client.query_generation,
        )

    def get_capacity(self, country, year):
        return self._cached_query(
            (country,),
            year,
            'capacity',
            country,
            self.client.query_installed_generation_capacity,
        )

    def get_hydro_charging(self, country, year):
        pass

    def _cached_query(self, args, year, kind_label, country_label, method):
        year = int(year)
        start, end = self._get_start_end(year)
        try:
            obj = File.select().where(File.kind==kind_label,
                                      File.country==country_label,
                                      File.year==year).get()
            return self._load_df(obj)
        except DoesNotExist:
            print("Querying ENTSO-E API. Please be patient...")
            start, end = self._get_start_end(year)
            df = method(*args, start=start, end=end)
            hash, name = self._store_df(
                df,
                "{}-{}-{}.pickle".format(kind_label, country_label, year)
            )
            File.create(
                filename=name,
                country=country_label,
                year=year,
                sha256=hash,
                kind=kind_label,
            )
            return df

    def _get_start_end(self, year):
        return (
            pd.Timestamp(year=year, month=1, day=1, hour=0, tz='Europe/Brussels'),
            pd.Timestamp(year=year + 1, month=1, day=1, hour=0, tz='Europe/Brussels'),
        )

    def _store_df(self, df, name):
        filepath = os.path.join(self.data_dir, name)
        df.to_pickle(filepath)
        return sha256(filepath), name

    def _load_df(self, obj):
        filepath = os.path.join(self.data_dir, obj.filename)
        if sha256(filepath) != obj.sha256:
            raise OSError("Corrupted cache file: {}".format(obj.filename))
        return pd.read_pickle(filepath)
