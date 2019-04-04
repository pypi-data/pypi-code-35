
from inspect import isgenerator

def create_stack(middleware):
	for func in middleware:
		gen = func()
		if isgenerator(gen):
			gen.send(None)
			yield gen

def notify_stack(stack, value=None, exception=None):
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
