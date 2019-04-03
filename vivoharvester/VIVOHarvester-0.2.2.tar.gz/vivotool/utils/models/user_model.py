#!/usr/bin/env python

"""
User Model

Modified + Inspired by:
  https://github.com/andreasf/pentabarf-rdf/
"""
import re
from rdflib import Graph, BNode, Namespace, Literal, URIRef, RDF, RDFS, URIRef, XSD
from rdflib.namespace import FOAF, DC, RDFS, RDF

COLLAB_VT = Namespace("http://collab.vt.edu/vivo/individual/")
VCARD = Namespace('http://www.w3.org/2006/vcard/ns#')
VIVO = Namespace('http://vivoweb.org/ontology/core#')
OBO = Namespace('http://purl.obolibrary.org/obo/')


class User:
    def __init__(
            self,
            title=None,
            first_name=None,
            last_name=None,
            username=None):
        self.title = title
        self.username = username
        self.user_id = None
        self.first_name = first_name
        self.last_name = last_name
        self.initial = None
        self.classification = 'FacultyMember'
        self.suffix = ''
        self.overview = ''
        self.email = ''
        self.email_is_public = False
        self.degrees = []
        self.institutions = []
        self.appointments = []
        self.vcard = VCard(self)
        self.is_academic = False
        self.is_current_staff = False
        self.is_public = False

    def id(self):
        return self.username

    def display_name(self):
        # TODO: need further check
        # if not self.first_name:
        #     return

        if self.last_name and self.first_name:
            return '{}, {}'.format(
                self.last_name.encode('utf-8'),
                self.first_name.encode('utf-8'))
        elif self.last_name and self.initial:
            return '{}, {}'.format(
                self.last_name.encode('utf-8'),
                self.initial.encode('utf-8'))
        elif self.last_name:
            return '{}'.format(self.last_name.encode('utf-8'))

    def name_in_uri(self):
        if self.last_name and self.initial:
            name = '-{}-{}'.format(self.last_name.encode('utf-8'),
                                   self.initial.encode('utf-8'))
        elif self.last_name:
            return '-{}'.format(self.last_name.encode('utf-8'))
        name = re.sub(r'["<>#%\{\}\|\\\^~\[\]`]', '', name)
        return name.lower().replace(' ', '-')

    def add_to_graph(self, graph):

        if self.classification == 'NonFacultyAcademic':
            user = self.uri
        else:
            if self.display_name() is None:
                return

            user = COLLAB_VT[self.id()]

            self.__add_bindings(graph)
            graph.add((user, VIVO.overview, Literal(self.overview)))

            for appointments in self.appointments:
                appointments.add_to_graph(graph, self)

            for degree in self.degrees:
                degree.add_to_graph(graph, self)

        graph.add((user, RDF.type, VIVO[self.classification]))
        graph.add(
            (user, RDFS.label, Literal(
                self.display_name().decode('utf-8'))))
        self.vcard.add_to_graph(graph)

    def __add_bindings(self, graph):
        graph.bind('vivo', VIVO)
        graph.bind('vcard', VCARD)
        graph.bind('obo', OBO)


class Institution:
    def __init__(self):
        self.label = None
        self.city = None
        self.country = None
        self.dept = None

    def add_to_graph(self, graph):
        institution = COLLAB_VT[self.id()]

        graph.add((institution, RDF.type, VIVO['University']))
        graph.add((institution, RDFS.label, Literal(self.label)))
        if self.dept:
            dept = COLLAB_VT[self.dept_id()]
            graph.add((institution, OBO.BFO_0000051, dept))
            graph.add((dept, OBO.BFO_0000050, institution))
            graph.add((dept, RDF.type, VIVO['AcademicDepartment']))
            graph.add((dept, RDFS.label, Literal(self.dept)))

    def id(self):
        return 'institution-{}'.format(self.label.lower().replace(' ', '-'))

    def dept_id(self):
        return 'dept-{}-{}'.format(self.dept.lower().replace(' ', '-'),
                                   self.label.lower().replace(' ', '-'))


