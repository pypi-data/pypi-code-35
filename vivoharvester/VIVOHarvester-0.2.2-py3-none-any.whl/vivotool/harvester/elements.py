import argparse
import collections
import logging
import lxml.etree as etree
import pytz
import requests
import os
import xmltodict
import yaml

from datetime import datetime, timedelta
from vivotool.utils.file_utils import Utils
from shutil import copyfile


class Elements(object):
    """docstring for ClassName"""

    def elements_request(self, elementsurl, headers, *category):

        try:
            response = requests.get(elementsurl, headers=headers)

        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something else is wrong", err)

        if category and category[0] == "photo":
            return response
        else:
            result = etree.fromstring(response.text.encode('utf-8'))
            return etree.tostring(result, pretty_print=True)

    def get_next_URL(self, content):

        if not content:
            return ""

        result_dict = xmltodict.parse(content)

        if "api:pagination" in result_dict["feed"]:
            pagination = result_dict["feed"]["api:pagination"]["api:page"]
            hasNext = False

            for p in pagination:
                if isinstance(p, collections.OrderedDict):
                    hasNext = True
                else:
                    hasNext = False

            if hasNext:
                nexturl = pagination[1]["@href"]
            else:
                nexturl = ""

        else:
            nexturl = ""

        return nexturl

    def harvest_elements_xml(
            self,
            elements_endpoint,
            headers,
            query_type,
            params,
            filename,
            *day):

        file_utils = Utils()

        if day and day[0] > 0:
            harvest_time = self.last_modified_date(day[0])
            query_url = self.createElementsQueryURL(
                elements_endpoint, query_type, params, harvest_time)
        else:
            query_url = self.createElementsQueryURL(
                elements_endpoint, query_type, params)

        if query_type == "photo":
            response = self.elements_request(query_url, headers, "photo")
            fullImages = filename + "fullImages/" + params + ".jpeg"
            thumbnails = filename + "thumbnails/" + params + ".jpeg"
            if response.status_code == 200:
                file_utils.save_photo_file(
                    response, fullImages)
                file_utils.save_photo_file(
                    response, thumbnails)
            else:
                stubphoto = filename + "thumbnails/userphoto.jpeg"
                copyfile(stubphoto, fullImages)
                copyfile(stubphoto, thumbnails)

        elif query_type == "users" or query_type == "publications" or query_type == "pubrelationships":
            response = self.elements_request(query_url, headers)
            file_utils.save_xml_file(response, filename)
            nexturl = self.get_next_URL(response)
            num = 1
            while len(nexturl) > 0:
                next_response = self.elements_request(nexturl, headers)
                next_filename = filename.replace(".xml", str(num) + ".xml")
                file_utils.save_xml_file(next_response, next_filename)
                num += 1
                nexturl = self.get_next_URL(next_response)
        else:
            response = self.elements_request(query_url, headers)
            file_utils.save_xml_file(response, filename)

    def createElementsQueryURL(
            self,
            elements_endpoint,
            query_type,
            params,
            *day):

        query_url = elements_endpoint

        if query_type == "user":
            query_url += "users/" + str(params)
        elif query_type == "users" and day:
            query_url += "users" + "?detail=full&per-page=" + \
                str(params) + "&modified-since=" + day[0]
        elif query_type == "users":
            query_url += "users" + "?detail=full&per-page=" + str(params)
        elif query_type == "publications" and day:
            query_url += "users/" + str(params) + \
                "/publications?detail=full&per-page=25&modified-since=" + day[0]
        elif query_type == "publications":
            query_url += "users/" + str(params) + \
                "/publications?detail=full&per-page=25"
        # elif query_type == "publicationbyday" and day:
        #     query_url += "publications" + "?detail=full&per-page=25" + \
        #         "&modified-since=" + day[0]
        elif query_type == "publication":
            query_url += "publications/" + str(params)
        elif query_type == "relationship":
            query_url += "relationships/" + str(params)
        elif query_type == "pubrelationships" and day:
            query_url += "publications/" + str(params) + \
                "/relationships?detail=full&per-page=25&modified-since=" + day[0]
        elif query_type == "pubrelationships":
            query_url += "publications/" + str(params) + \
                "/relationships?detail=full&per-page=25"
        elif query_type == "photo":
            query_url += "users/" + str(params) + "/photo"
        else:
            raise ValueError('Invalidated input')

        return query_url

    def last_modified_date(self, day):

        try:
            val = int(day)
        except ValueError:
            raise

        if day <= 0:
            logging.error("day should be a positive number")
            return ""

        sinceday = datetime.now() - timedelta(days=day)

        calculate_date = datetime(
            sinceday.year,
            sinceday.month,
            sinceday.day,
            sinceday.hour,
            sinceday.minute,
            sinceday.second,
            tzinfo=pytz.utc)

        return str(calculate_date.isoformat()).replace('+00:00', 'Z')
