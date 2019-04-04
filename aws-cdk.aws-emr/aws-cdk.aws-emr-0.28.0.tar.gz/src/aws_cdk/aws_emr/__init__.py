import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-emr", "0.28.0", __name__, "aws-emr@0.28.0.jsii.tgz")
class CfnCluster(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-emr.CfnCluster"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, instances: typing.Union["JobFlowInstancesConfigProperty", aws_cdk.cdk.Token], job_flow_role: str, name: str, service_role: str, additional_info: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, applications: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ApplicationProperty"]]]]=None, auto_scaling_role: typing.Optional[str]=None, bootstrap_actions: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "BootstrapActionConfigProperty"]]]]=None, configurations: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ConfigurationProperty"]]]]=None, custom_ami_id: typing.Optional[str]=None, ebs_root_volume_size: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, kerberos_attributes: typing.Optional[typing.Union[aws_cdk.cdk.Token, "KerberosAttributesProperty"]]=None, log_uri: typing.Optional[str]=None, release_label: typing.Optional[str]=None, scale_down_behavior: typing.Optional[str]=None, security_configuration: typing.Optional[str]=None, steps: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "StepConfigProperty"]]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, visible_to_all_users: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnClusterProps = {"instances": instances, "jobFlowRole": job_flow_role, "name": name, "serviceRole": service_role}

        if additional_info is not None:
            props["additionalInfo"] = additional_info

        if applications is not None:
            props["applications"] = applications

        if auto_scaling_role is not None:
            props["autoScalingRole"] = auto_scaling_role

        if bootstrap_actions is not None:
            props["bootstrapActions"] = bootstrap_actions

        if configurations is not None:
            props["configurations"] = configurations

        if custom_ami_id is not None:
            props["customAmiId"] = custom_ami_id

        if ebs_root_volume_size is not None:
            props["ebsRootVolumeSize"] = ebs_root_volume_size

        if kerberos_attributes is not None:
            props["kerberosAttributes"] = kerberos_attributes

        if log_uri is not None:
            props["logUri"] = log_uri

        if release_label is not None:
            props["releaseLabel"] = release_label

        if scale_down_behavior is not None:
            props["scaleDownBehavior"] = scale_down_behavior

        if security_configuration is not None:
            props["securityConfiguration"] = security_configuration

        if steps is not None:
            props["steps"] = steps

        if tags is not None:
            props["tags"] = tags

        if visible_to_all_users is not None:
            props["visibleToAllUsers"] = visible_to_all_users

        jsii.create(CfnCluster, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> str:
        return jsii.get(self, "clusterId")

    @property
    @jsii.member(jsii_name="clusterMasterPublicDns")
    def cluster_master_public_dns(self) -> str:
        return jsii.get(self, "clusterMasterPublicDns")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnClusterProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.ApplicationProperty")
    class ApplicationProperty(jsii.compat.TypedDict, total=False):
        additionalInfo: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        args: typing.List[str]
        name: str
        version: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.AutoScalingPolicyProperty")
    class AutoScalingPolicyProperty(jsii.compat.TypedDict):
        constraints: typing.Union[aws_cdk.cdk.Token, "CfnCluster.ScalingConstraintsProperty"]
        rules: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCluster.ScalingRuleProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.BootstrapActionConfigProperty")
    class BootstrapActionConfigProperty(jsii.compat.TypedDict):
        name: str
        scriptBootstrapAction: typing.Union[aws_cdk.cdk.Token, "CfnCluster.ScriptBootstrapActionConfigProperty"]

    class _CloudWatchAlarmDefinitionProperty(jsii.compat.TypedDict, total=False):
        dimensions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCluster.MetricDimensionProperty"]]]
        evaluationPeriods: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        namespace: str
        statistic: str
        unit: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.CloudWatchAlarmDefinitionProperty")
    class CloudWatchAlarmDefinitionProperty(_CloudWatchAlarmDefinitionProperty):
        comparisonOperator: str
        metricName: str
        period: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        threshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.ConfigurationProperty")
    class ConfigurationProperty(jsii.compat.TypedDict, total=False):
        classification: str
        configurationProperties: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        configurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCluster.ConfigurationProperty"]]]

    class _EbsBlockDeviceConfigProperty(jsii.compat.TypedDict, total=False):
        volumesPerInstance: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.EbsBlockDeviceConfigProperty")
    class EbsBlockDeviceConfigProperty(_EbsBlockDeviceConfigProperty):
        volumeSpecification: typing.Union[aws_cdk.cdk.Token, "CfnCluster.VolumeSpecificationProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.EbsConfigurationProperty")
    class EbsConfigurationProperty(jsii.compat.TypedDict, total=False):
        ebsBlockDeviceConfigs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCluster.EbsBlockDeviceConfigProperty"]]]
        ebsOptimized: typing.Union[bool, aws_cdk.cdk.Token]

    class _HadoopJarStepConfigProperty(jsii.compat.TypedDict, total=False):
        args: typing.List[str]
        mainClass: str
        stepProperties: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCluster.KeyValueProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.HadoopJarStepConfigProperty")
    class HadoopJarStepConfigProperty(_HadoopJarStepConfigProperty):
        jar: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.InstanceFleetConfigProperty")
    class InstanceFleetConfigProperty(jsii.compat.TypedDict, total=False):
        instanceTypeConfigs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCluster.InstanceTypeConfigProperty"]]]
        launchSpecifications: typing.Union[aws_cdk.cdk.Token, "CfnCluster.InstanceFleetProvisioningSpecificationsProperty"]
        name: str
        targetOnDemandCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        targetSpotCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.InstanceFleetProvisioningSpecificationsProperty")
    class InstanceFleetProvisioningSpecificationsProperty(jsii.compat.TypedDict):
        spotSpecification: typing.Union[aws_cdk.cdk.Token, "CfnCluster.SpotProvisioningSpecificationProperty"]

    class _InstanceGroupConfigProperty(jsii.compat.TypedDict, total=False):
        autoScalingPolicy: typing.Union[aws_cdk.cdk.Token, "CfnCluster.AutoScalingPolicyProperty"]
        bidPrice: str
        configurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCluster.ConfigurationProperty"]]]
        ebsConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnCluster.EbsConfigurationProperty"]
        market: str
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.InstanceGroupConfigProperty")
    class InstanceGroupConfigProperty(_InstanceGroupConfigProperty):
        instanceCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        instanceType: str

    class _InstanceTypeConfigProperty(jsii.compat.TypedDict, total=False):
        bidPrice: str
        bidPriceAsPercentageOfOnDemandPrice: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        configurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCluster.ConfigurationProperty"]]]
        ebsConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnCluster.EbsConfigurationProperty"]
        weightedCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.InstanceTypeConfigProperty")
    class InstanceTypeConfigProperty(_InstanceTypeConfigProperty):
        instanceType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.JobFlowInstancesConfigProperty")
    class JobFlowInstancesConfigProperty(jsii.compat.TypedDict, total=False):
        additionalMasterSecurityGroups: typing.List[str]
        additionalSlaveSecurityGroups: typing.List[str]
        coreInstanceFleet: typing.Union[aws_cdk.cdk.Token, "CfnCluster.InstanceFleetConfigProperty"]
        coreInstanceGroup: typing.Union[aws_cdk.cdk.Token, "CfnCluster.InstanceGroupConfigProperty"]
        ec2KeyName: str
        ec2SubnetId: str
        emrManagedMasterSecurityGroup: str
        emrManagedSlaveSecurityGroup: str
        hadoopVersion: str
        keepJobFlowAliveWhenNoSteps: typing.Union[bool, aws_cdk.cdk.Token]
        masterInstanceFleet: typing.Union[aws_cdk.cdk.Token, "CfnCluster.InstanceFleetConfigProperty"]
        masterInstanceGroup: typing.Union[aws_cdk.cdk.Token, "CfnCluster.InstanceGroupConfigProperty"]
        placement: typing.Union[aws_cdk.cdk.Token, "CfnCluster.PlacementTypeProperty"]
        serviceAccessSecurityGroup: str
        terminationProtected: typing.Union[bool, aws_cdk.cdk.Token]

    class _KerberosAttributesProperty(jsii.compat.TypedDict, total=False):
        adDomainJoinPassword: str
        adDomainJoinUser: str
        crossRealmTrustPrincipalPassword: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.KerberosAttributesProperty")
    class KerberosAttributesProperty(_KerberosAttributesProperty):
        kdcAdminPassword: str
        realm: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.KeyValueProperty")
    class KeyValueProperty(jsii.compat.TypedDict, total=False):
        key: str
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.MetricDimensionProperty")
    class MetricDimensionProperty(jsii.compat.TypedDict):
        key: str
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.PlacementTypeProperty")
    class PlacementTypeProperty(jsii.compat.TypedDict):
        availabilityZone: str

    class _ScalingActionProperty(jsii.compat.TypedDict, total=False):
        market: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.ScalingActionProperty")
    class ScalingActionProperty(_ScalingActionProperty):
        simpleScalingPolicyConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnCluster.SimpleScalingPolicyConfigurationProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.ScalingConstraintsProperty")
    class ScalingConstraintsProperty(jsii.compat.TypedDict):
        maxCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        minCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    class _ScalingRuleProperty(jsii.compat.TypedDict, total=False):
        description: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.ScalingRuleProperty")
    class ScalingRuleProperty(_ScalingRuleProperty):
        action: typing.Union[aws_cdk.cdk.Token, "CfnCluster.ScalingActionProperty"]
        name: str
        trigger: typing.Union[aws_cdk.cdk.Token, "CfnCluster.ScalingTriggerProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.ScalingTriggerProperty")
    class ScalingTriggerProperty(jsii.compat.TypedDict):
        cloudWatchAlarmDefinition: typing.Union[aws_cdk.cdk.Token, "CfnCluster.CloudWatchAlarmDefinitionProperty"]

    class _ScriptBootstrapActionConfigProperty(jsii.compat.TypedDict, total=False):
        args: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.ScriptBootstrapActionConfigProperty")
    class ScriptBootstrapActionConfigProperty(_ScriptBootstrapActionConfigProperty):
        path: str

    class _SimpleScalingPolicyConfigurationProperty(jsii.compat.TypedDict, total=False):
        adjustmentType: str
        coolDown: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.SimpleScalingPolicyConfigurationProperty")
    class SimpleScalingPolicyConfigurationProperty(_SimpleScalingPolicyConfigurationProperty):
        scalingAdjustment: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    class _SpotProvisioningSpecificationProperty(jsii.compat.TypedDict, total=False):
        blockDurationMinutes: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.SpotProvisioningSpecificationProperty")
    class SpotProvisioningSpecificationProperty(_SpotProvisioningSpecificationProperty):
        timeoutAction: str
        timeoutDurationMinutes: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    class _StepConfigProperty(jsii.compat.TypedDict, total=False):
        actionOnFailure: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.StepConfigProperty")
    class StepConfigProperty(_StepConfigProperty):
        hadoopJarStep: typing.Union[aws_cdk.cdk.Token, "CfnCluster.HadoopJarStepConfigProperty"]
        name: str

    class _VolumeSpecificationProperty(jsii.compat.TypedDict, total=False):
        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnCluster.VolumeSpecificationProperty")
    class VolumeSpecificationProperty(_VolumeSpecificationProperty):
        sizeInGb: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        volumeType: str


class _CfnClusterProps(jsii.compat.TypedDict, total=False):
    additionalInfo: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    applications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCluster.ApplicationProperty"]]]
    autoScalingRole: str
    bootstrapActions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCluster.BootstrapActionConfigProperty"]]]
    configurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCluster.ConfigurationProperty"]]]
    customAmiId: str
    ebsRootVolumeSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    kerberosAttributes: typing.Union[aws_cdk.cdk.Token, "CfnCluster.KerberosAttributesProperty"]
    logUri: str
    releaseLabel: str
    scaleDownBehavior: str
    securityConfiguration: str
    steps: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCluster.StepConfigProperty"]]]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    visibleToAllUsers: typing.Union[bool, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnClusterProps")
