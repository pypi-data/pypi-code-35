from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DbcronConfig(AppConfig):
    name = 'dbcron'
    label = 'dbcron'
    verbose_name = _("Job scheduling")

    def ready(self):
        from dbcron import signals  # noqa
        from dbcron import consumers  # noqa
