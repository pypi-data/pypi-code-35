# **************************************************************************
# *
# * Authors:     Carlos Oscar Sorzano (coss@cnb.csic.es)
# *
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************
"""
This sub-package contains data and protocol classes
wrapping ATSAS programs http://www.embl-hamburg.de/biosaxs/software.html
"""
from pyworkflow.utils import commandExists

_logo = "atsas_logo.gif"

import os
import pyworkflow.em

from pyworkflow.utils import Environ
from atsas.bibtex import _bibtex # Load bibtex dict with references
from atsas.protocols.protocol_pdb_to_saxs import AtsasProtConvertPdbToSAXS
from atsas.viewers import AtsasViewer
from atsas.constants import CRYSOL, ATSAS_HOME, V2_8_2


class Plugin(pyworkflow.em.Plugin):
    _homeVar = ATSAS_HOME


    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar(ATSAS_HOME, 'crysol-2.8.2')

    @classmethod
    def getEnviron(cls):
        """ Setup the environment variables needed to launch emx export. """
        environ = Environ(os.environ)

        environ.update({
            'PATH': Plugin.getHome(),
            'LD_LIBRARY_PATH': str.join(cls.getHome(), 'atsaslib')
                               + ":" + cls.getHome(),
        }, position=Environ.BEGIN)

        return environ

    @classmethod
    def isVersionActive(cls):
        return cls.getActiveVersion().startswith(V2_8_2)

    @classmethod
    def defineBinaries(cls, env):
        pass


pyworkflow.em.Domain.registerPlugin(__name__)





