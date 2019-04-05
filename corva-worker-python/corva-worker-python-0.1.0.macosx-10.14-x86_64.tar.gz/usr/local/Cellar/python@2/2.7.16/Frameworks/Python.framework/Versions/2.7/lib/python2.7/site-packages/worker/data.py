from worker import exceptions


class Result(object):

    def __init__(self, response, **kwargs):
        self.response = response
        self.params = kwargs
        self.data = None

        try:
            self.data = response.json()
        except Exception:
            raise exceptions.APIError("Invalid API response")

    def __repr__(self):
        return repr(self.data)

    def __iter__(self):
        return iter(self.data)

    @property
    def status(self):
        return self.response.status_code

    @property
    def count(self):
        if not self.data:
            return 0

        if isinstance(self.data, list):
            return len(self.data)

        if isinstance(self.data, dict):
            return 1

        return 0
