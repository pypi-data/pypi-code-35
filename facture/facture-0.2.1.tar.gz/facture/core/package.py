# -*- coding: utf-8 -*-

import re
from logging import getLogger

from facture.utils import validated_identifier


class Jetpack:
    """Associates components and meta with a package, for registration with a Facture Application.

    :param name: Package name
    :param description: Package description
    :param controller: Controller class
    :param services: List of Service objects
    :param models: List of Model classes
    """

    _path = None

    def __init__(self, name, description, controller=None, services=None, models=None):
        self.controller = controller
        self.services = services or []
        self.models = models or []
        self.name = validated_identifier(name)
        self.description = description
        self.log = getLogger(f'pkg.{self.name}')

    @property
    def path(self):
        """Package path accessor"""

        return self._path

    @path.setter
    def path(self, value):
        if not re.match(r'^/[a-zA-Z0-9-]*$', value):
            raise Exception(f'Package {self.name} path must be a valid path, example: /my-package-1')

        self._path = value

    def __repr__(self):
        return f'<{self.__class__.__name__} [{self.name}] at {hex(id(self))}>'
