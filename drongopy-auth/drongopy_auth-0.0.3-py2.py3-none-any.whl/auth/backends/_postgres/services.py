from datetime import datetime, timedelta

import jwt
from passlib.hash import pbkdf2_sha256

from .models import (Group, GroupUser, ObjectOwner, ObjectPermission,
                     Permission, Token, User, db)

HASHER = pbkdf2_sha256.using(rounds=10000)


class AuthServiceBase(object):
    @classmethod
    def init(cls, module):
        cls.module = module
        db.initialize(module.database.instance.get())
        models = [
            User, Group, GroupUser, ObjectOwner, ObjectPermission,
            Permission, Token
        ]
        for model in models:
            module.database.instance.auto_migrate(model)


class UserFromToken(AuthServiceBase):
    def __init__(self, token):
        self.token = token

    def call(self, ns='0000000000000000'):
        token = self.token

        if token is None:
            return None

        try:
            token = jwt.decode(
                token, self.module.config.token_secret, algorithms=['HS256'])
            if Token.get_or_none(token=self.token, _ns=ns) is None:
                return None
        except jwt.ExpiredSignatureError:
            return None
        except Exception:
            return None

        username = token.get('username')
        return User.get_or_none(username=username, _ns=ns)


class UserCreate(AuthServiceBase):
    def __init__(
            self, username, password, is_active=False, is_superuser=False):
        self.username = username
        self.password = HASHER.hash(password)
        self.is_active = is_active
        self.is_superuser = is_superuser

    def check_exists(self, ns='0000000000000000'):
        return User.filter(
            username=self.username,
            _ns=ns
        ).count() > 0

    def call(self, ns='0000000000000000'):
        return User.create(
            username=self.username,
            password=self.password,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            _ns=ns
        )


class UserVerifyCredentials(AuthServiceBase):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def call(self, ns='0000000000000000'):
        user = User.get_or_none(
            username=self.username, is_active=True, _ns=ns)
        if user is None:
            return False
        return HASHER.verify(self.password, user.password)


class UserTokenCreate(AuthServiceBase):
    def __init__(self, username):
        self.username = username

    def call(self, ns='0000000000000000'):
        user = User.get(
            username=self.username, is_active=True, _ns=ns)
        exp = datetime.utcnow() \
            + timedelta(seconds=self.module.config.token_age)
        token = jwt.encode({
            'username': user.username,
            'iat': datetime.utcnow(),
            'exp': exp
        }, self.module.config.token_secret, algorithm='HS256')
        token = token.decode('ascii')
        Token.create(token=token, expires_on=exp, _ns=ns)
        return token


class UserTokenDelete(AuthServiceBase):
    def __init__(self, token):
        self.token = token

    def call(self, ns='0000000000000000'):
        token = Token.get_or_none(token=self.token, _ns=ns)
        if token is not None:
            token.delete_instance()
        return True


class UserTokenRefresh(AuthServiceBase):
    def __init__(self, token):
        self.token = token

    def call(self, ns='0000000000000000'):
        try:
            token = jwt.decode(
                self.token, self.module.config.token_secret,
                algorithms=['HS256'])
            token.update({
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow()
                + timedelta(seconds=self.module.config.token_age)
            })
            return jwt.encode(
                token, self.module.config.token_secret, algorithm='HS256'
            ).decode('ascii')
        except jwt.ExpiredSignatureError:
            return None
        except Exception:
            return None


class UserChangePassword(AuthServiceBase):
    def __init__(self, username, password):
        self.username = username
        self.password = HASHER.hash(password)

    def call(self, ns='0000000000000000'):
        user = User.get_or_none(
            username=self.username, is_active=True, _ns=ns)
        if user is None:
            return False
        user.password = self.password
        user.save()
        return True


class UserActivate(AuthServiceBase):
    def __init__(self, username):
        self.username = username

    def call(self, ns='0000000000000000'):
        user = User.get_or_none(username=self.username, _ns=ns)
        if user is not None:
            user.is_active = True
            user.save()
            return True

        return False


