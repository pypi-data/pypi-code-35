
from inspect import isgenerator
from typing import Iterable, Callable, Generator, Any


class Stack(list):

	def add(self, middleware: Iterable[Callable]):
		for gen in create_stack(middleware):
			self.append(gen)

	def send(self, value: Any):
		return notify_stack(self, value = value)

	def throw(self, exception: Exception):
		return notify_stack(self, exception = exception)


def create_stack(
	middleware: Iterable[Callable]
) -> Iterable[Generator]:
	for func in middleware:
		gen = func()
		if isgenerator(gen):
			gen.send(None)
			yield gen

def notify_stack(
	stack: Iterable[Generator],
	value: Any = None,
	exception: Exception = None
):
	"""
    Errors should never pass silently.
    Unless explicitly silenced.
    """
	for gen in reversed(stack):
		try:
			if exception != None:
				value2 = gen.throw(exception)
			else:
				value2 = gen.send(value)
		except StopIteration:
			exception = None
		except Exception as new_exception:
			exception = new_exception
			value = None
		else:
			exception = None
			if value2 != None:
				value = value2
	if exception != None:
		raise exception
	return value
