#!/usr/bin/env python3

import time
import os
import sys
import requests
import json
import pytest
from mock import (patch, PropertyMock, MagicMock)
from pyfbx import Fbx
from pyfbx.client import (FbxErrorResponse, FbxTransport)
from pyfbx.mdns import FbxMDNS


def test_fbx_register():
    f = Fbx("http://192.168.1.254/api/v6")
    with patch('pyfbx.client.FbxTransport.api_exec',
               side_effect=iter([
                   {"track_id": "id", "app_token": "tok"},
                   {"status": "pending"},
                   {"status": "granted"}])):
        f.register(app_id="id", app_name="name", device="device")


@pytest.mark.local_fb
def test_fbx_session_local():
    tokname = os.path.join(os.path.dirname(__file__), 'token.txt')

    with open(tokname) as tokfile:
        token = tokfile.readline().rstrip()
        app_id = tokfile.readline().rstrip()
    print(f"token:{token}, app_id:{app_id}")
    f = Fbx()
    f.mksession(app_id=app_id, token=token)
    r = f.Contacts.Create_a_contact(post_data={"display_name": "Sandy Kilo",
                                               "first_name": "Sandy",
                                               "last_name": "Kilo"})
    f.Contacts.Delete_a_contact(id=r['id'])
    with pytest.raises(FbxErrorResponse):
        try:
            f.Contacts.Access_a_given_contact_entry(1)
        except FbxErrorResponse as e:
            print(e)
            raise
    with patch('requests.Response', PropertyMock) as mock_resp:
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json = MagicMock()
        f.Contacts.Get_a_list_of_contacts()
    f.mksession()


def test_mdns():
    prop = {
        'https_available': '0',
        'api_base_url': '/api',
        'api_version': '6.6',
        'api_domain': 'example.com'}

    m = FbxMDNS()
    m.search(svc_name="_foobar._tcp.local.")
    with patch('pyfbx.mdns.FbxMDNS.svc_prop', new_callable=PropertyMock) as mock_prop:
        mock_prop.return_value = prop
        m.search(svc_name="_foobar._tcp.local.")
        m.search()