class UserDeactivate(AuthServiceBase):
    def __init__(self, username):
        self.username = username

    def call(self, ns='0000000000000000'):
        user = User.get_or_none(username=self.username, _ns=ns)
        if user is not None:
            user.is_active = False
            user.save()
            return True

        return False


class UserList(AuthServiceBase):
    def __init__(self, active_only=False, page_number=1, page_size=50):
        self.active_only = active_only
        self.page_number = page_number
        self.page_size = page_size

    def call(self, ns='0000000000000000'):
        q = User.select().where(User._ns == ns)
        if self.active_only:
            q = q.where(
                (User.is_active == True)  # noqa: E712
            )
        return q.paginate(self.page_number, self.page_size)


class GroupCreate(AuthServiceBase):
    def __init__(self, groupname):
        self.groupname = groupname

    def call(self, ns='0000000000000000'):
        return Group.get_or_create(name=self.groupname, _ns=ns)[0]


class GroupDelete(AuthServiceBase):
    def __init__(self, groupname):
        self.groupname = groupname

    def call(self, ns='0000000000000000'):
        group = Group.get_or_none(name=self.groupname, _ns=ns)
        if group is not None:
            group.delete_instance()
            return True
        return False


class GroupList(AuthServiceBase):
    def __init__(self, page_number=1, page_size=50):
        self.page_number = page_number
        self.page_size = page_size

    def call(self, ns='0000000000000000'):
        return Group.select().where(
            Group._ns == ns
        ).paginate(self.page_number, self.page_size)


class GroupAddUser(AuthServiceBase):
    def __init__(self, groupname, username):
        self.groupname = groupname
        self.username = username

    def call(self, ns='0000000000000000'):
        group, _ = Group.get_or_create(name=self.groupname, _ns=ns)
        group.add_user(self.username)
        return True


class GroupDeleteUser(AuthServiceBase):
    def __init__(self, groupname, username):
        self.groupname = groupname
        self.username = username

    def call(self, ns='0000000000000000'):
        group = Group.get_or_none(name=self.groupname, _ns=ns)
        if group is None:
            return False
        group.remove_user(self.username)
        return True


class GroupListUsers(AuthServiceBase):
    def __init__(self, groupname):
        self.groupname = groupname

    def call(self, ns='0000000000000000'):
        group = Group.get_or_none(name=self.groupname, _ns=ns)
        if group is None:
            return []

        return group.users


class UserListGroups(AuthServiceBase):
    def __init__(self, username):
        self.username = username

    def call(self, ns='0000000000000000'):
        return Group.for_user(username=self.username, _ns=ns)


class PermissionAddClient(AuthServiceBase):
    def __init__(self, permission_id, client):
        self.permission_id = permission_id
        self.client = client

    def call(self, ns='0000000000000000'):
        Permission.get_or_create(
            permission_id=self.permission_id,
            client=self.client,
            _ns=ns)


class PermissionDeleteClient(AuthServiceBase):
    def __init__(self, permission_id, client):
        self.permission_id = permission_id
        self.client = client

    def call(self, ns='0000000000000000'):
        permission = Permission.get_or_none(
            permission_id=self.permission_id,
            client=self.client,
            _ns=ns)
        if permission is not None:
            permission.delete_instance()


class PermissionListClients(AuthServiceBase):
    def __init__(self, permission_id):
        self.permission_id = permission_id

    def call(self, ns='0000000000000000'):
        return Permission.select().where(
            (Permission._ns == ns) &
            (Permission.permission_id == self.permission_id)
        )


class PermissionCheckUser(AuthServiceBase):
    def __init__(self, permission_id, username):
        self.permission_id = permission_id
        self.username = username

    def call(self, ns='0000000000000000'):
        user = User.get_or_none(username=self.username, is_active=True, _ns=ns)
        if user is None:
            return False

        if user.is_superuser:
            return True

        permission = Permission.get_or_none(
            permission_id=self.permission_id,
            client='user.' + self.username,
            _ns=ns)
        if permission is not None:
            return True

        groups = list(map(
            lambda group: 'group.{group}'.format(group=group),
            Group.for_user(self.username)))
        permission = Permission.select().where(
            (Permission._ns == ns) &
            (Permission.permission_id == self.permission_id) &
            (Permission.client.in_(groups))
        ).count()
        if permission > 0:
            return True

        return False


