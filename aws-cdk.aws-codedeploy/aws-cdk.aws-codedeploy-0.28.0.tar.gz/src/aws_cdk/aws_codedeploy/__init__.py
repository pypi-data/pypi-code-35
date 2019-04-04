import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_autoscaling
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_codedeploy_api
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-codedeploy", "0.28.0", __name__, "aws-codedeploy@0.28.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.AutoRollbackConfig")
class AutoRollbackConfig(jsii.compat.TypedDict, total=False):
    deploymentInAlarm: bool
    failedDeployment: bool
    stoppedDeployment: bool

class CfnApplication(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.CfnApplication"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: typing.Optional[str]=None, compute_platform: typing.Optional[str]=None) -> None:
        props: CfnApplicationProps = {}

        if application_name is not None:
            props["applicationName"] = application_name

        if compute_platform is not None:
            props["computePlatform"] = compute_platform

        jsii.create(CfnApplication, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        return jsii.get(self, "applicationName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnApplicationProps")
class CfnApplicationProps(jsii.compat.TypedDict, total=False):
    applicationName: str
    computePlatform: str

class CfnDeploymentConfig(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentConfig"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, deployment_config_name: typing.Optional[str]=None, minimum_healthy_hosts: typing.Optional[typing.Union["MinimumHealthyHostsProperty", aws_cdk.cdk.Token]]=None) -> None:
        props: CfnDeploymentConfigProps = {}

        if deployment_config_name is not None:
            props["deploymentConfigName"] = deployment_config_name

        if minimum_healthy_hosts is not None:
            props["minimumHealthyHosts"] = minimum_healthy_hosts

        jsii.create(CfnDeploymentConfig, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="deploymentConfigId")
    def deployment_config_id(self) -> str:
        return jsii.get(self, "deploymentConfigId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDeploymentConfigProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentConfig.MinimumHealthyHostsProperty")
    class MinimumHealthyHostsProperty(jsii.compat.TypedDict):
        type: str
        value: typing.Union[jsii.Number, aws_cdk.cdk.Token]


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentConfigProps")
class CfnDeploymentConfigProps(jsii.compat.TypedDict, total=False):
    deploymentConfigName: str
    minimumHealthyHosts: typing.Union["CfnDeploymentConfig.MinimumHealthyHostsProperty", aws_cdk.cdk.Token]

class CfnDeploymentGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, service_role_arn: str, alarm_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "AlarmConfigurationProperty"]]=None, auto_rollback_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "AutoRollbackConfigurationProperty"]]=None, auto_scaling_groups: typing.Optional[typing.List[str]]=None, deployment: typing.Optional[typing.Union[aws_cdk.cdk.Token, "DeploymentProperty"]]=None, deployment_config_name: typing.Optional[str]=None, deployment_group_name: typing.Optional[str]=None, deployment_style: typing.Optional[typing.Union[aws_cdk.cdk.Token, "DeploymentStyleProperty"]]=None, ec2_tag_filters: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "EC2TagFilterProperty"]]]]=None, ec2_tag_set: typing.Optional[typing.Union[aws_cdk.cdk.Token, "EC2TagSetProperty"]]=None, load_balancer_info: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LoadBalancerInfoProperty"]]=None, on_premises_instance_tag_filters: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "TagFilterProperty"]]]]=None, on_premises_tag_set: typing.Optional[typing.Union[aws_cdk.cdk.Token, "OnPremisesTagSetProperty"]]=None, trigger_configurations: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "TriggerConfigProperty"]]]]=None) -> None:
        props: CfnDeploymentGroupProps = {"applicationName": application_name, "serviceRoleArn": service_role_arn}

        if alarm_configuration is not None:
            props["alarmConfiguration"] = alarm_configuration

        if auto_rollback_configuration is not None:
            props["autoRollbackConfiguration"] = auto_rollback_configuration

        if auto_scaling_groups is not None:
            props["autoScalingGroups"] = auto_scaling_groups

        if deployment is not None:
            props["deployment"] = deployment

        if deployment_config_name is not None:
            props["deploymentConfigName"] = deployment_config_name

        if deployment_group_name is not None:
            props["deploymentGroupName"] = deployment_group_name

        if deployment_style is not None:
            props["deploymentStyle"] = deployment_style

        if ec2_tag_filters is not None:
            props["ec2TagFilters"] = ec2_tag_filters

        if ec2_tag_set is not None:
            props["ec2TagSet"] = ec2_tag_set

        if load_balancer_info is not None:
            props["loadBalancerInfo"] = load_balancer_info

        if on_premises_instance_tag_filters is not None:
            props["onPremisesInstanceTagFilters"] = on_premises_instance_tag_filters

        if on_premises_tag_set is not None:
            props["onPremisesTagSet"] = on_premises_tag_set

        if trigger_configurations is not None:
            props["triggerConfigurations"] = trigger_configurations

        jsii.create(CfnDeploymentGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        return jsii.get(self, "deploymentGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDeploymentGroupProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.AlarmConfigurationProperty")
    class AlarmConfigurationProperty(jsii.compat.TypedDict, total=False):
        alarms: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.AlarmProperty"]]]
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        ignorePollAlarmFailure: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.AlarmProperty")
    class AlarmProperty(jsii.compat.TypedDict, total=False):
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.AutoRollbackConfigurationProperty")
    class AutoRollbackConfigurationProperty(jsii.compat.TypedDict, total=False):
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        events: typing.List[str]

    class _DeploymentProperty(jsii.compat.TypedDict, total=False):
        description: str
        ignoreApplicationStopFailures: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.DeploymentProperty")
    class DeploymentProperty(_DeploymentProperty):
        revision: typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.RevisionLocationProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.DeploymentStyleProperty")
    class DeploymentStyleProperty(jsii.compat.TypedDict, total=False):
        deploymentOption: str
        deploymentType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.EC2TagFilterProperty")
    class EC2TagFilterProperty(jsii.compat.TypedDict, total=False):
        key: str
        type: str
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.EC2TagSetListObjectProperty")
    class EC2TagSetListObjectProperty(jsii.compat.TypedDict, total=False):
        ec2TagGroup: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.EC2TagFilterProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.EC2TagSetProperty")
    class EC2TagSetProperty(jsii.compat.TypedDict, total=False):
        ec2TagSetList: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.EC2TagSetListObjectProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.ELBInfoProperty")
    class ELBInfoProperty(jsii.compat.TypedDict, total=False):
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.GitHubLocationProperty")
    class GitHubLocationProperty(jsii.compat.TypedDict):
        commitId: str
        repository: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.LoadBalancerInfoProperty")
    class LoadBalancerInfoProperty(jsii.compat.TypedDict, total=False):
        elbInfoList: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.ELBInfoProperty"]]]
        targetGroupInfoList: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.TargetGroupInfoProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.OnPremisesTagSetListObjectProperty")
    class OnPremisesTagSetListObjectProperty(jsii.compat.TypedDict, total=False):
        onPremisesTagGroup: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.TagFilterProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.OnPremisesTagSetProperty")
    class OnPremisesTagSetProperty(jsii.compat.TypedDict, total=False):
        onPremisesTagSetList: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.OnPremisesTagSetListObjectProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.RevisionLocationProperty")
    class RevisionLocationProperty(jsii.compat.TypedDict, total=False):
        gitHubLocation: typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.GitHubLocationProperty"]
        revisionType: str
        s3Location: typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.S3LocationProperty"]

    class _S3LocationProperty(jsii.compat.TypedDict, total=False):
        bundleType: str
        eTag: str
        version: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.S3LocationProperty")
    class S3LocationProperty(_S3LocationProperty):
        bucket: str
        key: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.TagFilterProperty")
    class TagFilterProperty(jsii.compat.TypedDict, total=False):
        key: str
        type: str
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.TargetGroupInfoProperty")
    class TargetGroupInfoProperty(jsii.compat.TypedDict, total=False):
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.TriggerConfigProperty")
    class TriggerConfigProperty(jsii.compat.TypedDict, total=False):
        triggerEvents: typing.List[str]
        triggerName: str
        triggerTargetArn: str


class _CfnDeploymentGroupProps(jsii.compat.TypedDict, total=False):
    alarmConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.AlarmConfigurationProperty"]
    autoRollbackConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.AutoRollbackConfigurationProperty"]
    autoScalingGroups: typing.List[str]
    deployment: typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.DeploymentProperty"]
    deploymentConfigName: str
    deploymentGroupName: str
    deploymentStyle: typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.DeploymentStyleProperty"]
    ec2TagFilters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.EC2TagFilterProperty"]]]
    ec2TagSet: typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.EC2TagSetProperty"]
    loadBalancerInfo: typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.LoadBalancerInfoProperty"]
    onPremisesInstanceTagFilters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.TagFilterProperty"]]]
    onPremisesTagSet: typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.OnPremisesTagSetProperty"]
    triggerConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeploymentGroup.TriggerConfigProperty"]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroupProps")
