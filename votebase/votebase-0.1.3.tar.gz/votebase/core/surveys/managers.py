from django.db import models


class SurveyQuerySet(models.query.QuerySet):
    def by_user(self, user):
        """ Gets surveys owned by user """
        return self.filter(user=user)

    def quizzes(self):
        """ Gets quizzes only """
        from votebase.core.questions.models import Question
        quiz_questions = Question.objects.filter(is_quiz=True)
        return self.filter(pk__in=quiz_questions.values_list('survey__pk', flat=True)).distinct()

    def not_quizzes(self):
        """ Gets non-quizzes only """
        from votebase.core.questions.models import Question
        quiz_questions = Question.objects.filter(is_quiz=True)
        return self.exclude(pk__in=quiz_questions.values_list('survey__pk', flat=True)).distinct()


class SurveyManager(models.Manager):
    def get_query_set(self):
        return SurveyQuerySet(self.model, using=self._db)

    def by_user(self, user):
        return self.get_query_set().by_user(user)

    def quizzes(self):
        return self.get_query_set().quizzes()

    def not_quizzes(self):
        return self.get_query_set().not_quizzes()






class RoundQuerySet(models.query.QuerySet):
    def get_last_round(self, survey):
        """ Gets last created round in survey """
        return self.filter(survey=survey).order_by('-created')[0]

    def by_user(self, user):
        """ Gets segments of surveys owned by user """
        return self.filter(survey__user=user)

    def by_slug(self, slug):
        """ Gets segments by slug """
        return self.filter(slug=slug)


class RoundManager(models.Manager):
    def get_query_set(self):
        return RoundQuerySet(self.model, using=self._db)

    def get_last_round(self, survey):
        return self.get_query_set().get_last_round(survey)

    def by_user(self, user):
        return self.get_query_set().by_user(user)

    def by_slug(self, slug):
        return self.get_query_set().by_slug(slug)




class BrandingImageQuerySet(models.query.QuerySet):
    def by_user(self, user):
        return self.filter(user=user)

    def by_survey(self, survey):
        return self.filter(survey=survey)


class BrandingImageManager(models.Manager):
    def get_query_set(self):
        return BrandingImageQuerySet(self.model, using=self._db)

    def by_user(self, user):
        return self.get_query_set().by_user(user)

    def by_survey(self, survey):
        return self.get_query_set().by_survey(survey)
