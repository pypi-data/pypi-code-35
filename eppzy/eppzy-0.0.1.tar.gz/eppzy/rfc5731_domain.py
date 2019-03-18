from eppzy.bases import EPPMapping, object_handler


def extract_optional(se, xml, d, xml_name, dict_name=None):
    dict_name = dict_name or xml_name
    node = se(xml, xml_name)
    if node is not None:
        d[dict_name] = node.text


@object_handler('domain', 'urn:ietf:params:xml:ns:domain-1.0')
class Domain(EPPMapping):
    def _info_response(self, resData):
        dse = self._get_in_xmlns(self.ns_url)
        dses = self._get_all_xmlns(self.ns_url)
        i = dse(resData, 'infData')
        data = {
            'name': dse(i, 'name').text,
            'roid': dse(i, 'roid').text,
            'host': [n.text for n in dses(i, 'host')]
        }
        extract_optional(dse, i, data, 'registrant')
        extract_optional(dse, i, data, 'crDate')
        extract_optional(dse, i, data, 'exDate')
        return data

    def info(self, domain_name, domain_pw=''):
        render, d, se = self._cmd_node('info')
        se(d, 'name', attrib={'hosts': 'all'}).text = domain_name
        ai = se(d, 'authInfo')
        se(ai, 'pw').text = domain_pw
        return self._mk_request(render(), self._info_response)
