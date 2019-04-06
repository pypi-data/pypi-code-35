import logging
import logging.config
import pkg_resources
import json
import os

from flask import Flask, render_template, session
from werkzeug.wsgi import DispatcherMiddleware

from .config import load, Mode
from .db import Database
from .models import User
from .controllers.api import add_api_controllers
from .controllers.auth import add_auth_controllers
from .auth import is_logged_in
from .tools import get_all_project_data
from .javascript_libraries import javascript_libraries
from .changelog import CHANGELOG_FILE_PATH

frontend = Flask('pabu')
api = Flask('api')
auth = Flask('auth')

secret_key = 'j32bd4kj2d4jkvgh23jk4hvgj23hg4ekjhg'

frontend.secret_key = secret_key
auth.secret_key = secret_key
api.secret_key = secret_key

wsgi_application = DispatcherMiddleware(frontend, {
    '/api': api,
    '/auth': auth,
})

config = load()

if not config:
    print('no config!')
    exit(1)

for name, cfg in config.auth.items():
    auth.config[(name + '_client_id').upper()] = cfg.id
    auth.config[(name + '_client_secret').upper()] = cfg.secret

logging.config.dictConfig(config.logger)

logger = logging.getLogger(__name__)

logger.info("App start")

db = Database(str(config.database))

changelog = []

if os.path.isfile(CHANGELOG_FILE_PATH):
    with open(CHANGELOG_FILE_PATH) as f:
        changelog = json.load(f)
else:
    if config.mode == Mode.PRODUCTION:
        logger.error("Changelog is missing!")
    else:
        logger.info("Changelog is missing.")

@frontend.route('/')
@frontend.route('/<path:path>')
def index(path = None):

    return render_template('index.html',
        data = {
            'changelog': changelog,
            'userInfo': session.get('user_info'),
            'isLoggedIn': is_logged_in(),
            'authBackendNames': list(config.auth.keys()),
            'version': pkg_resources.get_distribution('pabu').version,
            'initialData': get_all_project_data(db) if is_logged_in() else None,
        },
        javascript_libraries = javascript_libraries[config.mode],
    )

add_api_controllers(api, db)
add_auth_controllers(auth, config, db)
