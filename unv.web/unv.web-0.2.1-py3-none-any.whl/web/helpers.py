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

    return web.Response(
        text=template.render(context),
        status=status, charset='utf-8',
        content_type='text/html'
    )


def url_for_static(path, private=False, with_hash=False):
    scope = 'private' if private else 'public'
    static_url = SETTINGS['static'][scope]['url']
    static_path = SETTINGS['static'][scope]['path']
    real_path = pathlib.Path(static_path) / path.lstrip('/')
    hash_ = ''
    if with_hash:
        hash_ = '?hash={}'.format(calc_crc32_for_file(real_path))
    path = path.replace(static_path, '', 1).lstrip('/')
    return f"{static_url}/{path}{hash_}"


def url_with_domain(path):
    return '{}{}'.format(SETTINGS['domain'], path)


def make_url_for_func(app):
    def url_for(route, with_domain=False, **parts):
        parts = {key: str(value) for key, value in parts.items()}
        url = app.router[route].url_for(**parts)
        if with_domain:
            url = url_with_domain(url)
        return url
    return url_for


def inline_static_from(path, private=False):
    scope = 'private' if private else 'public'
    static_path = pathlib.Path(SETTINGS['static'][scope]['path'])
    with (static_path / path).open('r') as f:
        return f.read().replace("\n", "")
