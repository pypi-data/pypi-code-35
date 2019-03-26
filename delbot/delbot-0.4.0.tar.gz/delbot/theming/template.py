from django.conf import settings
from django.template.backends.django import DjangoTemplates
import os


class ThemedTemplates(DjangoTemplates):
    def __init__(self, params):
        params = params.copy()
        super().__init__(params)

        theme_dir = getattr(
            settings,
            'THEME_DIR',
            os.path.join(settings.BASE_DIR, 'themes')
        )

        self.dirs.insert(
            0,
            os.path.join(
                theme_dir,
                getattr(settings, 'THEME', 'default')
            )
        )
