import logging
import os

from drongo.app import Drongo
from drongo.addons.database import Database
from drongo.auth.module import Auth

from .middleware import NamespaceMiddleware

LOGGING_FORMAT = (
    '\033[36m%(asctime)-24s \033[34m%(name)-16s '
    '\033[32m%(levelname)-8s \033[97m%(message)s\033[39m'
)
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)


app = Drongo()

Database(
    app,
    _id='main',
    type=os.environ.get('DRONGO_DB_TYPE', 'postgres'),
    host=os.environ.get('DRONGO_DB_HOST', 'postgres'),
    port=int(os.environ.get('DRONGO_DB_PORT', '5432')),
    name=os.environ.get('DRONGO_DB_NAME', 'drongo'),
    user=os.environ.get('DRONGO_DB_USER', 'drongo'),
    password=os.environ.get('DRONGO_DB_PASSWORD', 'drongo')
)

Auth(
    app,
    database='main'
)
app.add_middleware(NamespaceMiddleware())
