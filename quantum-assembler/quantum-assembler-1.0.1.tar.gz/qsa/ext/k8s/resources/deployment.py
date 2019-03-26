from qsa.lib.datastructures import DTO
from .base import Resource
from .containerspec import ContainerSpec
from .prefixable import Prefixable
from .persistable import Persistable


class Deployment(Resource, Prefixable, Persistable, ContainerSpec):
    api_version = 'apps/v1'
    kind = 'Deployment'
    group = 'deployments'
    stage = 'applications'

    @property
    def containers(self):
        return self.template_spec.setdefault('containers', [])

    @property
    def template_spec(self):
        return self.template.setdefault('spec', DTO())

    @property
    def template(self):
        return self.spec.setdefault('template', DTO())

    @property
    def spec(self):
        return self._manifest.setdefault('spec', DTO())
