import csv
import gzip
import logging
import os

import requests

from productfeeds.api import AbstractImporterAPI
from productfeeds.models import Product

DEFAULT_ATTRIBUTES = "aw_deep_link,product_name,aw_product_id,merchant_product_id,merchant_image_url,description,merchant_category,search_price,store_price,aw_image_url,merchant_name,merchant_id,category_name,category_id,currency,delivery_cost,merchant_deep_link,language,last_updated,display_price,data_feed_id,brand_name,merchant_thumb_url,large_image,alternate_image,aw_thumb_url,alternate_image_two,alternate_image_three,alternate_image_four"
URL_PATTERN = "https://productdata.awin.com/datafeed/download/apikey/{api_key}/language/{language_code}/fid/{feed_id}" \
              "/columns/{attributes}/format/csv/delimiter/%3B/excel/1/compression/gzip/adultcontent/1/"

logger = logging.getLogger(__name__)


class AwinAPI(AbstractImporterAPI):
    def __init__(self, api_key=None, feeds=None, language_code="pl", articlecode_prefix='awin_', *args, **kwargs):
        super(AwinAPI, self).__init__(*args, articlecode_prefix=articlecode_prefix, **kwargs)
        self.api_key = api_key
        self.language_code = language_code
        self.prefix = articlecode_prefix
        self.feeds = feeds

    def _download_and_prepare_csv_for_reading(self, feed_id):
        url = URL_PATTERN.format(
            api_key=self.api_key, language_code=self.language_code, feed_id=feed_id, attributes=DEFAULT_ATTRIBUTES,
        )
        r = requests.get(url, allow_redirects=True)
        compressed_feed_file_path = os.path.join(self.tmp_dir, 'awin-feed.csv.gz')
        decompressed_feedfile_path = compressed_feed_file_path[:-3]
        with open(compressed_feed_file_path, 'wb') as f:
            f.write(r.content)
        with open(decompressed_feedfile_path, "wb") as fw:
            with gzip.open(compressed_feed_file_path, 'rb') as f:
                fw.write(f.read())
        os.unlink(compressed_feed_file_path)
        return decompressed_feedfile_path

    def _convert_row_to_product(self, feed_id, row, columns_map):
        product = {columns_map[map_index]: column for map_index, column in enumerate(row)}
        p = Product()
        articlecode = self._build_articlecode("{}_{}".format(feed_id, product['merchant_product_id']))
        p.product_data['articlecode'] = articlecode
        p.product_data['client'] = product['merchant_name']
        p.product_data['title'] = product['product_name']
        p.product_data['brand'] = product['brand_name']
        p.product_data['category'] = product['merchant_category']
        if not p.product_data['category']:
            p.product_data['category'] = p.product_data['client']

        p.product_data['description'] = product['description']
        p.product_data['producturl'] = product['\xef\xbb\xbfaw_deep_link']
        p.product_data['thumburl'] = product['aw_image_url']
        p.product_data['imageurl'] = product['merchant_image_url']
        p.product_data['price'] = product['display_price'].replace('PLN', '')
        return p

    def import_products(self):
        rs = {'status': 1}
        imported = 0
        feeds_count = len(self.feeds)
        for feed in self.feeds:
            total_imported_products = 0
            logger.info('Reading feed %s', feed)

            decompressed_feed_file_path = self._download_and_prepare_csv_for_reading(feed)

            with open(decompressed_feed_file_path, 'rb') as csvfile:
                csv_rows = csv.reader(csvfile, delimiter=';', quotechar='"')
                columns_map = {}
                first_row = next(csv_rows)
                for i, column in enumerate(first_row):
                    columns_map[i] = column
                for row in csv_rows:
                    p = self._convert_row_to_product(feed, row, columns_map)

                    self._save_product(p)

                    total_imported_products += 1

            os.unlink(decompressed_feed_file_path)

            imported += 1
            logger.info("Imported %s products", total_imported_products)
        rs['success_percent'] = 100 * imported / feeds_count

        return rs
