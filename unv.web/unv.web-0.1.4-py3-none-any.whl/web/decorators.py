import functools

import ujson as json

from aiohttp import web


def as_json(f):
    """Return json response from passed dict result."""
    @functools.wraps(f)
    async def wrapper(request, *args, **kwargs):
        data = await f(request, *args, **kwargs)
        return web.json_response(data, dumps=json.dumps)
    return wrapper


def as_json_method(f):
    """Return json response from passed dict result."""
    @functools.wraps(f)
    async def wrapper(self, request, *args, **kwargs):
        data = await f(self, request, *args, **kwargs)
        return web.json_response(data or {}, dumps=json.dumps)
    return wrapper


def cached(f):
    @functools.wraps(f)
    async def wrapper(request, *args, **kwargs):
        key = (f.__name__, request.path)
        if key in request.app['cache']:
            return request.app['cache'][key]
        result = await f(request, *args, **kwargs)
        request.app['cache'][key] = result
        return result
    return wrapper


def render(template_name: str, context_processors: dict = None, status = 200):
    """Render jinja2 template by given name and custom context processors."""
    context_processors = context_processors or {}

    def decorator(f):
        @functools.wraps(f)
        async def wrapper(request, *args, **kwargs):
            context = await f(request, *args, **kwargs)
            template = request.app['jinja2'].get_template(template_name)

            for key, processor in context_processors.items():
                if key not in context:
                    value = await processor(request)
                    context[key] = value

            context['request'] = request
            text = template.render(context)

            return web.Response(
                text=text, status=status, charset='utf-8',
                content_type='text/html'
            )
        return wrapper

    return decorator


def render_method(
        template_name: str, context_processors: dict = None, status = 200):
    """Render jinja2 template by given name and custom context processors."""
    context_processors = context_processors or {}

    def decorator(f):
        @functools.wraps(f)
        async def wrapper(self, request, *args, **kwargs):
            context = await f(self, request, *args, **kwargs)
            template = request.app['jinja2'].get_template(template_name)

            for key, processor in context_processors.items():
                if key not in context:
                    value = await processor(request)
                    context[key] = value

            text = template.render(context)

            return web.Response(
                text=text, status=status, charset='utf-8',
                content_type='text/html'
            )
        return wrapper

    return decorator
