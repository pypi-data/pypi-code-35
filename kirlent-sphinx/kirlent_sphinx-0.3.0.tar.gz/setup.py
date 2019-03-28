# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['kirlent_sphinx']

package_data = \
{'': ['*'],
 'kirlent_sphinx': ['templates/kirlent_impressjs/*',
                    'templates/kirlent_impressjs/static/css/*',
                    'templates/kirlent_impressjs/static/js/*',
                    'templates/kirlent_revealjs/*',
                    'templates/kirlent_revealjs/static/*',
                    'templates/kirlent_revealjs/static/css/*',
                    'templates/kirlent_revealjs/static/css/print/*',
                    'templates/kirlent_revealjs/static/js/*',
                    'templates/kirlent_revealjs/static/lib/js/*',
                    'templates/kirlent_revealjs/static/plugin/multiplex/*',
                    'templates/kirlent_revealjs/static/plugin/notes-server/*',
                    'templates/kirlent_revealjs/static/plugin/notes/*',
                    'templates/kirlent_revealjs/static/plugin/zoom-js/*',
                    'templates/styles/*']}

install_requires = \
['sphinx>=1.8,<2.0']

setup_kwargs = {
    'name': 'kirlent-sphinx',
    'version': '0.3.0',
    'description': 'Sphinx extension for slides and extended tables.',
    'long_description': 'kirlent_sphinx is a Sphinx extension that is primarily meant to be used with\nthe `Kırlent`_ educational content management system, although it can be used\nas a regular Sphinx extension.\n\nFeatures\n--------\n\nkirlent_sphinx provides the following components:\n\n- An extended ``table`` directive derived from the `Cloud Sphinx Theme`_\n  project.\n\n- A ``slide`` directive and corresponding HTML themes using `RevealJS`_\n  or `ImpressJS`_.\n\nGetting started\n---------------\n\nYou can install kirlent_sphinx with pip::\n\n  pip install kirlent_sphinx\n\nTo enable it in your project, make the following changes in ``conf.py``:\n\n- Add ``kirlent_sphinx`` to extensions::\n\n    extensions = ["kirlent_sphinx"]\n\n- Set the theme to use revealjs or impressjs using one of the below lines::\n\n    html_theme = "kirlent_revealjs"\n    html_theme = "kirlent_impressjs"\n\n- Disable index generation::\n\n    html_use_index = False\n\nUsage\n-----\n\nFor the extended ``table`` directive, consult the documentation\nof the `table_styling`_ extension of the `Cloud Sphinx Theme`_ project.\n\nThe ``slide`` directives can support most of the ``data-`` attributes\nas described in the documentations of the `RevealJS`_ and `ImpressJS`_\nprojects.\n\nThe themes include `Tailwind`_ utility classes for styling::\n\n  .. slide:: Slide title\n\n     .. container:: columns\n\n        .. container:: column w-1/3 bg-blue-lighter\n\n           - item 1a\n           - item 1b\n\n        .. container:: column bg-red-lighter\n\n           - item 2\n\n     .. speaker-notes::\n\n        some extra explanation\n\nLicense\n-------\n\nCopyright (C) 2019 H. Turgut Uyar <uyar@tekir.org>\n\nkirlent_sphinx is released under the BSD license. Read the included\n``LICENSE.txt`` file for details.\n\nkirlent_sphinx contains code derived from the `Cloud Sphinx Theme`_ project\nwhich is released under the BSD license. Read the included\n``LICENSE_cloud_spheme.txt`` file for details.\n\nkirlent_sphinx contains code derived from the `sphinxjp.themes.revealjs`_\nproject which is released under the MIT license. Read the included\n``LICENSE_sphinxjp.themes.revealjs.txt`` file for details.\n\nkirlent_sphinx contains code from the `RevealJS`_ project which is\nreleased under the MIT license. Read the included ``LICENSE_revealjs.txt``\nfile for details.\n\nkirlent_sphinx contains code from the `ImpressJS`_ project which is\nreleased under the MIT license. Read the included ``LICENSE_impressjs.txt``\nfile for details.\n\nkirlent_sphinx contains code from the `Tailwind`_ project which is\nreleased under the MIT license. Read the included ``LICENSE_tailwind.txt``\nfile for details.\n\n.. _Kırlent: https://gitlab.com/tekir/kirlent/\n.. _Cloud Sphinx Theme: https://cloud-sptheme.readthedocs.io/en/latest/\n.. _table_styling: https://cloud-sptheme.readthedocs.io/en/latest/lib/cloud_sptheme.ext.table_styling.html\n.. _sphinxjp.themes.revealjs: https://github.com/tell-k/sphinxjp.themes.revealjs\n.. _RevealJS: https://revealjs.com/\n.. _ImpressJS: https://impress.js.org/\n.. _Tailwind: https://tailwindcss.com/\n',
    'author': 'H. Turgut Uyar',
    'author_email': 'uyar@tekir.org',
    'url': 'https://gitlab.com/tekir/kirlent_sphinx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
