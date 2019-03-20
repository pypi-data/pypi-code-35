import os
from box import Box
# global settings
# directories
pjreports_project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
pjreports_dir_base = os.path.join(pjreports_project_root, 'pjreports')
pjreports_dir_static = os.path.join(pjreports_dir_base, 'static')
pjreports_dir_java = os.path.join(pjreports_dir_base, 'java')

configuration = {
    'DIRECTORIES': {
        # directories settings
        'PROJECT_ROOT': pjreports_project_root,
        'BASE': pjreports_dir_base,
        'STATIC': pjreports_dir_static,
        'JAVA': pjreports_dir_java
    },
    'LOGGER': {
        # logger system settings
        'ENABLE': True,
        'DEFAULT_NAME': 'pjreports_logs',
        'DEFAULT_LEVEL': 'INFO',
        'SENTRY_ENABLE': False,
        # todo: fetch from enviroment variable
        'SENTRY_URL': 'https://5c6820a5e1eb4c9f8f148c98ab67628d:5577c69b3f724e7f895e7c924bbd611e@sentry.io/190107'

    }
}
config_box = Box(configuration)