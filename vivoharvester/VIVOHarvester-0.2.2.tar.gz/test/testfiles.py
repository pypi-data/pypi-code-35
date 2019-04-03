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

config = yaml.safe_load(open("/Users/ylchen/temp/vivotest/local.yml"))
elements_endpoint = config['elements']['url']
authorization = config['elements']['authorization']
xml_folder = config['folders']['upload']
image_folder = config['folders']['photo']
logging_config = config['logging']['file']
vivo_endpoint = config['vivo']['url']

vivousername = config['vivo']['username']
vivopassword = config['vivo']['password']

file_utils = Utils()

extension = ".xml"
rsfolder = xml_folder + "xml/temp/"
print(rsfolder)
xmlfiles = file_utils.listdeletefiles(rsfolder, "delete")

print(xmlfiles)
