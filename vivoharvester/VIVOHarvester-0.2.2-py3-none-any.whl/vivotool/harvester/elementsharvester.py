import argparse
import collections
import logging
import lxml.etree as etree
import requests
import os
import xmltodict
import yaml

from logging.config import fileConfig

def elements_request(elementsurl, headers, *category):

    response = requests.get(elementsurl, headers=headers)

    if category and category[0] == "photo":
        return response
    else:
        result = etree.fromstring(response.text.encode('utf-8'))
        return etree.tostring(result, pretty_print=True)


def get_next_URL(content):

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


def save_photo_file(content, filename):
    file = open(filename, "w")
    for block in content.iter_content(1024):
        file.write(block)
    file.close()


def save_xml_file(content, filename):
    file = open(filename, "w")
    file.write(content)
    file.close()


def harvest_elements_xml(elements_endpoint, headers, query_type, params, filename):

    query_url = createElementsQueryURL(elements_endpoint, query_type, params)

    if query_type == "photo":
        response = elements_request(query_url, headers, "photo")
        save_photo_file(response, filename + "fullImages/" + params + ".jpeg")
        save_photo_file(response, filename + "thumbnails/" + params + ".jpeg")
    elif query_type == "users" or query_type == "publications":
        response = elements_request(query_url, headers)
        save_xml_file(response, filename)
        nexturl = get_next_URL(response)
        num = 1
        while len(nexturl) > 0:
            next_response = elements_request(nexturl, headers)
            next_filename = filename.replace(".xml", str(num) + ".xml")
            save_xml_file(next_response, next_filename)
            num += 1
            nexturl = get_next_URL(next_response)
    else:
        response = elements_request(query_url, headers)
        save_xml_file(response, filename)


def createElementsQueryURL(elements_endpoint, query_type, params):

    query_url = elements_endpoint

    if query_type == "user":
        query_url += "users/" + params
    elif query_type == "users":
        query_url += "users" + "?detail=full&per-page=" + str(params)
    elif query_type == "publications":
        query_url += "users/" + params + "/publications"
    elif query_type == "publication":
        query_url += "publications/" + params
    elif query_type == "relationship":
        query_url += "relationships/" + params
    elif query_type == "pubrelationships":
        query_url += "publications/" + params + "/relationships"
    elif query_type == "photo":
        query_url += "users/" + params + "/photo"
    else:
        raise ValueError('Invalidated input')

    return query_url


parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type=str, required=True)
args = parser.parse_args()

config = yaml.safe_load(open(args.file))
elements_endpoint = config['elements']['url']
authorization = config['elements']['authorization']
xml_folder = config['folders']['upload']
image_folder = config['folders']['photo']

# logger initialization
# TODO use config file
fileConfig('logging_config.ini')
logger = logging.getLogger()
logger.debug('Logger initialized')

headers = {}
headers["Authorization"] = "Basic " + authorization

# Harvest all users
logger.debug('Harvesting: Elements all users')

all_user_folder = xml_folder + "xml/temp/"

xmlfilename = xml_folder + "xml/temp/alluser.xml"
harvest_elements_xml(elements_endpoint, headers, "users", 25, xmlfilename)

# Process individual user
logger.debug('Harvesting: Elements individual user')

all_xml_files = list(filter(lambda x: x.endswith('.xml'), os.listdir(all_user_folder)))

total_public = 0
total_academic = 0
total_current_staff = 0

