import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-ssm", "0.28.0", __name__, "aws-ssm@0.28.0.jsii.tgz")
class CfnAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ssm.CfnAssociation"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, association_name: typing.Optional[str]=None, document_version: typing.Optional[str]=None, instance_id: typing.Optional[str]=None, output_location: typing.Optional[typing.Union[aws_cdk.cdk.Token, "InstanceAssociationOutputLocationProperty"]]=None, parameters: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,typing.Union[aws_cdk.cdk.Token, "ParameterValuesProperty"]]]]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "TargetProperty"]]]]=None) -> None:
        props: CfnAssociationProps = {"name": name}

        if association_name is not None:
            props["associationName"] = association_name

        if document_version is not None:
            props["documentVersion"] = document_version

        if instance_id is not None:
            props["instanceId"] = instance_id

        if output_location is not None:
            props["outputLocation"] = output_location

        if parameters is not None:
            props["parameters"] = parameters

        if schedule_expression is not None:
            props["scheduleExpression"] = schedule_expression

        if targets is not None:
            props["targets"] = targets

        jsii.create(CfnAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAssociationProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnAssociation.InstanceAssociationOutputLocationProperty")
    class InstanceAssociationOutputLocationProperty(jsii.compat.TypedDict, total=False):
        s3Location: typing.Union[aws_cdk.cdk.Token, "CfnAssociation.S3OutputLocationProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnAssociation.ParameterValuesProperty")
    class ParameterValuesProperty(jsii.compat.TypedDict):
        parameterValues: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnAssociation.S3OutputLocationProperty")
    class S3OutputLocationProperty(jsii.compat.TypedDict, total=False):
        outputS3BucketName: str
        outputS3KeyPrefix: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnAssociation.TargetProperty")
    class TargetProperty(jsii.compat.TypedDict):
        key: str
        values: typing.List[str]


class _CfnAssociationProps(jsii.compat.TypedDict, total=False):
    associationName: str
    documentVersion: str
    instanceId: str
    outputLocation: typing.Union[aws_cdk.cdk.Token, "CfnAssociation.InstanceAssociationOutputLocationProperty"]
    parameters: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,typing.Union[aws_cdk.cdk.Token, "CfnAssociation.ParameterValuesProperty"]]]
    scheduleExpression: str
    targets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnAssociation.TargetProperty"]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnAssociationProps")
class CfnAssociationProps(_CfnAssociationProps):
    name: str

