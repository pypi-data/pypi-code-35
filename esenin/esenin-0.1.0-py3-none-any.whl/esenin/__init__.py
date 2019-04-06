name = "esenin"

import requests

class Client:
    def __init__(self, ip="localhost", port="9000"):
        self.ip = ip
        self.port = port

    def __post(self, link, json):
        r = requests.post(link, json = json)
        r.raise_for_status()
        try:
            res = r.json()
        except ValueError:
            raise ValueError("Wrong format from server: {}. \n Check your server status.".format(r.text))
        return res

    def get_pos(self, text):
        return self.__post("http://{}:{}/nlp/pos".format(self.ip, self.port), {"text": text})
        
    def fit_topics(self, terms, topics):
        return self.__post("http://{}:{}/nlp/tm/fit".format(self.ip, self.port), {"terms": terms, "topics": topics})

    def get_topics(self, id, term):
        return self.__post("http://{}:{}/nlp/tm/topics".format(self.ip, self.port), {"id": id, "term": term})