class CfnDeploymentGroupProps(_CfnDeploymentGroupProps):
    applicationName: str
    serviceRoleArn: str

@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.ILambdaApplication")
class ILambdaApplication(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ILambdaApplicationProxy

    @property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "LambdaApplicationImportProps":
        ...


class _ILambdaApplicationProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-codedeploy.ILambdaApplication"
    @property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        return jsii.get(self, "applicationArn")

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        return jsii.get(self, "applicationName")

    @jsii.member(jsii_name="export")
    def export(self) -> "LambdaApplicationImportProps":
        return jsii.invoke(self, "export", [])


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.ILambdaDeploymentConfig")
class ILambdaDeploymentConfig(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ILambdaDeploymentConfigProxy

    @property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        ...

    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self, scope: aws_cdk.cdk.IConstruct) -> str:
        ...


class _ILambdaDeploymentConfigProxy():
    __jsii_type__ = "@aws-cdk/aws-codedeploy.ILambdaDeploymentConfig"
    @property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        return jsii.get(self, "deploymentConfigName")

    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self, scope: aws_cdk.cdk.IConstruct) -> str:
        return jsii.invoke(self, "deploymentConfigArn", [scope])


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.ILambdaDeploymentGroup")
class ILambdaDeploymentGroup(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ILambdaDeploymentGroupProxy

    @property
    @jsii.member(jsii_name="application")
    def application(self) -> "ILambdaApplication":
        ...

    @property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "LambdaDeploymentGroupImportProps":
        ...


class _ILambdaDeploymentGroupProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-codedeploy.ILambdaDeploymentGroup"
    @property
    @jsii.member(jsii_name="application")
    def application(self) -> "ILambdaApplication":
        return jsii.get(self, "application")

    @property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        return jsii.get(self, "deploymentGroupArn")

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        return jsii.get(self, "deploymentGroupName")

    @jsii.member(jsii_name="export")
    def export(self) -> "LambdaDeploymentGroupImportProps":
        return jsii.invoke(self, "export", [])


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.IServerApplication")
class IServerApplication(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IServerApplicationProxy

    @property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "ServerApplicationImportProps":
        ...


class _IServerApplicationProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-codedeploy.IServerApplication"
    @property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        return jsii.get(self, "applicationArn")

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        return jsii.get(self, "applicationName")

    @jsii.member(jsii_name="export")
    def export(self) -> "ServerApplicationImportProps":
        return jsii.invoke(self, "export", [])


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.IServerDeploymentConfig")
class IServerDeploymentConfig(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IServerDeploymentConfigProxy

    @property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        ...

    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self, scope: aws_cdk.cdk.IConstruct) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "ServerDeploymentConfigImportProps":
        ...


class _IServerDeploymentConfigProxy():
    __jsii_type__ = "@aws-cdk/aws-codedeploy.IServerDeploymentConfig"
    @property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        return jsii.get(self, "deploymentConfigName")

    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self, scope: aws_cdk.cdk.IConstruct) -> str:
        return jsii.invoke(self, "deploymentConfigArn", [scope])

    @jsii.member(jsii_name="export")
    def export(self) -> "ServerDeploymentConfigImportProps":
        return jsii.invoke(self, "export", [])


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.IServerDeploymentGroup")
class IServerDeploymentGroup(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IServerDeploymentGroupProxy

    @property
    @jsii.member(jsii_name="application")
    def application(self) -> "IServerApplication":
        ...

    @property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "IServerDeploymentConfig":
        ...

    @property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_autoscaling.AutoScalingGroup]]:
        ...

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.Role]:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "ServerDeploymentGroupImportProps":
        ...


