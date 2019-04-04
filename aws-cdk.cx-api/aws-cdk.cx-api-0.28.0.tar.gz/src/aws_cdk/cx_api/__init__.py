import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/cx-api", "0.28.0", __name__, "cx-api@0.28.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/cx-api.AppRuntime")
class AppRuntime(jsii.compat.TypedDict):
    libraries: typing.Mapping[str,str]

class _Artifact(jsii.compat.TypedDict, total=False):
    autoDeploy: bool
    dependencies: typing.List[str]
    metadata: typing.Mapping[str,typing.Any]
    missing: typing.Mapping[str,typing.Any]
    properties: typing.Mapping[str,typing.Any]

@jsii.data_type(jsii_type="@aws-cdk/cx-api.Artifact")
class Artifact(_Artifact):
    environment: str
    type: "ArtifactType"

@jsii.enum(jsii_type="@aws-cdk/cx-api.ArtifactType")
class ArtifactType(enum.Enum):
    AwsCloudFormationStack = "AwsCloudFormationStack"
    AwsEcrDockerImage = "AwsEcrDockerImage"
    AwsS3Object = "AwsS3Object"

class _AssemblyManifest(jsii.compat.TypedDict, total=False):
    artifacts: typing.Mapping[str,"Artifact"]
    runtime: "AppRuntime"

@jsii.data_type(jsii_type="@aws-cdk/cx-api.AssemblyManifest")
class AssemblyManifest(_AssemblyManifest):
    version: str

@jsii.data_type(jsii_type="@aws-cdk/cx-api.AvailabilityZonesContextQuery")
class AvailabilityZonesContextQuery(jsii.compat.TypedDict, total=False):
    account: str
    region: str

@jsii.data_type(jsii_type="@aws-cdk/cx-api.BuildManifest")
class BuildManifest(jsii.compat.TypedDict):
    steps: typing.Mapping[str,"BuildStep"]

class _BuildStep(jsii.compat.TypedDict, total=False):
    depends: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/cx-api.BuildStep")
class BuildStep(_BuildStep):
    parameters: typing.Mapping[str,typing.Any]
    type: str

@jsii.enum(jsii_type="@aws-cdk/cx-api.BuildStepType")
class BuildStepType(enum.Enum):
    CopyFile = "CopyFile"
    ZipDirectory = "ZipDirectory"

class _ContainerImageAssetMetadataEntry(jsii.compat.TypedDict, total=False):
    repositoryName: str

@jsii.data_type(jsii_type="@aws-cdk/cx-api.ContainerImageAssetMetadataEntry")
class ContainerImageAssetMetadataEntry(_ContainerImageAssetMetadataEntry):
    id: str
    imageNameParameter: str
    packaging: str
    path: str

@jsii.data_type(jsii_type="@aws-cdk/cx-api.Environment")
class Environment(jsii.compat.TypedDict):
    account: str
    name: str
    region: str

@jsii.data_type(jsii_type="@aws-cdk/cx-api.FileAssetMetadataEntry")
class FileAssetMetadataEntry(jsii.compat.TypedDict):
    id: str
    packaging: str
    path: str
    s3BucketParameter: str
    s3KeyParameter: str

class _HostedZoneContextQuery(jsii.compat.TypedDict, total=False):
    account: str
    privateZone: bool
    region: str
    vpcId: str

@jsii.data_type(jsii_type="@aws-cdk/cx-api.HostedZoneContextQuery")
class HostedZoneContextQuery(_HostedZoneContextQuery):
    domainName: str

class _MetadataEntry(jsii.compat.TypedDict, total=False):
    data: typing.Any

@jsii.data_type(jsii_type="@aws-cdk/cx-api.MetadataEntry")
class MetadataEntry(_MetadataEntry):
    trace: typing.List[str]
    type: str

@jsii.data_type(jsii_type="@aws-cdk/cx-api.MissingContext")
class MissingContext(jsii.compat.TypedDict):
    props: typing.Mapping[str,typing.Any]
    provider: str

@jsii.data_type(jsii_type="@aws-cdk/cx-api.SSMParameterContextQuery")
class SSMParameterContextQuery(jsii.compat.TypedDict, total=False):
    account: str
    parameterName: str
    region: str

@jsii.data_type(jsii_type="@aws-cdk/cx-api.SynthesizeResponse")
class SynthesizeResponse(AssemblyManifest, jsii.compat.TypedDict):
    stacks: typing.List["SynthesizedStack"]

class _SynthesizedStack(jsii.compat.TypedDict, total=False):
    autoDeploy: bool
    dependsOn: typing.List[str]
    missing: typing.Mapping[str,"MissingContext"]

@jsii.data_type(jsii_type="@aws-cdk/cx-api.SynthesizedStack")
class SynthesizedStack(_SynthesizedStack):
    environment: "Environment"
    metadata: typing.Mapping[str,typing.List["MetadataEntry"]]
    name: str
    template: typing.Any

class _VpcContextQuery(jsii.compat.TypedDict, total=False):
    account: str
    region: str

@jsii.data_type(jsii_type="@aws-cdk/cx-api.VpcContextQuery")
class VpcContextQuery(_VpcContextQuery):
    filter: typing.Mapping[str,str]

class _VpcContextResponse(jsii.compat.TypedDict, total=False):
    isolatedSubnetIds: typing.List[str]
    isolatedSubnetNames: typing.List[str]
    privateSubnetIds: typing.List[str]
    privateSubnetNames: typing.List[str]
    publicSubnetIds: typing.List[str]
    publicSubnetNames: typing.List[str]
    vpnGatewayId: str

@jsii.data_type(jsii_type="@aws-cdk/cx-api.VpcContextResponse")
class VpcContextResponse(_VpcContextResponse):
    availabilityZones: typing.List[str]
    vpcId: str

__all__ = ["AppRuntime", "Artifact", "ArtifactType", "AssemblyManifest", "AvailabilityZonesContextQuery", "BuildManifest", "BuildStep", "BuildStepType", "ContainerImageAssetMetadataEntry", "Environment", "FileAssetMetadataEntry", "HostedZoneContextQuery", "MetadataEntry", "MissingContext", "SSMParameterContextQuery", "SynthesizeResponse", "SynthesizedStack", "VpcContextQuery", "VpcContextResponse", "__jsii_assembly__"]

publication.publish()
