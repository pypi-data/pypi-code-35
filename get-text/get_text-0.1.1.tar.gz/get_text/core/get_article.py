import os
from textwrap import shorten

import click
from bs4 import BeautifulSoup
from jinja2 import Template
from urllib3 import get_host

from get_text.core.config import Config
from get_text.core.decomposes import HOOKS
from get_text.helper.url_convertor import url_query_convert_to_path


class Article:
    hooks = HOOKS
    config = None  # type: Config
    soup = None  # type: BeautifulSoup
    title = ''
    content = ''

    def __init__(self, html_text, url, settings=None):
        self._url = url
        self.config = Config(get_host(url)[1], settings)
        self.soup = BeautifulSoup(html_text, features='html.parser')

    def run_parse(self):
        """Запуск "хуков".
        Хуки - это функции где выполняеться определенные
         действии над текстом полученный со страницы.
         Например: Полчение заголовка статьи, удаление рекламы и.т.д"""
        for hook in self.hooks:
            hook(self.soup, self)
        return self

    def template_active(self):
        """Применение шаблона jinga2."""
        template = Template(self.config['template'])
        return template.render(
            news_title=self.title, news_content=self.content, config=self.config
        )

    def save(self):
        """Сохранение текста полученный с веб страницы."""
        if not self.content or not self.title:
            click.echo("Не удалось найти тело статьи или заголовок\n"
                       "Вы можете указать точные css селекторы "
                       "на тело и заголовок"
                       " для конкретного сайта. Подробнее [https://github.com"
                       "/NMelis/get_text/blob/master/docs/usage.rst]",
                       color='red')
            return False
        path, file_name = url_query_convert_to_path(self._url,
                                                    self.config['file_type'])
        current_dir = os.getcwd()
        full_path_dir = os.path.join(current_dir, path)
        if not os.path.exists(full_path_dir):
            os.makedirs(full_path_dir)

        full_path = os.path.join(full_path_dir, file_name)
        with open(full_path, 'w') as f:
            f.write(self.template_active())
        click.echo('Текст успешно получен с сайта: Файл сохранене: \n{}'.format(
            full_path
        ), color='green')

    def __str__(self):
        return shorten(self.title, 10)
