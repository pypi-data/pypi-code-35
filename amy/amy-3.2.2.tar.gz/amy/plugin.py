from .env import *
from .instance import Instance
from .message import Message
from . import actions
from threading import Thread
import json
from cryptography.fernet import Fernet
import datetime
import types

from kombu import Connection, Queue
from kombu.mixins import ConsumerProducerMixin


# try catcher for errors in funcs
def onError(code=400, message='Error'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                ## if there is no satus code set 200
                res = func(*args, **kwargs)
                return res
            except Exception as e:
                mes = statusMessage(code, message)
                print(e)
                print(mes)
                return mes
        return wrapper
    return decorator


def statusMessage(code=200, message='Success', payload = {}):
    if payload != {}:
        payload = {'info': payload}


    return {
        'status': code,
        'message': message,
        **payload
    }


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

    def sendStatus(self, properties, payload):
        self.producer.publish(
            payload,
            exchange='', routing_key=properties['reply_to'],
            correlation_id=properties['correlation_id'],
            serializer='json',
            retry=True,
        )


class Plugin:
    __instances = {}
    conn = Connection(AMY_Q_HOST)
    __crypto = Fernet(AMY_HASHKEY.encode())

    @classmethod
    def plublishMessage(cls, message: Message):
        cls.conn.SimpleQueue('messages').put(message.toDict())

    def __init__(self, name='plugin', instanceCls=Instance):
        self.name = name.lower()
        self.__instanceCls = instanceCls
        self.startListener()
        self.conn.SimpleQueue('plugins').put({'name': self.name, 'status': 'online'})

    def startListener(self):
        if not hasattr(self, '__listener'):
            self.__listner = Listner(
                self.conn, self.request_handler, self.name)
        self.__listner.should_stop = False
        self.__listner_thread = Thread(
            target=self.__listner.run)
        self.__listner_thread.start()
        print('listen on q')

    def stopListener(self):
        if hasattr(self, '__listner_thread'):
            self.__listner.should_stop = True
            self.__listner_thread.join()

    def request_handler(self, message):
        username = message.headers.get('username', None)

        if username:
            action = message.headers.get('action', None)

            if action == actions.CREATE_USER:
                session = message.payload.get('session', None)
                session = self.__encrypt(session) if session else None
                statusCode = self.create(username, session)

            elif action == actions.AUTHORIZE_USER:
                statusCode = self.authorize(
                    username, message.payload['token'])

            elif action == actions.START_USER:
                statusCode = self.start(username)

            elif action == actions.STOP_USER:
                statusCode = self.stop(username)

            elif action == actions.SEND_MESSAGE:
                statusCode = self.sendMessage(
                    username, message.payload['message'])

            elif action == actions.STATUS_USER:
                statusCode = self.status(username)

            else:
                statusCode = 500

            # message.ack()
            self.__listner.sendStatus(message.properties, statusCode)

        message.ack()

    @classmethod
    def __encrypt(cls, unhashstring: str):
        return cls.__crypto.encrypt(unhashstring.encode()).decode()
    
    @classmethod
    def __decrypt(cls, hashedstring: str):
        # print(hashedstring)
        return cls.__crypto.decrypt(hashedstring.encode()).decode()
 

    @onError(500, 'failed to create User')
    def create(self, username, session):
        if username not in self.__instances:
            self.__instances[username] = self.__instanceCls()
            session = self.__instances[username].onCreate(username, session)
        return statusMessage(201, 'User created')

    @onError(500, 'failed to check Status Running')
    def isRunning(self, username):
        return statusMessage(200, 'Running') if hasattr(self.__instances[username], '__thread') else statusMessage(400, 'not running')

    @onError(500, 'failed to autheticate User')
    def authorize(self, username, token):
        session = self.__encrypt(self.__instances[username].onAuth(token=token))
        return { **self.isAuth(username), "session" : session }

    @onError(500, 'failed autheticate Process')
    def isAuth(self, username):
        return statusMessage(200, 'Logged in') if self.__instances[username].isAuthorized() else statusMessage(401, 'Failed to authenticate')

    @onError(500, 'failed to read created user')
    def isCreated(self, username):
        return statusMessage(200, 'created') if username in self.__instances else statusMessage(404, 'not created')

    @onError(500, 'failed to send status')
    def status(self, username):
        payload = {
            'create': self.isCreated(username),
            'authorize': self.isAuth(username),
            'start': self.isRunning(username),
        }
        return statusMessage(200, 'User running and authorized', payload) if 199 < payload['create']['status'] and payload['authorize']['status'] and payload['start']['status'] < 300 else statusMessage(400, 'User not running or authorized', payload)

    @onError(500, 'failed to start User')
    def start(self, username):
        self.__instances[username].onStart()
        return statusMessage(200, 'User started')

    @onError(500, 'failed to stop User')
    def stop(self, username):
        self.__instances[username].onStop()
        return statusMessage(200, 'User stopped')

    @onError(500, 'failed to delete User')
    def delete(self, username):
        self.__instances[username].onDelete(username)
        del self.__instances[username]
        return statusMessage(204, 'User deleted')

    @onError(500, 'failed to send Message')
    def sendMessage(self, username, message):
        self.__instances[username].onSendMessage(message)
        return statusMessage(200, 'Message send')
