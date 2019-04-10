import json
import logging
from json import JSONDecodeError
from random import choice
from string import digits, ascii_letters
import gevent
import six
import uuid
import ssl
from locust import TaskSet
from locust.events import request_success, request_failure, EventHook
from time import time
from urllib.parse import urlparse

import sqlite3
from websocket import create_connection, WebSocketConnectionClosedException


# todo add asserts to statements to validate response.
# todo dockerize all locust things and swarm it with docker compose / scale
from benchgrape.config import DB_FILE, WS
from benchgrape.core.db import TestDataMapper
from benchgrape.core.statement import login
from cement.utils import fs

logger = logging.getLogger(__name__)

db_file = fs.abspath(DB_FILE)
db_conn = sqlite3.connect(db_file, isolation_level='EXCLUSIVE')


def generate_call_id():
    return ''.join(choice(digits + ascii_letters) for _ in range(6))


websocket_dropped = EventHook()


def on_websocket_dropped(ex, *args, **kwargs):
    logger.exception(
        'could not receive data from websocket, '
        'reconnecting... exception was: %s', ex
    )


websocket_dropped += on_websocket_dropped


class MembershipSession(object):
    """
    represents a util class for a user session. can query channels a user
    has access to and save them, etc..
    """
    _ch_mbs = None
    user = None

    def __init__(self, task_set, user, organizatoin):
        self.user = user
        self.client = task_set.client
        self.wamp_client = task_set
        self.host = task_set.host
        self.auth_token = login(self.client, self.user['username'], self.user['password'])
        self.org = organizatoin['id']

    def get_client(self, task_set):
        if not hasattr(task_set, 'client'):
            return self.get_client(task_set.parent)
        return task_set.client

    # @property
    # def channel_memberships(self):
    #     if not self._ch_mbs:
    #         self.ch_mbs = self.wamp_client.send(
    #             'rooms', 'get_rooms', str(self.user['org_id']),
    #             **{'membership': True, 'page_size': 1000}
    #         )
    #     return self._ch_mbs

    @property
    def channel_memberships(self):
        # todo save to db - only when missing fetch all of them.
        if not self._ch_mbs:
            params = {
                "args": [self.user['org_id'], {'membership': True, 'page_size': 1000}],
                "action": 'get_rooms',
                "ns": 'rooms',
            }

            with self.client.post(
                    "/lp/rpc/", data=json.dumps(params),
                    catch_response=True,
                    headers={
                        "Authorization": "Token {}".format(self.auth_token),
                        "Content-Type": "application/json; charset=utf-8",
                    },
                    verify=False,
            ) as response:
                logger.debug('get_rooms response: %i' % response.status_code)
                if response.status_code < 200 or response.status_code > 299:
                    response.failure(response.status_code)
                else:
                    self._ch_mbs = json.loads(
                        response.content
                    )['response']['results'] if response.content else {}

        return self._ch_mbs

    def get_random_channel(self):
        return choice(self.channel_memberships)['id']


class PubSubMixin(object):
    """
    mixin to subscribe to the org right away when the set starts.
    """
    def on_start(self):
        logger.info("on_start called")
        super(PubSubMixin, self).on_start()
        self.organizations__join()


class PickleUserMixin(object):
    mapper = None
    organization = None

    def __init__(self, *args, **kwargs):
        super(PickleUserMixin, self).__init__(*args, **kwargs)
        self.mapper = mapper = TestDataMapper(db_conn, logger)
        self.host = mapper.get_host()
        self.user = mapper.pick_user()
        self.org = mapper.get_organization()

    def on_quit(self, *args, **kwargs):
        super(PickleUserMixin, self).on_quit(*args, **kwargs)
        self.mapper.relieve_user(self.user['id'])


