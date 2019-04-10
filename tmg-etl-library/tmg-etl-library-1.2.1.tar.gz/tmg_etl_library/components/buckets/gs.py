from tmg_etl_library.components.buckets.bucket import Bucket

from google.cloud import storage

import re

class GSClient(Bucket):
    def __init__(self, log, project, bucket_name):
        super().__init__(log)
        self.logger = log
        self.project = project
        self.bucket_name = bucket_name
        self.google_client = storage.Client(project=self.project)

    def list_files(self, pattern='', prefix=None):
        # TODO: Should we have pattern and prefix

        if prefix:
            prefix = prefix[:-1] if prefix[-1] == '*' else prefix

        bucket = self.google_client.get_bucket(self.bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)
        re_pattern = re.compile(pattern)
        file_names = list(filter(lambda blob: re_pattern.match(blob.name), blobs))
        file_objects = [GSFile(self, self.project, self.bucket_name, filename.name) for filename in file_names]
        return file_objects


class GSFile:
    def __init__(self, client, project, bucket_name, file_name):
        self.project = project
        self.bucket_name = bucket_name
        self.file_name = file_name
        self.full_path = bucket_name + '/' + file_name
        if isinstance(client, GSClient):
            self._client = client
        else:
            raise TypeError('Client should be of GSClient type')

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        raise RuntimeError('The client should not updated after creation of the GSClient')

    def delete(self):

        bucket = self.client.google_client.get_bucket(self.bucket_name)

        blob = bucket.blob(self.file_name)

        blob.delete()

        self.client.logger.info("Deleting {filename} from bucket gs://{bucket}".format(
            filename=self.file_name,
            bucket=self.bucket_name,
        ))

    def upload(self, file):
        bucket = self.client.google_client.get_bucket(self.bucket_name)
        blob = bucket.blob(self.full_path)

        blob.upload_from_filename(file.full_path)

        self.client.logger.info('Uploaded {} to {}'.format(file.full_path, self.bucket_name))

    def download(self, destination_file):
        bucket = self.client.google_client.get_bucket(self.bucket_name)
        blob = bucket.blob(self.file_name)

        blob.download_to_filename(destination_file.full_path)

        self.client.logger.info('Downloading {} to {}'.format(self.full_path, self.bucket_name))
