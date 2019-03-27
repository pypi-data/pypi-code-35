from django.core.management.base import BaseCommand, CommandError
from djangoldp_conversation.factories import ThreadFactory, MessageFactory

class Command(BaseCommand):
    help = 'Mock data'

    def add_arguments(self, parser):
        parser.add_argument('--size', type=int, default=0, help='Number of thread to create')
        parser.add_argument('--sizeof', type=int, default=10, help='Number of message into each thread created')

    def handle(self, *args, **options):
        for i in range(0, options['size']):
            thread = ThreadFactory.create()
            MessageFactory.create_batch(options['sizeof'], thread=thread)

        self.stdout.write(self.style.SUCCESS('Successful data mock install'))
