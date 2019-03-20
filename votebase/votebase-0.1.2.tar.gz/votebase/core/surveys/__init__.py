# from django.db.models.signals import post_delete
# from django.dispatch import receiver

# from votehub.apps.polls.models import Question, Option
# from votehub.apps.rounds.models import Round

#@receiver(post_delete, sender=Round)
#def round_deleted(sender, **kwargs):
#    round = kwargs['instance']
#    poll = round.poll
#    rounds_count = Round.objects.filter(poll=poll).count()
#
#    if rounds_count is 0 and poll.is_visible is True:
#        poll.is_visible = False
#        poll.save()
#
#@receiver(post_delete, sender=Question)
#def question_deleted(sender, **kwargs):
#    question = kwargs['instance']
#    poll = question.poll
#    questions_count = Question.objects.filter(poll=poll).count()
#
#    if questions_count is 0 and poll.is_visible is True:
#        poll.is_visible = False
#        poll.save()
#
#@receiver(post_delete, sender=Option)
#def option_deleted(sender, **kwargs):
#    option = kwargs['instance']
#    poll = option.question.poll
#    questions = Question.objects.filter(poll=poll)
#
#    change_is_visible = True
#    for question in questions:
#        options_count = Option.objects.filter(question=question).count()
#        if options_count > 1:
#            change_is_visible = False
#
#    if change_is_visible and poll.is_visible is True:
#        poll.is_visible = False
#        poll.save()
#
