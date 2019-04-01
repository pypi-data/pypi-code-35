from .base import Resource
from .batch import ResourceBatch
from .certificate import Certificate
from .crd import CustomResourceDefinition
from .clusterissuer import ClusterIssuer
from .clusterrole import ClusterRole
from .clusterrolebinding import ClusterRoleBinding
from .deployment import Deployment
from .namespace import Namespace
from .networkpolicy import NetworkPolicy
from .persistable import Persistable
from .prefixable import Prefixable
from .serviceaccount import ServiceAccount
from .service import LoadBalancer
from .service import NodePort
from .service import Service


class ConfigMap(Resource, Persistable, Prefixable):
    kind = 'ConfigMap'
    api_version = 'v1'
    group = 'config'
    stage = 'cluster'


class Role(Resource, Persistable, Prefixable):
    kind = 'Role'
    api_version = 'rbac.authorization.k8s.io/v1'
    group = 'iam'
    stage = 'cluster'

    @property
    def rules(self):
        return self._manifest.rules


class RoleBinding(Resource, Persistable, Prefixable):
    api_version = 'rbac.authorization.k8s.io/v1'
    kind = 'RoleBinding'
    group = 'rbac'
    stage = 'security'

    @property
    def subjects(self):
        return self._manifest.get('subjects', [])

    def getsubject(self, namespace, name):
        """Get a subject from the binding by its namespace and
        name.
        """
        if not self.isunbound():
            namespace = f'{self.prefix}{namespace}'
        for sub in self.subjects:
            if not (sub.name == name and sub.namespace == namespace):
                continue
            break
        else:
            raise LookupError(f"No such subject in namespace {namespace}: {subject}")
        return sub

    def on_bound(self):
        """Ensure that all subjects mentioned in the :class:`RoleBinding`
        have their namespaces prefixed.
        """
        for sub in self.subjects:
            if self.prefix in sub.namespace:
                continue
            sub.namespace = f'{self.prefix}{sub.namespace}'


resource_types = {
    'Certificate'   : Certificate,
    'ClusterIssuer' : ClusterIssuer,
    'ClusterRole'   : ClusterRole,
    'ClusterRoleBinding': ClusterRoleBinding,
    'ConfigMap': ConfigMap,
    'CustomResourceDefinition'  : CustomResourceDefinition,
    'Deployment'    : Deployment,
    'LoadBalancer'  : LoadBalancer,
    'Namespace'     : Namespace,
    'NetworkPolicy' : NetworkPolicy,
    'NodePort'      : NodePort,
    'Role'          : Role,
    'RoleBinding'   : RoleBinding,
    'ServiceAccount': ServiceAccount
}


get_resource = resource_types.get
