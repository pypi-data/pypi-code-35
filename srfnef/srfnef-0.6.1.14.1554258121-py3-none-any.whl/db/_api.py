# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: _api.py
@date: 3/7/2019
@desc:
'''

from datetime import datetime
from getpass import getuser
from platform import python_version, node

from srfnef.typing import make_dataclass
from srfnef.version import full_version

APIIdentity = make_dataclass('APIIdentity', [('datetime', 'str'),
                                             ('author', 'str'),
                                             ('environment', 'str'),
                                             ('package_version', 'str')])
api_id = APIIdentity(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), getuser(),
                     node() + ': Python ' + python_version(), 'srfnef==' + full_version)


def parse_api_to_class(dct: dict, cls_name = 'API'):
    assert isinstance(dct, dict)
    fields = []
    for key, val in dct.items():
        if isinstance(val, dict):
            obj = parse_api_to_class(val, 'API' + key.capitalize())
            val = (obj.__class__.__name__, obj)
        if isinstance(val, tuple):
            fields.append((key,) + val)
        else:
            fields.append((key, val.__class__.__name__, val))
    try:
        return make_dataclass(cls_name, fields)
    except:
        print(cls_name, fields)


def parse_api(dct: dict, cls_name = 'API'):
    """
    dct = {
        "identity": {
            "datetime": "",
            "author": "",
            "environment": "",
            "package_version": ""
        },
        "config": {
            "scanner": {
                "type": "PetCylindricalScanner",
                "inner_radius": 424.5,
                "outer_radius": 444.5,
                "nb_rings": 4,
                "nb_blocks_per_ring": 48,
                "gap": 0.0
            }
        }
    }
    api = parse_api(dct)
        = API(identity=APIIdentity(datetime='', author='', environment='', package_version=''),
        config=APIConfig(scanner=APIScanner(type='PetCylindricalScanner', inner_radius=424.5,
        outer_radius=444.5, nb_rings=4, nb_blocks_per_ring=48, gap=0.0)))
   """
    assert isinstance(dct, dict)
    cls = parse_api_to_class(dct, cls_name)
    for key, val in dct.items():
        if isinstance(val, dict):
            if key == 'identity':
                dct['identity'] = api_id
            else:
                dct[key] = parse_api(val, cls_name = 'API' + key.capitalize())
    return cls(**dct)
