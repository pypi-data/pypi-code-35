# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['udp_filetransfer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'udp-filetransfer',
    'version': '0.2.0',
    'description': 'Reliable filetransfer over UDP',
    'long_description': '# UDP Filetransfer\nFast file transfer over UDP Broadcast.\n\n## Install (CLI)\n### From PyPI\n```bash\npip install udp-filetransfer\n```\n### From Git\n```bash\ngit clone https://gitlab.com/Trickster-Animations/udp-filetransfer.git\ncd udp-filetransfer\npoetry || pip install poetry\npoetry install\n```\nNow, you can use it through poetry:  \n`poetry run python -m udp_filetransfer`  \nTo use it from system python, do:\n```bash\npoetry build\ncd dist\npip3 install *.whl\n```\nNow, you can use it by running:  \n`python3 -m udp_filetransfer`\n\n## Usage (CLI)\nTo send a file:\n```\npython3 -m udp_filetransfer send [filepath]\n```\nTo receive a file:\n```\npython3 -m udp_filetransfer receive\n```\nNote: The receiver has to be started first. \n\n## Install (Dependency)\nJust add the `udp-filetransfer` package, like with any other dependency.\n\n## Usage (Dependency)\n```py\n# receive.py\nimport udp_filetransfer\noutput = udp_filetransfer.receive()\nprint(output)\n```\n```py\n# send.py\nfrom sys import argv\nimport udp_filetransfer\nudp_filetransfer.send(argv[1])\n```\nNote: Just like with CLI, the receiver needs to be started first. Otherwise the sender will hang indefinitely. \n\n\n## Credits\nPackage maintained by Trickster Animations',
    'author': 'golyalpha',
    'author_email': 'golyalpha@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
