__author__ = ('Imam Omar Mochtar', ('iomarmochtar@gmail.com',))

"""
Base of cakap library bot class
"""

import logging
import os
import re
import sys
import inspect
import json
from glob import glob
from ConfigParser import ConfigParser
from colorlog import ColoredFormatter
from pprint import pprint
from .utils import Utils 
from .decorators import auth, catch_error, chelp, AutoSet
from .filters import FilterNotMatch
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, Job 

# agar bisa jalan async
from telegram.ext.dispatcher import run_async

# untuk job queue
from telegram.ext import Job 


class BotBase(object):

    __metaclass__ = AutoSet

    users = {} 
    allowed_users = []
    allowed_gids = []
    helps = [] 
    debug = False 
    cmd_prefix = 'cmd_' 

    def __init__(self, token, workers=3, users=[], 
        groups=[], name=None, debug=False):

        self.debug = debug
        self.name = name if name else type(self).__name__

        self.allowed_users = users
        self.allowed_gids = groups
        self.init_logger()

        self.updater = Updater(
            token, 
            workers=workers
        )


    def check_auth(self, bot, update, func_name=None):
        """
        Auth & authorization check which using @auth decorator
        """
        chat_id = Utils.chat_id(update)
        if Utils.is_group(update):
            if chat_id not in self.allowed_gids:
                self.logger.warn('receiving message from group id {} is not alowed'.format(chat_id))
                return False 

        user_details = Utils.user_details(update)
        if user_details['username'] not in self.allowed_users:
            self.logger.warn('{} is not allowed for accessing {}'.format(
                    user_details['username'],
                    func_name
                ))
            return False 
        return True 

    def init_logger(self, logger=None, level=logging.DEBUG):
        formatter = ColoredFormatter(
            '%(yellow)s%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s',
            # datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red',
                }
        )

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        if not logger:
            self.logger = logging.getLogger(
                    type(self).__name__ if not self.name else self.name
                )
            logger = self.logger
        logger.addHandler(handler)
        logger.setLevel(level)

    def filter_args(self, argfilters, args):
        """
        Filter given argument parsers
        """
        # if number of filters is more than arguments means not enought
        if len(argfilters) > len(args):
            return 'Need more argument, please check /help for command documentation'

        result = {}
        count = 0
        for argfilter in argfilters:
            name = argfilter['name']
            # if filters didn't exist 
            if not 'filters' in argfilter or not argfilter['filters']:
                result[name] = args[count]
                count += 1
                continue

            for fltr in argfilter['filters']:
                try:
                    result[name] = fltr(argnum=count, args=args)  
                except FilterNotMatch as e:
                    return str(e)
            count += 1 
        
        return result 

    def error_handler(self, msg):
        self.logger.error(msg)

    @chelp('Get available command with it\'s description')
    @auth
    def cmd_help(self, bot, update):
        """Show available help"""
        Utils.send(bot, update, '\n'.join(self.helps))


    @classmethod
    def get_cmd_name(self, name):
        """
        Get name of cmd which is startswith {{cmd_prefix}}
        """
        re_name =  re.search('^{0}(.*?)$'.format(self.cmd_prefix), name)
        return re_name.group(1) if re_name else None 

    def pre_main(self):
        """
        Executed before registering main command handlers
        """
        pass

    def after_main(self):
        """
        Executed after registering main command handlers
        """
        pass

    def polling(self):
        self.updater.start_polling()
        self.updater.idle()

    def main(self):

        self.pre_main()
        for command in inspect.getmembers(self, predicate=inspect.ismethod):
            name = command[0]
            handler = command[1]

            if not name.startswith(self.cmd_prefix):
                continue

            cmd_name = self.get_cmd_name(name)
            cmd_is_async = handler.is_async if hasattr(handler, 'is_async') else False
            cmd_args = handler.args if hasattr(handler, 'args') else None 

            # TODO: help di set dalam bentuk markdown 
            hlp = '/{}'.format(cmd_name)
            if cmd_args:
                hlp += ' - {0}'.format(' '.join( map(lambda x: '[%s]'%x['name'].upper(), cmd_args) )) 

            if hasattr(handler, 'desc'):
                hlp += ' - {0}'.format(handler.desc)

            self.helps.append(hlp)

            self.logger.debug('Registering cmd {}'.format(cmd_name))
           
            self.updater.dispatcher.add_handler(
                    CommandHandler(cmd_name, 
                        run_async(handler) if cmd_is_async else handler, 
                        pass_args=True if cmd_args else False
                    )
                )


        self.after_main()

        self.logger.info('{} is running'.format(self.name))		
        self.polling()
