import random
from progressbar import ProgressBar, Percentage, Bar

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand, CommandError

from votehub.apps.polls.models import Poll, Question, Option
from votehub.apps.rounds.models import Round
from votehub.apps.voting.models import Voter, Answer

class Command(BaseCommand):
    args = '<amount, poll_id>'
    help = 'Generates random voters'

    def handle(self, *args, **options):
        try:
            amount = args[0]
        except IndexError:
            raise CommandError('Amount is not defined!')

        try:
            poll_id = args[1]
        except IndexError:
            raise CommandError('Poll ID is not defined!')

        try:
            poll = Poll.objects.get(pk=poll_id)
        except ObjectDoesNotExist:
            raise CommandError('Poll does not exist!')

        progress_bar = ProgressBar(widgets=[Percentage(), Bar()], maxval=int(amount)).start()
        rounds = Round.objects.filter(poll=poll)
        round = rounds.order_by('?')[:1][0]

        questions = Question.objects.filter(poll=poll)

        for i in range(int(amount)):
            progress_bar.update(i+1)

            # Save voter
            voter = Voter.objects.create(round=round)
            voter.save()

            # Save answers for each question
            for question in questions:
                # SINGLE
                if question.widget == Question.SINGLE:
                    option = Option.objects.filter(
                        question=question,
                    ).order_by('?')[:1][0]

                    answer = Answer.objects.create(
                        voter=voter,
                        question=question,
                        option=option,
                    )
                    answer.save()
                # MULTIPLE
                elif question.widget == Question.MULTIPLE:
                    option_ids = []
                    # Get count of options for question
                    options_count = Option.objects.filter(
                        question=question
                    ).count()

                    # Generate random number of selected options
                    answers_count = random.randint(0, options_count)
                    if answers_count is not 0:
                        for i in range(answers_count):
                            # Select random option
                            option = Option.objects.filter(
                                question=question,
                            ).exclude(id__in=option_ids).order_by('?')[:1][0]

                            option_ids.append(option.id)
                            # Create new answer
                            answer = Answer.objects.create(
                                voter=voter,
                                question=question,
                                option=option,
                            )
                            answer.save()
                # RATING
                elif question.widget == Question.RATING:
                    of_stars = random.randint(1, question.rating_stars)

                    answer = Answer.objects.create(
                        voter=voter,
                        question=question,
                        rating_stars=of_stars,
                    )
                    answer.save()
        progress_bar.finish()