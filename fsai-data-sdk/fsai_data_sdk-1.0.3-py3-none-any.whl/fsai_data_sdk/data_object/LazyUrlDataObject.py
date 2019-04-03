import requests
import json


class LazyUrlDataObject:
    def __init__(self, url):
        self.url = url
        self.data = None

    def get(self):
        if self.data is None:
            response = requests.get(self.url)
            if response.ok:
                self.data = json.loads(response.content)
            else:
                response.raise_for_status()

        return self.data
