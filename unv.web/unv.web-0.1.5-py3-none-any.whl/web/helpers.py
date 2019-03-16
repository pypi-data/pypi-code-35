import pathlib

from aiohttp import web

from unv.utils.files import calc_crc32_for_file

from .settings import SETTINGS


async def render_template(
        request, template_name, context=None, context_processors=None,
        status=web.HTTPOk.status_code):
    context = context or {}
    context_processors = context_processors or {}
    template = request.app['jinja2'].get_template(template_name)

    for key, processor in context_processors.items():
        if key not in context:
            value = await processor(request)
            context[key] = value

    text = template.render(context)

    return web.Response(
        text=text, status=status, charset='utf-8', content_type='text/html')


def url_for_static(path):
    real_path = pathlib.Path(SETTINGS['static']['paths']['public'])
    real_path = real_path / path.lstrip('/')
    hash_ = '?hash={}'.format(calc_crc32_for_file(real_path))
    path = path.replace(SETTINGS['static']['paths']['public'], '')
    return ''.join([SETTINGS['static']['urls']['public'], path, hash_])


def url_for_private_static(path):
    real_path = pathlib.Path(SETTINGS['static']['paths']['private'])
    real_path = real_path / path.lstrip('/')
    hash_ = '?hash={}'.format(calc_crc32_for_file(real_path))
    path = path.replace(SETTINGS['static']['paths']['private'], '')
    return ''.join([SETTINGS['static']['urls']['private'], path, hash_])


def url_with_domain(path):
    return '{}://{}{}'.format(SETTINGS['protocol'], SETTINGS['domain'], path)


def make_url_for_func(app):
    def url_for(route, **parts):
        parts = {key: str(value) for key, value in parts.items()}
        return app.router[route].url_for(**parts)
    return url_for


def make_url_with_domain_for_func(app):
    def url_with_domain_for(route, **parts):
        url = app.router[route].url_for(**parts)
        return url_with_domain(str(url))
    return url_with_domain_for


def inline_static_from(path):
    static_path = pathlib.Path(SETTINGS['static']['paths']['public'])
    with open(str(static_path / path.lstrip('/')), 'r') as f:
        return f.read().replace("\n", "")
