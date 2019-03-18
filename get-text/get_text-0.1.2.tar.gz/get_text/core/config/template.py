"""Шаблон по умолачние.

Шаблон будет рендрить Jinga2
"""


DEFAULT_TEMPLATE_NEWS = """{{ news_title }}

{{ news_content }}

{% for _ in range(0, config['width']) %}-{% endfor %}

"""
