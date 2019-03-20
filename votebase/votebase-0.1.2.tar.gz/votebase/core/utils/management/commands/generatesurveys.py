import random
import string

from progressbar import ProgressBar, Percentage, Bar

from django.contrib.auth.models import User
from django.core.management import BaseCommand, CommandError

from votebase.core.surveys.models import Survey

class Command(BaseCommand):
    args = '<amount>'
    help = 'Generates random surveys'

    def handle(self, *args, **options):
        try:
            amount = args[0]
        except IndexError:
            raise CommandError('Amount is not defined!')

        user = User.objects.get(pk=1)
        progress_bar = ProgressBar(widgets=[Percentage(), Bar()], maxval=int(amount)).start()

        for i in range(int(amount)):
            progress_bar.update(i+1)
            title = ''.join(random.choice(string.ascii_uppercase + string.whitespace) for x in range(random.randint(1, 70)))            
            Survey.objects.create(user=user, title=title)

        progress_bar.finish()
