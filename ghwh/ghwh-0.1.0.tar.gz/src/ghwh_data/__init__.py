import json

from jinja2 import Environment
from jinja2 import PackageLoader


_env = Environment(loader=PackageLoader(__name__, "payloads"))


def render(template, context=None):
    tmpl = _env.get_template(template + ".j2")
    return tmpl.render(**(context or {}))


def load(template, context=None):
    rendered = render(template, context)
    if template.endswith(".json"):
        rendered = json.loads(rendered)
    return rendered