class _IServerDeploymentGroupProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-codedeploy.IServerDeploymentGroup"
    @property
    @jsii.member(jsii_name="application")
    def application(self) -> "IServerApplication":
        return jsii.get(self, "application")

    @property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "IServerDeploymentConfig":
        return jsii.get(self, "deploymentConfig")

    @property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        return jsii.get(self, "deploymentGroupArn")

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        return jsii.get(self, "deploymentGroupName")

    @property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_autoscaling.AutoScalingGroup]]:
        return jsii.get(self, "autoScalingGroups")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.Role]:
        return jsii.get(self, "role")

    @jsii.member(jsii_name="export")
    def export(self) -> "ServerDeploymentGroupImportProps":
        return jsii.invoke(self, "export", [])


class InstanceTagSet(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.InstanceTagSet"):
    def __init__(self, *instance_tag_groups: typing.Mapping[str,typing.List[str]]) -> None:
        jsii.create(InstanceTagSet, self, [instance_tag_groups])

    @property
    @jsii.member(jsii_name="instanceTagGroups")
    def instance_tag_groups(self) -> typing.List[typing.Mapping[str,typing.List[str]]]:
        return jsii.get(self, "instanceTagGroups")


@jsii.implements(ILambdaApplication)
class LambdaApplication(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.LambdaApplication"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: typing.Optional[str]=None) -> None:
        props: LambdaApplicationProps = {}

        if application_name is not None:
            props["applicationName"] = application_name

        jsii.create(LambdaApplication, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str) -> "ILambdaApplication":
        props: LambdaApplicationImportProps = {"applicationName": application_name}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "LambdaApplicationImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        return jsii.get(self, "applicationArn")

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        return jsii.get(self, "applicationName")


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.LambdaApplicationImportProps")
class LambdaApplicationImportProps(jsii.compat.TypedDict):
    applicationName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.LambdaApplicationProps")
class LambdaApplicationProps(jsii.compat.TypedDict, total=False):
    applicationName: str

class LambdaDeploymentConfig(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.LambdaDeploymentConfig"):
    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, deployment_config_name: str) -> "ILambdaDeploymentConfig":
        props: LambdaDeploymentConfigImportProps = {"deploymentConfigName": deployment_config_name}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @classproperty
    @jsii.member(jsii_name="AllAtOnce")
    def ALL_AT_ONCE(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "AllAtOnce")

    @classproperty
    @jsii.member(jsii_name="Canary10Percent10Minutes")
    def CANARY10_PERCENT10_MINUTES(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "Canary10Percent10Minutes")

    @classproperty
    @jsii.member(jsii_name="Canary10Percent15Minutes")
    def CANARY10_PERCENT15_MINUTES(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "Canary10Percent15Minutes")

    @classproperty
    @jsii.member(jsii_name="Canary10Percent30Minutes")
    def CANARY10_PERCENT30_MINUTES(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "Canary10Percent30Minutes")

    @classproperty
    @jsii.member(jsii_name="Canary10Percent5Minutes")
    def CANARY10_PERCENT5_MINUTES(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "Canary10Percent5Minutes")

    @classproperty
    @jsii.member(jsii_name="Linear10PercentEvery10Minutes")
    def LINEAR10_PERCENT_EVERY10_MINUTES(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "Linear10PercentEvery10Minutes")

    @classproperty
    @jsii.member(jsii_name="Linear10PercentEvery1Minute")
    def LINEAR10_PERCENT_EVERY1_MINUTE(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "Linear10PercentEvery1Minute")

    @classproperty
    @jsii.member(jsii_name="Linear10PercentEvery2Minutes")
    def LINEAR10_PERCENT_EVERY2_MINUTES(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "Linear10PercentEvery2Minutes")

    @classproperty
    @jsii.member(jsii_name="Linear10PercentEvery3Minutes")
    def LINEAR10_PERCENT_EVERY3_MINUTES(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "Linear10PercentEvery3Minutes")


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.LambdaDeploymentConfigImportProps")
class LambdaDeploymentConfigImportProps(jsii.compat.TypedDict):
    deploymentConfigName: str

@jsii.implements(ILambdaDeploymentGroup)
class LambdaDeploymentGroup(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.LambdaDeploymentGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, alias: aws_cdk.aws_lambda.Alias, alarms: typing.Optional[typing.List[aws_cdk.aws_cloudwatch.Alarm]]=None, application: typing.Optional["ILambdaApplication"]=None, auto_rollback: typing.Optional["AutoRollbackConfig"]=None, deployment_config: typing.Optional["ILambdaDeploymentConfig"]=None, deployment_group_name: typing.Optional[str]=None, ignore_poll_alarms_failure: typing.Optional[bool]=None, post_hook: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, pre_hook: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> None:
        props: LambdaDeploymentGroupProps = {"alias": alias}

        if alarms is not None:
            props["alarms"] = alarms

        if application is not None:
            props["application"] = application

        if auto_rollback is not None:
            props["autoRollback"] = auto_rollback

        if deployment_config is not None:
            props["deploymentConfig"] = deployment_config

        if deployment_group_name is not None:
            props["deploymentGroupName"] = deployment_group_name

        if ignore_poll_alarms_failure is not None:
            props["ignorePollAlarmsFailure"] = ignore_poll_alarms_failure

        if post_hook is not None:
            props["postHook"] = post_hook

        if pre_hook is not None:
            props["preHook"] = pre_hook

        if role is not None:
            props["role"] = role

        jsii.create(LambdaDeploymentGroup, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, application: "ILambdaApplication", deployment_group_name: str) -> "ILambdaDeploymentGroup":
        props: LambdaDeploymentGroupImportProps = {"application": application, "deploymentGroupName": deployment_group_name}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addAlarm")
    def add_alarm(self, alarm: aws_cdk.aws_cloudwatch.Alarm) -> None:
        return jsii.invoke(self, "addAlarm", [alarm])

    @jsii.member(jsii_name="export")
    def export(self) -> "LambdaDeploymentGroupImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grantPutLifecycleEventHookExecutionStatus")
    def grant_put_lifecycle_event_hook_execution_status(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantPutLifecycleEventHookExecutionStatus", [grantee])

    @jsii.member(jsii_name="onPostHook")
    def on_post_hook(self, post_hook: aws_cdk.aws_lambda.IFunction) -> None:
        return jsii.invoke(self, "onPostHook", [post_hook])

    @jsii.member(jsii_name="onPreHook")
    def on_pre_hook(self, pre_hook: aws_cdk.aws_lambda.IFunction) -> None:
        return jsii.invoke(self, "onPreHook", [pre_hook])

    @property
    @jsii.member(jsii_name="application")
    def application(self) -> "ILambdaApplication":
        return jsii.get(self, "application")

    @property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        return jsii.get(self, "deploymentGroupArn")

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        return jsii.get(self, "deploymentGroupName")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.get(self, "role")


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.LambdaDeploymentGroupImportProps")
class LambdaDeploymentGroupImportProps(jsii.compat.TypedDict):
    application: "ILambdaApplication"
    deploymentGroupName: str

class _LambdaDeploymentGroupProps(jsii.compat.TypedDict, total=False):
    alarms: typing.List[aws_cdk.aws_cloudwatch.Alarm]
    application: "ILambdaApplication"
    autoRollback: "AutoRollbackConfig"
    deploymentConfig: "ILambdaDeploymentConfig"
    deploymentGroupName: str
    ignorePollAlarmsFailure: bool
    postHook: aws_cdk.aws_lambda.IFunction
    preHook: aws_cdk.aws_lambda.IFunction
    role: aws_cdk.aws_iam.IRole

@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.LambdaDeploymentGroupProps")
class LambdaDeploymentGroupProps(_LambdaDeploymentGroupProps):
    alias: aws_cdk.aws_lambda.Alias

@jsii.implements(IServerApplication)
class ServerApplication(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.ServerApplication"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: typing.Optional[str]=None) -> None:
        props: ServerApplicationProps = {}

        if application_name is not None:
            props["applicationName"] = application_name

        jsii.create(ServerApplication, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str) -> "IServerApplication":
        props: ServerApplicationImportProps = {"applicationName": application_name}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "ServerApplicationImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        return jsii.get(self, "applicationArn")

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        return jsii.get(self, "applicationName")


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.ServerApplicationImportProps")
class ServerApplicationImportProps(jsii.compat.TypedDict):
    applicationName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.ServerApplicationProps")
class ServerApplicationProps(jsii.compat.TypedDict, total=False):
    applicationName: str

@jsii.implements(IServerDeploymentConfig)
class ServerDeploymentConfig(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentConfig"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, deployment_config_name: typing.Optional[str]=None, min_healthy_host_count: typing.Optional[jsii.Number]=None, min_healthy_host_percentage: typing.Optional[jsii.Number]=None) -> None:
        props: ServerDeploymentConfigProps = {}

        if deployment_config_name is not None:
            props["deploymentConfigName"] = deployment_config_name

        if min_healthy_host_count is not None:
            props["minHealthyHostCount"] = min_healthy_host_count

        if min_healthy_host_percentage is not None:
            props["minHealthyHostPercentage"] = min_healthy_host_percentage

        jsii.create(ServerDeploymentConfig, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, deployment_config_name: str) -> "IServerDeploymentConfig":
        props: ServerDeploymentConfigImportProps = {"deploymentConfigName": deployment_config_name}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self, scope: aws_cdk.cdk.IConstruct) -> str:
        return jsii.invoke(self, "deploymentConfigArn", [scope])

    @jsii.member(jsii_name="export")
    def export(self) -> "ServerDeploymentConfigImportProps":
        return jsii.invoke(self, "export", [])

    @classproperty
    @jsii.member(jsii_name="AllAtOnce")
    def ALL_AT_ONCE(cls) -> "IServerDeploymentConfig":
        return jsii.sget(cls, "AllAtOnce")

    @classproperty
    @jsii.member(jsii_name="HalfAtATime")
    def HALF_AT_A_TIME(cls) -> "IServerDeploymentConfig":
        return jsii.sget(cls, "HalfAtATime")

    @classproperty
    @jsii.member(jsii_name="OneAtATime")
    def ONE_AT_A_TIME(cls) -> "IServerDeploymentConfig":
        return jsii.sget(cls, "OneAtATime")

    @property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        return jsii.get(self, "deploymentConfigName")


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentConfigImportProps")
class ServerDeploymentConfigImportProps(jsii.compat.TypedDict):
    deploymentConfigName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentConfigProps")
class ServerDeploymentConfigProps(jsii.compat.TypedDict, total=False):
    deploymentConfigName: str
    minHealthyHostCount: jsii.Number
    minHealthyHostPercentage: jsii.Number

@jsii.implements(IServerDeploymentGroup)
class ServerDeploymentGroupBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentGroupBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _ServerDeploymentGroupBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, deployment_config: typing.Optional["IServerDeploymentConfig"]=None) -> None:
        jsii.create(ServerDeploymentGroupBase, self, [scope, id, deployment_config])

    @jsii.member(jsii_name="export")
    @abc.abstractmethod
    def export(self) -> "ServerDeploymentGroupImportProps":
        ...

    @property
    @jsii.member(jsii_name="application")
    @abc.abstractmethod
    def application(self) -> "IServerApplication":
        ...

    @property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "IServerDeploymentConfig":
        return jsii.get(self, "deploymentConfig")

    @property
    @jsii.member(jsii_name="deploymentGroupArn")
    @abc.abstractmethod
    def deployment_group_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    @abc.abstractmethod
    def deployment_group_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="autoScalingGroups")
    @abc.abstractmethod
    def auto_scaling_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_autoscaling.AutoScalingGroup]]:
        ...

    @property
    @jsii.member(jsii_name="role")
    @abc.abstractmethod
    def role(self) -> typing.Optional[aws_cdk.aws_iam.Role]:
        ...


