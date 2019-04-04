
from werkzeug.exceptions import *
from werkzeug.exceptions import abort

from .routing import *
from .wrappers import response
from .context import request, context as g
from .application import Application as application

def run(view_func, **kwargs):
	"""runs a single route application"""
	application(route('/', view_func)).run(**kwargs)
