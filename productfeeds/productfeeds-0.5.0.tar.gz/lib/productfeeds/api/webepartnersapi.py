# -*- coding: utf-8 -*-
import requests
import logging
import json
import time
import re
import xml.etree.ElementTree as ET
import unicodedata
import random

from . import AbstractImporterAPI
from productfeeds.models import Product

logger = logging.getLogger(__name__)

PRODUCT_URL_TEMPLATE = 'http://api.webepartners.pl/wydawca/XML?programid={program_id}&page=1&pageSize={page_size}'
PROGRAMS_URL = 'http://api.webepartners.pl/wydawca/Programs'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 '
                  'Safari/537.36'}


class WebepartnersAPI(AbstractImporterAPI):

    def __init__(self, login=None, password=None, articlecode_prefix='web_', page_size=20000, *args, **kwargs):
        super(WebepartnersAPI, self).__init__(*args, articlecode_prefix=articlecode_prefix, **kwargs)
        self.page_size = page_size
        self.login = login
        self.password = password

    def _read_programs(self):
        # get list of programs
        response = requests.get(PROGRAMS_URL, auth=(self.login, self.password), headers=HEADERS)

        if response.status_code != 200:
            logger.debug("REST API connection error: %s \n" % response.status_code)

        data = response.content

        data = json.loads(data)

        programs = []
        for row in data:
            # normalize
            row['ProgramName'] = unicodedata.normalize('NFKD', row['ProgramName']).encode('ascii',
                                                                                          'ignore').lower().replace('.',
                                                                                                                    '').strip()
            programs.append({'program_id': row['ProgramId'], 'program_name': row['ProgramName']})

        return programs

    def _read_products(self, program, products_limit):

        articlecodes_set = set([])
        logger.info("Processing feed for: %s (id %s)" % (program['program_name'].encode('utf8'), program['program_id']))
        url = PRODUCT_URL_TEMPLATE.format(program_id=program['program_id'], page_size=products_limit)
        try:
            response = requests.get(url, auth=(self.login, self.password), headers=HEADERS)
        except Exception as e:
            logger.warning(e)

            random_sleep = random.randint(30, 45)
            logger.info("\tprocessing error ... trying again in %s sec." % random_sleep)
            time.sleep(random_sleep)
            try:
                response = requests.get(url, auth=(self.login, self.password),
                                        headers=HEADERS)
            except:
                random_sleep = random.randint(60, 80)
                logger.info("\tprocessing error ... trying again in %s sec." % random_sleep)
                time.sleep(random_sleep)
                try:
                    response = requests.get(url, auth=(self.login, self.password),
                                            headers=HEADERS)
                except:
                    logger.warning(
                        "\t give up :( connection aborted by API provider. Import failed. Will try again at the end of this script")
                    return 0
        # parse XML
        xml_content = response.content
        xml_content = xml_content.replace('\\"', '"').replace('\\n', '')
        xml_content = xml_content.strip('"')
        try:
            products = ET.fromstring(xml_content)
        except:
            logger.info("\tno products found")
            return 1

        logger.info("\tfound products:%s" % len(products))

        if len(products) > 0:
            logger.info("\tImporting ...")

        for product in products:
            p = Product()
            # program_name
            p.product_data['client'] = program['program_name']

            # articlecode
            try:
                p.product_data['articlecode'] = '%s%s_%s' % (
                self.articlecode_prefix, product.find('awId').text.strip(), product.find('pId').text.strip())
            except:
                continue

            if p.product_data['articlecode'] in articlecodes_set:
                continue

            # title
            if not product.find('name').text:
                continue

            name = product.find('name').text.encode('utf8')
            name = name.replace(' -BOGATY WYBÓR! NAJNIŻSZE CENY! SPRAWDŹ NAS! (71) 397 49 99', '')
            name = name.replace(' _______ BŁYSKAWICZNA REALIZACJA ZAMÓWIENIA ________', '')
            name = re.sub(r'"?__.*', '', name)
            name = name.strip()
            p.product_data['title'] = name

            # categories
            try:
                fullcat = product.find('awCat').text.encode('utf8')
                categories = fullcat.split('/')
                p.product_data['category'] = categories[0]
                p.product_data['subcategory1'] = categories[1]
            except AttributeError:
                continue
            try:
                p.product_data['subcategory2'] = categories[2]
            except IndexError:
                pass

            # brand
            try:
                p.product_data['brand'] = product.find('brand').text.encode('utf8')
            except AttributeError:
                pass

            try:
                p.product_data['description'] = product.find('desc').text.encode('utf8')
            except AttributeError:
                pass

            # productUrl
            p.product_data['producturl'] = product.find('awLink').text

            # thumbUrl
            try:
                p.product_data['thumburl'] = product.find('awThumb').text
            except AttributeError:
                pass

            # imageUrl
            p.product_data['imageurl'] = product.find('awImage').text

            # deliveryTime
            try:
                p.product_data['delivery'] = product.find('deliveryTime').text.encode('utf8')
            except AttributeError:
                pass

            # price
            p.product_data['price'] = product.find('price').text
            # print type(p.product_data['price'])
            if float(p.product_data['price']) == 0:
                continue

            # remove whitespaces
            for key in p.product_data:
                try:
                    p.product_data[key] = p.product_data[key].strip()
                except:
                    pass

            articlecodes_set.add(p.product_data['articlecode'])
            self._save_product(p)

        return 1

    def import_products(self):

        rs = {}
        programs = self._read_programs()
        programs_count = len(programs)
        programs_imported = 0
        for program in programs:
            status = self._read_products(program, self.page_size)
            if status == 1:
                programs_imported += 1

        rs['status'] = 1
        rs['success_percent'] = 100 * programs_imported / programs_count
        return rs
