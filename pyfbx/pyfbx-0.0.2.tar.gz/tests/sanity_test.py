#!/usr/bin/env python3

import time
import sys
import requests
import pytest
from mock import patch, MagicMock

from pyfbx import Fbx


@pytest.mark.local_fb
def test_fbx_hardcoded_url():
    f = Fbx()
    assert isinstance(f, Fbx)
    with patch('pyfbx.mdns.FbxMDNS.search', return_value=None):
        f = Fbx()
    f = Fbx(url="http://12.34.56.78/api/v4")
    f = Fbx(url="12.34.56.78/api/v4")
    f = Fbx(url="http://192.168.1.254")


@pytest.mark.local_fb
def test_fbx_mdns():
    f = Fbx()
    f = Fbx(session=requests.Session())
