import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-iotanalytics", "0.28.0", __name__, "aws-iotanalytics@0.28.0.jsii.tgz")
class CfnChannel(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iotanalytics.CfnChannel"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, channel_name: typing.Optional[str]=None, retention_period: typing.Optional[typing.Union["RetentionPeriodProperty", aws_cdk.cdk.Token]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnChannelProps = {}

        if channel_name is not None:
            props["channelName"] = channel_name

        if retention_period is not None:
            props["retentionPeriod"] = retention_period

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnChannel, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="channelId")
    def channel_id(self) -> str:
        return jsii.get(self, "channelId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnChannelProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnChannel.RetentionPeriodProperty")
    class RetentionPeriodProperty(jsii.compat.TypedDict, total=False):
        numberOfDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        unlimited: typing.Union[bool, aws_cdk.cdk.Token]


@jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnChannelProps")
class CfnChannelProps(jsii.compat.TypedDict, total=False):
    channelName: str
    retentionPeriod: typing.Union["CfnChannel.RetentionPeriodProperty", aws_cdk.cdk.Token]
    tags: typing.List[aws_cdk.cdk.CfnTag]

class CfnDataset(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ActionProperty"]]], dataset_name: typing.Optional[str]=None, retention_period: typing.Optional[typing.Union[aws_cdk.cdk.Token, "RetentionPeriodProperty"]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, triggers: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "TriggerProperty"]]]]=None) -> None:
        props: CfnDatasetProps = {"actions": actions}

        if dataset_name is not None:
            props["datasetName"] = dataset_name

        if retention_period is not None:
            props["retentionPeriod"] = retention_period

        if tags is not None:
            props["tags"] = tags

        if triggers is not None:
            props["triggers"] = triggers

        jsii.create(CfnDataset, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> str:
        return jsii.get(self, "datasetId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDatasetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    class _ActionProperty(jsii.compat.TypedDict, total=False):
        containerAction: typing.Union[aws_cdk.cdk.Token, "CfnDataset.ContainerActionProperty"]
        queryAction: typing.Union[aws_cdk.cdk.Token, "CfnDataset.QueryActionProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.ActionProperty")
    class ActionProperty(_ActionProperty):
        actionName: str

    class _ContainerActionProperty(jsii.compat.TypedDict, total=False):
        variables: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDataset.VariableProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.ContainerActionProperty")
    class ContainerActionProperty(_ContainerActionProperty):
        executionRoleArn: str
        image: str
        resourceConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDataset.ResourceConfigurationProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.DatasetContentVersionValueProperty")
    class DatasetContentVersionValueProperty(jsii.compat.TypedDict, total=False):
        datasetName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.DeltaTimeProperty")
    class DeltaTimeProperty(jsii.compat.TypedDict):
        offsetSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        timeExpression: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.FilterProperty")
    class FilterProperty(jsii.compat.TypedDict, total=False):
        deltaTime: typing.Union[aws_cdk.cdk.Token, "CfnDataset.DeltaTimeProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.OutputFileUriValueProperty")
    class OutputFileUriValueProperty(jsii.compat.TypedDict, total=False):
        fileName: str

    class _QueryActionProperty(jsii.compat.TypedDict, total=False):
        filters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDataset.FilterProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.QueryActionProperty")
    class QueryActionProperty(_QueryActionProperty):
        sqlQuery: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.ResourceConfigurationProperty")
    class ResourceConfigurationProperty(jsii.compat.TypedDict):
        computeType: str
        volumeSizeInGb: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.RetentionPeriodProperty")
    class RetentionPeriodProperty(jsii.compat.TypedDict):
        numberOfDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        unlimited: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.ScheduleProperty")
    class ScheduleProperty(jsii.compat.TypedDict):
        scheduleExpression: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.TriggerProperty")
    class TriggerProperty(jsii.compat.TypedDict, total=False):
        schedule: typing.Union[aws_cdk.cdk.Token, "CfnDataset.ScheduleProperty"]
        triggeringDataset: typing.Union[aws_cdk.cdk.Token, "CfnDataset.TriggeringDatasetProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.TriggeringDatasetProperty")
    class TriggeringDatasetProperty(jsii.compat.TypedDict):
        datasetName: str

    class _VariableProperty(jsii.compat.TypedDict, total=False):
        datasetContentVersionValue: typing.Union[aws_cdk.cdk.Token, "CfnDataset.DatasetContentVersionValueProperty"]
        doubleValue: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        outputFileUriValue: typing.Union[aws_cdk.cdk.Token, "CfnDataset.OutputFileUriValueProperty"]
        stringValue: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.VariableProperty")
    class VariableProperty(_VariableProperty):
        variableName: str


class _CfnDatasetProps(jsii.compat.TypedDict, total=False):
    datasetName: str
    retentionPeriod: typing.Union[aws_cdk.cdk.Token, "CfnDataset.RetentionPeriodProperty"]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    triggers: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDataset.TriggerProperty"]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDatasetProps")
class CfnDatasetProps(_CfnDatasetProps):
    actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDataset.ActionProperty"]]]

class CfnDatastore(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iotanalytics.CfnDatastore"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, datastore_name: typing.Optional[str]=None, retention_period: typing.Optional[typing.Union[aws_cdk.cdk.Token, "RetentionPeriodProperty"]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnDatastoreProps = {}

        if datastore_name is not None:
            props["datastoreName"] = datastore_name

        if retention_period is not None:
            props["retentionPeriod"] = retention_period

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDatastore, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="datastoreId")
    def datastore_id(self) -> str:
        return jsii.get(self, "datastoreId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDatastoreProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDatastore.RetentionPeriodProperty")
    class RetentionPeriodProperty(jsii.compat.TypedDict, total=False):
        numberOfDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        unlimited: typing.Union[bool, aws_cdk.cdk.Token]


@jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDatastoreProps")
class CfnDatastoreProps(jsii.compat.TypedDict, total=False):
    datastoreName: str
    retentionPeriod: typing.Union[aws_cdk.cdk.Token, "CfnDatastore.RetentionPeriodProperty"]
    tags: typing.List[aws_cdk.cdk.CfnTag]

class CfnPipeline(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, pipeline_activities: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ActivityProperty"]]], pipeline_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnPipelineProps = {"pipelineActivities": pipeline_activities}

        if pipeline_name is not None:
            props["pipelineName"] = pipeline_name

        if tags is not None:
            props["tags"] = tags

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

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.ActivityProperty")
    class ActivityProperty(jsii.compat.TypedDict, total=False):
        addAttributes: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.AddAttributesProperty"]
        channel: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.ChannelProperty"]
        datastore: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.DatastoreProperty"]
        deviceRegistryEnrich: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.DeviceRegistryEnrichProperty"]
        deviceShadowEnrich: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.DeviceShadowEnrichProperty"]
        filter: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.FilterProperty"]
        lambda_: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.LambdaProperty"]
        math: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.MathProperty"]
        removeAttributes: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.RemoveAttributesProperty"]
        selectAttributes: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.SelectAttributesProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.AddAttributesProperty")
    class AddAttributesProperty(jsii.compat.TypedDict, total=False):
        attributes: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        name: str
        next: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.ChannelProperty")
    class ChannelProperty(jsii.compat.TypedDict, total=False):
        channelName: str
        name: str
        next: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.DatastoreProperty")
    class DatastoreProperty(jsii.compat.TypedDict, total=False):
        datastoreName: str
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.DeviceRegistryEnrichProperty")
    class DeviceRegistryEnrichProperty(jsii.compat.TypedDict, total=False):
        attribute: str
        name: str
        next: str
        roleArn: str
        thingName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.DeviceShadowEnrichProperty")
    class DeviceShadowEnrichProperty(jsii.compat.TypedDict, total=False):
        attribute: str
        name: str
        next: str
        roleArn: str
        thingName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.FilterProperty")
    class FilterProperty(jsii.compat.TypedDict, total=False):
        filter: str
        name: str
        next: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.LambdaProperty")
    class LambdaProperty(jsii.compat.TypedDict, total=False):
        batchSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        lambdaName: str
        name: str
        next: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.MathProperty")
    class MathProperty(jsii.compat.TypedDict, total=False):
        attribute: str
        math: str
        name: str
        next: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.RemoveAttributesProperty")
    class RemoveAttributesProperty(jsii.compat.TypedDict, total=False):
        attributes: typing.List[str]
        name: str
        next: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.SelectAttributesProperty")
    class SelectAttributesProperty(jsii.compat.TypedDict, total=False):
        attributes: typing.List[str]
        name: str
        next: str


class _CfnPipelineProps(jsii.compat.TypedDict, total=False):
    pipelineName: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipelineProps")
class CfnPipelineProps(_CfnPipelineProps):
    pipelineActivities: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.ActivityProperty"]]]

__all__ = ["CfnChannel", "CfnChannelProps", "CfnDataset", "CfnDatasetProps", "CfnDatastore", "CfnDatastoreProps", "CfnPipeline", "CfnPipelineProps", "__jsii_assembly__"]

publication.publish()
