from megaphone.client import APIObject, HTTPClient


class Campaign(APIObject):
    path = 'campaigns'

    @property
    def orders(self):
        for order in self.http.get('orders'):
            yield Order(self.http, order)


class Order(APIObject):
    path = 'orders'

    @property
    def advertisements(self):
        for ad in self.http.get('advertisements'):
            yield Advertisement(self.http, ad)


class Advertisement(APIObject):
    path = 'advertisements'


class OrganizationClient(APIObject):
    path = "organizations"

    def __init__(self, token, objid):
        super().__init__(HTTPClient(token), {'id': objid})

    @property
    def campaigns(self):
        for campaign in self.http.get('campaigns'):
            yield Campaign(self.http, campaign)
