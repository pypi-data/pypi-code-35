from os.path import dirname, join

from eppzy.rfc5733_contact import Contact


class MockTransport:
    def __init__(self, respond, greeting=None):
        self._respond = respond
        self._response = greeting

    def send(self, body):
        self._response = self._respond(body)

    def recv(self):
        return self._response


def data_file_contents(relpath):
    p = join(dirname(__file__), relpath)
    with open(p) as f:
        return f.read().encode('utf8')


def test_contact_create():
    def checks(body):
        assert b'sop' in body
        return data_file_contents('rfc5733/contact_create_example.xml')
    mt = MockTransport(checks)
    ct = Contact(mt)
    r = ct.create(
        'cid', 'nam', 'org', 'street', 'city', 'sop', 'RC32 NFQ', 'GB',
        '+44.382919', 'fax', 'bob@bob.bob', '')
    assert r.data['id'] == 'sh8013'


def test_contact_info():
    def checks(body):
        assert b'passable' in body
        return data_file_contents('rfc5733/contact_info_example.xml')
    mt = MockTransport(checks)
    ct = Contact(mt)
    r = ct.info('cid', 'passable')
    assert r.data['city'] == 'Dulles'


def test_contact_update():
    def checks(body):
        assert b'Frodo' in body
        return data_file_contents('rfc5733/contact_update_example.xml')
    mt = MockTransport(checks)
    ct = Contact(mt)
    r = ct.update(
        'conid', state_or_province='The Shire', name='Frodo',
        email='a@hob.bit')
    assert 'completed' in r.msg
