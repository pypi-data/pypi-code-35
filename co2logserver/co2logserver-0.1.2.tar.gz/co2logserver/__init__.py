# system modules
import os
import logging

# internal modules
from co2logserver.app import app
from co2logserver import index, download, upload
from co2logserver.version import __version__

# external modules

# gunicorn expects a variable called 'application'
application = app