class WampTaskSet(PickleUserMixin, TaskSet):
    """
    task set specially for wamp driven connections (v1 of course :D).
    """

    """
    pending requests, means to store sent request ids and meta info like
    request time and call type / name.
    those infos shall be deleted when the response is received
    asynchronously via _receive.
    """
    pending = None
    ws = None
    """
    user="thread" id aka random number. not a chatgrape user id
    """
    user_id = None
    """HistoryTaskSet
    store the auth token received from the login method (http "rest").
    """
    auth_token = None

    """
    falls back to ws://localhost:8000/ws
    """
    ws_location = None
    """
    ws or wss
    """
    ws_prot = None
    """
    I could tell you a joke here but it would be a waste of time.
    this was aleady a little waste of time.
    """
    org = None

    """
    we dont know the id of the first call so we dont find a start_time.
    the first call though is the create_connection handshake so we try
    to remember if we just opened the connection so we can ignore the first
    recv event.
    """
    awaiting_login_confirmation = False

    _mb = None

    @property
    def membership(self):
        if not self._mb:
            self._mb = MembershipSession(task_set=self, user=self.user, organizatoin=self.org)
        return self._mb

    def on_start(self):
        self.pending = {}
        self.org = self.membership.org
        logger.info('configured organization: %i', self.org)
        self.auth_token = self.membership.auth_token
        self.user_id = six.text_type(uuid.uuid4())

        if not self.host:
            raise AssertionError(
                '--host must be appended to determine the websocket location.'
            )

        # always use wss except if we are connecting to http.
        prot = 'wss' if urlparse(self.host).scheme != 'http' else 'ws'
        ws_location = '{}://{}/ws'.format(
            prot, self.host.replace('http://', '').replace('https://', '')
        )

        url = "{}?auth_token={}".format(ws_location, self.auth_token)
        logger.debug('connecting to %s' % url)
        try:
             # if necessary add  sslopt={"cert_reqs": ssl.CERT_NONE} to connect
            self.ws = ws = create_connection(
                url, origin=self.host, sslopt={"cert_reqs": ssl.CERT_REQUIRED}
            )
        except Exception as ex:
            error = 'cannot connect to websocket at %s. error was: %s' % (url, ex)
            logger.error(error)
            raise RuntimeError(error)
        if not ws:
            raise RuntimeError('cannot create websocket connection %s' % url)
        self.awaiting_login_confirmation = True

        def _receive():
            def reconnect():
                logger.info('reconnecting...')
                self.on_start()
                logger.info('reconnected.')

            while True:
                end_at = time()
                try:
                    res = ws.recv()
                except WebSocketConnectionClosedException as ex:
                    websocket_dropped.fire(ex=ex)
                    logger.exception(
                        'could not receive data from websocket, '
                        'reconnecting... exception was: %s', ex
                    )
                    request_failure.fire(
                        request_type='WEBSOCKET_DROP',
                        name='websocket dropped',
                        response_time=end_at,
                        exception=ex,
                    )
                    reconnect()
                    return

                try:
                    data = json.loads(res)
                except JSONDecodeError:
                    emsg = 'unable to decode response: %s' % res
                    logger.error(emsg)
                    request_failure.fire(
                        request_type='MALEFORMED RESPONSE',
                        name='Maleformed Response',
                        response_time=time(),
                        exception=RuntimeError(emsg),
                    )

                """
                response type cheat sheet for the hero extending this logic :).
                Message     Type    ID  Direction   Category
                WELCOME     0    Server-to-client    Auxiliary
                PREFIX      1    Client-to-server    Auxiliary
                CALL        2    Client-to-server    RPC
                CALLRESULT  3    Server-to-client    RPC
                CALLERROR   4    Server-to-client    RPC
                SUBSCRIBE   5    Client-to-server    PubSub
                UNSUBSCRIBE 6    Client-to-server    PubSub
                PUBLISH     7    Client-to-server    PubSub
                EVENT       8    Server-to-client    PubSub
                """

                call_id = data[1]
                response_type = data[0]
                try:
                    start_at = self.pending[call_id]['start_at']
                    name = self.pending[call_id]['name']
                    # clean up this dict otherwise it gets huuuge
                    del self.pending[call_id]
                except KeyError:
                    start_at = end_at
                    name = ''
                    # server to client has never a start time
                    if not self.awaiting_login_confirmation and response_type in (1, 2, 5, 6, 7):
                        logger.error(
                            'call %s has no start time or name', call_id
                        )
                    else:
                        self.awaiting_login_confirmation = False

                response_time = int((end_at - start_at) * 1000)
                event_type = 'WebSocket Recv'

                if response_type == 4:
                    """
                    last entry of wamp error response is either errorDetails on
                    pos 4 or errorDesc on pos 3 so no matter last entry it is.
                    """
                    error_msg = data.pop()
                    logger.error('CALLERROR: %s (%s)', data.pop(), error_msg)
                    request_failure.fire(
                        request_type=event_type,
                        name=name,
                        response_time=response_time,
                        exception=RuntimeError(error_msg),
                    )
                elif response_type == 8:
                    """
                    event
                    """
                    request_success.fire(
                        request_type='Event Revc',
                        name=str(data[1].replace("http://domain/", "")),
                        response_time=0,
                        response_length=len(res),
                    )
                else:
                    """
                    currently every other response type means success.
                    deciding what response type is requested might happen
                    via the `pending` variable on request time.
                    that could come in handy sometimes I guess.
                    """
                    request_success.fire(
                        request_type=event_type,
                        name=name,
                        response_time=response_time,
                        response_length=len(res),
                    )

        def _ping():
            while True:
                gevent.sleep(10)
                cid = generate_call_id()
                body = '[2,"{}","http://domain/ping"]'.format(cid)
                self._send_ws(cid, 'ping', body)

        gevent.spawn(_receive)
        gevent.spawn(_ping)

    def _send_ws(self, cid, name, body):
        """
        does the actual ws sending
        """
        start_at = time()
        self.pending[cid] = {
            'start_at': start_at,
            'name': name
        }
        logger.info('sending request with name %s for payload %s', name, body)
        logger.debug(body)
        try:
            self.ws.send(body)
        except WebSocketConnectionClosedException as ex:
            websocket_dropped.fire(ex=ex)
            request_failure.fire(
                request_type='WEBSOCKET_DROP',
                name='websocket dropped',
                response_time=start_at,
                exception=ex,
            )
            self.on_start()
            return

        request_success.fire(
            request_type='WebSocket Sent',
            name=name,
            # this basically is always 0ish as its just the delay of the
            # sending...but one might see connection delays. also we need
            # this count as to match whether all requests got responses
            response_time=int((time() - start_at) * 1000),
            response_length=len(body),
        )

    def send_ws(self, ns, action, *args, **kwargs):
        call_id = generate_call_id()
        positional = ','.join([str(a) for a in args]) if args else ''
        keyword = str(json.dumps(kwargs)) if kwargs else None
        payload = positional
        if kwargs:
            payload += ',' + keyword

        body = '[2,"{call_id}","http://domain/{ns}/{action}",{payload}]'.format(
            call_id=call_id, ns=ns, action=action, payload=payload
        )
        # this is t place for finding slow requests if the have special params.
        # just make the name more unique.

        name = '{}.{}.{}'.format('ws', ns, action)

        if 'description' in kwargs:
            name += f" ({kwargs.pop('description')})"

        self._send_ws(call_id, name, body)

    def send_lp(self, ns, action, *args, **kwargs):
        args += (kwargs,)
        name = '{}.{}.{}'.format('lp', ns, action)

        if 'description' in kwargs:
            name += f" ({kwargs.pop('description')})"

        params = {
            "args": args,
            "action": action,
            "ns": ns,
            "debug": {'name': name}
        }

        with self.client.post(
                "/lp/rpc/", data=json.dumps(params), name=name,
                catch_response=True,
                headers={
                    "Authorization": "Token {}".format(self.auth_token),
                    "Content-Type": "application/json; charset=utf-8",
                },
                verify=False,
        ) as response:
            logger.debug('get_users response: %i' % response.status_code)
            if response.status_code < 200 or response.status_code > 299:
                response.failure(response.status_code)

    def send(self, ns, action, *args, **kwargs):
        # default should be WS, long polling is disabled for now as it does
        # not reflect the true performance (events and subscriptions on ws).
        if WS:
            self.send_ws(ns, action, *args, **kwargs)
        else:
            self.send_lp(ns, action, *args, **kwargs)

    def on_quit(self):
        # wait for the last responses to finish.
        i = 0
        max_wait_sec = 5
        while len(self.pending) and i < max_wait_sec:
            logger.info(
                'waiting to shutdown websocket, %i responses missing.',
                len(self.pending)
            )
            gevent.sleep(1)
            i += 1
        if i == max_wait_sec:
            logger.error(
                'waited for %i seconds but there are still %i requests '
                'missing. killing websocket.', i, len(self.pending)
            )
        self.ws.close()
        self.logger.info('websocket closed.')
