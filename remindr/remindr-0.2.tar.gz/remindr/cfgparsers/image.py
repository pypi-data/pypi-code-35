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

# Get values of the configuration file for Mastodon
'''Get values of the configuration file for Mastodon'''

# standard library imports
import sys

def parseimage(config):
    # image section
    section = 'image'
    imageconf = {}
    #######################
    # path_to_image option
    #######################
    confoption = 'path_to_image'
    if config.has_section(section):
        if config.has_option(section, confoption):
            imageconf['path_to_image'] = config.get(section, confoption)
        ##############################
        # {network}_image_path option
        ##############################
        for networkoption in ('mastodon', 'twitter'):
            possiblenetwork = ''.join([networkoption, '_image_path'])
            if config.has_option(section, possiblenetwork):
                imageconf[possiblenetwork] = config.get(section, possiblenetwork)
        ##############################
        # {lang}_image_path option
        ##############################
        for langoption in config[section]:
            if langoption.endswith('_image_path') and langoption != 'mastodon' and langoption != 'twitter':
                imageconf[langoption] = config.get(section, langoption)
    return imageconf
