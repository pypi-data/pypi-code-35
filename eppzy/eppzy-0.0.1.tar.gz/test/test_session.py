from mock import Mock, patch

from eppzy.rfc5730_epp import EPP
from eppzy.session import session


def test_session():
    with patch('eppzy.session.connection'):
        mock_epp = Mock(spec=EPP)
        with patch('eppzy.session.EPP', lambda _: mock_epp):
            mock_epp.objUris = {'urn:ietf:params:xml:ns:domain-1.0'}
            with session('h', 12, 'someone', 'somepass') as objs:
                assert 'domain' in objs
