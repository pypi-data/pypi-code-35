
from dataclasses import replace
from typing import Callable, List
from functools import partial
from collections import OrderedDict

from more_itertools import collapse, partition
from werkzeug.routing import Map
from werkzeug.serving import run_simple
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Request, Response as response

from .context import local, g, local_manager, G, request
from .routing import routes, Route
from .middleware import create_stack, notify_stack, Stack


def abort_middleware():
	"""support for abort()"""
	global HTTPException
	try:
		yield
	except HTTPException as response:
		yield response


def create_app(
	*args,
	g_factory: Callable = G,
	strict_slashes = False,
	request_class = Request
) -> Callable:
	"""convert routes into a WSGI application
	middleware added here is initilized BEFORE routing, so it can catch NotFound
	"""
	global Map, local_manager

	middleware, args = partition(
		lambda obj: isinstance(obj, Route),
		collapse(args)
	)

	endpoints = OrderedDict(enumerate(routes(*args)))
	rules = [
		route.as_rule(
			endpoint = i,
			strict_slashes = strict_slashes if route.strict_slashes is None else route.strict_slashes
		)
		for i, route in endpoints.items()
	]
	url_map = Map(rules)

	middleware = [
		abort_middleware,
		#force_type_middleware,
		*middleware,
		#force_type_middleware
	]

	@local_manager.make_middleware
	def application(environ, start_response):
		global local, force_type_middleware, Stack, Request
		nonlocal middleware, url_map, endpoints, g_factory, request_class

		print('NEW REQUEST', environ)

		# initialize thread locals
		environ['madness.request'] = local.request = request_class(environ)
		environ['madness.stack'] = stack = Stack()
		environ['madness.g'] = local.g = g_factory()

		try:

			try:
				# route the request, may raise HTTPException such as NotFound
				urls = url_map.bind_to_environ(environ)
				endpoint, kwargs = urls.match()

			except HTTPException as exception:
				# initialize the stack with application middleware
				stack.add(middleware)
				raise exception

			else:
				# apply defaults
				for key, value in kwargs.items():
					setattr(local.g, key, value)

				# initialize the stack with application middleware
				stack.add(middleware)

				route = endpoints[endpoint]

				# add the route's middleware to the stack
				stack.add(route.middleware)

				response = route.view_func()

		# allow the stack to swap out the response application
		except Exception as exception:
			response = stack.throw(exception)
		else:
			response = stack.send(response)

		# allow stack to handle errors that happen while streaming the response
		try:
			yield from response(environ, start_response)
		except Exception as exception:
			stack.throw(exception)
		else:
			stack.send(None)

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