for xmlfile in all_xml_files:
    with open(all_user_folder + xmlfile) as fd:
        doc = xmltodict.parse(fd.read())

    entries = doc["feed"]["entry"]
    for e in entries:
        elementid = e["api:object"]["@id"]
        username = e["api:object"]["@username"]
        if "@proprietary-id" in e["api:object"]:
            uid = e["api:object"]["@proprietary-id"]
        else:
            uid = ""
        is_public = e["api:object"]["api:is-public"]
        is_academic = e["api:object"]["api:is-academic"]
        is_current_staff = e["api:object"]["api:is-current-staff"]

        if is_public == "true":
            total_public += 1

        if is_academic == "true":
            total_academic += 1

        if is_current_staff == "true":
            total_current_staff += 1

        if is_public == "true" and is_academic == "true" and is_current_staff == "true":

            logger.debug('Harvesting: Elements user - ' + elementid)

            filename = xml_folder + "xml/users/" + elementid + ".xml"
            harvest_elements_xml(elements_endpoint, headers, "user", elementid, filename)

            logger.debug('Harvesting: Elements user - ' + elementid + '\'s publications')

            xmlfilename = xml_folder + "xml/temp/" + elementid + "publications.xml"
            harvest_elements_xml(elements_endpoint, headers, "publications", elementid, xmlfilename)

            logger.debug('Harvesting: Elements user - ' + elementid + '\'s photo')

            harvest_elements_xml(elements_endpoint, headers, "photo", elementid, image_folder)

        if is_public == "false" and is_academic == "true" and is_current_staff == "true":

            pass
            # logger.debug('Harvesting: Elements user - ' + elementid)

            # filename = xml_folder + "xml/users/" + elementid + ".xml"
            # harvest_elements_xml(elements_endpoint, headers, "user", elementid, filename)

    os.remove(all_user_folder + xmlfile)

# Process all publications
logger.debug('Harvesting: Elements user - ' + elementid + '\'s individual publication')

pubfolder = xml_folder + "xml/temp/"
xmlfiles = list(filter(lambda x: x.endswith('.xml'), os.listdir(pubfolder)))

for xmlfile in xmlfiles:

    with open(pubfolder + xmlfile) as fd:
        doc = xmltodict.parse(fd.read())

    if "entry" in doc["feed"]:
        entries = doc["feed"]["entry"]
        logger.debug("Process file: " + xmlfile)

        if isinstance(entries, collections.OrderedDict):
            pubid = entries["api:relationship"]["api:related"]["@id"]

            logger.debug('Harvesting: Elements publication - ' + pubid)

            filename = xml_folder + "xml/publications/" + pubid + ".xml"
            harvest_elements_xml(elements_endpoint, headers, "publication", pubid, filename)

            logger.debug('Harvesting: Elements relationship from publicationid - ' + pubid)

            filename = xml_folder + "xml/temp/" + pubid + "relationships.xml"
            harvest_elements_xml(elements_endpoint, headers, "pubrelationships", pubid, filename)

        else:
            for e in entries:
                pubid = e["api:relationship"]["api:related"]["@id"]

                logger.debug('Harvesting: Elements publication - ' + pubid)

                filename = xml_folder + "xml/publications/" + pubid + ".xml"
                harvest_elements_xml(elements_endpoint, headers, "publication", pubid, filename)

                logger.debug('Harvesting: Elements relationship from publicationid - ' + pubid)

                filename = xml_folder + "xml/temp/" + pubid + "relationships.xml"
                harvest_elements_xml(elements_endpoint, headers, "pubrelationships", pubid, filename)

    os.remove(pubfolder + xmlfile)

# Process all relationships
logger.debug('Harvesting: Elements individual relationship')

rsfolder = xml_folder + "xml/temp/"
xmlfiles = list(filter(lambda x: x.endswith('.xml'), os.listdir(rsfolder)))

for xmlfile in xmlfiles:
    with open(rsfolder + xmlfile) as fd:
        doc = xmltodict.parse(fd.read())

    entries = doc["feed"]["entry"]
    if isinstance(entries, collections.OrderedDict):
        rsid = entries["api:relationship"]["@id"]

        logger.debug('Harvesting: Elements relationship - ' + rsid)

        filename = xml_folder + "xml/relations/" + rsid + ".xml"
        harvest_elements_xml(elements_endpoint, headers, "relationship", rsid, filename)

    else:
        for e in entries:
            rsid = e["api:relationship"]["@id"]

            logger.debug('Harvesting: Elements relationship - ' + rsid)

            filename = xml_folder + "xml/relations/" + rsid + ".xml"
            harvest_elements_xml(elements_endpoint, headers, "relationship", rsid, filename)

# TODO remove all files at once
    os.remove(rsfolder + xmlfile)

print "Total public: " + str(total_public)
print "Total academic: " + str(total_academic)
print "Total current staff: " + str(total_current_staff)
