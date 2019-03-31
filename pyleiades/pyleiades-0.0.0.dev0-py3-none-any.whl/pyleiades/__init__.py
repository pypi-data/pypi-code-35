# Licensed under the FreeBSD license

"""
pyleiades: Python Library for EIA Data Examination & Exhibition

Tools to use with the EIA Monthly Energy Review datasets. This package provides
an API for performing more sophisticated examination and visualization of the
Energy Information Administration (EIA) Monthly Energy Review (MER) datasets.

Data can be accessed directly at the EIA website:
    https://www.eia.gov/totalenergy/data/browser/
"""

import os
from pyleiades.energies import Energy
from pyleiades.visuals import Visual

package_dir = os.path.dirname(__file__)
project_dir = os.path.join(package_dir, '..')

# Read the contents of the VERSION file
with open(os.path.join(project_dir, 'VERSION')) as version_file:
    __version__ = version_file.read().strip()

DATA_DIR = os.path.join(package_dir, 'data')
ARCHIVE_DIR = os.path.join(DATA_DIR, 'archive')


