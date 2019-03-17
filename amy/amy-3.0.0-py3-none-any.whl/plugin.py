from .env import *

from threading import Thread
import datetime
import types

from kombu import Connection, Queue
from kombu.mixins import ConsumerProducerMixin

from .message import Message


class Listner(ConsumerProducerMixin):
    def __init__(self, conn, cb, name):
        self.connection = conn
        self.cb = cb
        self.name = name

    def get_consumers(self, Consumer, channel):
        return [Consumer(
            queues=[Queue(self.name)],
            on_message=self.cb,
            accept={'application/json'},
            prefetch_count=1)]


class Instance(object):
    def __init__(self):
        pass

    def onCreate(self, username):
        pass

    def onAuth(self, token):
        pass

    def onStart(self, token):
        pass

    def onStop(self, token):
        pass


class Plugin:
    __instances = {}
    __connection = Connection(AMY_Q_HOST)

    def __init__(self, name, instanceCls):
        self.name = name.lower()
        self.__instanceCls = instanceCls
        self.__startListener()

    def __startListener(self):
        if not hasattr(self, '__listener'):
            self.__listner = Listner(
                self.__connection, self.__request_handler, self.name)
        self.__listner.should_stop = False
        self.__listner_thread = Thread(
            target=self.__listner.run)
        self.__listner_thread.start()
        print('listen')

    def __stopListener(self):
        if hasattr(self, '__listner_thread'):
            self.__listner.should_stop = True
            self.__listner_thread.join()

    def __request_handler(self, message):
        action = message.headers['action']
        username = username = message.payload['username']

        if action == 'create':
            self.create(username)
        if action == 'authorize':
            self.__instances[username].onAuth(token=message.payload['token'])
        if action == 'start':
            self.__instances[username].onStart()
        if action == 'stop':
            self.__instances[username].onStop()

        message.ack()

    def create(self, username):
        if username not in self.__instances:
            self.__instances[username] = self.__instanceCls()
            self.__instances[username].onCreate(username)

    def delete(self, username):
        del self.__instances[username]

    @classmethod
    def plublishMessage(cls, message: Message):
        cls.__connection.SimpleQueue('messages').put(message)
