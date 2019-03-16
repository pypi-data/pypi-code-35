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

def parsetwitter(config):
   # twitter section
    twitterconf = {}
    twitterconf['image'] = True
    section = 'twitter'
    if config.has_section(section):
        possibleoptions = ['consumer_key', 'consumer_secret', 'access_token', 'access_token_secret']
        for confkey in possibleoptions:
            if config.has_option(section, confkey):
                twitterconf[confkey] = config.get(section, confkey)
            else:
                sys.exit('You should define a "{confkey}" parameter in the [{section}] section'.format(confkey=confkey, section=section))
        # image (true of false) for not diplaying an image on this social network (in order to use og or twitter card)
        confkey = 'image'
        if config.has_option(section, confkey):
            twitterconf[confkey] = config.getboolean(section, confkey)
    return twitterconf
