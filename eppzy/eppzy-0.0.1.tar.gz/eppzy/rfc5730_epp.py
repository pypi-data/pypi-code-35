import xml.etree.ElementTree as ET

from eppzy.bases import (
    EPPMapping, handled_objects, UnexpectedServerMessageType)


class EPP(EPPMapping):
    def __init__(self, transp):
        super().__init__(transp)
        self.greeting = self._recv_greeting()
        self._objUris = None

    def _recv_greeting(self):
        xml = self._transp.recv()
        e = ET.fromstring(xml)
        se = self._get_in_xmlns(self._epp_ns_url)
        g = se(e, 'greeting')
        m = se(g, 'svcMenu')
        if g:
            return {
                'svID': se(g, 'svID').text,
                'objURIs': {n.text for n in m.findall(
                    '{' + self._epp_ns_url + '}objURI')}
            }
        else:
            raise UnexpectedServerMessageType(xml.decode('utf8'))

    @property
    def objUris(self):
        if self._objUris is None:
            self._objUris = self.greeting['objURIs'] & set(handled_objects)
        return self._objUris

    def login(self, client_id, password):
        render, l, se = self._cmd_node('login')
        se(l, 'clID').text = client_id
        se(l, 'pw').text = password
        opts = se(l, 'options')
        se(opts, 'version').text = '1.0'
        se(opts, 'lang').text = 'en'
        svcs = se(l, 'svcs')
        for objUri in self.objUris:
            se(svcs, 'objURI').text = objUri
        return self._mk_request(render())

    def logout(self):
        render, l, se = self._cmd_node('logout')
        return self._mk_request(render())
