import requests
import json


class EcoUrbisSP():

    def __init__(self,lat,longitude):
        self._lat=lat
        self._longitude=longitude


    def get_collect_schedule(self):
        response = requests.get('https://apicoleta.ecourbis.com.br/coleta?lat={}&lng={}&dst=20'.format(self._lat,self._longitude))
        body = json.loads(response.text)
        return body['result']