class CfnClusterProps(_CfnClusterProps):
    instances: typing.Union["CfnCluster.JobFlowInstancesConfigProperty", aws_cdk.cdk.Token]
    jobFlowRole: str
    name: str
    serviceRole: str

class CfnInstanceFleetConfig(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-emr.CfnInstanceFleetConfig"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cluster_id: str, instance_fleet_type: str, instance_type_configs: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "InstanceTypeConfigProperty"]]]]=None, launch_specifications: typing.Optional[typing.Union[aws_cdk.cdk.Token, "InstanceFleetProvisioningSpecificationsProperty"]]=None, name: typing.Optional[str]=None, target_on_demand_capacity: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, target_spot_capacity: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnInstanceFleetConfigProps = {"clusterId": cluster_id, "instanceFleetType": instance_fleet_type}

        if instance_type_configs is not None:
            props["instanceTypeConfigs"] = instance_type_configs

        if launch_specifications is not None:
            props["launchSpecifications"] = launch_specifications

        if name is not None:
            props["name"] = name

        if target_on_demand_capacity is not None:
            props["targetOnDemandCapacity"] = target_on_demand_capacity

        if target_spot_capacity is not None:
            props["targetSpotCapacity"] = target_spot_capacity

        jsii.create(CfnInstanceFleetConfig, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="instanceFleetConfigId")
    def instance_fleet_config_id(self) -> str:
        return jsii.get(self, "instanceFleetConfigId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnInstanceFleetConfigProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceFleetConfig.ConfigurationProperty")
    class ConfigurationProperty(jsii.compat.TypedDict, total=False):
        classification: str
        configurationProperties: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        configurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstanceFleetConfig.ConfigurationProperty"]]]

    class _EbsBlockDeviceConfigProperty(jsii.compat.TypedDict, total=False):
        volumesPerInstance: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceFleetConfig.EbsBlockDeviceConfigProperty")
    class EbsBlockDeviceConfigProperty(_EbsBlockDeviceConfigProperty):
        volumeSpecification: typing.Union[aws_cdk.cdk.Token, "CfnInstanceFleetConfig.VolumeSpecificationProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceFleetConfig.EbsConfigurationProperty")
    class EbsConfigurationProperty(jsii.compat.TypedDict, total=False):
        ebsBlockDeviceConfigs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstanceFleetConfig.EbsBlockDeviceConfigProperty"]]]
        ebsOptimized: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceFleetConfig.InstanceFleetProvisioningSpecificationsProperty")
    class InstanceFleetProvisioningSpecificationsProperty(jsii.compat.TypedDict):
        spotSpecification: typing.Union[aws_cdk.cdk.Token, "CfnInstanceFleetConfig.SpotProvisioningSpecificationProperty"]

    class _InstanceTypeConfigProperty(jsii.compat.TypedDict, total=False):
        bidPrice: str
        bidPriceAsPercentageOfOnDemandPrice: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        configurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstanceFleetConfig.ConfigurationProperty"]]]
        ebsConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnInstanceFleetConfig.EbsConfigurationProperty"]
        weightedCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceFleetConfig.InstanceTypeConfigProperty")
    class InstanceTypeConfigProperty(_InstanceTypeConfigProperty):
        instanceType: str

    class _SpotProvisioningSpecificationProperty(jsii.compat.TypedDict, total=False):
        blockDurationMinutes: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceFleetConfig.SpotProvisioningSpecificationProperty")
    class SpotProvisioningSpecificationProperty(_SpotProvisioningSpecificationProperty):
        timeoutAction: str
        timeoutDurationMinutes: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    class _VolumeSpecificationProperty(jsii.compat.TypedDict, total=False):
        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceFleetConfig.VolumeSpecificationProperty")
    class VolumeSpecificationProperty(_VolumeSpecificationProperty):
        sizeInGb: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        volumeType: str


class _CfnInstanceFleetConfigProps(jsii.compat.TypedDict, total=False):
    instanceTypeConfigs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstanceFleetConfig.InstanceTypeConfigProperty"]]]
    launchSpecifications: typing.Union[aws_cdk.cdk.Token, "CfnInstanceFleetConfig.InstanceFleetProvisioningSpecificationsProperty"]
    name: str
    targetOnDemandCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    targetSpotCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceFleetConfigProps")
class CfnInstanceFleetConfigProps(_CfnInstanceFleetConfigProps):
    clusterId: str
    instanceFleetType: str

class CfnInstanceGroupConfig(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-emr.CfnInstanceGroupConfig"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, instance_count: typing.Union[jsii.Number, aws_cdk.cdk.Token], instance_role: str, instance_type: str, job_flow_id: str, auto_scaling_policy: typing.Optional[typing.Union[aws_cdk.cdk.Token, "AutoScalingPolicyProperty"]]=None, bid_price: typing.Optional[str]=None, configurations: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ConfigurationProperty"]]]]=None, ebs_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "EbsConfigurationProperty"]]=None, market: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
        props: CfnInstanceGroupConfigProps = {"instanceCount": instance_count, "instanceRole": instance_role, "instanceType": instance_type, "jobFlowId": job_flow_id}

        if auto_scaling_policy is not None:
            props["autoScalingPolicy"] = auto_scaling_policy

        if bid_price is not None:
            props["bidPrice"] = bid_price

        if configurations is not None:
            props["configurations"] = configurations

        if ebs_configuration is not None:
            props["ebsConfiguration"] = ebs_configuration

        if market is not None:
            props["market"] = market

        if name is not None:
            props["name"] = name

        jsii.create(CfnInstanceGroupConfig, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="instanceGroupConfigId")
    def instance_group_config_id(self) -> str:
        return jsii.get(self, "instanceGroupConfigId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnInstanceGroupConfigProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceGroupConfig.AutoScalingPolicyProperty")
    class AutoScalingPolicyProperty(jsii.compat.TypedDict):
        constraints: typing.Union[aws_cdk.cdk.Token, "CfnInstanceGroupConfig.ScalingConstraintsProperty"]
        rules: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstanceGroupConfig.ScalingRuleProperty"]]]

    class _CloudWatchAlarmDefinitionProperty(jsii.compat.TypedDict, total=False):
        dimensions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstanceGroupConfig.MetricDimensionProperty"]]]
        evaluationPeriods: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        namespace: str
        statistic: str
        unit: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceGroupConfig.CloudWatchAlarmDefinitionProperty")
    class CloudWatchAlarmDefinitionProperty(_CloudWatchAlarmDefinitionProperty):
        comparisonOperator: str
        metricName: str
        period: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        threshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceGroupConfig.ConfigurationProperty")
    class ConfigurationProperty(jsii.compat.TypedDict, total=False):
        classification: str
        configurationProperties: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        configurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstanceGroupConfig.ConfigurationProperty"]]]

    class _EbsBlockDeviceConfigProperty(jsii.compat.TypedDict, total=False):
        volumesPerInstance: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceGroupConfig.EbsBlockDeviceConfigProperty")
    class EbsBlockDeviceConfigProperty(_EbsBlockDeviceConfigProperty):
        volumeSpecification: typing.Union[aws_cdk.cdk.Token, "CfnInstanceGroupConfig.VolumeSpecificationProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceGroupConfig.EbsConfigurationProperty")
    class EbsConfigurationProperty(jsii.compat.TypedDict, total=False):
        ebsBlockDeviceConfigs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstanceGroupConfig.EbsBlockDeviceConfigProperty"]]]
        ebsOptimized: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceGroupConfig.MetricDimensionProperty")
    class MetricDimensionProperty(jsii.compat.TypedDict):
        key: str
        value: str

    class _ScalingActionProperty(jsii.compat.TypedDict, total=False):
        market: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceGroupConfig.ScalingActionProperty")
    class ScalingActionProperty(_ScalingActionProperty):
        simpleScalingPolicyConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnInstanceGroupConfig.SimpleScalingPolicyConfigurationProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceGroupConfig.ScalingConstraintsProperty")
    class ScalingConstraintsProperty(jsii.compat.TypedDict):
        maxCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        minCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    class _ScalingRuleProperty(jsii.compat.TypedDict, total=False):
        description: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceGroupConfig.ScalingRuleProperty")
    class ScalingRuleProperty(_ScalingRuleProperty):
        action: typing.Union[aws_cdk.cdk.Token, "CfnInstanceGroupConfig.ScalingActionProperty"]
        name: str
        trigger: typing.Union[aws_cdk.cdk.Token, "CfnInstanceGroupConfig.ScalingTriggerProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceGroupConfig.ScalingTriggerProperty")
    class ScalingTriggerProperty(jsii.compat.TypedDict):
        cloudWatchAlarmDefinition: typing.Union[aws_cdk.cdk.Token, "CfnInstanceGroupConfig.CloudWatchAlarmDefinitionProperty"]

    class _SimpleScalingPolicyConfigurationProperty(jsii.compat.TypedDict, total=False):
        adjustmentType: str
        coolDown: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceGroupConfig.SimpleScalingPolicyConfigurationProperty")
    class SimpleScalingPolicyConfigurationProperty(_SimpleScalingPolicyConfigurationProperty):
        scalingAdjustment: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    class _VolumeSpecificationProperty(jsii.compat.TypedDict, total=False):
        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceGroupConfig.VolumeSpecificationProperty")
    class VolumeSpecificationProperty(_VolumeSpecificationProperty):
        sizeInGb: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        volumeType: str


