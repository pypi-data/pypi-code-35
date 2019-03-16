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

# Get values of the configuration file
'''Get values of the configuration file'''

# standard library imports
from configparser import ConfigParser, NoOptionError, NoSectionError
import logging
import os
import os.path
import socket
import sys

# 3rd party library imports
import feedparser

# local imports
from remindr.cfgparsers.image import parseimage
from remindr.cfgparsers.prefix import parseprefix
from remindr.cfgparsers.networks.mastodon import parsemastodon
from remindr.cfgparsers.networks.twitter import parsetwitter

def cfgparse(clioptions):
    '''Parse the configurations'''
    for pathtoconfig in clioptions.configs:
        options = {}
        # read the configuration file
        config = ConfigParser()
        if not config.read(os.path.expanduser(pathtoconfig)):
            sys.exit('Could not read the configuration file')
        ###########################
        # the mastodon section
        ###########################
        options['mastodon'] = parsemastodon(config)
        options['twitter'] = parsetwitter(config)
        ###########################
        # the image section
        ###########################
        options['image'] = parseimage(config)
        ###########################
        # the entrylist section
        ###########################
        section = 'entrylist'
        if config.has_section(section):
            confoption = 'path_to_list'
            options['path_to_list'] = config.get(section, confoption)
        else:
            sys.exit('You should provide a {confoption} parameter in the [{section}] section'.format(section=section, confoption=confoption))
        ###########################
        # the prefix section
        ###########################
        options['prefix'] = parseprefix(config)
    return options
