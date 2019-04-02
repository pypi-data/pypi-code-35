from .clusterwide import ClusterWideResource
from .prefixable import Prefixable
from .persistable import Persistable


EMPTY = object()


class ClusterRoleBinding(ClusterWideResource, Prefixable, Persistable):
    api_version = 'rbac.authorization.k8s.io/v1'
    kind = 'ClusterRoleBinding'
    group = 'iam'
    stage = 'security'

    @property
    def subjects(self):
        return self._manifest.get('subjects', [])

    def addsubject(self, subject):
        """Adds a new subject to the ``ClusterRoleBinding``."""
        self.subjects.append(subject)

    def popsubject(self, namespace, name, default=EMPTY):
        """Pop a subject from the array and return it."""
        i = self.index(namespace, name)
        try:
            return self.subjects.pop(i)
        except IndexError:
            if default == EMPTY:
                raise
            return default

    def getsubject(self, namespace, name):
        """Get a subject from the binding by its namespace and
        name.
        """
        for sub in self.subjects:
            if not (sub.name == name and sub.namespace == namespace):
                continue
            break
        else:
            raise LookupError(f"No such subject in namespace {namespace}: {subject}")
        return sub

    def index(self, namespace, name):
        """Return the index of the given subject identified by namespace
        and name.
        """
        for i, sub in enumerate(self.subjects):
            if not (sub.name == name and sub.namespace == namespace):
                continue
            break
        else:
            raise IndexError(f"No such subject in namespace {namespace}: {subject}")
        return i
