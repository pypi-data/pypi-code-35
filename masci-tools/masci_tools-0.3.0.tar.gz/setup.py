# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['masci_tools',
 'masci_tools.io',
 'masci_tools.io.parsers',
 'masci_tools.tests',
 'masci_tools.tools',
 'masci_tools.util',
 'masci_tools.vis']

package_data = \
{'': ['*'],
 'masci_tools.tests': ['files/interpol/*',
                       'files/kkr/import_calc_old_style/*',
                       'files/kkr/kkr_run_dos_output/*',
                       'files/kkr/kkr_run_slab_nosoc/*',
                       'files/kkr/kkr_run_slab_soc_mag/*',
                       'files/kkr/kkr_run_slab_soc_simple/*',
                       'files/kkr/outputfiles/*',
                       'files/kkr/parse_Nan_result/*',
                       'files/kkr/parser_3Dsymmetries/*',
                       'files/kkrimp_parser/test1/*',
                       'files/kkrimp_parser/test2/*',
                       'files/mod_pot/test1/*',
                       'files/mod_pot/test2/*',
                       'files/voronoi/*']}

install_requires = \
['bumpversion', 'h5py', 'matplotlib', 'numpy', 'pytest-cov', 'scipy']

setup_kwargs = {
    'name': 'masci-tools',
    'version': '0.3.0',
    'description': 'Tools for Materials science. Vis contains wrapers of matplotlib functionality to visualalize common material science data. Plus wrapers of visualisation for aiida-fleur workflow nodes',
    'long_description': '[![Build Status](https://travis-ci.com/JuDFTteam/masci-tools.svg?branch=master)](https://travis-ci.com/JuDFTteam/masci-tools)\n[![Coverage Status](https://coveralls.io/repos/github/JuDFTteam/masci-tools/badge.svg?branch=develop)](https://coveralls.io/github/JuDFTteam/masci-tools?branch=develop)\n[![Documentation Status](https://readthedocs.org/projects/masci-tools/badge/?version=latest)](https://masci-tools.readthedocs.io/en/latest/?badge=latest)\n[![GitHub version](https://badge.fury.io/gh/JuDFTteam%2Fmasci-tools.svg)](https://badge.fury.io/gh/JuDFTteam%2Fmasci-tools)\n[![PyPI version](https://badge.fury.io/py/masci_tools.svg)](https://badge.fury.io/py/masci_tools)\n\n\n# masci-tools\n\n**This is a collection of tools, common things used by packages of material science.**\n\nFeel free to contribute.\n\nThe code is hosted on GitHub at\n<https://github.com/JuDFTteam/masci-tools>\n\nThe documentation is hosted on https://masci-tools.readthedocs.io.\n\n## Installation\n\n```\npip install masci-tools\n```\n\n## Dependencies\n\nThese python packages are needed:\n* `pymatgen`\n* `ase`\n* `lxml`\n* `matplotlib`\n* `h5py`\n\nIt should not depend on `aiida_core`!\n\n## Layout of`masci-tools`\n\n* `io`\n    * Contains methods to write certain files\n    * `io.parsers`: Contains parsers of certain code output or input files\n* `tests`\n    * auto tests of `masci-tools` functions\n* `util`\n    * Contains rather low level utility\n* `tools`\n    * Contains rather highlevel utility which is rather complete\n* `vis`\n    * Contain a collection of matplotlib, pyplot, gnuplot methods used for ploting common results from material science simulations, e.g. bandsstructures, DOS, ... \n\n## License\n\n\n*masci-tools* is distributed under the terms and conditions of the MIT license which is specified in the `LICENSE.txt` file.\n',
    'author': 'Jens Br\xc3\xb6der',
    'author_email': 'j.broeder@fz-juelich.de',
    'url': 'https://github.com/JuDFTteam/masci-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
