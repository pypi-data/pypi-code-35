import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-sagemaker", "0.28.0", __name__, "aws-sagemaker@0.28.0.jsii.tgz")
class CfnEndpoint(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sagemaker.CfnEndpoint"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, endpoint_config_name: str, endpoint_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnEndpointProps = {"endpointConfigName": endpoint_config_name}

        if endpoint_name is not None:
            props["endpointName"] = endpoint_name

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnEndpoint, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="endpointArn")
    def endpoint_arn(self) -> str:
        return jsii.get(self, "endpointArn")

    @property
    @jsii.member(jsii_name="endpointName")
    def endpoint_name(self) -> str:
        return jsii.get(self, "endpointName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEndpointProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class CfnEndpointConfig(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sagemaker.CfnEndpointConfig"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, production_variants: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["ProductionVariantProperty", aws_cdk.cdk.Token]]], endpoint_config_name: typing.Optional[str]=None, kms_key_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnEndpointConfigProps = {"productionVariants": production_variants}

        if endpoint_config_name is not None:
            props["endpointConfigName"] = endpoint_config_name

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnEndpointConfig, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="endpointConfigArn")
    def endpoint_config_arn(self) -> str:
        return jsii.get(self, "endpointConfigArn")

    @property
    @jsii.member(jsii_name="endpointConfigName")
    def endpoint_config_name(self) -> str:
        return jsii.get(self, "endpointConfigName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEndpointConfigProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    class _ProductionVariantProperty(jsii.compat.TypedDict, total=False):
        acceleratorType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnEndpointConfig.ProductionVariantProperty")
    class ProductionVariantProperty(_ProductionVariantProperty):
        initialInstanceCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        initialVariantWeight: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        instanceType: str
        modelName: str
        variantName: str


class _CfnEndpointConfigProps(jsii.compat.TypedDict, total=False):
    endpointConfigName: str
    kmsKeyId: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnEndpointConfigProps")
class CfnEndpointConfigProps(_CfnEndpointConfigProps):
    productionVariants: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnEndpointConfig.ProductionVariantProperty", aws_cdk.cdk.Token]]]

class _CfnEndpointProps(jsii.compat.TypedDict, total=False):
    endpointName: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnEndpointProps")
class CfnEndpointProps(_CfnEndpointProps):
    endpointConfigName: str

class CfnModel(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sagemaker.CfnModel"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, execution_role_arn: str, containers: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ContainerDefinitionProperty"]]]]=None, model_name: typing.Optional[str]=None, primary_container: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ContainerDefinitionProperty"]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpc_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "VpcConfigProperty"]]=None) -> None:
        props: CfnModelProps = {"executionRoleArn": execution_role_arn}

        if containers is not None:
            props["containers"] = containers

        if model_name is not None:
            props["modelName"] = model_name

        if primary_container is not None:
            props["primaryContainer"] = primary_container

        if tags is not None:
            props["tags"] = tags

        if vpc_config is not None:
            props["vpcConfig"] = vpc_config

        jsii.create(CfnModel, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="modelArn")
    def model_arn(self) -> str:
        return jsii.get(self, "modelArn")

    @property
    @jsii.member(jsii_name="modelName")
    def model_name(self) -> str:
        return jsii.get(self, "modelName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnModelProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    class _ContainerDefinitionProperty(jsii.compat.TypedDict, total=False):
        containerHostname: str
        environment: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        modelDataUrl: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnModel.ContainerDefinitionProperty")
    class ContainerDefinitionProperty(_ContainerDefinitionProperty):
        image: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnModel.VpcConfigProperty")
    class VpcConfigProperty(jsii.compat.TypedDict):
        securityGroupIds: typing.List[str]
        subnets: typing.List[str]


class _CfnModelProps(jsii.compat.TypedDict, total=False):
    containers: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnModel.ContainerDefinitionProperty"]]]
    modelName: str
    primaryContainer: typing.Union[aws_cdk.cdk.Token, "CfnModel.ContainerDefinitionProperty"]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    vpcConfig: typing.Union[aws_cdk.cdk.Token, "CfnModel.VpcConfigProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnModelProps")
class CfnModelProps(_CfnModelProps):
    executionRoleArn: str

class CfnNotebookInstance(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sagemaker.CfnNotebookInstance"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, instance_type: str, role_arn: str, direct_internet_access: typing.Optional[str]=None, kms_key_id: typing.Optional[str]=None, lifecycle_config_name: typing.Optional[str]=None, notebook_instance_name: typing.Optional[str]=None, root_access: typing.Optional[str]=None, security_group_ids: typing.Optional[typing.List[str]]=None, subnet_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, volume_size_in_gb: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnNotebookInstanceProps = {"instanceType": instance_type, "roleArn": role_arn}

        if direct_internet_access is not None:
            props["directInternetAccess"] = direct_internet_access

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if lifecycle_config_name is not None:
            props["lifecycleConfigName"] = lifecycle_config_name

        if notebook_instance_name is not None:
            props["notebookInstanceName"] = notebook_instance_name

        if root_access is not None:
            props["rootAccess"] = root_access

        if security_group_ids is not None:
            props["securityGroupIds"] = security_group_ids

        if subnet_id is not None:
            props["subnetId"] = subnet_id

        if tags is not None:
            props["tags"] = tags

        if volume_size_in_gb is not None:
            props["volumeSizeInGb"] = volume_size_in_gb

        jsii.create(CfnNotebookInstance, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="notebookInstanceArn")
    def notebook_instance_arn(self) -> str:
        return jsii.get(self, "notebookInstanceArn")

    @property
    @jsii.member(jsii_name="notebookInstanceName")
    def notebook_instance_name(self) -> str:
        return jsii.get(self, "notebookInstanceName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnNotebookInstanceProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class CfnNotebookInstanceLifecycleConfig(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sagemaker.CfnNotebookInstanceLifecycleConfig"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, notebook_instance_lifecycle_config_name: typing.Optional[str]=None, on_create: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "NotebookInstanceLifecycleHookProperty"]]]]=None, on_start: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "NotebookInstanceLifecycleHookProperty"]]]]=None) -> None:
        props: CfnNotebookInstanceLifecycleConfigProps = {}

        if notebook_instance_lifecycle_config_name is not None:
            props["notebookInstanceLifecycleConfigName"] = notebook_instance_lifecycle_config_name

        if on_create is not None:
            props["onCreate"] = on_create

        if on_start is not None:
            props["onStart"] = on_start

        jsii.create(CfnNotebookInstanceLifecycleConfig, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="notebookInstanceLifecycleConfigArn")
    def notebook_instance_lifecycle_config_arn(self) -> str:
        return jsii.get(self, "notebookInstanceLifecycleConfigArn")

    @property
    @jsii.member(jsii_name="notebookInstanceLifecycleConfigName")
    def notebook_instance_lifecycle_config_name(self) -> str:
        return jsii.get(self, "notebookInstanceLifecycleConfigName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnNotebookInstanceLifecycleConfigProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnNotebookInstanceLifecycleConfig.NotebookInstanceLifecycleHookProperty")
    class NotebookInstanceLifecycleHookProperty(jsii.compat.TypedDict, total=False):
        content: str


@jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnNotebookInstanceLifecycleConfigProps")
class CfnNotebookInstanceLifecycleConfigProps(jsii.compat.TypedDict, total=False):
    notebookInstanceLifecycleConfigName: str
    onCreate: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnNotebookInstanceLifecycleConfig.NotebookInstanceLifecycleHookProperty"]]]
    onStart: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnNotebookInstanceLifecycleConfig.NotebookInstanceLifecycleHookProperty"]]]

class _CfnNotebookInstanceProps(jsii.compat.TypedDict, total=False):
    directInternetAccess: str
    kmsKeyId: str
    lifecycleConfigName: str
    notebookInstanceName: str
    rootAccess: str
    securityGroupIds: typing.List[str]
    subnetId: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    volumeSizeInGb: typing.Union[jsii.Number, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnNotebookInstanceProps")
class CfnNotebookInstanceProps(_CfnNotebookInstanceProps):
    instanceType: str
    roleArn: str

__all__ = ["CfnEndpoint", "CfnEndpointConfig", "CfnEndpointConfigProps", "CfnEndpointProps", "CfnModel", "CfnModelProps", "CfnNotebookInstance", "CfnNotebookInstanceLifecycleConfig", "CfnNotebookInstanceLifecycleConfigProps", "CfnNotebookInstanceProps", "__jsii_assembly__"]

publication.publish()
