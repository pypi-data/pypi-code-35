#!/usr/bin/env python
# pylint: disable=wrong-import-position,wrong-import-order
"""
OpenTEA scientific GUI library.
Documentation is hosted at: http://cerfacs.fr/opentea
"""

__author__ = "Antoine Dautpain"
__credits__ = ["Antoine Dautpain",
               "Guillaume Frichet",
               "Adrien Bonhomme",
               "Corentin Lapeyre",
               "Gregory Hannebique",
               "Franchine Ni",
               "Benjamin Farcy",
               "Luis Segui",
               "Melissa Ferand",
               "Quentin Douasbin"
              ]

__license__ = "CeCILL-B"
__version__ = "3.0.0"
__maintainer__ = "Antoine Dauptain"
__email__ = "coop@cerfacs.fr"
__status__ = "Development"

# Check python version
import sys
if sys.hexversion < 0x030000A0:
    raise Exception("Must be run with python version"
                    " at least 3.0.0, and not python 2\n"
                    "Your version is %i.%i.%i" % sys.version_info[:3])

