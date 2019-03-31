# Licensed under the FreeBSD license

"""
pyleiades: Python Library for EIA Data Examination & Exhibition

Tools to use with the EIA Monthly Energy Review datasets. This package provides
an API for performing more sophisticated examination and visualization of the
Energy Information Administration (EIA) Monthly Energy Review (MER) datasets.

Data can be accessed directly at the EIA website:
    https://www.eia.gov/totalenergy/data/browser/
"""

__version__ = '0.1.dev'

import os
from pyleiades.energies import Energy
from pyleiades.visuals import Visual

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
ARCHIVE_DIR = os.path.join(DATA_DIR, 'archive')


