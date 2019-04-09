
from werkzeug.exceptions import *
from werkzeug.exceptions import abort

from .routing import *
from .context import request, g, G
from .application import Application as application, response

def run(view_func, **kwargs):
	"""runs a single route application"""
	application(route('/', view_func)).run(**kwargs)
