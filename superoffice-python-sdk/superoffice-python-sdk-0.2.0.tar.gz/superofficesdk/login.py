import os
import ssl
import xml.etree.ElementTree as et

from base64 import b64encode, b64decode
from collections import OrderedDict
from datetime import datetime
from OpenSSL import crypto
from suds.client import Client

ns = {
    'saml2p': '{urn:oasis:names:tc:SAML:2.0:protocol}',
    'saml2': '{urn:oasis:names:tc:SAML:2.0:assertion}',
    'ds': '{http://www.w3.org/2000/09/xmldsig#}',
    'xs': '{http://www.w3.org/2001/XMLSchema}',
    'ec': '{http://www.w3.org/2001/10/xml-exc-c14n#}',
    'xsi': '{http://www.w3.org/2001/XMLSchema-instance}'
}

login_endpoint = 'login/Services/PartnerSystemUserService.svc'
wsdl_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'partner.wsdl')


def SuperOfficeLogin(cust_id, app_token, sys_token,
                     private_key, environment='online'):
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

    time_utc = datetime.utcnow()
    time_formatted = datetime.strftime(time_utc, "%Y%m%d%H%M")
    system_token = sys_token + '.' + time_formatted

    key = crypto.load_privatekey(crypto.FILETYPE_PEM, private_key)
    signature = crypto.sign(key, system_token, 'sha256')
    signed_system_token = system_token + "." + b64encode(signature).decode('UTF-8')

    headers = OrderedDict([
        ('ApplicationToken', app_token),
        ('ContextIdentifier', cust_id)
    ])

    client = Client('file:%s' % wsdl_path)
    client.set_options(soapheaders=headers)
    client.set_options(location='https://{env}.superoffice.com/{endpoint}'.format(
        env=environment, endpoint=login_endpoint))
    token_type = client.factory.create('TokenType')['Saml']

    response = client.service.Authenticate(signed_system_token, token_type)
    saml_token = response.Token
    xml = b64decode(saml_token)

    tree = et.ElementTree(et.fromstring(xml))
    root = tree.getroot()
    for attribute in root.iter('{saml2}Attribute'.format(**ns)):
        attribute_value = attribute.find('{saml2}AttributeValue'.format(**ns)).text
        s = ''.join(attribute.attrib.values())
        if 'http://schemes.superoffice.net/identity/ticket' == s:
            ticket = attribute_value
            break

    return ticket
