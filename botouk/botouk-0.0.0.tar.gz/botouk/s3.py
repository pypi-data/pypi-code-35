# -*- coding: utf-8 -*-

from .base import Service, ResourceMixIn

from logging import getLogger

logger = getLogger(__name__)


class S3(Service, ResourceMixIn):
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
    """
    service_name = 's3'

    def __init__(self, session=None):
        super().__init__(session)

    def bucket(self, bucket_name):
        return self.resource.Bucket(bucket_name)

    def download_file(self, bucket, key, filename, **kwargs):
        return self.bucket(bucket) \
            .download_file(Key=key, Filename=filename, **kwargs)

    def list_objects(self, bucket, **kwargs):
        class Content:
            def __init__(self, content):
                self.key = content['Key']
                self.last_modified = content['LastModified']
                self.etag = content['ETag']
                self.size = content['Size']
                self.storage_class = content['StorageClass']

            def __str__(self):
                return self.key

            def __repr__(self):
                return self.__str__()

        class Response:
            def __init__(self, response):
                self.body = response
                self.metadata = response['ResponseMetadata']
                self.is_truncated = response['IsTruncated']
                self.contents = [Content(c) for c in response['Contents']]
                self.name = response['Name']
                self.prefix = response['Prefix']
                self.key_count = response['KeyCount']

            @property
            def files(self):
                return [c for c in self.contents
                        if not c.key.endswith('/')]

        res = self.client.list_objects_v2(
            Bucket=bucket,
            **kwargs
        )
        return Response(res)
