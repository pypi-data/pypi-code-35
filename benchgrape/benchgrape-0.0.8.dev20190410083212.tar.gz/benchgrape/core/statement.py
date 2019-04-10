import json
import logging
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)


def login(client, user, password):
    if not user:
        logger.info('no user set in env var, falling back to admin')
        user = 'admin'

    if not password:
        logger.info('no password set in env var, falling back to admin')
        password = 'admin'

    with client.get(
            url="/api/accounts/session/",
            auth=HTTPBasicAuth(user, password),
            catch_response=True,
            verify=False,
    ) as response:
        print('login response: %i' % response.status_code)
        content = json.loads(response.content) if response.content else {}

        if response.status_code != 200 or 'detail' in content:
            msg = 'login failed %i %s' % (
                    response.status_code, content.get('detail')
            )
            print(msg)
            response.failure(msg)
            return
        return content['authtoken']


class PreparedStatementsMixin(object):
    """
    prepare statements for common requests like get_users or get_history,
    to be continued, those shall use the self.send in an abstract way so this
    mixin can be used by a HttpLocust OR a WampLocust Taskset equally.
    """
    org = None

    def send(self, ns, action, *args, **kwargs):
        raise NotImplementedError(
            'this mixin requires to be used with a taskset or adapter '
            'implementing a "send" method. see WampTaskSet implementation.'
        )

    @staticmethod
    def get_parameters(**kwargs):
        params = {}
        description = ''

        for param, value in kwargs.items():
            if value in ["", None]:
                description += f'without {param} '
            else:
                description += f'with {param} "{value}" '
                params[param] = value

        params['description'] = description

        return params

    def utils__connect_stack(self):
        self.organizations__get_organization()
        self.organizations__join()
        self.channels__get_overview()

    def utils__disconnect_stack(self):
        self.organizations__leave()

    def organizations__join(self):
        self.send('organizations', 'join', str(self.org))

    def organizations__leave(self):
        self.send('organizations', 'leave', str(self.org))

    def users__get_users(self, membership=None, query=None):
        params = self.get_parameters(membership=membership, query=query)

        self.send('users', 'get_users', str(self.org), **params)

    def rooms__get_rooms(self, membership=None, query=None):
        params = self.get_parameters(membership=membership, query=query)

        self.send('rooms', 'get_rooms', str(self.org), **params)

    def channels__get_history(self, ch, params=None):
        params = params or {}
        self.send('channels', 'get_history', ch, **params)

    def search__search_channels(self, search_text, limit=25, current_channel=None):
        self.send(
            'search', 'search_channels',
            self.org, search_text, limit, current_channel
        )

    def search__search_users(self, search_text, limit=25, current_channel=None):
        self.send(
            'search', 'search_users',
            self.org, search_text, limit, current_channel
        )

    def channels__get_overview(self, params=None):
        self.send(
            'channels', 'get_overview',
            str(self.org), params
        )

    def channels__post(self, ch_id, message):
        self.send(
            'channels', 'post',
            ch_id, '"' + str(message) + '"'
        )

    def channels__join(self, ch_id):
        self.send(
            'channels', 'join',
            ch_id
        )

    def channels__leave(self, ch_id):
        self.send(
            'channels', 'leave',
            ch_id
        )

    def channels__read(self, ch_id, msg_id):
        self.send(
            'channels', 'read',
            ch_id, msg_id
        )

    def channels__set_typing(self, ch_id, typing):
        self.send(
            'channels', 'set_typing',
            ch_id, typing
        )

    def organizations__get_organization(self):
        self.send(
            'organizations', 'get_organization',
            str(self.org), return_channels=False, return_user=False
        )
