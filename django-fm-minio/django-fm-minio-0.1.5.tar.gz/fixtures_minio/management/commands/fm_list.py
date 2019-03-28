#!env python

from django.core.management.base import BaseCommand

from fixtures_minio.conf import settings

from minio import Minio
from minio.error import ResponseError

CLIENT = Minio(settings.FM_MINIO_URL,
                    access_key=settings.FM_MINIO_ACCESS_KEY,
                    secret_key=settings.FM_MINIO_SECRET_KEY,
                    secure=settings.FM_MINIO_SECURE)

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            fixtures = CLIENT.list_objects(bucket_name=settings.FM_MINIO_BUCKET)
        except ResponseError as err:
            print(err)

        for fixture in fixtures:
            print(fixture.object_name, fixture.last_modified, fixture.size)
