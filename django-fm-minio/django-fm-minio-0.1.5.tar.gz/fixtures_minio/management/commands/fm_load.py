#!env python

from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils.text import slugify

from fixtures_minio.conf import settings

from minio import Minio
from minio.error import ResponseError

from tempfile import NamedTemporaryFile

CLIENT = Minio(settings.FM_MINIO_URL,
                    access_key=settings.FM_MINIO_ACCESS_KEY,
                    secret_key=settings.FM_MINIO_SECRET_KEY,
                    secure=settings.FM_MINIO_SECURE)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='fixture_name', nargs='*',
            help='Fixture to take'
        )

    def load_fixture(self, fixture_file):
        call_command('loaddata', fixture_file)

    def get_latest_fixture_key(self):
        fixtures = CLIENT.list_objects(bucket_name=settings.FM_MINIO_BUCKET)

        latest_fixture = None
        for fixture in fixtures:
            fixture.last_modified_dt = fixture.last_modified
            if latest_fixture is None:
                latest_fixture = fixture
            elif fixture.last_modified_dt > latest_fixture.last_modified_dt:
                latest_fixture = fixture
        return latest_fixture.object_name

    def get_file(self, object_name):
        fixture_file = NamedTemporaryFile(suffix='fixture.json')
        try:
            CLIENT.fget_object(settings.FM_MINIO_BUCKET, object_name, fixture_file.name)
        except ResponseError as err:
            print(err)
            fixture_file.close()
        return fixture_file

    def handle(self, *args, **options):
        if len(args) > 0:
            fixture_key = args[0]
        else:
            fixture_key = self.get_latest_fixture_key()

        fixture_file = self.get_file(fixture_key)

        self.load_fixture(fixture_file.name)
        fixture_file.close()
