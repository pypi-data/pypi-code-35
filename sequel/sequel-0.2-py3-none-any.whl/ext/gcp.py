from urllib.parse import urlparse

try:
    from google.cloud.storage.client import Client
    from google.cloud.exceptions import Conflict
except ImportError as e:  # noqa
    raise RuntimeError('You need to install "google-cloud-storage" in '
                       'order to use a Google Bucket') from e

from sequel.io import Storage


def get_blob(url):
    parsed = urlparse(url)
    bucket_name = parsed.netloc
    path = parsed.path

    bucket = Client().bucket(bucket_name)

    try:
        bucket.create()
    except Conflict:
        pass

    return bucket.blob(path)


class GoogleCloudStorage(Storage):
    def write(self, text):
        blob = get_blob(self.url)
        blob.upload_from_string(text, content_type='application/json')

    def read(self):
        blob = get_blob(self.url)
        as_string = blob.download_as_string()
        return as_string
