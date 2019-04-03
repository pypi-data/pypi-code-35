from drongo.utils.endpoint import APIEndpoint
from drongo.utils.helpers import URLHelper


class UserFromToken(APIEndpoint):
    __url__ = '/users/from-token'
    __http_methods__ = ['GET']

    def init(self):
        self.token = self.ctx.request.query.get('token', [None])[0]
        self.auth = self.ctx.modules.auth
        self.svc = self.auth.services.UserFromToken(token=self.token)

    def validate(self):
        if self.token is None:
            self.error(message='No auth token specified.')
            return False

        self.user = self.svc.call(self.ctx.ns)
        if self.user is None:
            self.error(message='Invalid or unauthorized token.')
            return False

        return True

    def call(self):
        return {
            'username': self.user.username,
            'is_authenticated': True,
            'is_superuser': self.user.is_superuser
        }


class UserCreate(APIEndpoint):
    __url__ = '/users'
    __http_methods__ = ['POST']

    def init(self):
        self.obj = self.ctx.request.json
        self.auth = self.ctx.modules.auth
        self.svc = self.auth.services.UserCreate(
            username=self.obj.get('username'),
            password=self.obj.get('password'),
            is_active=self.auth.config.active_on_register,
            is_superuser=False
        )

    def validate(self):
        if self.svc.check_exists():
            self.error(
                group='username',
                message='Username already exists.'
            )
            return False
        return True

    def call(self):
        self.svc.call(self.ctx.ns)
        return {'username': self.obj.get('username')}


class UserVerifyCredentials(APIEndpoint):
    __url__ = '/users/operations/verify-credentials'
    __http_methods__ = ['POST']

    def init(self):
        self.obj = self.ctx.request.json
        self.auth = self.ctx.modules.auth
        self.svc = self.auth.services.UserVerifyCredentials(
            username=self.obj.get('username'),
            password=self.obj.get('password')
        )

    def validate(self):
        if not self.svc.call(self.ctx.ns):
            self.error(message='Invalid username or password.')
            return False
        return True

    def call(self):
        return True


class UserTokenCreate(APIEndpoint):
    __url__ = '/users/{username}/operations/token-create'
    __http_methods__ = ['POST']

    def init(self):
        self.auth = self.ctx.modules.auth
        self.svc = self.auth.services.UserTokenCreate(
            username=self.username)

    def call(self):
        return self.svc.call(self.ctx.ns)


class UserTokenDelete(APIEndpoint):
    __url__ = '/users/operations/token-delete'
    __http_methods__ = ['DELETE']

    def init(self):
        self.token = self.ctx.request.query.get('token', [None])[0]
        self.auth = self.ctx.modules.auth
        self.svc = self.auth.services.UserTokenDelete(token=self.token)

    def call(self):
        self.svc.call(self.ctx.ns)
        return True


class UserChangePassword(APIEndpoint):
    __url__ = '/users/operations/change-password'
    __http_methods__ = ['POST']

    def init(self):
        self.obj = self.ctx.request.json
        self.auth = self.ctx.modules.auth

        self.svc = self.auth.services.UserChangePassword(
            username=self.obj.get('username'),
            password=self.obj.get('password')
        )

    def validate(self):
        if not self.svc.call(self.ctx.ns):
            return False
        return True

    def call(self):
        return True


class UserTokenRefresh(APIEndpoint):
    __url__ = '/users/operations/refresh-token'
    __http_methods__ = ['POST']

    def init(self):
        self.auth = self.ctx.modules.auth
        self.token = self.ctx.request.json.get('token')

    def call(self):
        return self.auth.services.UserTokenRefresh(
            self.token).call(self.ctx.ns)


class UserActivate(APIEndpoint):
    __url__ = '/users/{username}/operations/activate'
    __http_methods__ = ['POST']

    def init(self):
        self.auth = self.ctx.modules.auth
        self.svc = self.auth.services.UserActivate(username=self.username)

    def call(self):
        return self.svc.call(self.ctx.ns)


class UserDeactivate(APIEndpoint):
    __url__ = '/users/{username}/operations/deactivate'
    __http_methods__ = ['POST']

    def init(self):
        self.auth = self.ctx.modules.auth
        self.svc = self.auth.services.UserDeactivate(username=self.username)

    def call(self):
        return self.svc.call(self.ctx.ns)