class Degree:
    def __init__(self, username=None, type=None, label=None, field=''):
        self.username = username
        self.type = type
        self.label = label
        self.field = field
        self.institution = Institution()
        self.start_date = None
        self.end_date = None
        self.date_interval = None
        self.is_public = False

    def add_to_graph(self, graph, user_obj):
        degree = COLLAB_VT[self.degree_id()]
        degree_institution = COLLAB_VT[self.institution.id()]
        awarded_degree = COLLAB_VT[self.individual_degree_id()]
        user = COLLAB_VT[user_obj.id()]

        graph.add((user, VIVO.relatedBy, degree))
        graph.add((degree, RDF.type, VIVO['AcademicDegree']))
        graph.add((degree, RDFS.label, Literal(self.label)))
        graph.add((awarded_degree, RDF.type, VIVO['AwardedDegree']))
        graph.add((awarded_degree, VIVO.relates, COLLAB_VT[self.degree_id()]))
        graph.add((awarded_degree, VIVO.relates, COLLAB_VT[self.username]))
        graph.add((awarded_degree, OBO.RO_0002353,
                   COLLAB_VT[self.eduprocess_id()]))
        graph.add(
            (awarded_degree,
             RDFS.label,
             Literal(
                 '{}: {}'.format(
                     user_obj.display_name().decode('utf-8'),
                     self.label))))
        graph.add((awarded_degree, VIVO.assignedBy, degree_institution))
        graph.add((degree_institution, VIVO.relatedBy, awarded_degree))

        self.institution.add_to_graph(graph)
        self.__add_dates_to_graph(graph)
        self.__add_eduprocess_to_graph(graph, user_obj)

    def __add_eduprocess_to_graph(self, graph, user):
        edu_process = COLLAB_VT[self.eduprocess_id()]
        degree_institution = COLLAB_VT[self.institution.id()]
        awarded_degree = COLLAB_VT[self.individual_degree_id()]

        graph.add((edu_process, RDF.type, VIVO['EducationalProcess']))
        graph.add((edu_process, VIVO.dateTimeInterval,
                   COLLAB_VT[self.date_time_interval_id()]))
        graph.add((edu_process, OBO.RO_0000057, degree_institution))
        graph.add((edu_process, OBO.RO_0002234, awarded_degree))
        graph.add((edu_process, OBO.RO_0000057, COLLAB_VT[user.id()]))

    def __add_dates_to_graph(self, graph):
        if self.start_date or self.end_date:
            degree_start_date = COLLAB_VT[self.individual_degree_id(
            ) + '-startDate']
            degree_end_date = COLLAB_VT[self.individual_degree_id(
            ) + '-endDate']
            degree_interval = COLLAB_VT[self.date_time_interval_id()]

            graph.add((degree_interval, RDF.type, VIVO['DateTimeInterval']))
            if self.start_date:
                self.__add_degree_date_to_graph(
                    graph, degree_start_date, self.start_date)
                graph.add((degree_interval, VIVO.start, degree_start_date))
            if self.end_date:
                self.__add_degree_date_to_graph(
                    graph, degree_end_date, self.end_date)
                graph.add((degree_interval, VIVO.end, degree_end_date))

    def __add_degree_date_to_graph(self, graph, subject, date):
        graph.add((subject, RDF.type, VIVO['DateTimeValue']))
        graph.add(
            (subject,
             VIVO.dateTime,
             Literal(
                 date,
                 datatype=XSD.dateTime)))
        graph.add((subject, VIVO.dateTimePrecision, VIVO['yearPrecision']))

    def degree_id(self):
        # example: 'degree-ma-geography'
        return 'degree-' + self.type.lower().replace(' ', '-') + \
            '-' + self.field.lower().replace(' ', '-')

    def individual_degree_id(self):
        # example: 'degree-username-ma-geography'
        return 'degree-{}-{}-{}'.format(self.username.lower(),
                                        self.type.lower().replace(' ', '-'),
                                        self.field.lower().replace(' ', '-'))

    def date_time_interval_id(self):
        # example: 'degree-username-ma-geography-dateInterval-2000-2001'
        # TODO: find a better way to store, parse out years for the datetime interval
        # Assumption: Will return different format if both start and end dates
        # aren't defined
        from datetime import datetime
        if self.start_date and self.end_date:
            start_year = datetime.strptime(
                self.start_date, '%Y-%m-%dT%H:%M:%S').year
            end_year = datetime.strptime(
                self.end_date, '%Y-%m-%dT%H:%M:%S').year
            return '{}-dateInterval-{}-{}'.format(
                self.individual_degree_id(), start_year, end_year)
        else:
            return self.individual_degree_id() + '-dateInterval'

    def eduprocess_id(self):
        # example: 'eduprocess-username-ma-geography'
        return 'eduprocess-{}-{}-{}'.format(
            self.username.lower(), self.type.lower().replace(
                ' ', '-'), self.field.lower().replace(' ', '-'))


