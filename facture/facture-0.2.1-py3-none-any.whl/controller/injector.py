# -*- coding: utf-8 -*-

from functools import partial
from enum import Enum

from facture.utils import request_ip


class Injector(Enum):
    remote_addr = partial(request_ip)
    request = 'request'
