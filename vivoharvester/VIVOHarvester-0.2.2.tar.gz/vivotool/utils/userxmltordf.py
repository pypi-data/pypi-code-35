import collections

from rdflib import Graph, Literal, BNode, RDF, RDFS, URIRef, Namespace
from rdflib.namespace import FOAF, DC
from datetime import datetime
# from utils.models.user_model import User, Appointment, Degree, Institution
from vivotool.utils.models.user_model import User, Appointment, Degree, Institution


class UserElementXml2Rdf(object):

    def convert(self, doc, rdf_filename):
        user = self.__get_user(doc)

        if user:
            g = Graph()
            user.add_to_graph(g)
            g.serialize(rdf_filename, format='nt')

    def __get_datetime(self, doc_date):
        yyyy = int(doc_date['api:year'])        # year is required
        # defaults to january if not defined
        mm = int(doc_date.get('api:month', 1))
        # defaults to january if not defined
        dd = int(doc_date.get('api:day', 1))
        return '{:%Y-%m-%dT%H:%M:%S}'.format(datetime(yyyy, mm, dd))

    def __get_user(self, doc):
        # TODO: handle properly when expected values don't exist...
        try:
            user = User()
            api_obj = doc['feed']['entry']['api:object']

            user.username = api_obj['@username']

            if 'api:first-name' in api_obj:
                user.first_name = api_obj['api:first-name']
            else:
                return user

            if 'api:last-name' in api_obj:
                user.last_name = api_obj['api:last-name']
            else:
                return user

            user.is_academic = api_obj.get(
                'api:is-academic', 'false').lower() == 'true'
            user.is_current_staff = api_obj.get(
                'api:is-current-staff', 'false').lower() == 'true'
            user.is_public = api_obj.get(
                'api:is-public', 'false').lower() == 'true'

            if 'api:suffix' in api_obj:
                user.suffix = api_obj['api:suffix']
            user.email = api_obj['api:email-address']

            if 'api:position' in api_obj:
                user.title = api_obj['api:position']
            user.email_is_public = api_obj.get(
                'api:institutional-email-is-public', '').lower() == 'true'

            if api_obj["api:records"]["api:record"]["api:native"]:

                userfields = api_obj["api:records"]["api:record"]["api:native"]["api:field"]

                fulldetail = False
                if (user.is_public and user.is_academic and user.is_current_staff):
                    fulldetail = True

                for f in userfields:
                    if isinstance(f, collections.OrderedDict):
                        if fulldetail and f['@name'] == 'overview':
                            if f['api:text']['@privacy'].lower() == 'public':
                                user.overview = f['api:text']['#text']
                        elif fulldetail and f['@name'] == 'academic-appointments':
                            appointments = f['api:academic-appointments']['api:academic-appointment']
                            idx = 1
                            if (isinstance(appointments, list)
                                ):  # many appointments
                                for i, appt in enumerate(
                                        f['api:academic-appointments']['api:academic-appointment']):
                                    if appt['@privacy'].lower() == 'public':
                                        appointment = self.__get_appointment(
                                            appt, user.username, idx)
                                        user.institutions.append(
                                            appointment.institution)
                                        user.appointments.append(appointment)
                                        idx += 1
                            elif isinstance(appointments, dict):  # single appointment
                                appt = appointments
                                if appt['@privacy'].lower() == 'public':
                                    appointment = self.__get_appointment(
                                        appt, user.username, idx)
                                    user.institutions.append(
                                        appointment.institution)
                                    user.appointments.append(appointment)
                        elif fulldetail and f['@name'] == 'degrees':
                            p = f['api:degrees']['api:degree']
                            if isinstance(p, collections.OrderedDict):
                                if p['@privacy'].lower() == 'public':
                                    degree = self.__get_degree(
                                        p, user.username)
                                    user.institutions.append(
                                        degree.institution)
                                    user.degrees.append(degree)
                            else:
                                for deg in f['api:degrees']['api:degree']:
                                    if deg['@privacy'].lower() == 'public':
                                        degree = self.__get_degree(
                                            deg, user.username)
                                        user.institutions.append(
                                            degree.institution)
                                        user.degrees.append(degree)
                        elif f['@name'] == 'email-addresses':
                            p = f['api:email-addresses']['api:email-address']
                            if isinstance(
                                    p, collections.OrderedDict) and p['@privacy'].lower() == 'public':
                                if ('api:type' in p) and p['api:type'].lower(
                                ) == 'work':
                                    user.email = p['api:address']
                    else:
                        if f == 'email-addresses':
                            print(
                                "This user is private and has a work email:" +
                                user.username)
                            print(f)

            # NOTE: Some information is not necessary in resulting graph
            # (e.g., Photo info, addresses, phone numbers, personal websites, Relationships)
            return user
        except KeyError as ke_error:
            # TODO: logger that doc is invalid for getting user
            print(
                'Unable able to properly parse input xml file: ' +
                str(ke_error))
            return None

    def __get_degree(self, doc, username):
        degree = Degree()
        degree.username = username
        degree.field = doc.get(
            'api:field-of-study',
            '')  # default to '' if none exists
        degree.label = '{} {}'.format(doc['api:name'], degree.field)
        degree.type = ''.join(
            x for x in doc['api:name'] if x.isalpha()).lower()
        if 'api:start-date' in doc:
            degree.start_date = self.__get_datetime(doc['api:start-date'])
        if 'api:end-date' in doc:
            degree.end_date = self.__get_datetime(doc['api:end-date'])
        degree.institution = self.__get_institution(doc['api:institution'])
        return degree

    def __get_appointment(self, doc, username, idx):
        appointment = Appointment(
            id_suffix='{}-{}'.format(username, idx), is_public=True)
        appointment.label = doc['api:position']
        if 'api:start-date' in doc:
            appointment.start_date = self.__get_datetime(doc['api:start-date'])
        if 'api:end-date' in doc:
            appointment.end_date = self.__get_datetime(doc['api:end-date'])
        appointment.institution = self.__get_institution(
            doc['api:institution'])
        return appointment

    def __get_institution(self, institution_doc):
        institution = Institution()
        for line in institution_doc['api:line']:
            if line['@type'] == 'organisation':
                institution.label = line['#text']
            elif line['@type'] == 'suborganisation':
                institution.dept = line['#text']
            elif line['@type'] == 'city':
                institution.city = line['#text']
            elif line['@type'] == 'country':
                institution.country = line['#text']
        return institution
