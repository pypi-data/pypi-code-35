from django.conf import settings
from django.contrib.staticfiles.finders import FileSystemFinder
from django.contrib.staticfiles.storage import FileSystemStorage
import os


class ThemeFileFinder(FileSystemFinder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        theme_dir = getattr(
            settings,
            'THEME_DIR',
            os.path.join(settings.BASE_DIR, 'themes')
        )

        root = os.path.join(
            theme_dir,
            getattr(settings, 'THEME', 'default'),
            'static'
        )

        self.locations.append(('theme', root))
        filesystem_storage = FileSystemStorage(location=root)
        filesystem_storage.prefix = 'theme'
        self.storages[root] = filesystem_storage
