import logging
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    @property
    def logger(self):
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger('dbcron')
        return self._logger
