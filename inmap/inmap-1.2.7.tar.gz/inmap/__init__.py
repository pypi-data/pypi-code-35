# -*- coding: latin-1 -*-

"""
inmap - 2019.02.27

inmap is a python library which helps in using nmap port scanner.
It allows to easilly manipulate nmap scan results and will be a perfect
tool for systems administrators who want to automatize scanning task
and reports. It also supports nmap script outputs.


Author :

* Aalouane Soufiane - aalouane.s@gmail.com

Licence : GPL v3 or any later version


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

name = "inmap"

from inmap.controller.scans import ScanController
from inmap.model.host import HostModel
from inmap.model.port import PortModel


