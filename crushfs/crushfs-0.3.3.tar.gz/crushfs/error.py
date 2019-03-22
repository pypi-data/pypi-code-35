class DownloadObjectError(Exception):
    def __init__(self, response):
        self.message = f'{response.status_code}: {response.data.decode()}'


class UploadObjectError(Exception):
    def __init__(self, response):
        self.message = f'{response.status_code}: {response.data.decode()}'


class CombineObjectsError(Exception):
    def __init__(self, response):
        self.message = f'{response.status_code}: {response.data.decode()}'

