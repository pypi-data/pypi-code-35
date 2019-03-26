from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_MEDIA_STORAGE_BUCKET_NAME
    location = settings.AWS_MEDIA_LOCATION

    def __init__(self, acl=None, bucket=None, **kwargs):
        self.custom_domain = getattr(settings, 'AWS_S3_MEDIA_CUSTOM_DOMAIN', None)
        super(MediaStorage, self).__init__(acl=acl, bucket=bucket, **kwargs)
