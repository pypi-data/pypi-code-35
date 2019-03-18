import requests
import logging
import json

from . import AbstractImporterAPI
from productfeeds.models import Product

logger = logging.getLogger(__name__)

PRODUCTS_URL = 'https://api.convertiser.com/publisher/products/v2/?key={}'
REQUEST_TIMEOUT = 120


class ConvertiserAPI(AbstractImporterAPI):

    def __init__(self, token=None, offers=None, website_key=None, articlecode_prefix='con_', page_size=20000, *args,
                 **kwargs):
        super(ConvertiserAPI, self).__init__(*args, articlecode_prefix=articlecode_prefix, **kwargs)
        self.page_size = page_size
        self.website_key = website_key
        self.offers = offers
        self.token = token

    def import_products(self):
        rs = {'status': 1}
        imported = 0
        offers_count = len(self.offers)
        for offer in self.offers:
            try:
                response = requests.post(
                    PRODUCTS_URL.format(self.website_key),
                    headers={'Authorization': 'Token {}'.format(self.token), 'Content-Type': 'application/json'},
                    data=json.dumps({
                        "filters": {"offer_id": {"lookup": "exact", "value": offer}},
                        "page": 1, "page_size": self.page_size
                    }),
                    timeout=REQUEST_TIMEOUT
                )
            except Exception as e:
                logger.error(e)
                continue

            results = response.json()
            logger.info('Returned {} products'.format(len(results['data'])))
            for product in results['data']:
                p = Product()
                p.product_data['client'] = product['offer']
                articlecode = self._build_articlecode("{}_{}".format(product['offer_id'], product['id']))
                p.product_data['articlecode'] = articlecode
                p.product_data['title'] = product['title'].encode('utf-8')
                p.product_data['brand'] = product['brand'].encode('utf-8')
                categories = product['product_type'].encode('utf-8').split('/')
                p.product_data['category'] = categories[0]
                try:
                    p.product_data['subcategory1'] = categories[1]
                except:
                    pass
                try:
                    p.product_data['subcategory2'] = categories[2]
                except:
                    pass
                p.product_data['description'] = product['description'].encode('utf-8')
                p.product_data['producturl'] = product['link']
                p.product_data['thumburl'] = product['images']['thumb_180']
                p.product_data['imageurl'] = product['images']['default']
                p.product_data['price'] = product['price'].replace('PLN ', '')
                self._save_product(p)

            imported += 1
        rs['success_percent'] = 100 * imported / offers_count

        return rs
