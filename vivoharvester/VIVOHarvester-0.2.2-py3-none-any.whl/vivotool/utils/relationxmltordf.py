import collections
import xmltodict

from rdflib import Graph, Literal, BNode, RDF, RDFS, URIRef, Namespace
from rdflib.namespace import FOAF, DC

from vivotool.utils.models.user_model import User
from vivotool.utils.models.publication_model import Publication, Authorship

VIVO = Namespace('http://vivoweb.org/ontology/core#')


class RelationshipTranslator(object):

    def __add_bindings(self, graph):
        graph.bind('vivo', VIVO)

    def get_user_record(self, doc):
        user_doc = None
        for related in doc['entry']['api:relationship']['api:related']:
            if related['@category'] == 'user':
                user_doc = related
        return user_doc

    def get_user_email(self, user_doc):
        user_email = None
        records = []
        user_identifier_association = user_doc['api:object'][
            'api:user-identifier-associations']['api:user-identifier-association']

        if isinstance(user_identifier_association, collections.OrderedDict):
            records.append(user_identifier_association)
        else:
            records = user_identifier_association

        email_assoc = None
        for assoc in records:
            if assoc['@scheme'] == 'email-address':
                email_assoc = assoc
        if email_assoc is not None:
            user_email = email_assoc['#text']
        return user_email

    def get_user_id(self, user_doc):
        return user_doc['api:object']['@id']

    def get_username(self, user_doc):
        return user_doc['api:object']['@username']

    def get_publication_record(self, doc):
        pub_doc = None
        for related in doc['entry']['api:relationship']['api:related']:
            if related['@category'] == 'publication':
                pub_doc = related
        return pub_doc

    def get_publication_id(self, pub_doc):
        return pub_doc['api:object']['@id']

    def get_authorship_id(self, doc):
        return doc['entry']['api:relationship']['@id']

    def parse(self, input_file, target_dir=""):
        with open(input_file) as fd:
            doc = xmltodict.parse(fd.read())
            feed = doc['feed']

        vivo_user = User()
        user_record = self.get_user_record(feed)
        if user_record is not None:
            vivo_user.user_id = self.get_user_id(user_record)
            vivo_user.username = self.get_username(user_record)
            vivo_user.email = self.get_user_email(user_record)

        vivo_publication = Publication()
        publication_record = self.get_publication_record(feed)

        if publication_record and user_record:
            vivo_publication.id = self.get_publication_id(publication_record)

            vivo_authorship = Authorship(vivo_user, vivo_publication)
            vivo_authorship.id = self.get_authorship_id(feed)

            g = Graph()
            self.__add_bindings(g)
            vivo_authorship.add_to_graph(g)
            g.serialize(target_dir + vivo_authorship.id + ".rdf", format='nt')
