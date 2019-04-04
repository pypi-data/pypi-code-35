
from dataclasses import dataclass, field, replace
from typing import Callable
from functools import partial, wraps

from more_itertools import collapse
from werkzeug.routing import Rule

from .routines import run_in_kwargs
from .context import context

__all__ = (
	'routes',
	'route',
	'get', 'post', 'put', 'delete', 'patch', 'options',
	'index', 'new', 'create', 'show', 'edit', 'update', 'destroy'
)


@dataclass
class Route():
	path: str
	view_func: Callable
	methods: list = field(default_factory=list)
	defaults: dict = field(default_factory=dict)
	middleware: list = field(default_factory=list)

	def as_rule(self, **kwargs):
		return Rule(
			self.path,
			methods = self.methods or None,
			defaults = self.defaults,
			**kwargs
		)

	def mount(self, path=None):
		return replace(self, path = f'{path}{self.path}' if path else self.path)

	def insert_middleware(self, middleware):
		return replace(self, middleware = [*middleware, *self.middleware])

	def add_methods(self, methods):
		return replace(self, methods = list(set([*methods, *self.methods])))

	def add_defaults(self, defaults):
		return replace(self, defaults = {**defaults, **self.defaults})

def routes(
	*args,
	path: str = None,
	middleware: list = [],
	methods: list = [],
	defaults: dict = {}
):
	"""DRY: create routes with similar configuration"""
	return tuple(
		route\
			.insert_middleware(middleware)\
			.mount(path)\
			.add_methods(methods)\
			.add_defaults(defaults)
		for route in collapse(args)
	)



def route(*args, **kwargs):
	""""""
	if len(args) == 1:
		view_func = args[0]
		path = f'/{view_func.__name__}'
	elif len(args) == 2:
		path, view_func = args
	else:
		raise ValueError(f'route() expected 1-2 args, got {len(args)}')
	return Route(
		path = path,
		view_func = wraps(view_func)(lambda: run_in_kwargs(context, view_func)),
		**kwargs
	)


# some standard http methods
get = partial(route, methods=['GET'])
post = partial(route, methods=['POST'])
put = partial(route, methods=['PUT'])
delete = partial(route, methods=['DELETE'])
patch = partial(route, methods=['PATCH'])
options = partial(route, methods=['OPTIONS'])

# the 7 RESTful routes
index = partial(get, '/')
new = partial(get, '/new')
create = partial(post, '/')
show = partial(get, '/<id>')
edit = partial(get, '<id>/edit')
update = partial(route, '/<id>', methods=['PATCH', 'PUT'])
destroy = partial(delete, '/<id>')
