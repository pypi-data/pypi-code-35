#
# Copyright (c) 2016, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from django.conf import settings

# All next settings must be within the dictionary DIRECTAPPS, when you
# define them in the file settings.py
conf = getattr(settings, 'DIRECTAPPS', {})

# Function allowing access to all controllers of the application.
ACCESS_FUNCTION = conf.get('ACCESS_FUNCTION', 'directapps.access.staff')

# The name of the attribute in the model that is bound to the controller.
# By default is directapps_controller.
ATTRIBUTE_NAME = conf.get('ATTRIBUTE_NAME', 'directapps_controller')

# The options for the checksum compilation of the scheme. By default is "1".
CHECKSUM_VERSION = conf.get('CHECKSUM_VERSION', '1')

# Dictionary own controllers for models of third-party applications.
# By default is blank.
CONTROLLERS = conf.get('CONTROLLERS', {})

# The list of excluded applications. By default is blank.
EXCLUDE_APPS = conf.get('EXCLUDE_APPS', ())

# The list of excluded models. By default is blank.
EXCLUDE_MODELS = conf.get('EXCLUDE_MODELS', ())

# The options for creating JSON. By default indent as 2.
JSON_DUMPS_PARAMS = conf.get(
    'JSON_DUMPS_PARAMS', {'indent': 2, 'ensure_ascii': False}
)

# The options for masking all the fields with the name "password".
# By default is True.
MASK_PASSWORD_FIELDS = conf.get('MASK_PASSWORD_FIELDS', True)

# Class (as string for import) of the master controller, which is used by
# default. By default is None and uses internal class.
MASTER_CONTROLLER = conf.get('MASTER_CONTROLLER', None)

# The options for the using ISO time with microseconds into JSONEncoder.
# By default is False and JSONEncoder used ECMA-262 format.
# Turn on the format 'ISO' if all clients can parse the full time format
# and you need it for business logic.
USE_TIME_ISOFORMAT = conf.get('USE_TIME_ISOFORMAT', False)

# Valid request methods for the actions.
VALID_ACTIONS = {
    'get': ('GET',),
    'post': ('POST',),
    'create': ('POST',),
    'add': ('POST',),
    'put': ('POST', 'PUT'),
    'patch': ('POST', 'PATCH'),
    'update': ('POST', 'PUT', 'PATCH'),
    'delete': ('POST', 'DELETE'),
    # other actions can be any method, even 'GET'
}
VALID_ACTIONS.update(conf.get('VALID_ACTIONS', {}))

# The key by which data is received for search.
SEARCH_KEY = conf.get('SEARCH_KEY', 'q')

# The key by which the name of the field or column with a relation
# (for the "_fkey" action) is received from the client.
FOREIGN_KEY = conf.get('FOREIGN_KEY', 'f')

# The key by which the list of fields for rendering is received.
COLUMNS_KEY = conf.get('COLUMNS_KEY', 'c')

# The key by which sorting is accepted from the client.
ORDERING_KEY = conf.get('ORDERING_KEY', 'o')

# The key by which the limit of records is accepted from the client.
LIMIT_KEY = conf.get('LIMIT_KEY', 'l')

# The key by which the client receives the page number.
PAGE_KEY = conf.get('PAGE_KEY', 'p')

# Working limit of returned records.
LIMIT = conf.get('LIMIT', 10)

# The maximum limit of returned records, which does not allow to kill the
# server with huge data sets.
MAX_LIMIT = conf.get('MAX_LIMIT', 50)
