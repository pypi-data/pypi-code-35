# coding=utf-8
from __future__ import print_function

import itertools

from suanpan import g, interfaces
from suanpan.components import Component
from suanpan.dw import dw
from suanpan.log import logger
from suanpan.mstorage import mstorage
from suanpan.storage import storage


class DockerComponent(
    Component, interfaces.HasBaseServices, interfaces.HasLogger, interfaces.HasDevMode
):
    ENABLED_BASE_SERVICES = {"dw", "storage", "mstorage"}

    def initBase(self, args):
        logger.setLogger(self.name)
        self.setBaseServices(args)
