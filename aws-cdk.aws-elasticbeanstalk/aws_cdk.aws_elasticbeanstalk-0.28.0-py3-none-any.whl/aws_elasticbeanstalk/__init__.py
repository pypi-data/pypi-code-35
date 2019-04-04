import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-elasticbeanstalk", "0.28.0", __name__, "aws-elasticbeanstalk@0.28.0.jsii.tgz")
class CfnApplication(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: typing.Optional[str]=None, description: typing.Optional[str]=None, resource_lifecycle_config: typing.Optional[typing.Union["ApplicationResourceLifecycleConfigProperty", aws_cdk.cdk.Token]]=None) -> None:
        props: CfnApplicationProps = {}

        if application_name is not None:
            props["applicationName"] = application_name

        if description is not None:
            props["description"] = description

        if resource_lifecycle_config is not None:
            props["resourceLifecycleConfig"] = resource_lifecycle_config

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

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication.ApplicationResourceLifecycleConfigProperty")
    class ApplicationResourceLifecycleConfigProperty(jsii.compat.TypedDict, total=False):
        serviceRole: str
        versionLifecycleConfig: typing.Union[aws_cdk.cdk.Token, "CfnApplication.ApplicationVersionLifecycleConfigProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication.ApplicationVersionLifecycleConfigProperty")
    class ApplicationVersionLifecycleConfigProperty(jsii.compat.TypedDict, total=False):
        maxAgeRule: typing.Union[aws_cdk.cdk.Token, "CfnApplication.MaxAgeRuleProperty"]
        maxCountRule: typing.Union[aws_cdk.cdk.Token, "CfnApplication.MaxCountRuleProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication.MaxAgeRuleProperty")
    class MaxAgeRuleProperty(jsii.compat.TypedDict, total=False):
        deleteSourceFromS3: typing.Union[bool, aws_cdk.cdk.Token]
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        maxAgeInDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication.MaxCountRuleProperty")
    class MaxCountRuleProperty(jsii.compat.TypedDict, total=False):
        deleteSourceFromS3: typing.Union[bool, aws_cdk.cdk.Token]
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        maxCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplicationProps")
class CfnApplicationProps(jsii.compat.TypedDict, total=False):
    applicationName: str
    description: str
    resourceLifecycleConfig: typing.Union["CfnApplication.ApplicationResourceLifecycleConfigProperty", aws_cdk.cdk.Token]

class CfnApplicationVersion(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplicationVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, source_bundle: typing.Union[aws_cdk.cdk.Token, "SourceBundleProperty"], description: typing.Optional[str]=None) -> None:
        props: CfnApplicationVersionProps = {"applicationName": application_name, "sourceBundle": source_bundle}

        if description is not None:
            props["description"] = description

        jsii.create(CfnApplicationVersion, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="applicationVersionName")
    def application_version_name(self) -> str:
        return jsii.get(self, "applicationVersionName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationVersionProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplicationVersion.SourceBundleProperty")
    class SourceBundleProperty(jsii.compat.TypedDict):
        s3Bucket: str
        s3Key: str


class _CfnApplicationVersionProps(jsii.compat.TypedDict, total=False):
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplicationVersionProps")
class CfnApplicationVersionProps(_CfnApplicationVersionProps):
    applicationName: str
    sourceBundle: typing.Union[aws_cdk.cdk.Token, "CfnApplicationVersion.SourceBundleProperty"]

