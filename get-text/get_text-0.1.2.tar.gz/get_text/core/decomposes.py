"""Алгаритмы для удаление не нужных частей сайта"""
import re
from textwrap import wrap

import click
from bs4 import BeautifulSoup
from get_text.core.config import Config


def some_elements(soup, article):
    """Удаление ненужных элементов со страницы

    :type response: requests.get
    :type soup: BeautifulSoup
    :type config: Config
    :type article: Article
    """
    role = article.config['exclude_elements']
    _delete(soup, role)
    for css_selector in role['css_selectors']:
        elements = soup.select(css_selector)
        for element in elements:
            element.decompose()


def script_and_style(soup, article):
    """Удаление скриптов и стилей

    :type response: requests.get
    :type soup: BeautifulSoup
    :type config: Config
    :type article: Article
    """
    for element in soup.find_all(['script', 'style']):
        element.decompose()


def _delete(soup, role):
    for element in soup.find_all([role['tags']]):
        element.decompose()

    for class_ in role['class']:
        for element in soup.find_all(class_=re.compile(class_)):
            element.decompose()

    for class_ in role['id']:
        for element in soup.find_all(id=re.compile(class_)):
            element.decompose()
    return soup


def get_title(soup, article):
    """Получение заголовка статьи

    :type response: requests.get
    :type soup: BeautifulSoup
    :type config: Config
    :type article: Article
    """
    title = soup.select('title')[0].get_text()

    t = soup.find('meta', attrs={"property": "og:title"})
    if t:
        title = t.attrs['content']
    else:
        title_selector = article.config['title']
        if title_selector:
            title = soup.select(title_selector)[0].get_text()
        else:
            titles = soup.find_all(article.config['general']['title']['tags'])
            if titles:
                title = titles[0].get_text()

    article.title = '\n'.join(wrap(title, article.config['width']))


def _replace_link_to_text(selector, article):
    if article.config['show_link']:
        for a in selector.findAll('a'):
            try:
                a.string = "{} -> [{}]".format(a.text, a['href'])
            except KeyError:
                continue


def get_content(soup, article):
    """Получение заголовка статьи

    :type response: requests.get
    :type soup: BeautifulSoup
    :type config: Config
    :type article: Article
    """
    content = ''

    content_selector = article.config['content']
    if content_selector:
        _replace_link_to_text(soup.select(content_selector)[0], article)
        content = soup.select(content_selector)[0].get_text().replace('<br>', '\n')
    else:
        for element in soup.find_all(
                article.config['general']['content']['tags']):
            if element.name == 'span':
                if not element.get_text().count('.') >= 2:
                    continue
            _replace_link_to_text(element, article)
            content += '{}\n\n'.format(element.get_text())

    article.content = '\n'.join(wrap(content, article.config['width'],
                                     replace_whitespace=False))
    if not content:
        click.echo("Не найдено тело статьи", color='red')


HOOKS = [script_and_style, some_elements, get_title, get_content]
