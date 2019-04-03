from datetime import datetime

from peewee import (BooleanField, CharField, DateTimeField, Model, Proxy,
                    TextField)

db = Proxy()


class ModelBase(Model):
    _ns = CharField(max_length=16, index=True)
    created_on = DateTimeField(default=datetime.utcnow)


class User(ModelBase):
    username = CharField(unique=True)
    password = CharField()
    is_active = BooleanField(index=True)
    is_superuser = BooleanField()
    extras = TextField(null=True)

    class Meta:
        database = db
        table_name = 'auth_users'
        indexes = (
            (('_ns', 'username'), True),
        )


class Token(ModelBase):
    token = CharField(max_length=256, index=True)
    expires_on = DateTimeField()

    class Meta:
        database = db
        table_name = 'auth_tokens'


class Group(ModelBase):
    name = CharField()
    extras = TextField(null=True)

    def add_user(self, username):
        if GroupUser.filter(
                group=self.name, user=username, _ns=self._ns).count() == 0:
            GroupUser.create(group=self.name, user=username, _ns=self._ns)

    def remove_user(self, username):
        if GroupUser.filter(
                group=self.name, user=username, _ns=self._ns).count() > 0:
            GroupUser.delete().where(
                (GroupUser._ns == self._ns) &
                (GroupUser.group == self.name) &
                (GroupUser.user == username)
            ).execute()

    @classmethod
    def for_user(cls, username, _ns='0000000000000000'):
        return list(map(
            lambda item: item.group,
            GroupUser.filter(user=username, _ns=_ns)
        ))

    @property
    def users(self):
        return list(map(
            lambda item: item.user,
            GroupUser.filter(group=self.name, _ns=self._ns)
        ))

    class Meta:
        database = db
        table_name = 'auth_groups'
        indexes = (
            (('_ns', 'name'), True),
        )


class GroupUser(ModelBase):
    group = CharField()
    user = CharField()

    class Meta:
        database = db
        table_name = 'auth_group_users'
        indexes = (
            (('group', 'user', '_ns'), True),
        )


class ObjectOwner(ModelBase):
    object_type = CharField()
    object_id = CharField()
    user = CharField()

    class Meta:
        database = db
        table_name = 'auth_object_owners'
        indexes = (
            (('object_type', 'object_id', 'user', '_ns'), True),
        )


class Permission(ModelBase):
    permission_id = CharField()
    client = CharField()

    class Meta:
        database = db
        table_name = 'auth_permissions'
        indexes = (
            (('_ns', 'permission_id', 'client'), True),
        )


class ObjectPermission(ModelBase):
    object_type = CharField()
    object_id = CharField()
    permission_id = CharField()
    client = CharField()

    class Meta:
        database = db
        table_name = 'auth_object_permissions'
        indexes = (
            (
                ('_ns', 'object_type', 'object_id', 'permission_id', 'client'),
                True
            ),
        )