class CfnConfigurationTemplate(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnConfigurationTemplate"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, description: typing.Optional[str]=None, environment_id: typing.Optional[str]=None, option_settings: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ConfigurationOptionSettingProperty"]]]]=None, platform_arn: typing.Optional[str]=None, solution_stack_name: typing.Optional[str]=None, source_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "SourceConfigurationProperty"]]=None) -> None:
        props: CfnConfigurationTemplateProps = {"applicationName": application_name}

        if description is not None:
            props["description"] = description

        if environment_id is not None:
            props["environmentId"] = environment_id

        if option_settings is not None:
            props["optionSettings"] = option_settings

        if platform_arn is not None:
            props["platformArn"] = platform_arn

        if solution_stack_name is not None:
            props["solutionStackName"] = solution_stack_name

        if source_configuration is not None:
            props["sourceConfiguration"] = source_configuration

        jsii.create(CfnConfigurationTemplate, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="configurationTemplateName")
    def configuration_template_name(self) -> str:
        return jsii.get(self, "configurationTemplateName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigurationTemplateProps":
        return jsii.get(self, "propertyOverrides")

    class _ConfigurationOptionSettingProperty(jsii.compat.TypedDict, total=False):
        resourceName: str
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnConfigurationTemplate.ConfigurationOptionSettingProperty")
    class ConfigurationOptionSettingProperty(_ConfigurationOptionSettingProperty):
        namespace: str
        optionName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnConfigurationTemplate.SourceConfigurationProperty")
    class SourceConfigurationProperty(jsii.compat.TypedDict):
        applicationName: str
        templateName: str


class _CfnConfigurationTemplateProps(jsii.compat.TypedDict, total=False):
    description: str
    environmentId: str
    optionSettings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnConfigurationTemplate.ConfigurationOptionSettingProperty"]]]
    platformArn: str
    solutionStackName: str
    sourceConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationTemplate.SourceConfigurationProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnConfigurationTemplateProps")
class CfnConfigurationTemplateProps(_CfnConfigurationTemplateProps):
    applicationName: str

class CfnEnvironment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnEnvironment"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, cname_prefix: typing.Optional[str]=None, description: typing.Optional[str]=None, environment_name: typing.Optional[str]=None, option_settings: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "OptionSettingProperty"]]]]=None, platform_arn: typing.Optional[str]=None, solution_stack_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, template_name: typing.Optional[str]=None, tier: typing.Optional[typing.Union[aws_cdk.cdk.Token, "TierProperty"]]=None, version_label: typing.Optional[str]=None) -> None:
        props: CfnEnvironmentProps = {"applicationName": application_name}

        if cname_prefix is not None:
            props["cnamePrefix"] = cname_prefix

        if description is not None:
            props["description"] = description

        if environment_name is not None:
            props["environmentName"] = environment_name

        if option_settings is not None:
            props["optionSettings"] = option_settings

        if platform_arn is not None:
            props["platformArn"] = platform_arn

        if solution_stack_name is not None:
            props["solutionStackName"] = solution_stack_name

        if tags is not None:
            props["tags"] = tags

        if template_name is not None:
            props["templateName"] = template_name

        if tier is not None:
            props["tier"] = tier

        if version_label is not None:
            props["versionLabel"] = version_label

        jsii.create(CfnEnvironment, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="environmentEndpointUrl")
    def environment_endpoint_url(self) -> str:
        return jsii.get(self, "environmentEndpointUrl")

    @property
    @jsii.member(jsii_name="environmentName")
    def environment_name(self) -> str:
        return jsii.get(self, "environmentName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEnvironmentProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    class _OptionSettingProperty(jsii.compat.TypedDict, total=False):
        resourceName: str
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnEnvironment.OptionSettingProperty")
    class OptionSettingProperty(_OptionSettingProperty):
        namespace: str
        optionName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnEnvironment.TierProperty")
    class TierProperty(jsii.compat.TypedDict, total=False):
        name: str
        type: str
        version: str


class _CfnEnvironmentProps(jsii.compat.TypedDict, total=False):
    cnamePrefix: str
    description: str
    environmentName: str
    optionSettings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnEnvironment.OptionSettingProperty"]]]
    platformArn: str
    solutionStackName: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    templateName: str
    tier: typing.Union[aws_cdk.cdk.Token, "CfnEnvironment.TierProperty"]
    versionLabel: str

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnEnvironmentProps")
class CfnEnvironmentProps(_CfnEnvironmentProps):
    applicationName: str

__all__ = ["CfnApplication", "CfnApplicationProps", "CfnApplicationVersion", "CfnApplicationVersionProps", "CfnConfigurationTemplate", "CfnConfigurationTemplateProps", "CfnEnvironment", "CfnEnvironmentProps", "__jsii_assembly__"]

publication.publish()
