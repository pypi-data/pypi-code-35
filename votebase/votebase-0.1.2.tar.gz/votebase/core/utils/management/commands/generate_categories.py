import random
import string

from progressbar import ProgressBar, Percentage, Bar

from django.contrib.auth.models import User
from django.core.management import BaseCommand, CommandError

from votehub.apps.categories.models import Category

class Command(BaseCommand):
    args = '<amount>'
    help = 'Generates random categories'

    def handle(self, *args, **options):
        try:
            amount = args[0]
        except IndexError:
            raise CommandError('Amount is not defined!')

        user = User.objects.get(pk=1)

        progress_bar = ProgressBar(widgets=[Percentage(), Bar()], maxval=int(amount)).start()

        for i in range(int(amount)):
            progress_bar.update(i+1)

            name = ''.join(random.choice(string.ascii_uppercase + string.whitespace) for x in range(random.randint(1, 30)))
            category = Category.objects.create(
                user=user,
                name=name,
            )
            category.save()

        progress_bar.finish()
