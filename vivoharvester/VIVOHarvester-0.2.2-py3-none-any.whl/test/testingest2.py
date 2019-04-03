import logging
import xmltodict
import yaml
import collections

from logging.config import fileConfig
from vivotool.harvester.elements import Elements
from vivotool.vivo.vivo import VIVO
from vivotool.utils.file_utils import Utils
from vivotool.utils.photo import Photo
from vivotool.utils.publicationxmltordf import PublicationXml2Rdf
from vivotool.utils.relationxmltordf import RelationshipTranslator
from vivotool.utils.userxmltordf import UserElementXml2Rdf
from vivotool.harvester.elements import Elements
from vivotool.vivo.vivo import VIVO
import rdflib
from rdflib import Graph


config = yaml.safe_load(open("local.yml"))
elements_endpoint = config['elements']['url']
authorization = config['elements']['authorization']
xml_folder = config['folders']['upload']
image_folder = config['folders']['photo']
rdfurl = config['folders']['localurl']
logging_config = config['logging']['file']
vivo_endpoint = config['vivo']['url']

vivousername = config['vivo']['username']
vivopassword = config['vivo']['password']

headers = {
    'Accept': "text/turtle",
}

data = {
    'email': vivousername,
    'password': vivopassword
}

vivo_endpoint = vivo_endpoint + '/api/sparqlUpdate'
# print vivo_endpoint
# print rdfurl

vivo = VIVO()

rdf_file = "users/3924.rdf"

# response = vivo.request_vivo(
#     rdfurl, rdf_file,
#     vivo_endpoint,
#     headers,
#     data)

# print(response.text)

utils = Utils()

# rdfcontent = utils.read_file("6830.rdf")

# print rdfcontent

g = Graph()
g.parse("6830.rdf", format="xml")

s = g.serialize(format='nt')
# g.serialize("test.nt", format="nt")

# print (s)

rdfcontent = s

response = vivo.insert_vivo(
    rdfcontent,
    vivo_endpoint,
    headers,
    data)

print(response.text)
