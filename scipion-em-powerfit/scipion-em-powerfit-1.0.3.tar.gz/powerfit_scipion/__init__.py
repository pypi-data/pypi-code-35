# **************************************************************************
# *
# * Authors:     Carlos Oscar Sorzano (coss@cnb.csic.es)
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
wrapping Powerfit programs https://github.com/haddocking/powerfit
"""
import os
import pyworkflow.em
from pyworkflow.utils import Environ
from powerfit_scipion.constants import POWERFIT_HOME, V2_0


_logo = "powerfit_logo.gif"


class Plugin(pyworkflow.em.Plugin):
    _homeVar = POWERFIT_HOME

    @classmethod
    def getEnviron(cls):
        """ Setup the environment variables needed to launch powerfit. """
        environ = Environ(os.environ)
        environ.update({
            'PATH': Plugin.getHome(),
            'LD_LIBRARY_PATH': str.join(cls.getHome(), 'powerfitlib')
                               + ":" + cls.getHome(),
        }, position=Environ.BEGIN)

        return environ

    @classmethod
    def isVersionActive(cls):
        return cls.getActiveVersion().startswith(V2_0)

    @classmethod
    def defineBinaries(cls, env):
        """ Define required binaries in the given Environment. """
        env.addPackage('powerfit', version='2.0',
                       tar='powerfit.tgz',
                       targets=['powerfit-2.0*'],
                       pythonMod=True,
                       deps=['numpy', 'scipy', 'fftw3'],
                       default=True)


pyworkflow.em.Domain.registerPlugin(__name__)
