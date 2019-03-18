import copy
import json
from typing import Any, Dict, List, Optional

import attr
from cattr import structure_attrs_fromdict

attrs = attr.s
attrib = attr.ib


class _DataMixin:
    def to_dict(self, **kwargs) -> Dict:
        return attr.asdict(self, **kwargs)

    def to_json(self, **kwargs) -> str:
        return json.dumps(self.to_dict(), **kwargs)


@attrs(slots=True, frozen=True, auto_attribs=True)
class _Status:
    state: str
    innerState: str
    stateStartTime: str


@attrs(slots=True, frozen=True, auto_attribs=True)
class _Meta:
    _at_type: str
    clusterName: str
    clusterUuid: str
    operationType: str
    description: str
    status: _Status


@attrs(slots=True, frozen=True, auto_attribs=True)
class Operation:
    """[Reference](https://cloud.google.com/dataproc/docs/reference/rest/Shared.Types/ListOperationsResponse#Operation)"""

    name: str
    metadata: _Meta
    done: Optional[bool] = None
    result: Any = None

    @classmethod
    def from_dataproc_api(cls, incoming: Dict):
        cloned: Dict = copy.deepcopy(incoming)
        cloned["metadata"]["at_type"] = cloned["metadata"].pop("@type")

        return structure_attrs_fromdict(cloned, cls)


@attrs(slots=True, auto_attribs=True)
class _DiskConfig:
    bootDiskSizeGb: int = 1000
    bootDiskType: str = "pd-standard"
    numLocalSsds: int = 0


@attrs(slots=True, auto_attribs=True)
class _MachineConfig:
    numInstances: int = 1
    machineTypeUri: str = "n1-standard-4"
    diskConfig: _DiskConfig = attrib(factory=_DiskConfig)
    instanceNames: List[str] = attrib(factory=list)
    imageUri: str = ""


@attrs(slots=True, auto_attribs=True)
class _GceCusterConfig:
    zoneUri: str = ""
    subnetworkUri: str = "default"
    # serviceAccountScopes: List[str]  # TODO


@attrs(slots=True, auto_attribs=True)
class _InitAction:
    executableFile: str = ""


@attrs(slots=True, auto_attribs=True)
class _SoftwareConfig:
    imageVersion: str = ""
    properties: Dict = attrib(factory=dict)


@attrs(slots=True, auto_attribs=True)
class _Cluster:
    configBucket: str = ""
    gceClusterConfig: _GceCusterConfig = attrib(factory=_GceCusterConfig)
    masterConfig: _MachineConfig = attrib(factory=_MachineConfig)
    workerConfig: _MachineConfig = attrib(factory=_MachineConfig)
    initializationActions: List[_InitAction] = attrib(factory=list)
    # softwareConfig: _SoftwareConfig


@attrs(slots=True, auto_attribs=True)
class DataprocSpec(_DataMixin):
    """[Reference](https://cloud.google.com/dataproc/docs/reference/rest/v1beta2/projects.regions.clusters#Cluster)"""

    projectId: str
    clusterName: str

    config: _Cluster = attrib(factory=_Cluster)


@attrs(slots=True, auto_attribs=True)
class _PysparkJob(_DataMixin):
    mainPythonFileUri: str = ""
    args: List[str] = attrib(factory=list)
    pythonFileUris: List[str] = attrib(factory=list)
    jarFileUris: List[str] = attrib(factory=list)
    fileUris: List[str] = attrib(factory=list)
    archiveUris: List[str] = attrib(factory=list)
    properties: Dict[str, str] = attrib(factory=dict)
    # loggingConfig: Any


@attrs(slots=True, auto_attribs=True)
class _JobPlace:
    clusterName: str = ""
    clusterUuid: str = ""


@attrs(slots=True, auto_attribs=True)
class _JobRef:
    projectId: str = ""
    jobId: str = ""


@attrs(slots=True, auto_attribs=True)
class _Job:
    pysparkJob: _PysparkJob = attrib(factory=_PysparkJob)
    placement: _JobPlace = attrib(factory=_JobPlace)
    reference: _JobRef = attrib(factory=_JobRef)


@attrs(slots=True, auto_attribs=True)
class JobSpec:
    """[Reference](https://cloud.google.com/dataproc/docs/reference/rest/v1/projects.regions.jobs#Job)"""

    job: _Job = attrib(factory=_Job)
    requestId: str = ""
