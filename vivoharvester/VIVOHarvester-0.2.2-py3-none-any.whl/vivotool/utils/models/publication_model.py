from rdflib import BNode, Namespace, Literal, URIRef, RDF, RDFS, XSD
from datetime import datetime
import pytz
import re

COLLAB_VT = Namespace("http://collab.vt.edu/vivo/individual/")
BIBO = Namespace("http://purl.org/ontology/bibo/")
VCARD = Namespace('http://www.w3.org/2006/vcard/ns#')
VIVO = Namespace('http://vivoweb.org/ontology/core#')
OBO = Namespace('http://purl.obolibrary.org/obo/')
SKOS = Namespace('http://www.w3.org/2008/05/skos#')


class Publication:
    def __init__(self):
        self.id = ''
        self.is_public = False
        self.is_publication = True
        self.types = list()
        self.title = None
        self.abstract = None
        self.issue = None
        self.handle = None
        self.doi = None
        self.pm_id = None
        self.page_start = None
        self.page_end = None
        self.volume = None
        self.keywords = list()
        self.subject_areas = list()
        self.status = None
        self.publication_date = None
        self.journal = None
        self.webpages_publisher = None
        self.authorships = list()

    def __add_bindings(self, graph):
        graph.bind('bibo', BIBO)
        graph.bind('vcard', VCARD)
        graph.bind('vivo', VIVO)
        graph.bind('obo', OBO)
        graph.bind('skos', SKOS)

    def add_to_graph(self, graph):
        self.__add_bindings(graph)

        this = COLLAB_VT['publication' + self.id]
        # types
        for pub_type in self.types:
            if pub_type in [
                'AcademicArticle',
                'Book',
                'Chapter',
                'Journal',
                'Patent',
                'Report',
                    'Thesis']:
                graph.add((this, RDF.type, BIBO[pub_type]))
            elif pub_type == 'Software':
                graph.add((this, RDF.type, OBO['ERO_0000071']))
            else:
                graph.add((this, RDF.type, VIVO[pub_type]))
        graph.add((this, RDFS.label, Literal(self.title)))
        if self.abstract:
            graph.add((this, BIBO.abstract, Literal(self.abstract)))
        if self.issue:
            graph.add((this, BIBO.issue, Literal(self.issue)))
        if self.doi:
            graph.add((this, BIBO.doi, Literal(self.doi)))
        if self.pm_id:
            graph.add((this, BIBO.pmid, Literal(self.pm_id)))
        if self.handle:
            graph.add((this, BIBO.handle, Literal(self.handle)))
        if self.page_start:
            graph.add((this, BIBO.pageStart, Literal(self.page_start)))
        if self.page_start:
            graph.add((this, BIBO.pageEnd, Literal(self.page_end)))
        if self.volume:
            graph.add((this, BIBO.volume, Literal(self.volume)))

        # keywords
        for k in self.keywords:
            graph.add((this, VIVO.freetextKeyword, Literal(k)))

        # subject areas
        for sub_area in self.subject_areas:
            sub_area.uri = COLLAB_VT[sub_area.name()]
            sub_area.add_to_graph(graph, this)
            graph.add((this, VIVO.hasSubjectArea, sub_area.uri))

        # publication date
        if self.publication_date:
            publication_date = self.publication_date
            publication_date.uri = URIRef(this + '-publicationDate')
            publication_date.add_to_graph(graph)
            graph.add((this, VIVO.dateTimeValue, publication_date.uri))

        # journal
        if self.journal:
            journal = self.journal
            j_label = re.sub(r'["<>#%\{\}\|\\\^~\[\]`]', '', journal.label)
            journal.uri = COLLAB_VT['journal-' +
                                    j_label.lower().replace(' ', '-')]
            journal.add_to_graph(graph, this)
            graph.add((this, VIVO.hasPublicationVenue, journal.uri))

        # webpages and webpages publisher
        if self.webpages_publisher:
            webpages_publisher = self.webpages_publisher
            webpages_publisher.add_to_graph(graph, this)

        # published or not status
        if self.status:
            graph.add(
                (this, BIBO.status, BIBO[self.status.lower().replace(' ', '-')]))

        # authorships
        for authorship in self.authorships:
            authorship.add_to_graph(graph)


