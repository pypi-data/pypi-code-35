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

vivouploads = xml_folder
extension = '.xml'
userxmlpath = vivouploads + "xml/users/"
user_xml_files = file_utils.listfiles(userxmlpath, extension)
pubxmlpath = vivouploads + "xml/publications/"
pub_xml_files = file_utils.listfiles(pubxmlpath, extension)
rsxmlpath = vivouploads + "xml/relations/"
rs_xml_files = file_utils.listfiles(rsxmlpath, extension)
userrdfpath = vivouploads + "rdf/users/"
pubrdfpath = vivouploads + "rdf/publications/"
rsrdfpath = vivouploads + "rdf/relations/"
photordfpath = vivouploads + "rdf/photos/"

uex2rdf = UserElementXml2Rdf()
photo = Photo()

try:
    for xmlfile in user_xml_files:
        with open(userxmlpath + xmlfile) as fd:
            doc = xmltodict.parse(fd.read())

        userfilename = "rdf/users/" + xmlfile.replace(".xml", ".rdf")
        uex2rdf.convert(doc, vivouploads + userfilename)

        api_obj = doc['feed']['entry']['api:object']
        pid = api_obj['@username']
        eid = api_obj["@id"]
        public = api_obj["api:is-public"]

        if public == 'true':
            photofilename = "rdf/photos/" + eid + ".rdf"
            file_utils.save_xml_file(
                photo.create_user_photo_graph(
                    pid, eid), vivouploads + photofilename)

except IOError:
    logger.error('Error parsing file:' + xmlfile)

pub_xml_to_rdf = PublicationXml2Rdf()

try:
    for xmlfile in pub_xml_files:
        pub_xml_to_rdf.parse(
            pubxmlpath + xmlfile,
            pubrdfpath)

except IOError:
    logger.error('Error parsing file:' + xmlfile)

translator = RelationshipTranslator()

try:
    for xmlfile in rs_xml_files:
        translator.run(
            rsxmlpath +
            xmlfile,
            rsrdfpath)

except IOError:
    logger.error('Error parsing file:' + xmlfile)