class _CfnInstanceGroupConfigProps(jsii.compat.TypedDict, total=False):
    autoScalingPolicy: typing.Union[aws_cdk.cdk.Token, "CfnInstanceGroupConfig.AutoScalingPolicyProperty"]
    bidPrice: str
    configurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstanceGroupConfig.ConfigurationProperty"]]]
    ebsConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnInstanceGroupConfig.EbsConfigurationProperty"]
    market: str
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnInstanceGroupConfigProps")
class CfnInstanceGroupConfigProps(_CfnInstanceGroupConfigProps):
    instanceCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    instanceRole: str
    instanceType: str
    jobFlowId: str

class CfnSecurityConfiguration(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-emr.CfnSecurityConfiguration"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, security_configuration: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], name: typing.Optional[str]=None) -> None:
        props: CfnSecurityConfigurationProps = {"securityConfiguration": security_configuration}

        if name is not None:
            props["name"] = name

        jsii.create(CfnSecurityConfiguration, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSecurityConfigurationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="securityConfigurationName")
    def security_configuration_name(self) -> str:
        return jsii.get(self, "securityConfigurationName")


class _CfnSecurityConfigurationProps(jsii.compat.TypedDict, total=False):
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnSecurityConfigurationProps")
class CfnSecurityConfigurationProps(_CfnSecurityConfigurationProps):
    securityConfiguration: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

class CfnStep(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-emr.CfnStep"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, action_on_failure: str, hadoop_jar_step: typing.Union[aws_cdk.cdk.Token, "HadoopJarStepConfigProperty"], job_flow_id: str, name: str) -> None:
        props: CfnStepProps = {"actionOnFailure": action_on_failure, "hadoopJarStep": hadoop_jar_step, "jobFlowId": job_flow_id, "name": name}

        jsii.create(CfnStep, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnStepProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="stepId")
    def step_id(self) -> str:
        return jsii.get(self, "stepId")

    class _HadoopJarStepConfigProperty(jsii.compat.TypedDict, total=False):
        args: typing.List[str]
        mainClass: str
        stepProperties: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnStep.KeyValueProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnStep.HadoopJarStepConfigProperty")
    class HadoopJarStepConfigProperty(_HadoopJarStepConfigProperty):
        jar: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnStep.KeyValueProperty")
    class KeyValueProperty(jsii.compat.TypedDict, total=False):
        key: str
        value: str


@jsii.data_type(jsii_type="@aws-cdk/aws-emr.CfnStepProps")
class CfnStepProps(jsii.compat.TypedDict):
    actionOnFailure: str
    hadoopJarStep: typing.Union[aws_cdk.cdk.Token, "CfnStep.HadoopJarStepConfigProperty"]
    jobFlowId: str
    name: str

__all__ = ["CfnCluster", "CfnClusterProps", "CfnInstanceFleetConfig", "CfnInstanceFleetConfigProps", "CfnInstanceGroupConfig", "CfnInstanceGroupConfigProps", "CfnSecurityConfiguration", "CfnSecurityConfigurationProps", "CfnStep", "CfnStepProps", "__jsii_assembly__"]

publication.publish()
