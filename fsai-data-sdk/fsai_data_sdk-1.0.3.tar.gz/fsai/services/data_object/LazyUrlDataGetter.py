import requests
import json


class LazyUrlDataGetter:
    """ The data_object.DataGetter of a URL data. The get function will trigger the fetching to receive the actual data.
    """
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
