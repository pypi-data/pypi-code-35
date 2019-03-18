import jinja2

from aiohttp import web

from unv.app.settings import SETTINGS as APP_SETTINGS

from .helpers import (
    url_for_static, url_with_domain, inline_static_from,
    make_url_for_func, make_url_with_domain_for_func,
)
from .settings import SETTINGS


def setup_jinja2(app: web.Application):
    settings = SETTINGS.get('jinja2', {})
    if not settings.get('enabled'):
        return

    settings['loader'] = jinja2.ChoiceLoader([
        jinja2.PackageLoader(package)
        for package in APP_SETTINGS['components']
    ])
    if 'jinja2.ext.i18n' not in settings.setdefault('extensions', []):
        settings['extensions'].append('jinja2.ext.i18n')

    app['jinja2'] = jinja2.Environment(**settings)
    app['jinja2'].globals.update({
        'url_for_static': url_for_static,
        'inline_static_from': inline_static_from,
        'url_with_domain': url_with_domain,
        'url_for': make_url_for_func(app),
        'url_with_domain_for': make_url_with_domain_for_func(app),
        'DEBUG': not APP_SETTINGS['debug'],
    })


def setup(app: web.Application):
    setup_jinja2(app)
