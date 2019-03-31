import json
import ntpath
from magic import Magic

class Response:
    headers = {}

    def __init__(self, data, status_code=200, headers={}):
        self.data = data
        self.status_code = status_code
        self.headers = dict(**self.headers, **headers).items()


class JSON(Response):
    headers = {
        "Content-Type": "application/json"
    }

    def __init__(self, json_data, status_code=200, headers={}):
        Response.__init__(
            self, bytes(json.dumps(json_data), "utf-8"),
            status_code, headers=headers
        )

class File(Response):

    def __init__(self, path=None, headers={}):
        self.headers={
            'Content-Type': Magic(mime=True).from_file(path),
            'Content-Disposition': 'attachment; filename="%s"'%ntpath.basename(path)
        }
        file = open(path, 'rb')
        status_code = 200

        Response.__init__(
            self, file.read(), status_code, 
            headers=headers
        )

