from eppzy.rfc5730_epp import EPP

from test_contact import data_file_contents, MockTransport


def test_login():
    def checks(body):
        assert b'login' in body
        assert b'bobby' in body
        assert b'passable' in body
        return data_file_contents('rfc5730/login_example.xml')
    mt = MockTransport(
        checks, data_file_contents('rfc5730/greeting_example.xml'))
    e = EPP(mt)
    e.login('bobby', 'passable')


def test_logout():
    def checks(body):
        assert b'logout' in body
        return data_file_contents('rfc5730/logout_example.xml')
    mt = MockTransport(
        checks, data_file_contents('rfc5730/greeting_example.xml'))
    e = EPP(mt)
    e.logout()
