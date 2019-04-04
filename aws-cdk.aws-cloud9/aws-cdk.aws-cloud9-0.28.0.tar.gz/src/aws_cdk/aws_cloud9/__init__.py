import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-cloud9", "0.28.0", __name__, "aws-cloud9@0.28.0.jsii.tgz")
class CfnEnvironmentEC2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloud9.CfnEnvironmentEC2"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, instance_type: str, automatic_stop_time_minutes: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, description: typing.Optional[str]=None, name: typing.Optional[str]=None, owner_arn: typing.Optional[str]=None, repositories: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "RepositoryProperty"]]]]=None, subnet_id: typing.Optional[str]=None) -> None:
        props: CfnEnvironmentEC2Props = {"instanceType": instance_type}

        if automatic_stop_time_minutes is not None:
            props["automaticStopTimeMinutes"] = automatic_stop_time_minutes

        if description is not None:
            props["description"] = description

        if name is not None:
            props["name"] = name

        if owner_arn is not None:
            props["ownerArn"] = owner_arn

        if repositories is not None:
            props["repositories"] = repositories

        if subnet_id is not None:
            props["subnetId"] = subnet_id

        jsii.create(CfnEnvironmentEC2, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="environmentEc2Arn")
    def environment_ec2_arn(self) -> str:
        return jsii.get(self, "environmentEc2Arn")

    @property
    @jsii.member(jsii_name="environmentEc2Id")
    def environment_ec2_id(self) -> str:
        return jsii.get(self, "environmentEc2Id")

    @property
    @jsii.member(jsii_name="environmentEc2Name")
    def environment_ec2_name(self) -> str:
        return jsii.get(self, "environmentEc2Name")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEnvironmentEC2Props":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloud9.CfnEnvironmentEC2.RepositoryProperty")
    class RepositoryProperty(jsii.compat.TypedDict):
        pathComponent: str
        repositoryUrl: str


class _CfnEnvironmentEC2Props(jsii.compat.TypedDict, total=False):
    automaticStopTimeMinutes: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    description: str
    name: str
    ownerArn: str
    repositories: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnEnvironmentEC2.RepositoryProperty"]]]
    subnetId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-cloud9.CfnEnvironmentEC2Props")
class CfnEnvironmentEC2Props(_CfnEnvironmentEC2Props):
    instanceType: str

__all__ = ["CfnEnvironmentEC2", "CfnEnvironmentEC2Props", "__jsii_assembly__"]

publication.publish()
