# pylint: disable=unused-import
from django.apps import AppConfig

class LatchConfig(AppConfig):
    name = 'latch'
    verbose_name = 'Django Latch integration'

    def ready(self):
        from latch.signals import unpair_before_delete
