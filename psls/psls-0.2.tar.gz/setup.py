"""

PLATO Stellar Light-curve Simulator (PSLS)

Copyright (c) 2014, October 2017, R. Samadi (LESIA - Observatoire de Paris)

This is a free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with this code.  If not, see <http://www.gnu.org/licenses/>.
"""

from distutils.core import setup



setup(name = 'psls',
      version = '0.2',
      description = 'PLATO Stellar Light-curve Simulator (SLS): Simulate stochastically-excited oscillations and associated stellar and instrumental background noises',
      author = 'R. Samadi',
      author_email = 'reza.samadi@obspm.fr',
      url =  'http://lesia.obspm.fr/',
      scripts = ['psls.py'],
      py_modules = ['sls','universal_pattern','FortranIO','transit'],
      data_files=[('models',['models/m+0y24h.tar.gz','models/m+0y27l.tar.gz'])],
      long_description = open('README.txt').read()
      )
