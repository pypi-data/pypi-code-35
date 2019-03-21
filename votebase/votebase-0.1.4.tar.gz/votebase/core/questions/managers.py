from django.db import models


class OptionQuerySet(models.query.QuerySet):
    def by_question(self, question):
        """ Gets options in question """
        return self.filter(question=question)

    def rows_by_question(self, question):
        """ Gets row options in question """
        return self.by_question(question).filter(
            orientation=self.model.ORIENTATION_ROW)

    def columns_by_question(self, question):
        """ Gets column options in question """
        return self.by_question(question).filter(
            orientation=self.model.ORIENTATION_COLUMN)

    def orientation_row(self):
        return self.filter(orientation=self.model.ORIENTATION_ROW)

    def orientation_column(self):
        return self.filter(orientation=self.model.ORIENTATION_COLUMN)

    def prepare_as_list(self):
        return self.values_list('id', 'title')

    def correct(self, question):
        return self.filter(question=question, is_correct=True)


class OptionManager(models.Manager):
    def get_query_set(self):
        return OptionQuerySet(self.model, using=self._db)

    def by_question(self, question):
        """ Proxy for by_question """
        return self.get_query_set().by_question(question)

    def rows_by_question(self, question):
        """ Proxy for rows_by_question """
        return self.get_query_set().rows_by_question(question)

    def columns_by_question(self, question):
        """ Proxy for columns_by_question """
        return self.get_query_set().columns_by_question(question)

    def orientation_row(self):
        """ Proxy for orientation_row """
        return self.get_query_set().orientation_row()

    def orientation_column(self):
        """ Proxy for orientation_column """
        return self.get_query_set().orientation_column()

    def correct(self, question):
        """ Proxy for correct options """
        return self.get_query_set().correct(question)
