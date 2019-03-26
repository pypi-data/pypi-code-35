from django.core.management.base import BaseCommand
from ...signals import sample_data_requested


class Command(BaseCommand):
    help = 'Generate sample data for theme development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            dest='clear',
            help='Delete current data'
        )

    def handle(self, *args, **options):
        sample_data_requested.send(
            type(self),
            clear=options['clear']
        )