class Appointment:
    def __init__(self, is_public=False, id_suffix=''):
        self.is_public = is_public
        self.id_suffix = id_suffix
        self.label = None
        self.institution = Institution()
        self.start_date = None
        self.end_date = None

    def add_to_graph(self, graph, user_obj):
        if (self.is_public is False):
            return

        appointment = COLLAB_VT[self.id()]
        user = COLLAB_VT[user_obj.id()]

        graph.add((appointment, RDF.type, VIVO['Position']))
        graph.add((appointment, RDFS.label, Literal(self.label)))
        self.__add_interval_to_graph(graph, appointment)
        self.institution.add_to_graph(graph)
        if self.institution.dept:
            graph.add((appointment, VIVO.relates,
                       COLLAB_VT[self.institution.dept_id()]))
        graph.add((user, VIVO.relatedBy, appointment))
        graph.add((appointment, VIVO.relates, user))

    def id(self):
        return 'appointment-{}'.format(self.id_suffix)

    def date_interval_id(self):
        return '{}-dateInterval'.format(self.id())

    def __add_interval_to_graph(self, graph, appointment):
        if (self.start_date or self.end_date):
            interval = COLLAB_VT[self.date_interval_id()]
        graph.add((appointment, VIVO.dateTimeInterval, interval))
        graph.add((interval, RDF.type, VIVO['DateTimeInterval']))
        if self.start_date:
            start_date = COLLAB_VT[self.id() + '-startDate']
            graph.add((interval, VIVO.start, start_date))
            self.__add_date_to_graph(graph, start_date, self.start_date)
        if self.end_date:
            end_date = COLLAB_VT[self.id() + '-endDate']
            graph.add((interval, VIVO.end, end_date))
            self.__add_date_to_graph(graph, end_date, self.end_date)

    def __add_date_to_graph(self, graph, subject, date):
        graph.add((subject, RDF.type, VIVO['DateTimeValue']))
        graph.add(
            (subject,
             VIVO.dateTime,
             Literal(
                 date,
                 datatype=XSD.dateTime)))
        graph.add((subject, VIVO.dateTimePrecision, VIVO['yearPrecision']))


class VCard:
    def __init__(self, user=None):
        self.user = user
        if user is None:
            user = User()

    def add_to_graph(self, graph):
        self.__add_vcard(graph)

    def __add_vcard(self, graph):
        if self.user.classification == 'NonFacultyAcademic':
            user = self.user.uri
            # person vcard
            vt_vcard = COLLAB_VT['personvcard' +
                                 self.user.name_in_uri().decode('utf-8')]
            vt_vcardname = COLLAB_VT['personvcardname' +
                                     self.user.name_in_uri().decode('utf-8')]
        else:
            user = COLLAB_VT[self.user.username]

            # vcard
            vt_vcard = COLLAB_VT['vcard-' + self.user.username]

            # vcardemail
            vt_vcardemail = COLLAB_VT['vcardemail-' + self.user.username]
            if self.user.email_is_public:
                graph.add((vt_vcard, VCARD.hasEmail, vt_vcardemail))
                graph.add((vt_vcardemail, RDF.type, VCARD['Email']))
                graph.add((vt_vcardemail, RDF.type, VCARD['Work']))
                graph.add(
                    (vt_vcardemail,
                     VCARD.email,
                     Literal(
                         self.user.email)))

            # vcardname
            # TODO: Which fields are mandatory? Which fields are optional?
            vt_vcardname = COLLAB_VT['vcardname-' + self.user.username]
            if self.user.suffix:
                graph.add(
                    (vt_vcardname,
                     VCARD.suffix,
                     Literal(
                         self.user.suffix)))

            # vcardtitle
            vt_vcardtitle = COLLAB_VT['vcardtitle-' + self.user.username]
            graph.add((vt_vcard, VCARD.hasTitle, vt_vcardtitle))
            graph.add((vt_vcardtitle, RDF.type, VCARD['Title']))
            graph.add((vt_vcardtitle, VCARD.title, Literal(self.user.title)))
        graph.add((user, OBO.ARG_2000028, vt_vcard))
        graph.add((vt_vcard, RDF.type, VCARD.Individual))
        graph.add((vt_vcard, OBO.ARG_2000029, user))
        graph.add((vt_vcard, VCARD.hasName, vt_vcardname))
        graph.add((vt_vcardname, RDF.type, VCARD.Name))
        graph.add(
            (vt_vcardname,
             VCARD.givenName,
             Literal(
                 self.user.first_name)))
        graph.add(
            (vt_vcardname,
             VCARD.familyName,
             Literal(
                 self.user.last_name)))
