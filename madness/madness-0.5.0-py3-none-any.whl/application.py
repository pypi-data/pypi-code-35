
from dataclasses import replace
from typing import Callable, List
from functools import partial

from more_itertools import collapse
from werkzeug.routing import Map
from werkzeug.serving import run_simple
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Request

from .context import local, context, local_manager, Context
from .wrappers import response
from .routing import routes
from .middleware import create_stack, notify_stack
from .routines import run_in_kwargs

def force_type_middleware():
	"""...
	similar to Flask's force_type
	allows returning tuple

	body
	body, status
	body, status, headers
	"""
	obj = yield
	if isinstance(obj, (str, bytes)):
		yield response([obj])
	elif isinstance(obj, tuple):
		try:
			body, status, headers = obj
		except ValueError:
			body, status = obj
			headers = {}
		if isinstance(body, (str, bytes)):
			body = [body]
		yield response(body, status=status, headers=headers)


def abort_middleware():
	"""support for abort()"""
	global HTTPException
	try:
		yield
	except HTTPException as response:
		yield response


def create_app(*args, middleware: List[Callable] = []) -> Callable:
	"""allows middleware to catch routing errors, returns WSGI application"""
	global Map, local_manager

	endpoints = {}
	rules = []
	for i, route in enumerate(routes(*args)):
		endpoints[i] = route
		rule = route.as_rule(endpoint=i)
		rules.append(rule)

	url_map = Map(rules)

	middleware = tuple(
		partial(run_in_kwargs, context, func)
		for func in middleware
	)

	@local_manager.make_middleware
	def application(environ, start_response):
		global local, force_type_middleware, create_stack, notify_stack, context, Request, Context
		nonlocal middleware, url_map, endpoints

		# initialize thread locals
		local.request = Request(environ)
		local.context = Context() # user managed context

		stack = list(
			create_stack((
				abort_middleware,
				force_type_middleware,
				*middleware,
				force_type_middleware
			))
		)

		try:
			# route the request, may raise HTTPException such as NotFound
			urls = url_map.bind_to_environ(environ)
			endpoint, kwargs = urls.match()
			for key, value in kwargs.items():
				setattr(local.context, key, value)
			route = endpoints[endpoint]
			# add the route's middleware to the stack
			stack.extend(create_stack(route.middleware))
			response = route.view_func()

		# allow the stack to swap out the response application
		except Exception as exception:
			response = notify_stack(stack, exception = exception)
		else:
			response = notify_stack(stack, value = response)

		# allow stack to handle errors that happen while streaming the response
		try:
			yield from response(environ, start_response)
			# for chunk in response(environ, start_response):
			# 	print('send', len(chunk))
			# 	yield chunk
		except Exception as exception:
			notify_stack(stack, exception=exception)
		else:
			notify_stack(stack)

	return application


class Application():
	""""""

	def __init__(self, *args, **kwargs):
		super().__init__()
		self.wsgi_app = create_app(*args, **kwargs)

	def __call__(self, environ, start_response):
		return self.wsgi_app(environ, start_response)

	def run(
		self,
		host: str = '127.0.0.1',
		port: int = 9090,
		debug: bool = True
	):
		run_simple(
			host,
			port,
			self.wsgi_app,
			use_reloader = debug,
			use_debugger = False,
			use_evalex = False,
		)
