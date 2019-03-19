# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['packagr', 'packagr.commands']

package_data = \
{'': ['*'],
 'packagr': ['.mypy_cache/3.7/*',
             '.mypy_cache/3.7/collections/*',
             '.mypy_cache/3.7/importlib/*',
             '.mypy_cache/3.7/os/*'],
 'packagr.commands': ['.mypy_cache/3.7/*',
                      '.mypy_cache/3.7/collections/*',
                      '.mypy_cache/3.7/distutils/*',
                      '.mypy_cache/3.7/email/*',
                      '.mypy_cache/3.7/http/*',
                      '.mypy_cache/3.7/importlib/*',
                      '.mypy_cache/3.7/logging/*',
                      '.mypy_cache/3.7/os/*',
                      '.mypy_cache/3.7/requests/*',
                      '.mypy_cache/3.7/requests/packages/*',
                      '.mypy_cache/3.7/requests/packages/urllib3/*',
                      '.mypy_cache/3.7/requests/packages/urllib3/packages/*',
                      '.mypy_cache/3.7/requests/packages/urllib3/packages/ssl_match_hostname/*',
                      '.mypy_cache/3.7/requests/packages/urllib3/util/*',
                      '.mypy_cache/3.7/urllib/*']}

install_requires = \
['cleo>=0.7.2,<0.8.0',
 'requests>=2.21,<3.0',
 'toml>=0.10.0,<0.11.0',
 'wheel>=0.33.1,<0.34.0']

entry_points = \
{'console_scripts': ['packagr = packagr:run']}

