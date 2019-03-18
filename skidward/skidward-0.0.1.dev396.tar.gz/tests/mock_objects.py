import pkg_resources as pkg
from typing import Dict, List

from skidward.worker_detector import NamespaceModuleManager


class MockEntryPoint(pkg.EntryPoint):
    def __init__(self, name, module_name):
        self.name = name
        self.module_name = module_name
        self.attrs = []
        self.extras = []
        self.dist = []

    def load(self, *args, **kwargs) -> pkg.EntryPoint:
        return MockEntryPoint(self.name, self.module_name)

    def start(self, context):
        return True


class MockNamespaceModuleManager(NamespaceModuleManager):
    def __init__(self, namespace):
        super().__init__(namespace)

    def _get_module_entry_points_on_namespace(self) -> Dict[str, pkg.EntryPoint]:
        if self.namespace == "skidward.real.name.space":
            return {
                "real_name": MockEntryPoint("real-name", "real_name"),
                "other_name": MockEntryPoint("other-name", "other_name"),
            }

        return super()._get_module_entry_points_on_namespace()


def mock_create_namespace_module_manager(namespace: str) -> MockNamespaceModuleManager:
    return MockNamespaceModuleManager(namespace)


def mock_get_all_workers_on_namespace(namespace: str = None) -> List[str]:
    namespace = "skidward.real.name.space"
    nmm = mock_create_namespace_module_manager(namespace)
    return nmm.get_all_available_module_names()
