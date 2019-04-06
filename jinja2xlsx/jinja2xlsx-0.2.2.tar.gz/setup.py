# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jinja2xlsx']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.10,<3.0', 'openpyxl>=2.6,<3.0', 'requests-html>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'jinja2xlsx',
    'version': '0.2.2',
    'description': 'Convert jinja2-html to xlsx',
    'long_description': '# jinja2xlsx\n\nCreate xlsx-tables from html-tables\n\n## Example\n\nGiven html table str\n\nWhen render html to xlsx\n\nThen result xlsx has table values\n\n```python\nfrom jinja2xlsx import render_xlsx\nfrom openpyxl import Workbook\n\nhtml_str = """<!DOCTYPE html>\n<html lang="en">\n    <head>\n        <meta charset="UTF-8">\n        <title>Simple table</title>\n    </head>\n    <body>\n        <table>\n            <tbody>\n                <tr>\n                    <td>1</td>\n                    <td>2</td>\n                </tr>\n                <tr>\n                    <td>3</td>\n                    <td>4</td>\n                </tr>\n            </tbody>\n        </table>\n    </body>\n</html>"""\n\nworkbook: Workbook = render_xlsx(html_str)\nassert tuple(workbook.active.values) == ((1, 2), (3, 4))\n```\n\n## Publish to PyPI\n\n```shell\npoetry publish --build\n```',
    'author': 'potykion',
    'author_email': 'potykion@gmail.com',
    'url': 'https://github.com/potykion/jinja2xlsx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
