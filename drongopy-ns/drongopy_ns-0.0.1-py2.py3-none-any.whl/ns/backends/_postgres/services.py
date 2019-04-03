import random

from .models import Namespace, db

_KEY_SET = 'qwertyuiopasdfghjklzxcvbnm1234567890'


def _generate_key(length=8):
    s = ''
    for i in range(length):
        s += random.choice(_KEY_SET)
    return s


class NSServiceBase(object):
    @classmethod
    def init(cls, module):
        cls.module = module
        db.initialize(module.database.instance.get())
        module.database.instance.get().create_tables([Namespace])
        if Namespace.get_or_none(uid='0000000000000000') is None:
            Namespace.create(
                uid='0000000000000000',
                name='Drongo',
                _ns='0000000000000000'
            )


class NamespaceCreate(NSServiceBase):
    def __init__(self, name, description, is_active=False):
        self.name = name
        self.description = description
        self.is_active = is_active

    def call(self, ns='0000000000000000'):
        return Namespace.create(
            name=self.name,
            description=self.description,
            is_active=self.is_active,
            uid=_generate_key(32),
            _ns=ns
        )


class NamespaceGet(NSServiceBase):
    def __init__(self, uid):
        self.uid = uid

    def call(self, ns='0000000000000000'):
        return Namespace.get_or_none(
            uid=self.uid,
            _ns=ns)


class NamespaceActivate(NSServiceBase):
    def __init__(self, uid):
        self.uid = uid

    def call(self, ns='0000000000000000'):
        ns = Namespace.get_or_none(uid=self.uid, _ns=ns)
        if ns is not None:
            ns.is_active = True
            ns.save()
            return True
        return False


class NamespaceDeactivate(NSServiceBase):
    def __init__(self, uid):
        self.uid = uid

    def call(self, ns='0000000000000000'):
        ns = Namespace.get_or_none(uid=self.uid, _ns=ns)
        if ns is not None:
            ns.is_active = False
            ns.save()
            return True
        return False


class NamespaceUpdate(NSServiceBase):
    def __init__(self, uid, name=None, description=None):
        self.uid = uid
        self.name = name
        self.description = description

    def call(self, ns='0000000000000000'):
        ns = Namespace.get_or_none(uid=self.uid, _ns=ns)
        if ns is not None:
            ns.name = self.name or ns.name
            ns.description = self.description or ns.description
            ns.save()
            return True
        return False


class NamespaceDelete(NSServiceBase):
    def __init__(self, uid):
        self.uid = uid

    def call(self, ns='0000000000000000'):
        ns = Namespace.get_or_none(uid=self.uid, _ns=ns)
        if ns is not None:
            ns.del_inst()


class NamespaceList(NSServiceBase):
    def __init__(self, active_only=False, page_number=1, page_size=50):
        self.active_only = active_only
        self.page_number = page_number
        self.page_size = page_size

    def call(self, ns='0000000000000000'):
        q = Namespace.sel().where(Namespace._ns == ns)
        if self.active_only:
            q = q.where(Namespace.is_active == True)  # noqa: E712

        return q.count(), q.paginate(self.page_number, self.page_size)
