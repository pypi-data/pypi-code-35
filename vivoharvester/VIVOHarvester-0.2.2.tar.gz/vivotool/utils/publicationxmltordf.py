import collections
import os
import xmltodict

from rdflib import Graph, Literal, BNode, RDF, RDFS, URIRef, Namespace
from rdflib.namespace import FOAF, DC
from datetime import datetime
from vivotool.utils.models.publication_model import Publication, \
    PublicationDate, Journal, WebpagesPublisher, Authorship, SubjectArea
from vivotool.utils.models.user_model import User


class PublicationXml2Rdf(object):

    def __get_publication(self, doc):
        try:
            publication = Publication()

            # object general information
            api_obj = doc["feed"]["entry"]["api:object"]
            publication.is_public = api_obj["api:is-public"]

            if not publication.is_public:
                print("RDF graph is not generated as record is private.")
                return None

            id = api_obj["@id"]
            publication.id = id

            # Publication Types
            pub_type = doc["feed"]["entry"]["content"]["div"]["p"][0][13:][:-1]
            if pub_type == 'book chapter or section':
                pub_type = 'Chapter'
            elif pub_type == 'conference paper or presentation':
                pub_type = 'ConferencePaper'
            elif pub_type == 'internet publication':
                pub_type = 'InternetPublication'
            elif pub_type == 'journal article':
                pub_type = 'Journal'
            elif pub_type == 'numbered extension publication':
                pub_type = 'NumberedExtensionPublication'
            elif pub_type == 'poster':
                pub_type = 'ConferencePoster'
            elif pub_type == 'presentation (not at a conference)':
                pub_type = 'PresentationNotConference'
            elif pub_type == 'refereed journal article':
                pub_type = 'AcademicArticle'
            elif pub_type == 'scholarly edition':
                pub_type = 'EditorialArticle'
            elif pub_type == 'software / code':
                pub_type = 'Software'
            elif pub_type == 'thesis / dissertation':
                pub_type = 'Thesis'
            else:
                pub_type = pub_type.capitalize()
            publication.types.append(pub_type)

            # Journal
            journal = Journal()

            for obj_key in api_obj.keys():
                if obj_key == "api:repository-items":
                    # handle
                    publication.handle = api_obj[obj_key]["api:repository-item"]["api:public-url"].strip(
                    ).replace("http://hdl.handle.net/", '')
                    print('Handle: {}'.format(publication.handle))

                elif obj_key == "api:all-labels":
                    keywords = api_obj[obj_key]["api:keywords"]["api:keyword"]
                    if (isinstance(keywords, list)):
                        for keyword in keywords:
                            for key in keyword.keys():
                                if key == "@scheme":
                                    subject_area = SubjectArea()
                                    subject_area.label = keyword["#text"]
                                    subject_area.scheme = keyword[key]
                                    publication.subject_areas.append(
                                        subject_area)
                                    if keyword["@scheme"] == "mesh":
                                        publication.keywords.append(
                                            keyword["#text"])
                                    else:
                                        journal.subject_areas.append(
                                            subject_area)
                                elif key == "@source" and keyword[key] in ["manual", "pubmed"]:
                                    publication.keywords.append(
                                        keyword["#text"])
                        for keyword in publication.keywords:
                            print(
                                'Keyword: {}'.format(
                                    keyword.encode('utf-8')))

                elif obj_key == "api:records":
                    records = api_obj[obj_key]["api:record"]
                    # get the record from PubMed or first if there are many
                    # records
                    if (isinstance(records, list)):
                        record = records[0]
                        record_chosen = False
                        for r in records:
                            if r["@source-name"] == "pubmed":
                                record = r
                                record_chosen = True
                                if r["@id-at-source"]:
                                    publication.pm_id = r["@id-at-source"]
                                    print(
                                        'PubMed: {}'.format(
                                            publication.pm_id))
                            elif r["@source-name"] == "crossref":
                                if not record_chosen:
                                    record = r
                                for f in r["api:native"]["api:field"]:
                                    if f["@name"] == "doi":
                                        publication.doi = f["api:text"]
                                        print('doi: {}'.format(
                                            publication.doi))
                                    elif f["@name"] == "eissn":
                                        journal.eissn = f["api:text"]
                            elif r["@source-name"] == "dspace":
                                for f in r["api:native"]["api:field"]:
                                    if f["@name"] == "public-url":
                                        handle = f["api:text"].strip().replace(
                                            "http://hdl.handle.net/", '')
                                        if not publication.handle:
                                            publication.handle = handle
                                            print('Handle: {}'.format(
                                                publication.handle))
                                        elif int(handle.split('/')[1]) > int(publication.handle.split('/')[1]):
                                            publication.handle = handle
                                            print('Handle: {}'.format(
                                                publication.handle))
                    else:
                        record = records
                    # field info from the first record
                    publication_fields = record["api:native"]["api:field"]
                    for f in publication_fields:
                        f_name = f["@name"]
                        if f_name == "title":
                            publication.title = f["api:text"].strip('.')
                        elif f_name == "abstract":
                            publication.abstract = f["api:text"]
                        elif f_name == "pagination" and f["api:pagination"]:
                            pagination = f["api:pagination"]
                            if "api:begin-page" in pagination.keys():
                                publication.page_start = pagination["api:begin-page"]
                            if "api:end-page" in pagination.keys():
                                publication.page_end = pagination["api:end-page"]
                            else:
                                publication.page_end = publication.page_start
                        elif f_name == "issue":
                            publication.issue = f["api:text"]
                        elif f_name == "volume":
                            publication.volume = f["api:text"]
                        elif "publication-date" in f_name:
                            publication_date = PublicationDate(id)
                            date_info = f["api:date"]
                            time_precision = "Precision"
                            for key in date_info.keys():
                                if key == "api:day":
                                    time_precision = "Day" + time_precision
                                    publication_date.day = int(date_info[key])
                                elif key == "api:month":
                                    time_precision = "Month" + time_precision
                                    publication_date.month = int(
                                        date_info[key])
                                elif key == "api:year":
                                    time_precision = "year" + time_precision
                                    publication_date.year = int(date_info[key])
                            publication_date.time_precision = time_precision
                            publication_date.type = "DateTimeValue"
                            publication.publication_date = publication_date
                        elif f_name == "journal":
                            journal.label = f["api:text"]
                        elif f_name == "issn":
                            journal.issn = f["api:text"]
                        elif f_name == "publication-status":
                            publication.status = f["api:text"].lower()
                        elif f_name == "publisher-url" or f_name == "author-url":
                            if "publisher" in f_name:
                                webpages_publisher = WebpagesPublisher(
                                    'publisher')
                                webpages_publisher.label = "Publisher's Version"
                            else:
                                webpages_publisher = WebpagesPublisher(
                                    'author')
                                webpages_publisher.label = "Author's Version"
                            webpages_publisher.url = f["api:text"]
                            publication.webpages_publisher = webpages_publisher
                        elif f_name == "authors":
                            people = f["api:people"]["api:person"]
                            if (isinstance(people, list)):
                                for idx, p in enumerate(
                                        f["api:people"]["api:person"]):
                                    user = User()
                                    for key in p.keys():
                                        if key == "api:links":
                                            user.user_id = p[key]["api:link"]["@id"]
                                        elif key == "api:last-name":
                                            user.last_name = p[key].strip().replace(
                                                ' ', '-')
                                        elif key == "api:first-names":
                                            user.first_name = p[key]
                                        elif key == "api:initials":
                                            user.initial = p[key]
                                    authorship = Authorship(
                                        user, publication, idx + 1)
                                    publication.authorships.append(
                                        authorship)
                            else:
                                user = User()
                                p = people
                                for key in p.keys():
                                    if key == "api:links":
                                        user.user_id = p[key]["api:link"]["@id"]
                                    elif key == "api:last-name":
                                        user.last_name = p[key].strip().replace(
                                            ' ', '-')
                                    elif key == "api:first-names":
                                        user.first_name = p[key]
                                    elif key == "api:initials":
                                        user.initial = p[key]
                                authorship = Authorship(user, publication, 1)
                                publication.authorships.append(authorship)

            if journal.label:
                publication.journal = journal
            return publication
        except KeyError as key_error:
            print('Unable to properly parse xml file due to ' + str(key_error))
            return None

    def parse(self, fileName, target_dir=""):
        try:
            with open(fileName) as fd:
                doc = xmltodict.parse(fd.read())

            publication = self.__get_publication(doc)
            if publication:
                g = Graph()
                publication.add_to_graph(g)
                rdf_file = os.path.splitext(
                    os.path.basename(fileName))[0] + ".rdf"
                g.serialize(target_dir + rdf_file, format='nt')
                print("Resulting RDF graph in: " + rdf_file)
        except KeyError as key_error:
            print('Error parsing ' + fileName + ' due to ' + str(key_error))
