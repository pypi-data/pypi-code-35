import random
import string

from progressbar import ProgressBar, Percentage, Bar

from django.contrib.auth.models import User
from django.core.management import BaseCommand, CommandError

from votehub.apps.polls.models import Poll, Question, Option

class Command(BaseCommand):
    args = '<amount>'
    help = 'Generates random questions'

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
            poll = Poll.objects.all().order_by('?')[0]

            widget = random.choice(Question.WIDGET_TYPES)[0]

            question = Question.objects.create(
                text=name,
                poll=poll,
                user=user,
                widget=widget,
            )
            question.save()

            if widget == Question.RATING:
                question.rating_stars = random.choice(range(5, 10))
                question.save()
            elif widget == Question.SINGLE or widget == Question.MULTIPLE:
                for j in range(2, 10):
                    option = Option.objects.create(
                        question=question,
                        user=user,
                        text=''.join(random.choice(string.ascii_uppercase + string.whitespace) for x in range(random.randint(1, 30)))
                    )
                    option.save()

        progress_bar.finish()
