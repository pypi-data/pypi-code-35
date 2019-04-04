import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-datapipeline", "0.28.0", __name__, "aws-datapipeline@0.28.0.jsii.tgz")
class CfnPipeline(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, parameter_objects: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["ParameterObjectProperty", aws_cdk.cdk.Token]]], activate: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, description: typing.Optional[str]=None, parameter_values: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ParameterValueProperty"]]]]=None, pipeline_objects: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "PipelineObjectProperty"]]]]=None, pipeline_tags: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "PipelineTagProperty"]]]]=None) -> None:
        props: CfnPipelineProps = {"name": name, "parameterObjects": parameter_objects}

        if activate is not None:
            props["activate"] = activate

        if description is not None:
            props["description"] = description

        if parameter_values is not None:
            props["parameterValues"] = parameter_values

        if pipeline_objects is not None:
            props["pipelineObjects"] = pipeline_objects

        if pipeline_tags is not None:
            props["pipelineTags"] = pipeline_tags

        jsii.create(CfnPipeline, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="pipelineId")
    def pipeline_id(self) -> str:
        return jsii.get(self, "pipelineId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPipelineProps":
        return jsii.get(self, "propertyOverrides")

    class _FieldProperty(jsii.compat.TypedDict, total=False):
        refValue: str
        stringValue: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.FieldProperty")
    class FieldProperty(_FieldProperty):
        key: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.ParameterAttributeProperty")
    class ParameterAttributeProperty(jsii.compat.TypedDict):
        key: str
        stringValue: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.ParameterObjectProperty")
    class ParameterObjectProperty(jsii.compat.TypedDict):
        attributes: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.ParameterAttributeProperty"]]]
        id: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.ParameterValueProperty")
    class ParameterValueProperty(jsii.compat.TypedDict):
        id: str
        stringValue: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.PipelineObjectProperty")
    class PipelineObjectProperty(jsii.compat.TypedDict):
        fields: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.FieldProperty"]]]
        id: str
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.PipelineTagProperty")
    class PipelineTagProperty(jsii.compat.TypedDict):
        key: str
        value: str


class _CfnPipelineProps(jsii.compat.TypedDict, total=False):
    activate: typing.Union[bool, aws_cdk.cdk.Token]
    description: str
    parameterValues: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.ParameterValueProperty"]]]
    pipelineObjects: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.PipelineObjectProperty"]]]
    pipelineTags: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.PipelineTagProperty"]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-datapipeline.CfnPipelineProps")
class CfnPipelineProps(_CfnPipelineProps):
    name: str
    parameterObjects: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnPipeline.ParameterObjectProperty", aws_cdk.cdk.Token]]]

__all__ = ["CfnPipeline", "CfnPipelineProps", "__jsii_assembly__"]

publication.publish()
