import unittest

import requests_mock

from productfeeds.api.convertiserapi import ConvertiserAPI
from productfeeds.api.webepartnersapi import WebepartnersAPI
from productfeeds.importer import build_importer_instance
from productfeeds.models import Product, ProductError


class DummyStorage(object):
    def __init__(self, settings=None):
        self.products = []
        self.article_codes = set()

    def save_product(self, p):
        self.products.append(p.to_dict())
        self.article_codes.add(p.get('articlecode'))


class TestImporter(unittest.TestCase):
    def test_get_importer(self):
        importer = build_importer_instance('webepartners', {})
        self.assertIsInstance(importer, WebepartnersAPI)
        importer = build_importer_instance('convertiser', {})
        self.assertIsInstance(importer, ConvertiserAPI)
        with self.assertRaises(Exception) as ex:
            build_importer_instance('undefined-API', {})

    def test_product_model(self):
        a = 'my_article_code'
        p = Product()
        p.set('articlecode', a)
        self.assertEquals(p.get('articlecode'), a)
        self.assertEquals(p.product_data['articlecode'], a)
        with self.assertRaises(ProductError):
            Product({'dict': 'without required field'})

    def test_convertiser(self):
        storage = DummyStorage()
        settings = {'token': '123', 'offers': [123], 'website_key': '321', 'articlecode_prefix': 'p_'}
        api = ConvertiserAPI(storage=storage, **settings)
        with requests_mock.mock() as m:
            url = 'https://api.convertiser.com/publisher/products/v2/?key={}'.format(settings['website_key'])
            m.post(
                url,
                text='{"count":100000,"pagination":{"previous_page":null,"page":0,"page_size":50,"next_page":1},'
                     '"data":[{"id":"123123123",'
                     '"title":"GOODRAM USB 2.0 32GB 20MB/s UMO2-0320O0R11","description":"Specyfikacja: Parametry '
                     'ogolne - Kolor: Pomaranczowy, Wymiary mm: 54 x 18 x 8,5 mm, Waga g: 7,5 g, Parametry '
                     'techniczne","price":"PLN 19.22","sale_price":null,"sale_price_effective_date":"",'
                     '"discount":0,"offer":"Offerer","offer_id":"999","brand":"GOODRAM","images":'
                     '{"thumb_43":"https://img.convertiser.com/cnGdhDIrNF_","default":"https://img.convertiser.com/hg"'
                     ',"thumb_180":"https://img.convertiser.com/bzfg-HKx5E1KBOWcdi1C"},'
                     '"image_link":"https://static.convertiser.com/media/product_images/23","additional_images":{},'
                     '"additional_image_link":null,"link":"https://converti.se/click/0569ea91-71526c8b-f4.html",'
                     '"mobile_link":"https://converti.se/click/0569ea91-71.html","direct_link":"https://www.sfdsd.pl",'
                     '"google_product_category":"Komputery/Przechowywanie danych/PenDrive","product_type":"Komputery",'
                     '"gtin":"","mpn":"","color":"","gender":"","age_group":"","material":"","pattern":"","size":"",'
                     '"size_system":"","item_group_id":"","multipack":null,"is_bundle":null,"adult":null,'
                     '"updated_at":"2019-02-09T05:15:26.154018+00:00","offer_display_url":"http://www.sdfsdf.pl/",'
                     '"is_cpc":false,"cpc_rate":"PLN 0.00"}]}'
            )
            rs = api.import_products()
        self.assertEquals({'status': 1, 'success_percent': 100}, rs)
        self.assertTrue('p_999_123123123' in storage.article_codes)