class ObjectPermissionAddClient(AuthServiceBase):
    def __init__(self, object_type, object_id, permission_id, client):
        self.object_type = object_type
        self.object_id = object_id
        self.permission_id = permission_id
        self.client = client

    def call(self, ns='0000000000000000'):
        ObjectPermission.get_or_create(
            object_type=self.object_type,
            object_id=self.object_id,
            permission_id=self.permission_id,
            client=self.client,
            _ns=ns
        )


class ObjectPermissionDeleteClient(AuthServiceBase):
    def __init__(self, object_type, object_id, permission_id, client):
        self.object_type = object_type
        self.object_id = object_id
        self.permission_id = permission_id
        self.client = client

    def call(self, ns='0000000000000000'):
        permission = ObjectPermission.get_or_none(
            object_type=self.object_type,
            object_id=self.object_id,
            permission_id=self.permission_id,
            client=self.client,
            _ns=ns
        )
        if permission is not None:
            permission.delete_instance()


class ObjectPermissionListClients(AuthServiceBase):
    def __init__(self, object_type, object_id, permission_id):
        self.object_type = object_type
        self.object_id = object_id
        self.permission_id = permission_id

    def call(self, ns='0000000000000000'):
        return ObjectPermission.select().where(
            (ObjectPermission._ns == ns) &
            (ObjectPermission.object_type == self.object_type) &
            (ObjectPermission.object_id == self.object_id) &
            (ObjectPermission.permission_id == self.permission_id)
        )


class ObjectPermissionCheckUser(AuthServiceBase):
    def __init__(self, object_type, object_id, permission_id, username):
        self.object_type = object_type
        self.object_id = object_id
        self.permission_id = permission_id
        self.username = username

    def call(self, ns='0000000000000000'):
        user = User.get_or_none(username=self.username, is_active=True, _ns=ns)
        if user is None:
            return False

        if user.is_superuser:
            return True

        permission = ObjectPermission.get_or_none(
            object_type=self.object_type, object_id=self.object_id,
            permission_id=self.permission_id, client='user.' + self.username,
            _ns=ns)
        if permission is not None:
            return True

        groups = list(map(
            lambda group: 'group.{group}'.format(group=group),
            Group.for_user(self.username)
        ))
        permission = ObjectPermission.select().where(
            (ObjectPermission._ns == ns) &
            (ObjectPermission.object_type == self.object_type) &
            (ObjectPermission.object_id == self.object_id) &
            (ObjectPermission.permission_id == self.permission_id) &
            ObjectPermission.client.in_(groups)
        ).count()
        if permission > 0:
            return True

        return False


class PermissionListForClient(AuthServiceBase):
    def __init__(self, client):
        self.client = client

    def call(self, ns='0000000000000000'):
        return list(map(
            lambda item: item.permission_id,
            Permission.select().where(
                (Permission._ns == ns) &
                (Permission.client == self.client)
            )
        ))


class ObjectOwnerGet(AuthServiceBase):
    def __init__(self, object_type, object_id):
        self.object_type = object_type
        self.object_id = object_id

    def call(self, ns='0000000000000000'):
        owner = ObjectOwner.get_or_none(
            object_type=self.object_type, object_id=self.object_id, _ns=ns)

        if owner is not None:
            return owner.user


class ObjectOwnerSet(AuthServiceBase):
    def __init__(self, object_type, object_id, username):
        self.object_type = object_type
        self.object_id = object_id
        self.username = username

    def call(self, ns='0000000000000000'):
        owner = ObjectOwner.get_or_none(
            object_type=self.object_type, object_id=self.object_id, _ns=ns)

        if owner is not None:
            owner.user = self.username
            owner.save()
        else:
            ObjectOwner.create(
                object_type=self.object_type,
                object_id=self.object_id,
                user=self.username,
                _ns=ns
            )
