import logging

from time import sleep
from inspect import isfunction
from slackclient import SlackClient
from random import random

from ..module import MagiModule


class MagiIO:
    __callback_list = {}

    def __init__(self, magimodule, symbol='?'):
        assert isinstance(magimodule, MagiModule.MagiModule)
        assert isinstance(symbol, str)

        self.__module = magimodule
        self.__symbol = symbol
        self.__sc = SlackClient(magimodule.slack_token)
        self.__sc.rtm_connect(with_team_state=False)

        logging.basicConfig(filename='MagiIo.log', level=logging.DEBUG)
        logging.info('Program Started')

    def __connection(self):
        if self.__sc.rtm_connect(with_team_state=False):
            logging.info('slack connected')
            return True
        else:
            return False

    def __parse_message_and_exec_callback(self, message):
        if message['type'] == 'message' and message['text'][0] == self.__symbol:
            text_split = message['text'].split()
            text_args = text_split[1:]
            command = text_split[0].replace(self.__symbol, '')
            logging.info(f'message: {message["text"]}, user: {message["user"]}')

            if command in self.__callback_list:
                response = self.__sc.api_call('users.info',
                                               user=message['user'])
                user_info = response['user']
                user_profile = user_info['profile']
                return self.__callback_list[command](*text_args,
                                                     name=user_info['name'],
                                                     real_name=user_info['real_name'],
                                                     display_name=user_profile['display_name'])
            else:
                raise AttributeError

    def connected(self):
        return self.__sc.server.connected

    def set_callback_func(self, tag, callback):
        assert isfunction(callback)
        assert isinstance(tag, str)

        self.__callback_list[tag] = callback
        return True

    def get_callback_list(self):
        key_list = [x for x in self.__callback_list]
        return key_list

    def start(self):
        while True:
            # Check is connected
            if not self.connected:
                self.__connection()

            # Start main logic
            messages = self.__sc.rtm_read()

            # If user send a commend, call 'callback function'
            for message in messages:
                try:
                    response = self.__parse_message_and_exec_callback(message)
                    self.__sc.rtm_send_message(message['channel'], response)

                    if self.__module.is_user_can_get_exp(message['user']):
                        self.__module.user_own_exp(message['user'], random(2, 5))
                except AttributeError:
                    pass
                except KeyError:
                    pass
                except TypeError as e:
                    logging.info('Callback function argument need *args.')
                    print('Callback function argument need *args. ' + str(e))

            sleep(1)

