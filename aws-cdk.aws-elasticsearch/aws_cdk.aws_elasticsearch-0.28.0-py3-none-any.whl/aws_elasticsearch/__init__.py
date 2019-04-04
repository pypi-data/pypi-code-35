import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-elasticsearch", "0.28.0", __name__, "aws-elasticsearch@0.28.0.jsii.tgz")
class CfnDomain(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticsearch.CfnDomain"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, access_policies: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, advanced_options: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]]=None, domain_name: typing.Optional[str]=None, ebs_options: typing.Optional[typing.Union[aws_cdk.cdk.Token, "EBSOptionsProperty"]]=None, elasticsearch_cluster_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ElasticsearchClusterConfigProperty"]]=None, elasticsearch_version: typing.Optional[str]=None, encryption_at_rest_options: typing.Optional[typing.Union[aws_cdk.cdk.Token, "EncryptionAtRestOptionsProperty"]]=None, node_to_node_encryption_options: typing.Optional[typing.Union[aws_cdk.cdk.Token, "NodeToNodeEncryptionOptionsProperty"]]=None, snapshot_options: typing.Optional[typing.Union[aws_cdk.cdk.Token, "SnapshotOptionsProperty"]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpc_options: typing.Optional[typing.Union[aws_cdk.cdk.Token, "VPCOptionsProperty"]]=None) -> None:
        props: CfnDomainProps = {}

        if access_policies is not None:
            props["accessPolicies"] = access_policies

        if advanced_options is not None:
            props["advancedOptions"] = advanced_options

        if domain_name is not None:
            props["domainName"] = domain_name

        if ebs_options is not None:
            props["ebsOptions"] = ebs_options

        if elasticsearch_cluster_config is not None:
            props["elasticsearchClusterConfig"] = elasticsearch_cluster_config

        if elasticsearch_version is not None:
            props["elasticsearchVersion"] = elasticsearch_version

        if encryption_at_rest_options is not None:
            props["encryptionAtRestOptions"] = encryption_at_rest_options

        if node_to_node_encryption_options is not None:
            props["nodeToNodeEncryptionOptions"] = node_to_node_encryption_options

        if snapshot_options is not None:
            props["snapshotOptions"] = snapshot_options

        if tags is not None:
            props["tags"] = tags

        if vpc_options is not None:
            props["vpcOptions"] = vpc_options

        jsii.create(CfnDomain, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> str:
        return jsii.get(self, "domainArn")

    @property
    @jsii.member(jsii_name="domainEndpoint")
    def domain_endpoint(self) -> str:
        return jsii.get(self, "domainEndpoint")

    @property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        return jsii.get(self, "domainName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDomainProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticsearch.CfnDomain.EBSOptionsProperty")
    class EBSOptionsProperty(jsii.compat.TypedDict, total=False):
        ebsEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        volumeSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        volumeType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticsearch.CfnDomain.ElasticsearchClusterConfigProperty")
    class ElasticsearchClusterConfigProperty(jsii.compat.TypedDict, total=False):
        dedicatedMasterCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        dedicatedMasterEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        dedicatedMasterType: str
        instanceCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        instanceType: str
        zoneAwarenessEnabled: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticsearch.CfnDomain.EncryptionAtRestOptionsProperty")
    class EncryptionAtRestOptionsProperty(jsii.compat.TypedDict, total=False):
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        kmsKeyId: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticsearch.CfnDomain.NodeToNodeEncryptionOptionsProperty")
    class NodeToNodeEncryptionOptionsProperty(jsii.compat.TypedDict, total=False):
        enabled: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticsearch.CfnDomain.SnapshotOptionsProperty")
    class SnapshotOptionsProperty(jsii.compat.TypedDict, total=False):
        automatedSnapshotStartHour: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticsearch.CfnDomain.VPCOptionsProperty")
    class VPCOptionsProperty(jsii.compat.TypedDict, total=False):
        securityGroupIds: typing.List[str]
        subnetIds: typing.List[str]


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticsearch.CfnDomainProps")
class CfnDomainProps(jsii.compat.TypedDict, total=False):
    accessPolicies: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    advancedOptions: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
    domainName: str
    ebsOptions: typing.Union[aws_cdk.cdk.Token, "CfnDomain.EBSOptionsProperty"]
    elasticsearchClusterConfig: typing.Union[aws_cdk.cdk.Token, "CfnDomain.ElasticsearchClusterConfigProperty"]
    elasticsearchVersion: str
    encryptionAtRestOptions: typing.Union[aws_cdk.cdk.Token, "CfnDomain.EncryptionAtRestOptionsProperty"]
    nodeToNodeEncryptionOptions: typing.Union[aws_cdk.cdk.Token, "CfnDomain.NodeToNodeEncryptionOptionsProperty"]
    snapshotOptions: typing.Union[aws_cdk.cdk.Token, "CfnDomain.SnapshotOptionsProperty"]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    vpcOptions: typing.Union[aws_cdk.cdk.Token, "CfnDomain.VPCOptionsProperty"]

__all__ = ["CfnDomain", "CfnDomainProps", "__jsii_assembly__"]

publication.publish()
