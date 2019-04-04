# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['manageconf']

package_data = \
{'': ['*']}

install_requires = \
['anyconfig>=0.9.8,<0.10.0', 'boto3>=1.9,<2.0']

setup_kwargs = {
    'name': 'manageconf',
    'version': '0.1.5',
    'description': 'Builds a config object based on environment variables, settings files and (optional) parameters stored in AWS System Manager Parameter Store.',
    'long_description': '# Manage Conf\n\n[![CircleCI](https://circleci.com/gh/sam-atkins/manageconf/tree/master.svg?style=svg)](https://circleci.com/gh/sam-atkins/manageconf/tree/master)\n<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\n## Description\n\nBuilds a config object based on environment variables, settings files and (optional) parameters stored in AWS System Manager Parameter Store.\n\nThe config object merges in config, overriding any previous key/value pairs, in the following order:\n\n- ENV\n- default config: default.yml\n- stage config: {stage}.yml\n- remote config: remote_settings (AWS param store)\n\nAvailable to download as a package on [PyPi](https://pypi.org/project/manageconf/).\n\n### Settings Files\n\nSet an environment variable with the key name `project_config_dir`. It is important this is set before the package is imported. The value of `project_config_dir` should be the location of your `/settings` folder.\n\nSet-up your settings folder, adding in configuration to the appropriate file.\n\n```\n-- /settings\n----          default.yml\n----          {stage}.yml\n----          {stage}.yml\n```\n\nExample configuration:\n\n```yaml\n# default.yml\nproject_name: example-project\n\n# local.yml\nuse_remote_settings: false\n\n# dev.yml\nuse_remote_settings: true\n```\n\n### AWS\n\nAdd parameters in your AWS account with paths that match this pattern:\n\n`/{project_name}/{stage}/`\n\nIf you set `use_remote_settings: true` in a stage.yml config file, the package will attempt to fetch the parameters from the store that have this base path.\n\nUsing the example configuration above, the path would be:\n\n```\n/example-project/dev/\n```\n\n### Usage\n\nMake sure you set `project_config_dir` before importing.\n\n```python\nfrom manageconf import Config, get_config\n\nSECRET_KEY = get_config("SECRET_KEY")\nDEBUG = get_config("DEBUG", True)\n```\n\n## Development\n\n### Install\n\nRequires [Poetry](https://poetry.eustace.io).\n\n```bash\n# create a Python3 virtual environment\nvirtualenv -p python3 env\n\n# activate the virtual env\nsource env/bin/activate\n\n# install requirements\npoetry install\n```\n\n### Tests\n\n```bash\n# run tests\npytest -vv\n\n# coverage report in the Terminal\npytest --cov=manageconf tests/\n\n# coverage report in HTML\npytest --cov-report html --cov=manageconf tests/\n```\n',
    'author': 'Sam Atkins',
    'author_email': 'samatkins@outlook.com',
    'url': 'https://github.com/sam-atkins/manageconf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
