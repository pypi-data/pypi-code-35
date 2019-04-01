import os as _os

from ._bottle import cached_property_bottle
from ._cached_property import cached_property_cached_property
from ._distlib import cached_property_distlib
from ._distro import cached_property_distro
from ._django import cached_property_django
from ._pip import (
    cached_property_pip_internal,
    cached_property_pip_vendor_distlib,
    cached_property_pip_vendor_distro,
)
from ._werkzeug import cached_property_werkzeug

__version__ = '1.0'

ENV_NAME = 'CACHED_PROPERTY_TRY_ORDER'
_env = _os.getenv(ENV_NAME)
if _env:
    try:
        _try_order = [
            globals()["cached_property_%s" % name]
            for name in _env.split(',')
        ]
    except KeyError as e:
        raise ValueError(
            "Your environment variable '%s' contains '%s', which is not valid" % (
                ENV_NAME,
                e.args[0][len('cached_property_'):],
            ))
else:
    _try_order = [
        cached_property_bottle,
        cached_property_django,
        cached_property_werkzeug,
        cached_property_cached_property,
        cached_property_distlib,
        cached_property_distro,
        cached_property_pip_internal,
        cached_property_pip_vendor_distlib,
        cached_property_pip_vendor_distro,
    ]

try:
    cached_property = [cp for cp in _try_order if cp is not None][0]
except IndexError:
    raise ImportError("cached_property not importable from any package")
