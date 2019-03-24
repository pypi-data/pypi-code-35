import requests
import json
import base64

class Nominet (object):
    auth_token = ''
    header = ''
    base_endpoint = 'https://restapi.nominet.org.uk/rest'

    def __init__(self, reg_tag=None, api_key=None):
        self.auth_token = self.auth_encode(reg_tag, api_key)
        self.header = {'Authorization':f'{self.auth_token}'}

    def auth_encode(self, reg_tag, api_key):
        encoded = (base64.b64encode(bytes(f'{reg_tag}:{api_key}', encoding='utf-8'))).decode("utf-8")
        return f'Basic {encoded}'

    def getAllDomains(self):
        data = requests.get(f"{self.base_endpoint}/domains/all", headers=self.header)
        return data.json()

    def getAllContacts(self):
        data = requests.get(f"{self.base_endpoint}/contacts/all", headers=self.header)
        return data.json()

    def getExpireAfter(self, date):
        data = requests.get(f"{self.base_endpoint}/domains/expiry/after/{date}", headers=self.header)
        return data.json()

    def getExpireBefore(self, date):
        data = requests.get(f"{self.base_endpoint}/domains/expiry/before/{date}", headers=self.header)
        return data.json()

    def getExpireRange(self, date_from, date_to):
        data = requests.get(f"{self.base_endpoint}/domains/expiry/range/{date_from}/{date_to}", headers=self.header)
        return data.json()

    def getCreatedAfter(self, date):
        data = requests.get(f"{self.base_endpoint}/domains/created/after/{date}", headers=self.header)
        return data.json()

    def getCreatedBefore(self, date):
        data = requests.get(f"{self.base_endpoint}/domains/created/before/{date}", headers=self.header)
        return data.json()

    def getCreatedRange(self, date_from, date_to):
        data = requests.get(f"{self.base_endpoint}/domains/created/range/{date_from}/{date_to}", headers=self.header)
        return data.json()

    def getDomainsByRegId(self, id):
        data = requests.get(f"{self.base_endpoint}/domains/registrant/{id}", headers=self.header)
        return data.json()

    def getDomainsByRegEpp(self, id):
        data = requests.get(f"{self.base_endpoint}/domains/epp/{id}", headers=self.header)
        return data.json()

    def getContactsById(self, id):
        data = requests.get(f"{self.base_endpoint}/contacts/registrant/{id}", headers=self.header)
        return data.json()

    def getContactsByEpp(self, id):
        data = requests.get(f"{self.base_endpoint}/contacts/epp/{id}", headers=self.header)
        return data.json()

    def getContactsByName(self, name):
        data = requests.get(f"{self.base_endpoint}/contacts/name/{name}", headers=self.header)
        return data.json()

    def getContactsByEmail (self, email):
        data = requests.get(f"{self.base_endpoint}/contacts/email/{email}", headers=self.header)
        return data.json()
