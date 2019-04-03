import logging
import xmltodict
import yaml
import collections

from logging.config import fileConfig
# from vivotool.harvester.elements import Elements
# from vivotool.vivo.vivo import VIVO

# from utils.file_utils import Utils
# from utils.transform import Photo
# from utils.userxmltordf import UserElementXml2Rdf
# from utils.publicationxmltordf import PublicationXml2Rdf
# from utils.relationxmltordf import RelationshipTranslator
# from harvester.elements import Elements

# config = yaml.safe_load(open("/Users/ylchen/temp/vivotest/local.yml"))
# elements_endpoint = config['elements']['url']
# authorization = config['elements']['authorization']
# xml_folder = config['folders']['upload']
# image_folder = config['folders']['photo']
# logging_config = config['logging']['file']
# vivo_endpoint = config['vivo']['url']

# vivousername = config['vivo']['username']
# vivopassword = config['vivo']['password']

# headers = {
#     'Accept': "text/turtle",
# }

# data = {
#     'email': vivousername,
#     'password': vivopassword
# }


pubid = "1223434"
privacy = "N"

querystring = "INSERT INTO publications (pid, public) VALUES (\"%s\", \"%s\");" % (
    pubid, privacy,)

print(querystring)

# print (elements_endpoint)

# vivo = VIVO()

# vivo_query_endpoint = vivo_endpoint + '/api/sparqlQuery'
# print(vivo_endpoint)

# # http://localhost:8080/vivo/individual?uri=http%3A%2F%2Fcollab.vt.edu%2Fvivo%2Findividual%2Fpublication1108416
# response = vivo.describe_vivo_object("http://collab.vt.edu/vivo/individual/publication1095281", vivo_query_endpoint, headers, data)
# print(response.status_code)
# print(response.text)


# print("##############################")

# vivo_update_endpoint = vivo_endpoint + '/api/sparqlUpdate'

# response = vivo.delete_vivo_object(response.text, vivo_update_endpoint, headers, data)

# print(response.status_code)

# print(response.text)

# TODO
# check_exist


# print(vivo_endpoint)

# # delete http://collab.vt.edu/vivo/individual/publication1108416
# #  publication594909

# # delete relationships http://collab.vt.edu/vivo/individual/authorship594909-3924
# response = vivo.delete_vivo_object(response.text, vivo_update_endpoint, headers, data)

# print(response.status_code)

# print(response.text)

# filename = "1328relationships.xml"

# with open(filename) as fd:
#     doc = xmltodict.parse(fd.read())


# recid = doc["feed"]["id"]
# pubid = recid.split("/")[-2]

# print (recid)
# print (pubid)

# if "entry" in doc["feed"]:
#     entries = doc["feed"]["entry"]

#     # print(entries)

#     if isinstance(entries, collections.OrderedDict):
#         rsid = entries["api:relationship"]["@id"]
#         rstype = entries["api:relationship"]["@type"]
#         # print (rsid)
#         # print(entries["link"])
#         for rec in entries["link"]:
#         	if "users" in rec["@href"]:
#         		print(rec["@href"].split("/")[-1])


# from utils.transform import Transform

# elements = Elements()

# print (elements.last_modified_date(1))


# print (elements.harvest_elements_xml("test","test","pubrelationships","test","test",1))
# # file_utils = Utils()

# filename = "test.xml"
