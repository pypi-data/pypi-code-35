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
            'args', metavar='app_label[.ModelName]', nargs='*',
            help='Restricts dumped data to the specified app_label or app_label.ModelName.',
        )
        parser.add_argument(
            '--pks', dest='primary_keys',
            help="Only dump objects with given primary keys. Accepts a comma-separated "
                 "list of keys. This option only works when you specify one model.",
        )
        parser.add_argument(
            '--prefix', dest='manual_prefix',
            help="Manual additional prefix for minio files ",
        )

    def get_fixture_file(self, dumpdata_args, dumpdata_options):
        pks = dumpdata_options['primary_keys']
        fixture_file = NamedTemporaryFile(suffix='.json')
        call_command('dumpdata', *dumpdata_args, output=fixture_file.name, pks=pks)
        fixture_file.seek(0)
        return fixture_file

    def get_file_name(self, manual_prefix):
        return '{}{}fixture_{}.json'.format(
            slugify(manual_prefix), slugify(settings.FM_MINIO_PREFIX),
            slugify(int(datetime.utcnow().timestamp()))
        )

    def handle(self, *args, **options):
        manual_prefix = options['manual_prefix']
        filename = self.get_file_name(manual_prefix=manual_prefix)
        tmpfile = self.get_fixture_file(args, options)
        try:
            CLIENT.fput_object(settings.FM_MINIO_BUCKET, filename, tmpfile.name)
        except ResponseError as err:
            tmpfile.close()
        tmpfile.close()
        print('filename: %s' % filename)
