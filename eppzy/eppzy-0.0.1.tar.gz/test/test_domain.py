from eppzy.rfc5731_domain import Domain

from test_contact import data_file_contents, MockTransport


def test_minimal_domain_info():
    def checks(body):
        assert b'dname' in body
        assert b'domain-1.0' in body
        return data_file_contents('rfc5731/domain_info_example.xml')
    mt = MockTransport(checks)
    d = Domain(mt)
    r = d.info('dname')
    assert r.data['name'] == 'example.com'


def test_full_domain_info():
    def checks(body):
        assert b'dname' in body
        assert b'domain-1.0' in body
        return data_file_contents('rfc5731/domain_info_full_example.xml')
    mt = MockTransport(checks)
    d = Domain(mt)
    r = d.info('dname')
    assert r.data['name'] == 'example.com'
    assert r.data['host'] == ['ns1.example.com', 'ns2.example.com']
    assert r.data['registrant'] == 'jd1234'
