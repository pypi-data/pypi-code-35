import xml.etree.ElementTree as ET
from collections import namedtuple


class UnexpectedServerMessageType(Exception):
    pass


class MissingResult(Exception):
    pass


class ErrorResponse(Exception):
    pass


Response = namedtuple('Response', ('code', 'msg', 'data'))


class EPPMapping:
    _epp_ns_url = 'urn:ietf:params:xml:ns:epp-1.0'
    name = ns_url = None

    def __init__(self, transp):
        self._transp = transp

    def _mk_request(self, xml, response_data_extractor=None):
        self._transp.send(xml)
        resp = self._parse_response(self._transp.recv())
        if response_data_extractor:
            resp = resp._replace(data=response_data_extractor(resp.data))
        return resp

    @classmethod
    def _epp(cls):
        return ET.Element('epp', attrib={
            'xmlns': cls._epp_ns_url,
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:schemaLocation':
                'urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd'})

    def _cmd_node(self, cmd):
        e = self._epp()
        c = ET.SubElement(e, 'command')
        n = ET.SubElement(c, cmd)
        if self.ns_url:
            se = lambda e, tag, *a, **k: ET.SubElement(
                e, self.name + ':' + tag, *a, **k)
            n = se(n, cmd, attrib={'xmlns:' + self.name: self.ns_url})
        else:
            se = ET.SubElement
        return lambda: ET.tostring(e, encoding='utf8'), n, se

    @staticmethod
    def _get_in_xmlns(ns_url):
        return lambda e, match: e.find('{' + ns_url + '}' + match)

    @staticmethod
    def _get_all_xmlns(ns_url):
        return lambda e, match: e.findall('{' + ns_url + '}' + match)

    def _parse_response(self, xml):
        e = ET.fromstring(xml)
        se = self._get_in_xmlns(self._epp_ns_url)
        resp = se(e, 'response')
        if resp:
            result = se(resp, 'result')
            if result:
                code = result.get('code')
                r = Response(
                    result.get('code'),
                    se(result, 'msg').text.strip(),
                    se(resp, 'resData'))
                if code in {'1000', '1500'}:
                    return r
                else:
                    raise ErrorResponse(r)
            else:
                raise MissingResult(xml.decode('utf8'))
        else:
            raise UnexpectedServerMessageType(xml.decode('utf8'))


handled_objects = {}


def object_handler(name, ns_url):
    def wrap(cls):
        cls.name = name
        cls.ns_url = ns_url
        handled_objects[ns_url] = cls
        return cls
    return wrap