class CfnDocument(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ssm.CfnDocument"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, content: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], document_type: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnDocumentProps = {"content": content}

        if document_type is not None:
            props["documentType"] = document_type

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDocument, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="documentName")
    def document_name(self) -> str:
        return jsii.get(self, "documentName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDocumentProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnDocumentProps(jsii.compat.TypedDict, total=False):
    documentType: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnDocumentProps")
class CfnDocumentProps(_CfnDocumentProps):
    content: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

class CfnMaintenanceWindow(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindow"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, allow_unassociated_targets: typing.Union[bool, aws_cdk.cdk.Token], cutoff: typing.Union[jsii.Number, aws_cdk.cdk.Token], duration: typing.Union[jsii.Number, aws_cdk.cdk.Token], name: str, schedule: str, description: typing.Optional[str]=None, end_date: typing.Optional[str]=None, schedule_timezone: typing.Optional[str]=None, start_date: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnMaintenanceWindowProps = {"allowUnassociatedTargets": allow_unassociated_targets, "cutoff": cutoff, "duration": duration, "name": name, "schedule": schedule}

        if description is not None:
            props["description"] = description

        if end_date is not None:
            props["endDate"] = end_date

        if schedule_timezone is not None:
            props["scheduleTimezone"] = schedule_timezone

        if start_date is not None:
            props["startDate"] = start_date

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnMaintenanceWindow, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="maintenanceWindowId")
    def maintenance_window_id(self) -> str:
        return jsii.get(self, "maintenanceWindowId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnMaintenanceWindowProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnMaintenanceWindowProps(jsii.compat.TypedDict, total=False):
    description: str
    endDate: str
    scheduleTimezone: str
    startDate: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowProps")
class CfnMaintenanceWindowProps(_CfnMaintenanceWindowProps):
    allowUnassociatedTargets: typing.Union[bool, aws_cdk.cdk.Token]
    cutoff: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    duration: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    name: str
    schedule: str

class CfnMaintenanceWindowTask(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, max_concurrency: str, max_errors: str, priority: typing.Union[jsii.Number, aws_cdk.cdk.Token], service_role_arn: str, targets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "TargetProperty"]]], task_arn: str, task_type: str, description: typing.Optional[str]=None, logging_info: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LoggingInfoProperty"]]=None, name: typing.Optional[str]=None, task_invocation_parameters: typing.Optional[typing.Union[aws_cdk.cdk.Token, "TaskInvocationParametersProperty"]]=None, task_parameters: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, window_id: typing.Optional[str]=None) -> None:
        props: CfnMaintenanceWindowTaskProps = {"maxConcurrency": max_concurrency, "maxErrors": max_errors, "priority": priority, "serviceRoleArn": service_role_arn, "targets": targets, "taskArn": task_arn, "taskType": task_type}

        if description is not None:
            props["description"] = description

        if logging_info is not None:
            props["loggingInfo"] = logging_info

        if name is not None:
            props["name"] = name

        if task_invocation_parameters is not None:
            props["taskInvocationParameters"] = task_invocation_parameters

        if task_parameters is not None:
            props["taskParameters"] = task_parameters

        if window_id is not None:
            props["windowId"] = window_id

        jsii.create(CfnMaintenanceWindowTask, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="maintenanceWindowTaskId")
    def maintenance_window_task_id(self) -> str:
        return jsii.get(self, "maintenanceWindowTaskId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnMaintenanceWindowTaskProps":
        return jsii.get(self, "propertyOverrides")

    class _LoggingInfoProperty(jsii.compat.TypedDict, total=False):
        s3Prefix: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask.LoggingInfoProperty")
    class LoggingInfoProperty(_LoggingInfoProperty):
        region: str
        s3Bucket: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask.MaintenanceWindowAutomationParametersProperty")
    class MaintenanceWindowAutomationParametersProperty(jsii.compat.TypedDict, total=False):
        documentVersion: str
        parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask.MaintenanceWindowLambdaParametersProperty")
    class MaintenanceWindowLambdaParametersProperty(jsii.compat.TypedDict, total=False):
        clientContext: str
        payload: str
        qualifier: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty")
    class MaintenanceWindowRunCommandParametersProperty(jsii.compat.TypedDict, total=False):
        comment: str
        documentHash: str
        documentHashType: str
        notificationConfig: typing.Union[aws_cdk.cdk.Token, "CfnMaintenanceWindowTask.NotificationConfigProperty"]
        outputS3BucketName: str
        outputS3KeyPrefix: str
        parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        serviceRoleArn: str
        timeoutSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask.MaintenanceWindowStepFunctionsParametersProperty")
    class MaintenanceWindowStepFunctionsParametersProperty(jsii.compat.TypedDict, total=False):
        input: str
        name: str

    class _NotificationConfigProperty(jsii.compat.TypedDict, total=False):
        notificationEvents: typing.List[str]
        notificationType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask.NotificationConfigProperty")
    class NotificationConfigProperty(_NotificationConfigProperty):
        notificationArn: str

    class _TargetProperty(jsii.compat.TypedDict, total=False):
        values: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask.TargetProperty")
    class TargetProperty(_TargetProperty):
        key: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask.TaskInvocationParametersProperty")
    class TaskInvocationParametersProperty(jsii.compat.TypedDict, total=False):
        maintenanceWindowAutomationParameters: typing.Union[aws_cdk.cdk.Token, "CfnMaintenanceWindowTask.MaintenanceWindowAutomationParametersProperty"]
        maintenanceWindowLambdaParameters: typing.Union[aws_cdk.cdk.Token, "CfnMaintenanceWindowTask.MaintenanceWindowLambdaParametersProperty"]
        maintenanceWindowRunCommandParameters: typing.Union[aws_cdk.cdk.Token, "CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty"]
        maintenanceWindowStepFunctionsParameters: typing.Union[aws_cdk.cdk.Token, "CfnMaintenanceWindowTask.MaintenanceWindowStepFunctionsParametersProperty"]


class _CfnMaintenanceWindowTaskProps(jsii.compat.TypedDict, total=False):
    description: str
    loggingInfo: typing.Union[aws_cdk.cdk.Token, "CfnMaintenanceWindowTask.LoggingInfoProperty"]
    name: str
    taskInvocationParameters: typing.Union[aws_cdk.cdk.Token, "CfnMaintenanceWindowTask.TaskInvocationParametersProperty"]
    taskParameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    windowId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTaskProps")
class CfnMaintenanceWindowTaskProps(_CfnMaintenanceWindowTaskProps):
    maxConcurrency: str
    maxErrors: str
    priority: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    serviceRoleArn: str
    targets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnMaintenanceWindowTask.TargetProperty"]]]
    taskArn: str
    taskType: str

class CfnParameter(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ssm.CfnParameter"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, type: str, value: str, allowed_pattern: typing.Optional[str]=None, description: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
        props: CfnParameterProps = {"type": type, "value": value}

        if allowed_pattern is not None:
            props["allowedPattern"] = allowed_pattern

        if description is not None:
            props["description"] = description

        if name is not None:
            props["name"] = name

        jsii.create(CfnParameter, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> str:
        return jsii.get(self, "parameterName")

    @property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> str:
        return jsii.get(self, "parameterType")

    @property
    @jsii.member(jsii_name="parameterValue")
    def parameter_value(self) -> str:
        return jsii.get(self, "parameterValue")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnParameterProps":
        return jsii.get(self, "propertyOverrides")


class _CfnParameterProps(jsii.compat.TypedDict, total=False):
    allowedPattern: str
    description: str
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnParameterProps")
class CfnParameterProps(_CfnParameterProps):
    type: str
    value: str

class CfnPatchBaseline(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ssm.CfnPatchBaseline"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, approval_rules: typing.Optional[typing.Union[aws_cdk.cdk.Token, "RuleGroupProperty"]]=None, approved_patches: typing.Optional[typing.List[str]]=None, approved_patches_compliance_level: typing.Optional[str]=None, approved_patches_enable_non_security: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, description: typing.Optional[str]=None, global_filters: typing.Optional[typing.Union[aws_cdk.cdk.Token, "PatchFilterGroupProperty"]]=None, operating_system: typing.Optional[str]=None, patch_groups: typing.Optional[typing.List[str]]=None, rejected_patches: typing.Optional[typing.List[str]]=None, rejected_patches_action: typing.Optional[str]=None, sources: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "PatchSourceProperty"]]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnPatchBaselineProps = {"name": name}

        if approval_rules is not None:
            props["approvalRules"] = approval_rules

        if approved_patches is not None:
            props["approvedPatches"] = approved_patches

        if approved_patches_compliance_level is not None:
            props["approvedPatchesComplianceLevel"] = approved_patches_compliance_level

        if approved_patches_enable_non_security is not None:
            props["approvedPatchesEnableNonSecurity"] = approved_patches_enable_non_security

        if description is not None:
            props["description"] = description

        if global_filters is not None:
            props["globalFilters"] = global_filters

        if operating_system is not None:
            props["operatingSystem"] = operating_system

        if patch_groups is not None:
            props["patchGroups"] = patch_groups

        if rejected_patches is not None:
            props["rejectedPatches"] = rejected_patches

        if rejected_patches_action is not None:
            props["rejectedPatchesAction"] = rejected_patches_action

        if sources is not None:
            props["sources"] = sources

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnPatchBaseline, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="patchBaselineId")
    def patch_baseline_id(self) -> str:
        return jsii.get(self, "patchBaselineId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPatchBaselineProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnPatchBaseline.PatchFilterGroupProperty")
    class PatchFilterGroupProperty(jsii.compat.TypedDict, total=False):
        patchFilters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPatchBaseline.PatchFilterProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnPatchBaseline.PatchFilterProperty")
    class PatchFilterProperty(jsii.compat.TypedDict, total=False):
        key: str
        values: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnPatchBaseline.PatchSourceProperty")
    class PatchSourceProperty(jsii.compat.TypedDict, total=False):
        configuration: str
        name: str
        products: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnPatchBaseline.RuleGroupProperty")
    class RuleGroupProperty(jsii.compat.TypedDict, total=False):
        patchRules: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPatchBaseline.RuleProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnPatchBaseline.RuleProperty")
    class RuleProperty(jsii.compat.TypedDict, total=False):
        approveAfterDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        complianceLevel: str
        enableNonSecurity: typing.Union[bool, aws_cdk.cdk.Token]
        patchFilterGroup: typing.Union[aws_cdk.cdk.Token, "CfnPatchBaseline.PatchFilterGroupProperty"]


class _CfnPatchBaselineProps(jsii.compat.TypedDict, total=False):
    approvalRules: typing.Union[aws_cdk.cdk.Token, "CfnPatchBaseline.RuleGroupProperty"]
    approvedPatches: typing.List[str]
    approvedPatchesComplianceLevel: str
    approvedPatchesEnableNonSecurity: typing.Union[bool, aws_cdk.cdk.Token]
    description: str
    globalFilters: typing.Union[aws_cdk.cdk.Token, "CfnPatchBaseline.PatchFilterGroupProperty"]
    operatingSystem: str
    patchGroups: typing.List[str]
    rejectedPatches: typing.List[str]
    rejectedPatchesAction: str
    sources: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPatchBaseline.PatchSourceProperty"]]]
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnPatchBaselineProps")
class CfnPatchBaselineProps(_CfnPatchBaselineProps):
    name: str

class CfnResourceDataSync(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ssm.CfnResourceDataSync"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, bucket_name: str, bucket_region: str, sync_format: str, sync_name: str, bucket_prefix: typing.Optional[str]=None, kms_key_arn: typing.Optional[str]=None) -> None:
        props: CfnResourceDataSyncProps = {"bucketName": bucket_name, "bucketRegion": bucket_region, "syncFormat": sync_format, "syncName": sync_name}

        if bucket_prefix is not None:
            props["bucketPrefix"] = bucket_prefix

        if kms_key_arn is not None:
            props["kmsKeyArn"] = kms_key_arn

        jsii.create(CfnResourceDataSync, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnResourceDataSyncProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="resourceDataSyncName")
    def resource_data_sync_name(self) -> str:
        return jsii.get(self, "resourceDataSyncName")


class _CfnResourceDataSyncProps(jsii.compat.TypedDict, total=False):
    bucketPrefix: str
    kmsKeyArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ssm.CfnResourceDataSyncProps")
class CfnResourceDataSyncProps(_CfnResourceDataSyncProps):
    bucketName: str
    bucketRegion: str
    syncFormat: str
    syncName: str

@jsii.interface(jsii_type="@aws-cdk/aws-ssm.IParameter")
class IParameter(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IParameterProxy

    @property
    @jsii.member(jsii_name="parameterArn")
    def parameter_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> str:
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...


class _IParameterProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-ssm.IParameter"
    @property
    @jsii.member(jsii_name="parameterArn")
    def parameter_arn(self) -> str:
        return jsii.get(self, "parameterArn")

    @property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> str:
        return jsii.get(self, "parameterName")

    @property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> str:
        return jsii.get(self, "parameterType")

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantRead", [grantee])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantWrite", [grantee])


@jsii.interface(jsii_type="@aws-cdk/aws-ssm.IStringListParameter")
class IStringListParameter(IParameter, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IStringListParameterProxy

    @property
    @jsii.member(jsii_name="stringListValue")
    def string_list_value(self) -> typing.List[str]:
        ...


class _IStringListParameterProxy(jsii.proxy_for(IParameter)):
    __jsii_type__ = "@aws-cdk/aws-ssm.IStringListParameter"
    @property
    @jsii.member(jsii_name="stringListValue")
    def string_list_value(self) -> typing.List[str]:
        return jsii.get(self, "stringListValue")


@jsii.interface(jsii_type="@aws-cdk/aws-ssm.IStringParameter")
class IStringParameter(IParameter, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IStringParameterProxy

    @property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> str:
        ...


class _IStringParameterProxy(jsii.proxy_for(IParameter)):
    __jsii_type__ = "@aws-cdk/aws-ssm.IStringParameter"
    @property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> str:
        return jsii.get(self, "stringValue")


@jsii.implements(IParameter)
class ParameterBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ssm.ParameterBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _ParameterBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, allowed_pattern: typing.Optional[str]=None, description: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
        _props: ParameterProps = {}

        if allowed_pattern is not None:
            _props["allowedPattern"] = allowed_pattern

        if description is not None:
            _props["description"] = description

        if name is not None:
            _props["name"] = name

        jsii.create(ParameterBase, self, [scope, id, _props])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantRead", [grantee])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantWrite", [grantee])

    @property
    @jsii.member(jsii_name="parameterArn")
    def parameter_arn(self) -> str:
        return jsii.get(self, "parameterArn")

    @property
    @jsii.member(jsii_name="parameterName")
    @abc.abstractmethod
    def parameter_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="parameterType")
    @abc.abstractmethod
    def parameter_type(self) -> str:
        ...


class _ParameterBaseProxy(ParameterBase):
    @property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> str:
        return jsii.get(self, "parameterName")

    @property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> str:
        return jsii.get(self, "parameterType")


@jsii.data_type(jsii_type="@aws-cdk/aws-ssm.ParameterProps")
class ParameterProps(jsii.compat.TypedDict, total=False):
    allowedPattern: str
    description: str
    name: str

class ParameterStoreSecureString(aws_cdk.cdk.CfnDynamicReference, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ssm.ParameterStoreSecureString"):
    def __init__(self, *, parameter_name: str, version: jsii.Number) -> None:
        props: ParameterStoreSecureStringProps = {"parameterName": parameter_name, "version": version}

        jsii.create(ParameterStoreSecureString, self, [props])


@jsii.data_type(jsii_type="@aws-cdk/aws-ssm.ParameterStoreSecureStringProps")
class ParameterStoreSecureStringProps(jsii.compat.TypedDict):
    parameterName: str
    version: jsii.Number

class ParameterStoreString(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ssm.ParameterStoreString"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, parameter_name: str, version: typing.Optional[jsii.Number]=None) -> None:
        props: ParameterStoreStringProps = {"parameterName": parameter_name}

        if version is not None:
            props["version"] = version

        jsii.create(ParameterStoreString, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> str:
        return jsii.get(self, "stringValue")


class _ParameterStoreStringProps(jsii.compat.TypedDict, total=False):
    version: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-ssm.ParameterStoreStringProps")
class ParameterStoreStringProps(_ParameterStoreStringProps):
    parameterName: str

@jsii.implements(IStringListParameter)
class StringListParameter(ParameterBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ssm.StringListParameter"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, string_list_value: typing.List[str], allowed_pattern: typing.Optional[str]=None, description: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
        props: StringListParameterProps = {"stringListValue": string_list_value}

        if allowed_pattern is not None:
            props["allowedPattern"] = allowed_pattern

        if description is not None:
            props["description"] = description

        if name is not None:
            props["name"] = name

        jsii.create(StringListParameter, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> str:
        return jsii.get(self, "parameterName")

    @property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> str:
        return jsii.get(self, "parameterType")

    @property
    @jsii.member(jsii_name="stringListValue")
    def string_list_value(self) -> typing.List[str]:
        return jsii.get(self, "stringListValue")


@jsii.data_type(jsii_type="@aws-cdk/aws-ssm.StringListParameterProps")
class StringListParameterProps(ParameterProps, jsii.compat.TypedDict):
    stringListValue: typing.List[str]

@jsii.implements(IStringParameter)
class StringParameter(ParameterBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ssm.StringParameter"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, string_value: str, allowed_pattern: typing.Optional[str]=None, description: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
        props: StringParameterProps = {"stringValue": string_value}

        if allowed_pattern is not None:
            props["allowedPattern"] = allowed_pattern

        if description is not None:
            props["description"] = description

        if name is not None:
            props["name"] = name

        jsii.create(StringParameter, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> str:
        return jsii.get(self, "parameterName")

    @property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> str:
        return jsii.get(self, "parameterType")

    @property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> str:
        return jsii.get(self, "stringValue")


@jsii.data_type(jsii_type="@aws-cdk/aws-ssm.StringParameterProps")
class StringParameterProps(ParameterProps, jsii.compat.TypedDict):
    stringValue: str

__all__ = ["CfnAssociation", "CfnAssociationProps", "CfnDocument", "CfnDocumentProps", "CfnMaintenanceWindow", "CfnMaintenanceWindowProps", "CfnMaintenanceWindowTask", "CfnMaintenanceWindowTaskProps", "CfnParameter", "CfnParameterProps", "CfnPatchBaseline", "CfnPatchBaselineProps", "CfnResourceDataSync", "CfnResourceDataSyncProps", "IParameter", "IStringListParameter", "IStringParameter", "ParameterBase", "ParameterProps", "ParameterStoreSecureString", "ParameterStoreSecureStringProps", "ParameterStoreString", "ParameterStoreStringProps", "StringListParameter", "StringListParameterProps", "StringParameter", "StringParameterProps", "__jsii_assembly__"]

publication.publish()