class UserList(APIEndpoint):
    __url__ = '/users'
    __http_methods__ = 'GET'

    def init(self):
        self.auth = self.ctx.modules.auth
        self.user = self.ctx.auth.user
        q = self.ctx.request.query
        self.active_only = q.get('active_only', ['no'])[0] == 'yes'
        self.page_number = int(q.get('page_number', [1])[0])
        self.page_size = int(q.get('page_size', [50])[0])

    def _transform(self, obj):
        return {
            'username': obj.username,
            'is_active': obj.is_active,
            'is_superuser': obj.is_superuser
        }

    def call(self):
        return list(map(
            self._transform,
            self.auth.services.UserList(
                active_only=self.active_only,
                page_number=self.page_number,
                page_size=self.page_size
            ).call(self.ctx.ns)
        ))


class GroupCreate(APIEndpoint):
    __url__ = '/groups'
    __http_methods__ = ['POST']

    def init(self):
        self.auth = self.ctx.modules.auth
        self.obj = self.ctx.request.json

    def call(self):
        self.auth.services.GroupCreate(
            groupname=self.obj['name']).call(self.ctx.ns)
        return self.obj['name']


class GroupDelete(APIEndpoint):
    __url__ = '/groups/{group}'
    __http_methods__ = ['DELETE']

    def init(self):
        self.auth = self.ctx.modules.auth
        self.user = self.ctx.auth.user

    def call(self):
        self.auth.services.GroupDelete(groupname=self.group).call(self.ctx.ns)
        return True


class GroupList(APIEndpoint):
    __url__ = '/groups'
    __http_methods__ = 'GET'

    def init(self):
        self.auth = self.ctx.modules.auth
        q = self.ctx.request.query
        self.page_number = int(q.get('page_number', [1])[0])
        self.page_size = int(q.get('page_size', [50])[0])

    def _transform(self, obj):
        return {
            'name': obj.name,
            'users': obj.users
        }

    def call(self):
        return list(map(
            self._transform,
            self.auth.services.GroupList(
                page_number=self.page_number,
                page_size=self.page_size
            ).call(self.ctx.ns)
        ))


class GroupAddUser(APIEndpoint):
    __url__ = '/groups/{group}/users'
    __http_methods__ = 'POST'

    def init(self):
        self.auth = self.ctx.modules.auth

    def call(self):
        self.auth.services.GroupAddUser(
            groupname=self.group,
            username=self.ctx.request.json['username']
        ).call(self.ctx.ns)
        return True


class GroupDeleteUser(APIEndpoint):
    __url__ = '/groups/{group}/users/{username}'
    __http_methods__ = 'DELETE'

    def init(self):
        self.auth = self.ctx.modules.auth

    def call(self):
        self.auth.services.GroupDeleteUser(
            groupname=self.group,
            username=self.username
        ).call(self.ctx.ns)
        return True


class GroupListUsers(APIEndpoint):
    __url__ = '/groups/{group}/users'

    def init(self):
        self.auth = self.ctx.modules.auth

    def call(self):
        return self.auth.services.GroupListUsers(
            groupname=self.group).call(self.ctx.ns)


class UserListGroups(APIEndpoint):
    __url__ = '/users/{username}/groups'

    def init(self):
        self.auth = self.ctx.modules.auth

    def call(self):
        return self.auth.services.UserListGroups(
            username=self.username).call(self.ctx.ns)


class PermissionAddClient(APIEndpoint):
    __url__ = '/permissions/{_id}/clients'
    __http_methods__ = 'POST'

    def init(self):
        self.auth = self.ctx.modules.auth
        self.obj = self.ctx.request.json

    def call(self):
        self.auth.services.PermissionAddClient(
            permission_id=self._id,
            client=self.obj.get('client')
        ).call(self.ctx.ns)
        return True


class PermissionDeleteClient(APIEndpoint):
    __url__ = '/permissions/{_id}/clients/{client}'
    __http_methods__ = ['DELETE']

    def init(self):
        self.auth = self.ctx.modules.auth

    def call(self):
        self.auth.services.PermissionDeleteClient(
            permission_id=self._id,
            client=self.client
        ).call(self.ctx.ns)
        return True


class PermissionListClients(APIEndpoint):
    __url__ = '/permissions/{_id}/clients'
    __http_methods__ = ['GET']

    def init(self):
        self.auth = self.ctx.modules.auth

    def call(self):
        return list(map(
            lambda item: item.client,
            self.auth.services.PermissionListClients(
                permission_id=self._id
            ).call(self.ctx.ns)))


