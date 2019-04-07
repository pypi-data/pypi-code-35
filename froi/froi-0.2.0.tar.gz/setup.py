# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['froi']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.0,<2.0']

setup_kwargs = {
    'name': 'froi',
    'version': '0.2.0',
    'description': 'A Flask wrapper to easily handle routes defined as Python native objects',
    'long_description': "Froi (Flask Router Object Interface)\n====================================\n\nA wrapper for Flask's native routing as a form of template.\nRoutes will be defined as objects to easily define domains.\n\n.. code-block:: python\n\n    # Inside some route object\n    from froi import Froi\n    class SomeRoute(Froi):\n        def __init__(self, app):\n            super().__init__(app, 'SomeRoute', '/some_route')\n\n        def install(self):\n            # define a get route on base\n            self.get().route(view_func=sample_fxn_1)\n\n            # define a post\n            self.post().route('/do_something', view_func=sample_fxn_2)\n\n            # define a put\n            self.put().route('/edit_something', view_func=sample_fxn_3)\n\n            # define a delete\n            self.delete().route('/delete_something', view_func=sample_fxn_4)\n\n    # Inside your server handler\n    from flask import Flask\n    from some_route import SomeRoute\n    app = Flask(config.APP_NAME)\n    SomeRoute(app).install()\n    app.run()\n\nIf you want a RESTful pattern to handle the routes, you can omit defining the `install` function.\n\n.. code-block:: python\n\n    from froi import Froi\n    class SomeRoute(Froi):\n        def __init__(self, app):\n            super().__init__(app, 'SomeRoute', '/some_route')\n\nThis will automatically create a `GET`, `POST`, `PUT`, and `DELETE` endpoints.\n\nThis feature though is a work in progress and may not work as expected.\n",
    'author': 'Almer Mendoza',
    'author_email': 'atmalmer23@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