class _ServerDeploymentGroupBaseProxy(ServerDeploymentGroupBase):
    @jsii.member(jsii_name="export")
    def export(self) -> "ServerDeploymentGroupImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="application")
    def application(self) -> "IServerApplication":
        return jsii.get(self, "application")

    @property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        return jsii.get(self, "deploymentGroupArn")

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        return jsii.get(self, "deploymentGroupName")

    @property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_autoscaling.AutoScalingGroup]]:
        return jsii.get(self, "autoScalingGroups")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.Role]:
        return jsii.get(self, "role")


class ServerDeploymentGroup(ServerDeploymentGroupBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, alarms: typing.Optional[typing.List[aws_cdk.aws_cloudwatch.Alarm]]=None, application: typing.Optional["IServerApplication"]=None, auto_rollback: typing.Optional["AutoRollbackConfig"]=None, auto_scaling_groups: typing.Optional[typing.List[aws_cdk.aws_autoscaling.AutoScalingGroup]]=None, deployment_config: typing.Optional["IServerDeploymentConfig"]=None, deployment_group_name: typing.Optional[str]=None, ec2_instance_tags: typing.Optional["InstanceTagSet"]=None, ignore_poll_alarms_failure: typing.Optional[bool]=None, install_agent: typing.Optional[bool]=None, load_balancer: typing.Optional[aws_cdk.aws_codedeploy_api.ILoadBalancer]=None, on_premise_instance_tags: typing.Optional["InstanceTagSet"]=None, role: typing.Optional[aws_cdk.aws_iam.Role]=None) -> None:
        props: ServerDeploymentGroupProps = {}

        if alarms is not None:
            props["alarms"] = alarms

        if application is not None:
            props["application"] = application

        if auto_rollback is not None:
            props["autoRollback"] = auto_rollback

        if auto_scaling_groups is not None:
            props["autoScalingGroups"] = auto_scaling_groups

        if deployment_config is not None:
            props["deploymentConfig"] = deployment_config

        if deployment_group_name is not None:
            props["deploymentGroupName"] = deployment_group_name

        if ec2_instance_tags is not None:
            props["ec2InstanceTags"] = ec2_instance_tags

        if ignore_poll_alarms_failure is not None:
            props["ignorePollAlarmsFailure"] = ignore_poll_alarms_failure

        if install_agent is not None:
            props["installAgent"] = install_agent

        if load_balancer is not None:
            props["loadBalancer"] = load_balancer

        if on_premise_instance_tags is not None:
            props["onPremiseInstanceTags"] = on_premise_instance_tags

        if role is not None:
            props["role"] = role

        jsii.create(ServerDeploymentGroup, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, application: "IServerApplication", deployment_group_name: str, deployment_config: typing.Optional["IServerDeploymentConfig"]=None) -> "IServerDeploymentGroup":
        props: ServerDeploymentGroupImportProps = {"application": application, "deploymentGroupName": deployment_group_name}

        if deployment_config is not None:
            props["deploymentConfig"] = deployment_config

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addAlarm")
    def add_alarm(self, alarm: aws_cdk.aws_cloudwatch.Alarm) -> None:
        return jsii.invoke(self, "addAlarm", [alarm])

    @jsii.member(jsii_name="addAutoScalingGroup")
    def add_auto_scaling_group(self, asg: aws_cdk.aws_autoscaling.AutoScalingGroup) -> None:
        return jsii.invoke(self, "addAutoScalingGroup", [asg])

    @jsii.member(jsii_name="export")
    def export(self) -> "ServerDeploymentGroupImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="application")
    def application(self) -> "IServerApplication":
        return jsii.get(self, "application")

    @property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        return jsii.get(self, "deploymentGroupArn")

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        return jsii.get(self, "deploymentGroupName")

    @property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_autoscaling.AutoScalingGroup]]:
        return jsii.get(self, "autoScalingGroups")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.Role]:
        return jsii.get(self, "role")


