import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-kinesisanalytics", "0.28.0", __name__, "aws-kinesisanalytics@0.28.0.jsii.tgz")
class CfnApplication(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, inputs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["InputProperty", aws_cdk.cdk.Token]]], application_code: typing.Optional[str]=None, application_description: typing.Optional[str]=None, application_name: typing.Optional[str]=None) -> None:
        props: CfnApplicationProps = {"inputs": inputs}

        if application_code is not None:
            props["applicationCode"] = application_code

        if application_description is not None:
            props["applicationDescription"] = application_description

        if application_name is not None:
            props["applicationName"] = application_name

        jsii.create(CfnApplication, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> str:
        return jsii.get(self, "applicationId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.CSVMappingParametersProperty")
    class CSVMappingParametersProperty(jsii.compat.TypedDict):
        recordColumnDelimiter: str
        recordRowDelimiter: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.InputLambdaProcessorProperty")
    class InputLambdaProcessorProperty(jsii.compat.TypedDict):
        resourceArn: str
        roleArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.InputParallelismProperty")
    class InputParallelismProperty(jsii.compat.TypedDict, total=False):
        count: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.InputProcessingConfigurationProperty")
    class InputProcessingConfigurationProperty(jsii.compat.TypedDict, total=False):
        inputLambdaProcessor: typing.Union[aws_cdk.cdk.Token, "CfnApplication.InputLambdaProcessorProperty"]

    class _InputProperty(jsii.compat.TypedDict, total=False):
        inputParallelism: typing.Union[aws_cdk.cdk.Token, "CfnApplication.InputParallelismProperty"]
        inputProcessingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplication.InputProcessingConfigurationProperty"]
        kinesisFirehoseInput: typing.Union[aws_cdk.cdk.Token, "CfnApplication.KinesisFirehoseInputProperty"]
        kinesisStreamsInput: typing.Union[aws_cdk.cdk.Token, "CfnApplication.KinesisStreamsInputProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.InputProperty")
    class InputProperty(_InputProperty):
        inputSchema: typing.Union[aws_cdk.cdk.Token, "CfnApplication.InputSchemaProperty"]
        namePrefix: str

    class _InputSchemaProperty(jsii.compat.TypedDict, total=False):
        recordEncoding: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.InputSchemaProperty")
    class InputSchemaProperty(_InputSchemaProperty):
        recordColumns: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApplication.RecordColumnProperty"]]]
        recordFormat: typing.Union[aws_cdk.cdk.Token, "CfnApplication.RecordFormatProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.JSONMappingParametersProperty")
    class JSONMappingParametersProperty(jsii.compat.TypedDict):
        recordRowPath: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.KinesisFirehoseInputProperty")
    class KinesisFirehoseInputProperty(jsii.compat.TypedDict):
        resourceArn: str
        roleArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.KinesisStreamsInputProperty")
    class KinesisStreamsInputProperty(jsii.compat.TypedDict):
        resourceArn: str
        roleArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.MappingParametersProperty")
    class MappingParametersProperty(jsii.compat.TypedDict, total=False):
        csvMappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplication.CSVMappingParametersProperty"]
        jsonMappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplication.JSONMappingParametersProperty"]

    class _RecordColumnProperty(jsii.compat.TypedDict, total=False):
        mapping: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.RecordColumnProperty")
    class RecordColumnProperty(_RecordColumnProperty):
        name: str
        sqlType: str

    class _RecordFormatProperty(jsii.compat.TypedDict, total=False):
        mappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplication.MappingParametersProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.RecordFormatProperty")
    class RecordFormatProperty(_RecordFormatProperty):
        recordFormatType: str


class CfnApplicationCloudWatchLoggingOptionV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationCloudWatchLoggingOptionV2"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, cloud_watch_logging_option: typing.Union[aws_cdk.cdk.Token, "CloudWatchLoggingOptionProperty"]) -> None:
        props: CfnApplicationCloudWatchLoggingOptionV2Props = {"applicationName": application_name, "cloudWatchLoggingOption": cloud_watch_logging_option}

        jsii.create(CfnApplicationCloudWatchLoggingOptionV2, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationCloudWatchLoggingOptionV2Props":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty")
    class CloudWatchLoggingOptionProperty(jsii.compat.TypedDict):
        logStreamArn: str


@jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationCloudWatchLoggingOptionV2Props")
class CfnApplicationCloudWatchLoggingOptionV2Props(jsii.compat.TypedDict):
    applicationName: str
    cloudWatchLoggingOption: typing.Union[aws_cdk.cdk.Token, "CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty"]

class CfnApplicationOutput(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutput"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, output: typing.Union[aws_cdk.cdk.Token, "OutputProperty"]) -> None:
        props: CfnApplicationOutputProps = {"applicationName": application_name, "output": output}

        jsii.create(CfnApplicationOutput, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="applicationOutputId")
    def application_output_id(self) -> str:
        return jsii.get(self, "applicationOutputId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationOutputProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutput.DestinationSchemaProperty")
    class DestinationSchemaProperty(jsii.compat.TypedDict, total=False):
        recordFormatType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutput.KinesisFirehoseOutputProperty")
    class KinesisFirehoseOutputProperty(jsii.compat.TypedDict):
        resourceArn: str
        roleArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutput.KinesisStreamsOutputProperty")
    class KinesisStreamsOutputProperty(jsii.compat.TypedDict):
        resourceArn: str
        roleArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutput.LambdaOutputProperty")
    class LambdaOutputProperty(jsii.compat.TypedDict):
        resourceArn: str
        roleArn: str

    class _OutputProperty(jsii.compat.TypedDict, total=False):
        kinesisFirehoseOutput: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutput.KinesisFirehoseOutputProperty"]
        kinesisStreamsOutput: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutput.KinesisStreamsOutputProperty"]
        lambdaOutput: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutput.LambdaOutputProperty"]
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutput.OutputProperty")
    class OutputProperty(_OutputProperty):
        destinationSchema: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutput.DestinationSchemaProperty"]


@jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutputProps")
class CfnApplicationOutputProps(jsii.compat.TypedDict):
    applicationName: str
    output: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutput.OutputProperty"]

class CfnApplicationOutputV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutputV2"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, output: typing.Union[aws_cdk.cdk.Token, "OutputProperty"]) -> None:
        props: CfnApplicationOutputV2Props = {"applicationName": application_name, "output": output}

        jsii.create(CfnApplicationOutputV2, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationOutputV2Props":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutputV2.DestinationSchemaProperty")
    class DestinationSchemaProperty(jsii.compat.TypedDict, total=False):
        recordFormatType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutputV2.KinesisFirehoseOutputProperty")
    class KinesisFirehoseOutputProperty(jsii.compat.TypedDict):
        resourceArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutputV2.KinesisStreamsOutputProperty")
    class KinesisStreamsOutputProperty(jsii.compat.TypedDict):
        resourceArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutputV2.LambdaOutputProperty")
    class LambdaOutputProperty(jsii.compat.TypedDict):
        resourceArn: str

    class _OutputProperty(jsii.compat.TypedDict, total=False):
        kinesisFirehoseOutput: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutputV2.KinesisFirehoseOutputProperty"]
        kinesisStreamsOutput: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutputV2.KinesisStreamsOutputProperty"]
        lambdaOutput: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutputV2.LambdaOutputProperty"]
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutputV2.OutputProperty")
    class OutputProperty(_OutputProperty):
        destinationSchema: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutputV2.DestinationSchemaProperty"]


@jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutputV2Props")
class CfnApplicationOutputV2Props(jsii.compat.TypedDict):
    applicationName: str
    output: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutputV2.OutputProperty"]

class _CfnApplicationProps(jsii.compat.TypedDict, total=False):
    applicationCode: str
    applicationDescription: str
    applicationName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationProps")
class CfnApplicationProps(_CfnApplicationProps):
    inputs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnApplication.InputProperty", aws_cdk.cdk.Token]]]

class CfnApplicationReferenceDataSource(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, reference_data_source: typing.Union[aws_cdk.cdk.Token, "ReferenceDataSourceProperty"]) -> None:
        props: CfnApplicationReferenceDataSourceProps = {"applicationName": application_name, "referenceDataSource": reference_data_source}

        jsii.create(CfnApplicationReferenceDataSource, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="applicationReferenceDataSourceId")
    def application_reference_data_source_id(self) -> str:
        return jsii.get(self, "applicationReferenceDataSourceId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationReferenceDataSourceProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource.CSVMappingParametersProperty")
    class CSVMappingParametersProperty(jsii.compat.TypedDict):
        recordColumnDelimiter: str
        recordRowDelimiter: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource.JSONMappingParametersProperty")
    class JSONMappingParametersProperty(jsii.compat.TypedDict):
        recordRowPath: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource.MappingParametersProperty")
    class MappingParametersProperty(jsii.compat.TypedDict, total=False):
        csvMappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSource.CSVMappingParametersProperty"]
        jsonMappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSource.JSONMappingParametersProperty"]

    class _RecordColumnProperty(jsii.compat.TypedDict, total=False):
        mapping: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource.RecordColumnProperty")
    class RecordColumnProperty(_RecordColumnProperty):
        name: str
        sqlType: str

    class _RecordFormatProperty(jsii.compat.TypedDict, total=False):
        mappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSource.MappingParametersProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource.RecordFormatProperty")
    class RecordFormatProperty(_RecordFormatProperty):
        recordFormatType: str

    class _ReferenceDataSourceProperty(jsii.compat.TypedDict, total=False):
        s3ReferenceDataSource: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty"]
        tableName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource.ReferenceDataSourceProperty")
    class ReferenceDataSourceProperty(_ReferenceDataSourceProperty):
        referenceSchema: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSource.ReferenceSchemaProperty"]

    class _ReferenceSchemaProperty(jsii.compat.TypedDict, total=False):
        recordEncoding: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource.ReferenceSchemaProperty")
    class ReferenceSchemaProperty(_ReferenceSchemaProperty):
        recordColumns: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSource.RecordColumnProperty"]]]
        recordFormat: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSource.RecordFormatProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty")
    class S3ReferenceDataSourceProperty(jsii.compat.TypedDict):
        bucketArn: str
        fileKey: str
        referenceRoleArn: str


@jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceProps")
class CfnApplicationReferenceDataSourceProps(jsii.compat.TypedDict):
    applicationName: str
    referenceDataSource: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSource.ReferenceDataSourceProperty"]

class CfnApplicationReferenceDataSourceV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, reference_data_source: typing.Union[aws_cdk.cdk.Token, "ReferenceDataSourceProperty"]) -> None:
        props: CfnApplicationReferenceDataSourceV2Props = {"applicationName": application_name, "referenceDataSource": reference_data_source}

        jsii.create(CfnApplicationReferenceDataSourceV2, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationReferenceDataSourceV2Props":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2.CSVMappingParametersProperty")
    class CSVMappingParametersProperty(jsii.compat.TypedDict):
        recordColumnDelimiter: str
        recordRowDelimiter: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2.JSONMappingParametersProperty")
    class JSONMappingParametersProperty(jsii.compat.TypedDict):
        recordRowPath: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2.MappingParametersProperty")
    class MappingParametersProperty(jsii.compat.TypedDict, total=False):
        csvMappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSourceV2.CSVMappingParametersProperty"]
        jsonMappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSourceV2.JSONMappingParametersProperty"]

    class _RecordColumnProperty(jsii.compat.TypedDict, total=False):
        mapping: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2.RecordColumnProperty")
    class RecordColumnProperty(_RecordColumnProperty):
        name: str
        sqlType: str

    class _RecordFormatProperty(jsii.compat.TypedDict, total=False):
        mappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSourceV2.MappingParametersProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2.RecordFormatProperty")
    class RecordFormatProperty(_RecordFormatProperty):
        recordFormatType: str

    class _ReferenceDataSourceProperty(jsii.compat.TypedDict, total=False):
        s3ReferenceDataSource: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSourceV2.S3ReferenceDataSourceProperty"]
        tableName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty")
    class ReferenceDataSourceProperty(_ReferenceDataSourceProperty):
        referenceSchema: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty"]

    class _ReferenceSchemaProperty(jsii.compat.TypedDict, total=False):
        recordEncoding: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty")
    class ReferenceSchemaProperty(_ReferenceSchemaProperty):
        recordColumns: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSourceV2.RecordColumnProperty"]]]
        recordFormat: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSourceV2.RecordFormatProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2.S3ReferenceDataSourceProperty")
    class S3ReferenceDataSourceProperty(jsii.compat.TypedDict):
        bucketArn: str
        fileKey: str


@jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2Props")
class CfnApplicationReferenceDataSourceV2Props(jsii.compat.TypedDict):
    applicationName: str
    referenceDataSource: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty"]

class CfnApplicationV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, runtime_environment: str, service_execution_role: str, application_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ApplicationConfigurationProperty"]]=None, application_description: typing.Optional[str]=None, application_name: typing.Optional[str]=None) -> None:
        props: CfnApplicationV2Props = {"runtimeEnvironment": runtime_environment, "serviceExecutionRole": service_execution_role}

        if application_configuration is not None:
            props["applicationConfiguration"] = application_configuration

        if application_description is not None:
            props["applicationDescription"] = application_description

        if application_name is not None:
            props["applicationName"] = application_name

        jsii.create(CfnApplicationV2, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationV2Props":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.ApplicationCodeConfigurationProperty")
    class ApplicationCodeConfigurationProperty(jsii.compat.TypedDict):
        codeContent: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.CodeContentProperty"]
        codeContentType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.ApplicationConfigurationProperty")
    class ApplicationConfigurationProperty(jsii.compat.TypedDict, total=False):
        applicationCodeConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.ApplicationCodeConfigurationProperty"]
        applicationSnapshotConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.ApplicationSnapshotConfigurationProperty"]
        environmentProperties: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.EnvironmentPropertiesProperty"]
        flinkApplicationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.FlinkApplicationConfigurationProperty"]
        sqlApplicationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.SqlApplicationConfigurationProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.ApplicationSnapshotConfigurationProperty")
    class ApplicationSnapshotConfigurationProperty(jsii.compat.TypedDict):
        snapshotsEnabled: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.CSVMappingParametersProperty")
    class CSVMappingParametersProperty(jsii.compat.TypedDict):
        recordColumnDelimiter: str
        recordRowDelimiter: str

    class _CheckpointConfigurationProperty(jsii.compat.TypedDict, total=False):
        checkpointingEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        checkpointInterval: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        minPauseBetweenCheckpoints: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.CheckpointConfigurationProperty")
    class CheckpointConfigurationProperty(_CheckpointConfigurationProperty):
        configurationType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.CodeContentProperty")
    class CodeContentProperty(jsii.compat.TypedDict, total=False):
        s3ContentLocation: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.S3ContentLocationProperty"]
        textContent: str
        zipFileContent: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.EnvironmentPropertiesProperty")
    class EnvironmentPropertiesProperty(jsii.compat.TypedDict, total=False):
        propertyGroups: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.PropertyGroupProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.FlinkApplicationConfigurationProperty")
    class FlinkApplicationConfigurationProperty(jsii.compat.TypedDict, total=False):
        checkpointConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.CheckpointConfigurationProperty"]
        monitoringConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.MonitoringConfigurationProperty"]
        parallelismConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.ParallelismConfigurationProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.InputLambdaProcessorProperty")
    class InputLambdaProcessorProperty(jsii.compat.TypedDict):
        resourceArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.InputParallelismProperty")
    class InputParallelismProperty(jsii.compat.TypedDict, total=False):
        count: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.InputProcessingConfigurationProperty")
    class InputProcessingConfigurationProperty(jsii.compat.TypedDict, total=False):
        inputLambdaProcessor: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.InputLambdaProcessorProperty"]

    class _InputProperty(jsii.compat.TypedDict, total=False):
        inputParallelism: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.InputParallelismProperty"]
        inputProcessingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.InputProcessingConfigurationProperty"]
        kinesisFirehoseInput: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.KinesisFirehoseInputProperty"]
        kinesisStreamsInput: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.KinesisStreamsInputProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.InputProperty")
    class InputProperty(_InputProperty):
        inputSchema: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.InputSchemaProperty"]
        namePrefix: str

    class _InputSchemaProperty(jsii.compat.TypedDict, total=False):
        recordEncoding: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.InputSchemaProperty")
    class InputSchemaProperty(_InputSchemaProperty):
        recordColumns: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.RecordColumnProperty"]]]
        recordFormat: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.RecordFormatProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.JSONMappingParametersProperty")
    class JSONMappingParametersProperty(jsii.compat.TypedDict):
        recordRowPath: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.KinesisFirehoseInputProperty")
    class KinesisFirehoseInputProperty(jsii.compat.TypedDict):
        resourceArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.KinesisStreamsInputProperty")
    class KinesisStreamsInputProperty(jsii.compat.TypedDict):
        resourceArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.MappingParametersProperty")
    class MappingParametersProperty(jsii.compat.TypedDict, total=False):
        csvMappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.CSVMappingParametersProperty"]
        jsonMappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.JSONMappingParametersProperty"]

    class _MonitoringConfigurationProperty(jsii.compat.TypedDict, total=False):
        logLevel: str
        metricsLevel: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.MonitoringConfigurationProperty")
    class MonitoringConfigurationProperty(_MonitoringConfigurationProperty):
        configurationType: str

    class _ParallelismConfigurationProperty(jsii.compat.TypedDict, total=False):
        autoScalingEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        parallelism: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        parallelismPerKpu: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.ParallelismConfigurationProperty")
    class ParallelismConfigurationProperty(_ParallelismConfigurationProperty):
        configurationType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.PropertyGroupProperty")
    class PropertyGroupProperty(jsii.compat.TypedDict, total=False):
        propertyGroupId: str
        propertyMap: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

    class _RecordColumnProperty(jsii.compat.TypedDict, total=False):
        mapping: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.RecordColumnProperty")
    class RecordColumnProperty(_RecordColumnProperty):
        name: str
        sqlType: str

    class _RecordFormatProperty(jsii.compat.TypedDict, total=False):
        mappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.MappingParametersProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.RecordFormatProperty")
    class RecordFormatProperty(_RecordFormatProperty):
        recordFormatType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.S3ContentLocationProperty")
    class S3ContentLocationProperty(jsii.compat.TypedDict, total=False):
        bucketArn: str
        fileKey: str
        objectVersion: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.SqlApplicationConfigurationProperty")
    class SqlApplicationConfigurationProperty(jsii.compat.TypedDict, total=False):
        inputs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.InputProperty"]]]


class _CfnApplicationV2Props(jsii.compat.TypedDict, total=False):
    applicationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.ApplicationConfigurationProperty"]
    applicationDescription: str
    applicationName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2Props")
class CfnApplicationV2Props(_CfnApplicationV2Props):
    runtimeEnvironment: str
    serviceExecutionRole: str

__all__ = ["CfnApplication", "CfnApplicationCloudWatchLoggingOptionV2", "CfnApplicationCloudWatchLoggingOptionV2Props", "CfnApplicationOutput", "CfnApplicationOutputProps", "CfnApplicationOutputV2", "CfnApplicationOutputV2Props", "CfnApplicationProps", "CfnApplicationReferenceDataSource", "CfnApplicationReferenceDataSourceProps", "CfnApplicationReferenceDataSourceV2", "CfnApplicationReferenceDataSourceV2Props", "CfnApplicationV2", "CfnApplicationV2Props", "__jsii_assembly__"]

publication.publish()
