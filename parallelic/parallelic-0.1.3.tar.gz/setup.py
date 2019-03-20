# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['parallelic', 'parallelic.manager', 'parallelic.runner']

package_data = \
{'': ['*'], 'parallelic': ['util/*']}

install_requires = \
['psycopg2-binary>=2.7,<3.0',
 'sqlobject>=3.7,<4.0',
 'toml>=0.10.0,<0.11.0',
 'udp-filetransfer>=0.1.2,<0.2.0']

entry_points = \
{'console_scripts': ['parallelic = parallelic:main']}

setup_kwargs = {
    'name': 'parallelic',
    'version': '0.1.3',
    'description': 'Hyper-parallel multi-node task execution engine',
    'long_description': "# Parallelic\nParallelic is a hyperparallel multi-node task execution engine with shared data and wokspace capabilities.\n\n## Note of warning\nParallelic is not a containerization/sandboxing engine. It does not constitute a full task isolation, and provides no guarantee of such. That may change in the future, and feel free to contribute your code towards that goal, but in the mean time, keep this in consideration when giving access to a Parallelic system to third parties.\n\n## Installation\n### From git\n  1. Clone the git repo locally.\n  2. Download python3(.7) and corresponding pip\n  3. Install [Poetry](https://poetry.eustace.io)\n  4. Run `poetry install` to create a virtualenv and install dependencies  \n  At this point, you can use parallelic through   \n  `poetry run parallelic`\n  5. Run `poetry build` to build a wheel\n  6. Run `pip install dist/parallelic-[version]-py3-none-any.whl`  \n  Now you can use parallelic without poetry:  \n  `python -m parallelic`\n### From pip\n  1. Run `pip install parallelic`\n\n## Usage\n### Running a task\nTo run an already defined task, you upload the task package (a zipped up task root directory) via the Parallelic WebUI, or Parallelic CLI client, to the Parallelic manager instance.   \nYou may need to provide access credentials before being allowed to upload the task package, as per your Parallelic system configuration.  \nFrom there, the Parallelic manager instance will take care of everything else.\n\n### Defining a task\nThe task root contains a `task.toml` file, that contains metadata required for the manager to set up and prepare resources for the compute nodes in order to run the particullar task.  \nIf the task requires no additional files, the task definition can be only the `task.toml` file.\n\nThe directory tree doesn't follow a particullar convention, and can be different from task to task. The task definition file should contain a section where the entrypoint and working directory are defined. Both the entrypoint and the working directory have to be relative to the task root.\n\n## Credits\nPackage maintained by Trickster Animations",
    'author': 'golyalpha',
    'author_email': 'golyalpha@gmail.com',
    'url': 'https://gitlab.com/OnDev-Project/parallelic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
