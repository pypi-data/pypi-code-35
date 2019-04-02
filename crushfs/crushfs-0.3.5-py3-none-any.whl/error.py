class DownloadObjectError(Exception):
    def __init__(self, response):
        self.message = f'{response.status_code}: {response.data.decode()}'

    def __str__(self):
        return f'{type(self)}: {self.message}'


class UploadObjectError(Exception):
    def __init__(self, response):
        self.message = f'{response.status_code}: {response.data.decode()}'

    def __str__(self):
        return f'{type(self)}: {self.message}'


class CombineObjectsError(Exception):
    def __init__(self, response):
        self.message = f'{response.status_code}: {response.data.decode()}'

    def __str__(self):
        return f'{type(self)}: {self.message}'

