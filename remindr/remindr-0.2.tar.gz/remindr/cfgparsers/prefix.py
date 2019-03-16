# -*- coding: utf-8 -*-
# Copyright © 2017-2019 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/

# Get values of the prefix section
'''Get values of the prefix section'''

def parseprefix(config):
    # image section
    section = 'prefix'
    prefixconf = {}
    prefixconf['prefix'] = ''
    #######################
    # path_to_image option
    #######################
    if config.has_section(section):
        for prefixoption in config[section]:
            if prefixoption == 'prefix':
                prefixconf[prefixoption] = config.get(section, prefixoption)
            if prefixoption.endswith('_prefix'):
                prefixconf[prefixoption] = config.get(section, prefixoption)
    return prefixconf