class PublicationDate:
    def __init__(self, id=None, month=1, day=1):
        self.id = id
        self.time_precision = None
        self.year = None
        self.month = month
        self.day = day
        self.type = None

    @staticmethod
    def format_datetime(yyyy, mm, dd):
        d = datetime(yyyy, mm, dd, tzinfo=pytz.utc)
        return str(d.isoformat()).replace('+00:00', 'Z')

    def add_to_graph(self, graph):
        this = self.uri
        graph.add((this, VIVO.dateTimePrecision, VIVO[self.time_precision]))
        if self.year:
            graph.add(
                (this, VIVO.dateTime, Literal(
                    PublicationDate.format_datetime(
                        self.year, self.month, self.day))))
        graph.add((this, RDF.type, VIVO.DateTimeValue))


class Journal:
    def __init__(self, type='Journal'):
        self.label = None
        self.type = type
        self.issn = None
        self.eissn = None
        self.subject_areas = list()

    def add_to_graph(self, graph, venue_for):
        this = self.uri
        graph.add((this, RDFS.label, Literal(self.label)))
        graph.add((this, RDF.type, BIBO[self.type]))
        graph.add((this, VIVO.publicationVenueFor, venue_for))
        if self.issn:
            graph.add((this, BIBO.issn, Literal(self.issn)))
        if self.eissn:
            graph.add((this, BIBO.eissn, Literal(self.eissn)))
        # subject areas
        for sub_area in self.subject_areas:
            sub_area.uri = COLLAB_VT[sub_area.name()]
            sub_area.add_to_graph(graph, this)
            graph.add((this, VIVO.hasSubjectArea, sub_area.uri))


class WebpagesPublisher:
    def __init__(self, type="publisher"):
        self.type = type
        self.label = None
        self.url = None

    def add_to_graph(self, graph, webpages_for):
        webpages_uri = URIRef(webpages_for + '-webpages')
        this = URIRef(webpages_uri + '-' + self.type)
        graph.add((webpages_uri, RDF.type, VCARD.Kind))
        graph.add((webpages_uri, OBO.ARG_2000029, webpages_for))
        graph.add((webpages_uri, VCARD.hasURL, this))
        graph.add((webpages_for, OBO.ARG_2000028, webpages_uri))
        graph.add((this, RDF.type, VCARD.URL))
        graph.add((this, RDFS.label, Literal(self.label)))
        graph.add((this, VCARD.url, Literal(self.url)))


class Authorship:
    def __init__(self, user=None, publication=None, rank=None):
        self.user = user
        self.publication = publication
        self.rank = rank
        self.id = id

    def add_to_graph(self, graph):
        if self.user.user_id:
            this = COLLAB_VT['authorship' +
                             self.publication.id + '-' + self.user.user_id]
            self.user.uri = COLLAB_VT[self.user.username]
        elif self.user.last_name:
            with_initial = self.user.initial is not ''
            this = COLLAB_VT['authorship' + self.publication.id +
                             self.user.name_in_uri().decode('utf-8')]
            self.user.classification = 'NonFacultyAcademic'
            self.user.uri = COLLAB_VT['person' +
                                      self.user.name_in_uri().decode('utf-8')]
            self.user.add_to_graph(graph)
        else:
            return

        self.publication.uri = COLLAB_VT['publication' + self.publication.id]
        # Person block
        graph.add((self.user.uri, VIVO.relatedBy, this))
        # Publication block
        graph.add((self.publication.uri, VIVO.relatedBy, this))
        # Relationship block
        graph.add((this, VIVO.relates, self.publication.uri))
        graph.add((this, VIVO.relates, self.user.uri))
        graph.add((this, RDF.type, VIVO['Authorship']))

        if self.rank:
            graph.add((this, VIVO.rank, Literal(self.rank, datatype=XSD.int)))


class SubjectArea:
    def __init__(self):
        self.label = None
        self.scheme = None

    def name(self):
        return 'vocab-' + self.scheme + '-' + \
            self.label.lower().replace(',', '').replace(' ', '-')

    def add_to_graph(self, graph, subject_area_of):
        this = self.uri
        graph.add((this, RDF.type, SKOS.Concept))
        graph.add((this, RDFS.label, Literal(self.label)))
        if self.scheme == 'mesh':
            graph.add(
                (this,
                 RDFS.isDefinedBy,
                 URIRef("http://www.nlm.nih.gov/mesh")))
        elif self.scheme == 'science-metrix':
            graph.add((this, RDFS.isDefinedBy, URIRef(
                "http://www.science-metrix.com/")))
        elif self.scheme == 'for':
            graph.add((this, RDFS.isDefinedBy, URIRef(
                "http://www.arc.gov.au/era/for")))
        graph.add((this, VIVO.subjectAreaOf, subject_area_of))
