# -*- coding: utf-8 -*-

"""Functions to load data from Worldbank API.

We use its bulkdownload utilities.

Source link: `WorldBank website`_

.. _WorldBank website: http://data.worldbank.org

"""

import os.path as osp

import requests
import pandas as pd

from urllib.parse import urlsplit
from concurrent.futures import ThreadPoolExecutor, as_completed

from . common import DataFactory


class WorldBankLoader(DataFactory):
    __doc__ = """T.B.D"""
    url = 'http://api.worldbank.org/v2/datacatalog?format=json'

    def load_metadata(self):
        def load_url(url, page=None):
            if page:
                url = url + '&page=' + str(page)
            res = requests.get(url)
            return res.json()

        def handle_data(data):
            for v in data['datacatalog']:
                d = {}
                for v_ in v['metatype']:
                    d[v_['id']] = v_['value']
                yield d

        first_page = self.url
        data = load_url(first_page)

        metadata = []

        for d in handle_data(data):
            metadata.append(d)

        pages = range(2, data['pages']+1)

        executor = ThreadPoolExecutor(max_workers=3)
        res = [executor.submit(load_url, self.url, page=p) for p in pages]

        for r in as_completed(res):
            for d in handle_data(r.result()):
                # print(d)
                metadata.append(d)

        metadata = pd.DataFrame.from_records(metadata)
        self.metadata = metadata
        return metadata

    def has_newer_source(self, dataset, date):
        if self.metadata is None:
            self.load_metadata()
        metadata = self.metadata
        lastrevisiondate = metadata.loc[
            metadata.acronym == dataset,
            'lastrevisiondate'].values[0]
        if pd.to_datetime(lastrevisiondate) > pd.to_datetime(date):
            return True
        else:
            return False

    def bulk_download(self, dataset, out_dir):
        if self.metadata is None:
            self.load_metadata()
        metadata = self.metadata
        s = metadata.loc[metadata.acronym == dataset, 'bulkdownload'].values[0]
        url = s.split(';')[1].split('=')[1]
        res = requests.get(url, stream=True)

        fs_path = osp.join(out_dir, osp.basename(urlsplit(url).path))

        with open(fs_path, 'wb') as f:
            for c in res.iter_content(chunk_size=1024):
                f.write(c)
            f.close()

        return out_dir
