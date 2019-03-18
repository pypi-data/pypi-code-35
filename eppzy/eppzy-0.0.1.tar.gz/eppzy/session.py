from contextlib import contextmanager

from eppzy.bases import handled_objects
from eppzy.connection import connection
from eppzy.rfc5730_epp import EPP
from eppzy.rfc5733_contact import Contact
from eppzy.rfc5731_domain import Domain


_builtin_objects = (Contact, Domain)


@contextmanager
def session(host, port, client_id, password):
    with connection(host, port) as c:
        e = EPP(c)
        try:
            e.login(client_id, password)
            handled = {}
            for objUri in e.objUris:
                cls = handled_objects[objUri]
                handled[cls.name] = cls(c)
            yield handled
        finally:
            e.logout()
