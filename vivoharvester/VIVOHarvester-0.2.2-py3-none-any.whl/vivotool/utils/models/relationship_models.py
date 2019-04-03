#!/user/bin/python
import sys


# Models to be used for relationship xml to rdf
class RsUser(object):
    individualBaseUrl = "http://collab.vt.edu/vivo/individual/"

    userID = ""
    userName = ""
    userLink = ""
    email = ""

    def __init__(self, doc):
        userObject = None
        for related in doc['entry']['api:relationship']['api:related']:
            if related['@category'] == 'user':
                userObject = related
        if userObject is not None:
            self.makeUser(userObject)

    def makeUser(self, user):
        self.userID = user['api:object']['@id']
        self.userName = user['api:object']['@username']
        self.userLink = self.individualBaseUrl + self.userName

        email = None
        for assoc in user['api:object']['api:user-identifier-associations']['api:user-identifier-association']:
            if assoc['@scheme'] == 'email-address':
                email = assoc

        self.email = email['#text']


class RsPublication(object):
    publicationBaseUrl = "http://collab.vt.edu/vivo/individual/publication"

    publicationID = ""
    publicationLink = ""
    isPublication = True

    def __init__(self, doc):
        publicationObject = None
        for related in doc['entry']['api:relationship']['api:related']:
            if related['@category'] == 'publication':
                publicationObject = related

        if publicationObject is None:
            self.isPublication = False
        else:
            self.makePublication(publicationObject)

    def makePublication(self, publication):
        self.publicationID = publication['api:object']['@id']
        self.publicationLink = self.publicationBaseUrl + self.publicationID


class RsAuthorship(object):
    authorshipBaseUrl = "http://collab.vt.edu/vivo/individual/authorship"

    user = None
    publication = None
    authorshipID = ""

    def __init__(self, doc, user, publication):
        self.user = user
        self.publication = publication
        self.authorshipID = doc['entry']['api:relationship']['@id']

    def getAuthorshipURL(self):
        return self.authorshipBaseUrl + self.publication.publicationID + "-" + self.user.userID
