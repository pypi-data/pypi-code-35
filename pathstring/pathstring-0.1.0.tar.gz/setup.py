# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['pathstring']
setup_kwargs = {
    'name': 'pathstring',
    'version': '0.1.0',
    'description': 'String with path operations.',
    'long_description': 'pathstring is a very small module that provides a string class\nwhich supports path operations. Technically, it subclasses ``str``\nand delegates path related operations to ``pathlib.Path``.\n\nDifferences from pathlib paths are:\n\n- Paths are strings, no need to cast them to strings.\n\n- It adds an ``rmtree`` operation which invokes ``shutil.rmtree``.\n  Actually, since paths are also strings, in addition to ``path.rmtree()``,\n  ``shutil.rmtree(path)`` will also work.\n\n- It adds a ``strict`` parameter to the ``relative_to`` operation\n  which, when set to ``False`` will also navigate up in the hierarchy.\n\nLicense\n-------\n\nCopyright (C) 2019 H. Turgut Uyar <uyar@tekir.org>\n\npathstring is released under the BSD license. Read the included\n``LICENSE.txt`` file for details.\n',
    'author': 'H. Turgut Uyar',
    'author_email': 'uyar@tekir.org',
    'url': 'https://github.com/uyar/pathstring',
    'py_modules': modules,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