class _ServerDeploymentGroupImportProps(jsii.compat.TypedDict, total=False):
    deploymentConfig: "IServerDeploymentConfig"

@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentGroupImportProps")
class ServerDeploymentGroupImportProps(_ServerDeploymentGroupImportProps):
    application: "IServerApplication"
    deploymentGroupName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentGroupProps")
class ServerDeploymentGroupProps(jsii.compat.TypedDict, total=False):
    alarms: typing.List[aws_cdk.aws_cloudwatch.Alarm]
    application: "IServerApplication"
    autoRollback: "AutoRollbackConfig"
    autoScalingGroups: typing.List[aws_cdk.aws_autoscaling.AutoScalingGroup]
    deploymentConfig: "IServerDeploymentConfig"
    deploymentGroupName: str
    ec2InstanceTags: "InstanceTagSet"
    ignorePollAlarmsFailure: bool
    installAgent: bool
    loadBalancer: aws_cdk.aws_codedeploy_api.ILoadBalancer
    onPremiseInstanceTags: "InstanceTagSet"
    role: aws_cdk.aws_iam.Role

__all__ = ["AutoRollbackConfig", "CfnApplication", "CfnApplicationProps", "CfnDeploymentConfig", "CfnDeploymentConfigProps", "CfnDeploymentGroup", "CfnDeploymentGroupProps", "ILambdaApplication", "ILambdaDeploymentConfig", "ILambdaDeploymentGroup", "IServerApplication", "IServerDeploymentConfig", "IServerDeploymentGroup", "InstanceTagSet", "LambdaApplication", "LambdaApplicationImportProps", "LambdaApplicationProps", "LambdaDeploymentConfig", "LambdaDeploymentConfigImportProps", "LambdaDeploymentGroup", "LambdaDeploymentGroupImportProps", "LambdaDeploymentGroupProps", "ServerApplication", "ServerApplicationImportProps", "ServerApplicationProps", "ServerDeploymentConfig", "ServerDeploymentConfigImportProps", "ServerDeploymentConfigProps", "ServerDeploymentGroup", "ServerDeploymentGroupBase", "ServerDeploymentGroupImportProps", "ServerDeploymentGroupProps", "__jsii_assembly__"]

publication.publish()
