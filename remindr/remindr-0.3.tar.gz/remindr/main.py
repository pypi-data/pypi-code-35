#!/usr/bin/env python3
# vim:ts=4:sw=4:ft=python:fileencoding=utf-8
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>

'''Checks an RSS feed, format it, store it and posts new entries to the social networks.'''

# standard libraires imports
import codecs
import importlib
import logging
import logging.handlers
import os
import sys

# 3rd party libraries imports
import feedparser

# app libraries imports
from remindr.cliparse import cliparse
from remindr.cfgparse import cfgparse
from remindr.formatnextmessage import formatnextmessage
from remindr.getlastblogentry import getlastblogentry
from remindr.tootpost import tootpost
from remindr.tweetpost import tweetpost

class Main:
    '''Main class of Remindr'''

    def __init__(self):
        self.main()

    def setup_logging(self, options):
        if options.syslog:
            sl = logging.handlers.SysLogHandler(address='/dev/log')
            sl.setFormatter(logging.Formatter('remindr[%(process)d]: %(message)s'))
            # convert syslog argument to a numeric value
            loglevel = getattr(logging, options.syslog.upper(), None)
            if not isinstance(loglevel, int):
                raise ValueError('Invalid log level: %s' % loglevel)
            sl.setLevel(loglevel)
            logging.getLogger('').addHandler(sl)
            logging.debug('configured syslog level %s' % loglevel)
        logging.getLogger('').setLevel(logging.DEBUG)
        sh = logging.StreamHandler()
        sh.setLevel(options.log_level.upper())
        logging.getLogger('').addHandler(sh)
        logging.debug('configured stdout level %s' % sh.level)

    def main(self):
        '''The main function'''
        clioptions = cliparse()
        self.setup_logging(clioptions)
        # iterating over the different configuration files
        cfgvalues = cfgparse(clioptions)
        logging.debug('result after configuration parsing:')
        logging.debug(cfgvalues)
        nextcontent = getlastblogentry(cfgvalues)
        logging.debug('result after getting next content:')
        logging.debug(nextcontent)
        nextmessage, language = formatnextmessage(cfgvalues, nextcontent)
        logging.debug('result after formatting next message:')
        logging.debug(nextmessage)
        # check if mastodon instance_url is available, toot if so
        if 'instance_url' in cfgvalues['mastodon']:
            tootpost(clioptions, cfgvalues, nextmessage, language)
        # check if twitter consumer_key is available, tweet if so
        if 'consumer_key' in cfgvalues['twitter']:
            tweetpost(clioptions, cfgvalues, nextmessage, language)
