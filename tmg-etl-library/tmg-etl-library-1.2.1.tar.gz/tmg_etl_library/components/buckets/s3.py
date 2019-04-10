from tmg_etl_library.components.buckets.bucket import Bucket

import boto3
import botocore


class S3Client(Bucket):
    def __init__(self, log, bucket, access_key, secret_key):
        super().__init__(log)
        self.bucket = bucket
        self.s3_client = self._connect(access_key, secret_key)

    def _connect(self, access_key, secret_key):
        self.logger.info('Create S3 client.')

        s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

        return s3_client

    def list_files(self, prefix=None):
        self.logger.info('Finding files from s3 bucket {}/{}'.format(self.bucket, prefix))

        response = self.s3_client.list_objects(
            Bucket=self.bucket,
            Prefix=prefix,
            Delimiter='/'
        )

        files = [content.get('Key', None) for content in response.get('Contents', [])]

        s3_files = []

        for file in files:
            s3file = S3File(bucket=self.bucket,
                            prefix=prefix,
                            file_name=file
                            )
            s3_files.append(s3file)

        return s3_files


class S3File:

    def __init__(self, client, bucket, prefix, file_name):
        self.bucket = bucket
        self.prefix = prefix
        self.file_name = file_name
        if isinstance(client, S3Client):
            self._client = client
        else:
            raise TypeError('Client should be of S3Client type')

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        raise RuntimeError('The client should not updated after creation of the S3Client')

    def download(self, client, file):
        try:
            client.logger.info('Downloading {}/{}'.format(self.bucket, self.file_name))
            client.s3_client.download_file(self.bucket, self.file_name, file.full_path)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                raise Exception("File {} does not exist.".format(self.file_name))
            else:
                raise Exception(e)

    def upload(self, client, file):
        try:
            client.logger.info('Downloading {}/{}'.format(self.bucket, self.file_name))
            client.s3_client.upload_file(file.full_path, self.bucket, self.file_name)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                raise Exception("File {} does not exist.".format(self.file_name))
            else:
                raise Exception(e)

    def delete(self, client):
        client.s3_client.delete_object(bucket=self.bucket,
                                       key=self.file_name)

