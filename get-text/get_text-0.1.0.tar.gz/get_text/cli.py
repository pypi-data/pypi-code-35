# -*- coding: utf-8 -*-

"""Console script for get_text."""
import sys
import click
import requests

from get_text.core.get_article import Article
from get_text.helper.settings import load_setting_file


@click.command()
@click.option('--settings', '-s',
              type=click.Path(exists=True),
              help='Путь на конфигурационный yaml файл',
              default=None,
              )
@click.argument('url')
def main(url=None, settings=None):
    """Console script for get_text."""
    response = requests.get(url)
    if settings is not None:
        settings = load_setting_file(settings)
    article = Article(response.text, url, settings)
    article.run_parse()
    article.save()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