class PermissionCheckUser(APIEndpoint):
    __url__ = '/permissions/{_id}/check-user'
    __http_methods__ = 'POST'

    def init(self):
        self.auth = self.ctx.modules.auth
        self.obj = self.ctx.request.json

    def call(self):
        return self.auth.services.PermissionCheckUser(
            permission_id=self._id,
            username=self.obj.get('username')
        ).call(self.ctx.ns)


class ObjectPermissionAddClient(APIEndpoint):
    __url__ = '/permissions/{_id}/objects/{object_type}/{object_id}/clients'
    __http_methods__ = ['POST']

    def init(self):
        self.auth = self.ctx.modules.auth
        self.obj = self.ctx.request.json

    def call(self):
        self.auth.services.ObjectPermissionAddClient(
            object_type=self.object_type,
            object_id=self.object_id,
            permission_id=self._id,
            client=self.obj.get('client')
        ).call(self.ctx.ns)
        return 'OK'


class ObjectPermissionDeleteClient(APIEndpoint):
    __url__ = (
        '/permissions/{_id}/objects/'
        '{object_type}/{object_id}/clients/{client}'
    )
    __http_methods__ = ['DELETE']

    def init(self):
        self.auth = self.ctx.modules.auth

    def call(self):
        self.auth.services.ObjectPermissionDeleteClient(
            object_type=self.object_type,
            object_id=self.object_id,
            permission_id=self._id,
            client=self.client
        ).call(self.ctx.ns)
        return 'OK'


class ObjectPermissionListClients(APIEndpoint):
    __url__ = '/permissions/{_id}/objects/{object_type}/{object_id}/clients'
    __http_methods__ = ['GET']

    def init(self):
        self.auth = self.ctx.modules.auth

    def call(self):
        return list(map(
            lambda item: item.client,
            self.auth.services.ObjectPermissionListClients(
                object_type=self.object_type,
                object_id=self.object_id,
                permission_id=self._id
            ).call(self.ctx.ns)))


class ObjectPermissionCheckUser(APIEndpoint):
    __url__ = '/permissions/{_id}/objects/{object_type}/{object_id}/check-user'
    __http_methods__ = 'POST'

    def init(self):
        self.auth = self.ctx.modules.auth
        self.obj = self.ctx.request.json

    def call(self):
        return self.auth.services.ObjectPermissionCheckUser(
            object_type=self.object_type,
            object_id=self.object_id,
            permission_id=self._id,
            username=self.obj.get('username')
        ).call(self.ctx.ns)


class ObjectOwnerSet(APIEndpoint):
    __url__ = '/objects/{_type}/{_id}/operations/set-owner'
    __http_methods__ = 'PUT'

    def init(self):
        self.auth = self.ctx.modules.auth
        self.obj = self.ctx.request.json

    def call(self):
        self.auth.services.ObjectOwnerSet(
            object_type=self._type,
            object_id=self._id,
            username=self.obj.get('username')
        ).call(self.ctx.ns)
        return 'OK'


class ObjectOwnerGet(APIEndpoint):
    __url__ = '/objects/{_type}/{_id}/owner'
    __http_methods__ = 'GET'

    def init(self):
        self.auth = self.ctx.modules.auth

    def call(self):
        return self.auth.services.ObjectOwnerGet(
            object_type=self._type,
            object_id=self._id
        ).call(self.ctx.ns)


AVAILABLE_API = [
    UserFromToken,
    UserCreate,
    UserVerifyCredentials,
    UserTokenCreate,
    UserTokenDelete,
    UserTokenRefresh,
    UserChangePassword,
    UserActivate,
    UserDeactivate,
    UserList,

    GroupCreate,
    GroupDelete,
    GroupList,

    GroupAddUser,
    GroupDeleteUser,
    GroupListUsers,
    UserListGroups,

    ObjectOwnerSet,
    ObjectOwnerGet,

    PermissionAddClient,
    PermissionDeleteClient,
    PermissionListClients,
    PermissionCheckUser,

    ObjectPermissionAddClient,
    ObjectPermissionDeleteClient,
    ObjectPermissionListClients,
    ObjectPermissionCheckUser
]


class AuthAPI(object):
    def __init__(self, app, module, base_url):
        self.app = app
        self.module = module
        self.base_url = base_url

        self.init_endpoints()

    def init_endpoints(self):
        for endpoint in AVAILABLE_API:
            URLHelper.endpoint(
                app=self.app,
                klass=endpoint,
                base_url=self.base_url
            )