setup_kwargs = {
    'name': 'packagr-cli',
    'version': '0.2.0',
    'description': 'A CLI for https://www.packagr.app',
    'long_description': '# Packagr CLI\n\n## What is Packagr?\n\n[Packagr](https://www.packagr.app) is a cloud hosted private repository for your private Python packages. The Packagr\nCLI is a separate, open source project intended to support it by allowing you to perform most of Packagr\'s functionality\nvia the API \n\n## Installation\n\nPackagr CLI can be installed via pip:\n\n```bash\npip install packagr-cli\n```\n\nIt can then be invoked via the `packagr` command in any terminal window:\n\n```bash\npackagr [command] [args]\n```\n\n## Commands\n\n### Configure\n`packagr configure <hash-id> <email> <password>`\n\nYou should call the `configure` command straight after you install Packagr CLI. This command will store your credentials\nto a config file, `packagr_conf.toml`, that is referenced by many other of the Packagr CLI commands, and removes the\nneed for the Packagr CLI to contstantly prompt you for your password (as is the case with `pip`/`twine`)\n\n#### Parameters\n\n- `hash-id`: See below\n- `email`: The email address you registered for Packagr with\n- `password`: The password you registered for Packagr with\n\n#### Where do I get my Packagr hash id?\n\nWhen you first sign up for a [Packagr](https://www.packagr.app) account, you\'ll be assigned a unique repository url that\nlooks something like this:\n\n```bash\nhttps://api.packagr.app/u893rj/\n```\n\nThe last part of this url is your `hash-id`\n\n### Init \n`packagr init <name> [--overwrite]`\n\nIn order to create a Package, Packagr needs a file called `packagr.toml`, which contains information about your package.\nThe `package init` command creates this file for you\n\nThe `name` argument is optional - if not specified, the name will default to the name of the folder you invoke the call\nfrom. \n\nAdditionally, the `init` command will also create a subfolder called `name`, if one doesn\'t already exist. By default,\nPackagr assumes that the code you want to package is stored in this folder. However, if you want to customize that, you\ncan easily do so by editing the `packages` parameter in `packagr.toml`. It\'s also possible to modify any of the valuues\nin the config file manually.\n\n#### Arguments\n\n- `name` (Optional): The name of your package\n- `--overwrite` (Optional): If you try to run `packagr init` in a folder where a `packagr.toml` file already exists, you\n  will be prompted to confirm that you want to overwrite the existing file. Passing this argument overrides the prompt\n\n### Set\n`packagr set <key> <value>`\n\nOnce your `packagr.toml` file has been created, you can use the `set` command to set values within it. For example, if \nyou wanted to add a description to the config, you could enter the following command:\n\n```bash\npackagr set description "some information"\n```\n\nYou could equally just go into your `packagr.toml` file and add the line `description = "some information"` manually,\nbut the recommended way is to use the CLI - eventually, the CLI will validate the value of `key` to ensure that it is\nvalid.\n\nIf you enter a duplicate key, you will be prompted to confirm that you want to overwrite it\n\n#### Arguments\n\n- `key`: the setting key\n- `value`: the setting value\n\n### Add\n`packagr add <key> <value>`\n\nThe `add` command works in a similar way to the `set` command, but it\'s purpose is to append data to arrays already \ndefined in the config. For example, if your config already looks like this:\n\n```toml\nAuthors = [\'Chris <chris@packagr.app>\'] \n```\n\nThen you can update this value using `packagr add Authors "some guy <me@example.com>"` to change it to the following:\n\n```toml\nAuthors = [ "Chris <chris@packagr.app>", "Some guy <me@example.com>",]\n```\n\nThe `add` command will also add a value to a key that doesn\'t exist.\n\n#### Arguments\n\n- `key`: the setting key\n- `value`: the setting value\n\n\n### Install\n`packagr install <some-package>`\n\nThe `install` command works in a similar way to `pip install` - it installs a package using your current environment\'s\n`pip` installation. However, this command will also look for packages in your Packagr repository, as well as in the \npublic PyPI repository. Once a package is installed correctly, it will also be added to your config\'s `install_requires`\nsection\n\n#### Arguments\n\n- `packages`: a list of packages to install\n- `--ignore-errors`: In case of multiple packages, passing this argument means that Packagr will continue attempting to\n  install the remaining packages on the list in the case that one fails\n\n### Uninstall\n`packagr uninstall <some-package>`\n\n\nThis command does the opposite of `install` - it uninstalls a given package and removes it from the dependencies list.\n\n#### Arguments\n\n- `packages`: a list of packages to uninstall\n- `--ignore-errors`: In case of multiple packages, passing this argument means that Packagr will continue attempting to\n  \n  \n### Bump\n`packagr bump <version> [--minor] [--major]`\n\nThe `bump` command increases the version number of your package. Used without arguments, e.g. `packagr bump`, it \nincreases the version number, e.g. `1.0.0` becomes `1.0.0`. Using the `--minor` argument increases the minor version\nnumber, e.g. `1.0.0 > 1.1.0` and the `--major` argument converts `1.0.0` to `2.0.0`. The `--major` and `--minor` \narguments can be used in conjuction with each other.\n\nAlternatively, you can use `packagr bump 4.5.6` to set the version for a specific value. If you aren\'t using `semver`,\nwhich means that the `bump` command may not be able to parse the existing version number, then you can use this option\ninstead\n\n#### Arguments\n\n- `version` (optional): the version number to set. Not compatible with any other argument\n-  `--minor` (optional): Increase the minor version number\n-  `--major` (optional): Increase the major version number\n\n\n### Package\n`packagr package`\n\nCreates `sdist` and/or `wheel` packages based on your config file. Using the command without arguments will create a \npackage in both formats. Using `--no-wheel` or `no-sdist` will prevent creation of specific formats\n\n#### Arguments\n- `--no-sdist`: Don\'t build a tarball\n- `--no-wheel`: Don\'t build a wheel\n\n\n### Upload\n`packagr upload [--ignore-409]`\n\nThis command will push your package to Packagr. If you are uploading many packages at once, you may opt to use the \n`--ignore-409` argument, which will skip to the next package if encountering a 409 error (conflict for URL). In future,\nPackagr CLI will have the ability to display detailed logs from Packagr, which offers a big advantage over `twine`\'s\nlimited ability to handle error responses\n\n\n### Coming soon\n\nThe following commands will be added to future versions of Packagr CLI:\n\n- ``packagr set-readme <readme-file>``: passes the content of a readme file to `Description`\n- ``packagr token create <my-package> <email> [--read-only]``: Creates an access token for a package\n- ``packagr token delete <my-package> <email> [--no-warnings]``: Deletes an access token\n- ``packagr set-public <my-package>``: Sets a package as `public`\n- ``packagr set-private <my-package>``: Sets a package as `private`\n\n',
    'author': 'Chris Davies',
    'author_email': 'chris@packagr.app',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
