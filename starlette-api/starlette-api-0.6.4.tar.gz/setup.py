# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['starlette_api',
 'starlette_api.codecs',
 'starlette_api.codecs.http',
 'starlette_api.codecs.websockets',
 'starlette_api.components',
 'starlette_api.pagination']

package_data = \
{'': ['*'], 'starlette_api': ['templates/*']}

install_requires = \
['marshmallow>=3.0.0rc0,<4.0', 'starlette>=0.11']

extras_require = \
{'full': ['python-forge>=18.6,<19.0',
          'apispec>=0.39.0,<0.40.0',
          'pyyaml>=3.13,<4.0',
          'sqlalchemy>=1.2,<2.0',
          'databases>=0.1.9,<0.2.0']}

setup_kwargs = {
    'name': 'starlette-api',
    'version': '0.6.4',
    'description': 'Starlette API layer inherited from APIStar',
    'long_description': '<p align="center">\n  <img width="825" height="96" src="https://raw.githubusercontent.com/perdy/starlette-api/master/docs/images/logo.png" alt=\'Starlette API\'>\n</p>\n<p align="center">\n    <em>API power up for Starlette</em>\n</p>\n<p align="center">\n<a href="https://circleci.com/gh/perdy/starlette-api">\n    <img src="https://img.shields.io/circleci/project/github/perdy/starlette-api/master.svg" alt="Build Status">\n</a>\n<a href="https://codecov.io/gh/perdy/starlette-api">\n    <img src="https://codecov.io/gh/perdy/starlette-api/branch/master/graph/badge.svg" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/starlette-api/">\n    <img src="https://badge.fury.io/py/starlette-api.svg" alt="Package version">\n</a>\n</p>\n\n---\n\n**Documentation**: [https://starlette-api.perdy.io](https://starlette-api.perdy.io)\n\n---\n\n# Starlette API\n\nStarlette API aims to bring a layer on top of Starlette to provide a fast and easy way for building highly performant \nREST APIs.\n\nIt is production-ready and provides the following:\n\n* **Generic classes** for API resources that provides standard CRUD methods over SQLAlchemy tables.\n* **Schema system** based on [Marshmallow] that allows to **declare** the inputs and outputs of endpoints and provides \na reliable way of **validate** data against those schemas.\n* **Dependency Injection** that ease the process of managing parameters needed in endpoints. Starlette ASGI objects \nlike `Request`, `Response`, `Session` and so on are defined as components and ready to be injected in your endpoints.\n* **Components** as the base of the plugin ecosystem, allowing you to create custom or use those already defined in \nyour endpoints, injected as parameters.\n* **Auto generated API schema** using OpenAPI standard. It uses the schema system of your endpoints to extract all the \nnecessary information to generate your API Schema.\n* **Auto generated docs** providing a [Swagger UI] or [ReDoc] endpoint.\n* **Pagination** automatically handled using multiple methods such as limit and offset, page numbers...\n\n## Requirements\n\n* [Python] 3.6+\n* [Starlette] 0.10+\n* [Marshmallow] 3.0+\n\n## Installation\n\n```console\n$ pip install starlette-api\n```\n\n## Example\n\n```python\nfrom marshmallow import Schema, fields, validate\nfrom starlette_api.applications import Starlette\n\n\n# Data Schema\nclass Puppy(Schema):\n    id = fields.Integer()\n    name = fields.String()\n    age = fields.Integer(validate=validate.Range(min=0))\n\n\n# Database\npuppies = [\n    {"id": 1, "name": "Canna", "age": 6},\n    {"id": 2, "name": "Sandy", "age": 12},\n]\n\n\n# Application\napp = Starlette(\n    components=[],      # Without custom components\n    title="Foo",        # API title\n    version="0.1",      # API version\n    description="Bar",  # API description\n    schema="/schema/",  # Path to expose OpenAPI schema\n    docs="/docs/",      # Path to expose Swagger UI docs\n    redoc="/redoc/",    # Path to expose ReDoc docs\n)\n\n\n# Views\n@app.route("/", methods=["GET"])\ndef list_puppies(name: str = None) -> Puppy(many=True):\n    """\n    description:\n        List the puppies collection. There is an optional query parameter that \n        specifies a name for filtering the collection based on it.\n    responses:\n        200:\n            description: List puppies.\n    """\n    return [puppy for puppy in puppies if puppy["name"] == name]\n    \n\n@app.route("/", methods=["POST"])\ndef create_puppy(puppy: Puppy) -> Puppy:\n    """\n    description:\n        Create a new puppy using data validated from request body and add it \n        to the collection.\n    responses:\n        200:\n            description: Puppy created successfully.\n    """\n    puppies.append(puppy)\n    \n    return puppy\n```\n\n## Dependencies\n\nFollowing Starlette philosophy Starlette API reduce the number of hard dependencies to those that are used as the core:\n\n* [`starlette`][Starlette] - Starlette API is a layer on top of it.\n* [`marshmallow`][Marshmallow] - Starlette API data schemas and validation.\n\nIt does not have any more hard dependencies, but some of them are necessaries to use some features:\n\n* [`pyyaml`][pyyaml] - Required for API Schema and Docs auto generation.\n* [`apispec`][apispec] - Required for API Schema and Docs auto generation.\n* [`python-forge`][python-forge] - Required for pagination.\n* [`sqlalchemy`][SQLAlchemy] - Required for Generic API resources.\n* [`databases`][databases] - Required for Generic API resources.\n\nYou can install all of these with `pip3 install starlette-api[full]`.\n\n## Credits\n\nThat library started as an adaptation of [APIStar] to work with [Starlette], but a great amount of the code has been \nrewritten to use [Marshmallow] as the schema system.\n\n## Contributing\n\nThis project is absolutely open to contributions so if you have a nice idea, create an issue to let the community \ndiscuss it.\n\n[Python]: https://www.python.org\n[Starlette]: https://starlette.io\n[APIStar]: https://github.com/encode/apistar/tree/version-0.5.x\n[Marshmallow]: https://marshmallow.readthedocs.io/\n[Swagger UI]: https://swagger.io/tools/swagger-ui/\n[ReDoc]: https://rebilly.github.io/ReDoc/\n[pyyaml]: https://pyyaml.org/wiki/PyYAMLDocumentation\n[apispec]: https://apispec.readthedocs.io/\n[python-forge]: https://python-forge.readthedocs.io/\n[SQLAlchemy]: https://www.sqlalchemy.org/\n[databases]: https://github.com/encode/databases',
    'author': 'José Antonio Perdiguero López',
    'author_email': 'perdy@perdy.io',
    'url': 'https://github.com/PeRDy/starlette-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
