import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.aws_sns
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-ses", "0.28.0", __name__, "aws-ses@0.28.0.jsii.tgz")
class CfnConfigurationSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.CfnConfigurationSet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: typing.Optional[str]=None) -> None:
        props: CfnConfigurationSetProps = {}

        if name is not None:
            props["name"] = name

        jsii.create(CfnConfigurationSet, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="configurationSetName")
    def configuration_set_name(self) -> str:
        return jsii.get(self, "configurationSetName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigurationSetProps":
        return jsii.get(self, "propertyOverrides")


class CfnConfigurationSetEventDestination(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestination"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, configuration_set_name: str, event_destination: typing.Union["EventDestinationProperty", aws_cdk.cdk.Token]) -> None:
        props: CfnConfigurationSetEventDestinationProps = {"configurationSetName": configuration_set_name, "eventDestination": event_destination}

        jsii.create(CfnConfigurationSetEventDestination, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigurationSetEventDestinationProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestination.CloudWatchDestinationProperty")
    class CloudWatchDestinationProperty(jsii.compat.TypedDict, total=False):
        dimensionConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnConfigurationSetEventDestination.DimensionConfigurationProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestination.DimensionConfigurationProperty")
    class DimensionConfigurationProperty(jsii.compat.TypedDict):
        defaultDimensionValue: str
        dimensionName: str
        dimensionValueSource: str

    class _EventDestinationProperty(jsii.compat.TypedDict, total=False):
        cloudWatchDestination: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationSetEventDestination.CloudWatchDestinationProperty"]
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        kinesisFirehoseDestination: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty"]
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestination.EventDestinationProperty")
    class EventDestinationProperty(_EventDestinationProperty):
        matchingEventTypes: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty")
    class KinesisFirehoseDestinationProperty(jsii.compat.TypedDict):
        deliveryStreamArn: str
        iamRoleArn: str


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestinationProps")
class CfnConfigurationSetEventDestinationProps(jsii.compat.TypedDict):
    configurationSetName: str
    eventDestination: typing.Union["CfnConfigurationSetEventDestination.EventDestinationProperty", aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetProps")
class CfnConfigurationSetProps(jsii.compat.TypedDict, total=False):
    name: str

class CfnReceiptFilter(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.CfnReceiptFilter"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, filter: typing.Union[aws_cdk.cdk.Token, "FilterProperty"]) -> None:
        props: CfnReceiptFilterProps = {"filter": filter}

        jsii.create(CfnReceiptFilter, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnReceiptFilterProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="receiptFilterName")
    def receipt_filter_name(self) -> str:
        return jsii.get(self, "receiptFilterName")

    class _FilterProperty(jsii.compat.TypedDict, total=False):
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptFilter.FilterProperty")
    class FilterProperty(_FilterProperty):
        ipFilter: typing.Union[aws_cdk.cdk.Token, "CfnReceiptFilter.IpFilterProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptFilter.IpFilterProperty")
    class IpFilterProperty(jsii.compat.TypedDict):
        cidr: str
        policy: str


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptFilterProps")
class CfnReceiptFilterProps(jsii.compat.TypedDict):
    filter: typing.Union[aws_cdk.cdk.Token, "CfnReceiptFilter.FilterProperty"]

class CfnReceiptRule(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.CfnReceiptRule"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, rule: typing.Union[aws_cdk.cdk.Token, "RuleProperty"], rule_set_name: str, after: typing.Optional[str]=None) -> None:
        props: CfnReceiptRuleProps = {"rule": rule, "ruleSetName": rule_set_name}

        if after is not None:
            props["after"] = after

        jsii.create(CfnReceiptRule, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnReceiptRuleProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="receiptRuleName")
    def receipt_rule_name(self) -> str:
        return jsii.get(self, "receiptRuleName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.ActionProperty")
    class ActionProperty(jsii.compat.TypedDict, total=False):
        addHeaderAction: typing.Union["CfnReceiptRule.AddHeaderActionProperty", aws_cdk.cdk.Token]
        bounceAction: typing.Union["CfnReceiptRule.BounceActionProperty", aws_cdk.cdk.Token]
        lambdaAction: typing.Union["CfnReceiptRule.LambdaActionProperty", aws_cdk.cdk.Token]
        s3Action: typing.Union["CfnReceiptRule.S3ActionProperty", aws_cdk.cdk.Token]
        snsAction: typing.Union["CfnReceiptRule.SNSActionProperty", aws_cdk.cdk.Token]
        stopAction: typing.Union["CfnReceiptRule.StopActionProperty", aws_cdk.cdk.Token]
        workmailAction: typing.Union["CfnReceiptRule.WorkmailActionProperty", aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.AddHeaderActionProperty")
    class AddHeaderActionProperty(jsii.compat.TypedDict):
        headerName: str
        headerValue: str

    class _BounceActionProperty(jsii.compat.TypedDict, total=False):
        statusCode: str
        topicArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.BounceActionProperty")
    class BounceActionProperty(_BounceActionProperty):
        message: str
        sender: str
        smtpReplyCode: str

    class _LambdaActionProperty(jsii.compat.TypedDict, total=False):
        invocationType: str
        topicArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.LambdaActionProperty")
    class LambdaActionProperty(_LambdaActionProperty):
        functionArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.RuleProperty")
    class RuleProperty(jsii.compat.TypedDict, total=False):
        actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnReceiptRule.ActionProperty"]]]
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        name: str
        recipients: typing.List[str]
        scanEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        tlsPolicy: str

    class _S3ActionProperty(jsii.compat.TypedDict, total=False):
        kmsKeyArn: str
        objectKeyPrefix: str
        topicArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.S3ActionProperty")
    class S3ActionProperty(_S3ActionProperty):
        bucketName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.SNSActionProperty")
    class SNSActionProperty(jsii.compat.TypedDict, total=False):
        encoding: str
        topicArn: str

    class _StopActionProperty(jsii.compat.TypedDict, total=False):
        topicArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.StopActionProperty")
    class StopActionProperty(_StopActionProperty):
        scope: str

    class _WorkmailActionProperty(jsii.compat.TypedDict, total=False):
        topicArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.WorkmailActionProperty")
    class WorkmailActionProperty(_WorkmailActionProperty):
        organizationArn: str


class _CfnReceiptRuleProps(jsii.compat.TypedDict, total=False):
    after: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRuleProps")
class CfnReceiptRuleProps(_CfnReceiptRuleProps):
    rule: typing.Union[aws_cdk.cdk.Token, "CfnReceiptRule.RuleProperty"]
    ruleSetName: str

class CfnReceiptRuleSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.CfnReceiptRuleSet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, rule_set_name: typing.Optional[str]=None) -> None:
        props: CfnReceiptRuleSetProps = {}

        if rule_set_name is not None:
            props["ruleSetName"] = rule_set_name

        jsii.create(CfnReceiptRuleSet, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnReceiptRuleSetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="receiptRuleSetName")
    def receipt_rule_set_name(self) -> str:
        return jsii.get(self, "receiptRuleSetName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRuleSetProps")
class CfnReceiptRuleSetProps(jsii.compat.TypedDict, total=False):
    ruleSetName: str

class CfnTemplate(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.CfnTemplate"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, template: typing.Optional[typing.Union[aws_cdk.cdk.Token, "TemplateProperty"]]=None) -> None:
        props: CfnTemplateProps = {}

        if template is not None:
            props["template"] = template

        jsii.create(CfnTemplate, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTemplateProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="templateId")
    def template_id(self) -> str:
        return jsii.get(self, "templateId")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnTemplate.TemplateProperty")
    class TemplateProperty(jsii.compat.TypedDict, total=False):
        htmlPart: str
        subjectPart: str
        templateName: str
        textPart: str


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnTemplateProps")
class CfnTemplateProps(jsii.compat.TypedDict, total=False):
    template: typing.Union[aws_cdk.cdk.Token, "CfnTemplate.TemplateProperty"]

class DropSpamReceiptRule(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.DropSpamReceiptRule"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, rule_set: "IReceiptRuleSet", actions: typing.Optional[typing.List["IReceiptRuleAction"]]=None, after: typing.Optional["IReceiptRule"]=None, enabled: typing.Optional[bool]=None, name: typing.Optional[str]=None, recipients: typing.Optional[typing.List[str]]=None, scan_enabled: typing.Optional[bool]=None, tls_policy: typing.Optional["TlsPolicy"]=None) -> None:
        props: ReceiptRuleProps = {"ruleSet": rule_set}

        if actions is not None:
            props["actions"] = actions

        if after is not None:
            props["after"] = after

        if enabled is not None:
            props["enabled"] = enabled

        if name is not None:
            props["name"] = name

        if recipients is not None:
            props["recipients"] = recipients

        if scan_enabled is not None:
            props["scanEnabled"] = scan_enabled

        if tls_policy is not None:
            props["tlsPolicy"] = tls_policy

        jsii.create(DropSpamReceiptRule, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "ReceiptRule":
        return jsii.get(self, "rule")


@jsii.enum(jsii_type="@aws-cdk/aws-ses.EmailEncoding")
class EmailEncoding(enum.Enum):
    Base64 = "Base64"
    UTF8 = "UTF8"

@jsii.interface(jsii_type="@aws-cdk/aws-ses.IReceiptRule")
class IReceiptRule(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IReceiptRuleProxy

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "ReceiptRuleImportProps":
        ...


class _IReceiptRuleProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-ses.IReceiptRule"
    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @jsii.member(jsii_name="export")
    def export(self) -> "ReceiptRuleImportProps":
        return jsii.invoke(self, "export", [])


@jsii.interface(jsii_type="@aws-cdk/aws-ses.IReceiptRuleAction")
class IReceiptRuleAction(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IReceiptRuleActionProxy

    @jsii.member(jsii_name="render")
    def render(self) -> "ReceiptRuleActionProps":
        ...


class _IReceiptRuleActionProxy():
    __jsii_type__ = "@aws-cdk/aws-ses.IReceiptRuleAction"
    @jsii.member(jsii_name="render")
    def render(self) -> "ReceiptRuleActionProps":
        return jsii.invoke(self, "render", [])


@jsii.interface(jsii_type="@aws-cdk/aws-ses.IReceiptRuleSet")
class IReceiptRuleSet(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IReceiptRuleSetProxy

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        ...

    @jsii.member(jsii_name="addRule")
    def add_rule(self, id: str, *, actions: typing.Optional[typing.List["IReceiptRuleAction"]]=None, after: typing.Optional["IReceiptRule"]=None, enabled: typing.Optional[bool]=None, name: typing.Optional[str]=None, recipients: typing.Optional[typing.List[str]]=None, scan_enabled: typing.Optional[bool]=None, tls_policy: typing.Optional["TlsPolicy"]=None) -> "ReceiptRule":
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "ReceiptRuleSetImportProps":
        ...


class _IReceiptRuleSetProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-ses.IReceiptRuleSet"
    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @jsii.member(jsii_name="addRule")
    def add_rule(self, id: str, *, actions: typing.Optional[typing.List["IReceiptRuleAction"]]=None, after: typing.Optional["IReceiptRule"]=None, enabled: typing.Optional[bool]=None, name: typing.Optional[str]=None, recipients: typing.Optional[typing.List[str]]=None, scan_enabled: typing.Optional[bool]=None, tls_policy: typing.Optional["TlsPolicy"]=None) -> "ReceiptRule":
        options: ReceiptRuleOptions = {}

        if actions is not None:
            options["actions"] = actions

        if after is not None:
            options["after"] = after

        if enabled is not None:
            options["enabled"] = enabled

        if name is not None:
            options["name"] = name

        if recipients is not None:
            options["recipients"] = recipients

        if scan_enabled is not None:
            options["scanEnabled"] = scan_enabled

        if tls_policy is not None:
            options["tlsPolicy"] = tls_policy

        return jsii.invoke(self, "addRule", [id, options])

    @jsii.member(jsii_name="export")
    def export(self) -> "ReceiptRuleSetImportProps":
        return jsii.invoke(self, "export", [])


@jsii.enum(jsii_type="@aws-cdk/aws-ses.LambdaInvocationType")
class LambdaInvocationType(enum.Enum):
    Event = "Event"
    RequestResponse = "RequestResponse"

class ReceiptFilter(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptFilter"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, ip: typing.Optional[str]=None, name: typing.Optional[str]=None, policy: typing.Optional["ReceiptFilterPolicy"]=None) -> None:
        props: ReceiptFilterProps = {}

        if ip is not None:
            props["ip"] = ip

        if name is not None:
            props["name"] = name

        if policy is not None:
            props["policy"] = policy

        jsii.create(ReceiptFilter, self, [scope, id, props])


@jsii.enum(jsii_type="@aws-cdk/aws-ses.ReceiptFilterPolicy")
class ReceiptFilterPolicy(enum.Enum):
    Allow = "Allow"
    Block = "Block"

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptFilterProps")
class ReceiptFilterProps(jsii.compat.TypedDict, total=False):
    ip: str
    name: str
    policy: "ReceiptFilterPolicy"

@jsii.implements(IReceiptRule)
class ReceiptRule(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRule"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, rule_set: "IReceiptRuleSet", actions: typing.Optional[typing.List["IReceiptRuleAction"]]=None, after: typing.Optional["IReceiptRule"]=None, enabled: typing.Optional[bool]=None, name: typing.Optional[str]=None, recipients: typing.Optional[typing.List[str]]=None, scan_enabled: typing.Optional[bool]=None, tls_policy: typing.Optional["TlsPolicy"]=None) -> None:
        props: ReceiptRuleProps = {"ruleSet": rule_set}

        if actions is not None:
            props["actions"] = actions

        if after is not None:
            props["after"] = after

        if enabled is not None:
            props["enabled"] = enabled

        if name is not None:
            props["name"] = name

        if recipients is not None:
            props["recipients"] = recipients

        if scan_enabled is not None:
            props["scanEnabled"] = scan_enabled

        if tls_policy is not None:
            props["tlsPolicy"] = tls_policy

        jsii.create(ReceiptRule, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, name: str) -> "IReceiptRule":
        props: ReceiptRuleImportProps = {"name": name}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addAction")
    def add_action(self, action: "IReceiptRuleAction") -> None:
        return jsii.invoke(self, "addAction", [action])

    @jsii.member(jsii_name="export")
    def export(self) -> "ReceiptRuleImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleActionProps")
class ReceiptRuleActionProps(jsii.compat.TypedDict, total=False):
    addHeaderAction: "CfnReceiptRule.AddHeaderActionProperty"
    bounceAction: "CfnReceiptRule.BounceActionProperty"
    lambdaAction: "CfnReceiptRule.LambdaActionProperty"
    s3Action: "CfnReceiptRule.S3ActionProperty"
    snsAction: "CfnReceiptRule.SNSActionProperty"
    stopAction: "CfnReceiptRule.StopActionProperty"
    workmailAction: "CfnReceiptRule.WorkmailActionProperty"

@jsii.implements(IReceiptRuleAction)
class ReceiptRuleAddHeaderAction(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRuleAddHeaderAction"):
    def __init__(self, *, name: str, value: str) -> None:
        props: ReceiptRuleAddHeaderActionProps = {"name": name, "value": value}

        jsii.create(ReceiptRuleAddHeaderAction, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> "ReceiptRuleActionProps":
        return jsii.invoke(self, "render", [])


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleAddHeaderActionProps")
class ReceiptRuleAddHeaderActionProps(jsii.compat.TypedDict):
    name: str
    value: str

@jsii.implements(IReceiptRuleAction)
class ReceiptRuleBounceAction(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRuleBounceAction"):
    def __init__(self, *, sender: str, template: "ReceiptRuleBounceActionTemplate", topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None) -> None:
        props: ReceiptRuleBounceActionProps = {"sender": sender, "template": template}

        if topic is not None:
            props["topic"] = topic

        jsii.create(ReceiptRuleBounceAction, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> "ReceiptRuleActionProps":
        return jsii.invoke(self, "render", [])

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "ReceiptRuleBounceActionProps":
        return jsii.get(self, "props")


class _ReceiptRuleBounceActionProps(jsii.compat.TypedDict, total=False):
    topic: aws_cdk.aws_sns.ITopic

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleBounceActionProps")
class ReceiptRuleBounceActionProps(_ReceiptRuleBounceActionProps):
    sender: str
    template: "ReceiptRuleBounceActionTemplate"

class ReceiptRuleBounceActionTemplate(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRuleBounceActionTemplate"):
    def __init__(self, *, message: str, smtp_reply_code: str, status_code: typing.Optional[str]=None) -> None:
        props: ReceiptRuleBounceActionTemplateProps = {"message": message, "smtpReplyCode": smtp_reply_code}

        if status_code is not None:
            props["statusCode"] = status_code

        jsii.create(ReceiptRuleBounceActionTemplate, self, [props])

    @classproperty
    @jsii.member(jsii_name="MailboxDoesNotExist")
    def MAILBOX_DOES_NOT_EXIST(cls) -> "ReceiptRuleBounceActionTemplate":
        return jsii.sget(cls, "MailboxDoesNotExist")

    @classproperty
    @jsii.member(jsii_name="MailboxFull")
    def MAILBOX_FULL(cls) -> "ReceiptRuleBounceActionTemplate":
        return jsii.sget(cls, "MailboxFull")

    @classproperty
    @jsii.member(jsii_name="MessageContentRejected")
    def MESSAGE_CONTENT_REJECTED(cls) -> "ReceiptRuleBounceActionTemplate":
        return jsii.sget(cls, "MessageContentRejected")

    @classproperty
    @jsii.member(jsii_name="MessageTooLarge")
    def MESSAGE_TOO_LARGE(cls) -> "ReceiptRuleBounceActionTemplate":
        return jsii.sget(cls, "MessageTooLarge")

    @classproperty
    @jsii.member(jsii_name="TemporaryFailure")
    def TEMPORARY_FAILURE(cls) -> "ReceiptRuleBounceActionTemplate":
        return jsii.sget(cls, "TemporaryFailure")

    @property
    @jsii.member(jsii_name="message")
    def message(self) -> str:
        return jsii.get(self, "message")

    @property
    @jsii.member(jsii_name="smtpReplyCode")
    def smtp_reply_code(self) -> str:
        return jsii.get(self, "smtpReplyCode")

    @property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> typing.Optional[str]:
        return jsii.get(self, "statusCode")


class _ReceiptRuleBounceActionTemplateProps(jsii.compat.TypedDict, total=False):
    statusCode: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleBounceActionTemplateProps")
class ReceiptRuleBounceActionTemplateProps(_ReceiptRuleBounceActionTemplateProps):
    message: str
    smtpReplyCode: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleImportProps")
class ReceiptRuleImportProps(jsii.compat.TypedDict):
    name: str

@jsii.implements(IReceiptRuleAction)
class ReceiptRuleLambdaAction(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRuleLambdaAction"):
    def __init__(self, *, function: aws_cdk.aws_lambda.IFunction, invocation_type: typing.Optional["LambdaInvocationType"]=None, topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None) -> None:
        props: ReceiptRuleLambdaActionProps = {"function": function}

        if invocation_type is not None:
            props["invocationType"] = invocation_type

        if topic is not None:
            props["topic"] = topic

        jsii.create(ReceiptRuleLambdaAction, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> "ReceiptRuleActionProps":
        return jsii.invoke(self, "render", [])

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "ReceiptRuleLambdaActionProps":
        return jsii.get(self, "props")


class _ReceiptRuleLambdaActionProps(jsii.compat.TypedDict, total=False):
    invocationType: "LambdaInvocationType"
    topic: aws_cdk.aws_sns.ITopic

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleLambdaActionProps")
class ReceiptRuleLambdaActionProps(_ReceiptRuleLambdaActionProps):
    function: aws_cdk.aws_lambda.IFunction

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleOptions")
class ReceiptRuleOptions(jsii.compat.TypedDict, total=False):
    actions: typing.List["IReceiptRuleAction"]
    after: "IReceiptRule"
    enabled: bool
    name: str
    recipients: typing.List[str]
    scanEnabled: bool
    tlsPolicy: "TlsPolicy"

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleProps")
class ReceiptRuleProps(ReceiptRuleOptions, jsii.compat.TypedDict):
    ruleSet: "IReceiptRuleSet"

@jsii.implements(IReceiptRuleAction)
class ReceiptRuleS3Action(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRuleS3Action"):
    def __init__(self, *, bucket: aws_cdk.aws_s3.IBucket, kms_key: typing.Optional[aws_cdk.aws_kms.IEncryptionKey]=None, object_key_prefix: typing.Optional[str]=None, topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None) -> None:
        props: ReceiptRuleS3ActionProps = {"bucket": bucket}

        if kms_key is not None:
            props["kmsKey"] = kms_key

        if object_key_prefix is not None:
            props["objectKeyPrefix"] = object_key_prefix

        if topic is not None:
            props["topic"] = topic

        jsii.create(ReceiptRuleS3Action, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> "ReceiptRuleActionProps":
        return jsii.invoke(self, "render", [])

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "ReceiptRuleS3ActionProps":
        return jsii.get(self, "props")


class _ReceiptRuleS3ActionProps(jsii.compat.TypedDict, total=False):
    kmsKey: aws_cdk.aws_kms.IEncryptionKey
    objectKeyPrefix: str
    topic: aws_cdk.aws_sns.ITopic

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleS3ActionProps")
class ReceiptRuleS3ActionProps(_ReceiptRuleS3ActionProps):
    bucket: aws_cdk.aws_s3.IBucket

@jsii.implements(IReceiptRuleSet)
class ReceiptRuleSetBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ses.ReceiptRuleSetBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _ReceiptRuleSetBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(ReceiptRuleSetBase, self, [scope, id])

    @jsii.member(jsii_name="addDropSpamRule")
    def _add_drop_spam_rule(self) -> None:
        return jsii.invoke(self, "addDropSpamRule", [])

    @jsii.member(jsii_name="addRule")
    def add_rule(self, id: str, *, actions: typing.Optional[typing.List["IReceiptRuleAction"]]=None, after: typing.Optional["IReceiptRule"]=None, enabled: typing.Optional[bool]=None, name: typing.Optional[str]=None, recipients: typing.Optional[typing.List[str]]=None, scan_enabled: typing.Optional[bool]=None, tls_policy: typing.Optional["TlsPolicy"]=None) -> "ReceiptRule":
        options: ReceiptRuleOptions = {}

        if actions is not None:
            options["actions"] = actions

        if after is not None:
            options["after"] = after

        if enabled is not None:
            options["enabled"] = enabled

        if name is not None:
            options["name"] = name

        if recipients is not None:
            options["recipients"] = recipients

        if scan_enabled is not None:
            options["scanEnabled"] = scan_enabled

        if tls_policy is not None:
            options["tlsPolicy"] = tls_policy

        return jsii.invoke(self, "addRule", [id, options])

    @jsii.member(jsii_name="export")
    @abc.abstractmethod
    def export(self) -> "ReceiptRuleSetImportProps":
        ...

    @property
    @jsii.member(jsii_name="name")
    @abc.abstractmethod
    def name(self) -> str:
        ...


class _ReceiptRuleSetBaseProxy(ReceiptRuleSetBase):
    @jsii.member(jsii_name="export")
    def export(self) -> "ReceiptRuleSetImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")


@jsii.implements(IReceiptRuleSet)
class ReceiptRuleSet(ReceiptRuleSetBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRuleSet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, drop_spam: typing.Optional[bool]=None, name: typing.Optional[str]=None, rules: typing.Optional[typing.List["ReceiptRuleOptions"]]=None) -> None:
        props: ReceiptRuleSetProps = {}

        if drop_spam is not None:
            props["dropSpam"] = drop_spam

        if name is not None:
            props["name"] = name

        if rules is not None:
            props["rules"] = rules

        jsii.create(ReceiptRuleSet, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, name: str) -> "IReceiptRuleSet":
        props: ReceiptRuleSetImportProps = {"name": name}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "ReceiptRuleSetImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleSetImportProps")
class ReceiptRuleSetImportProps(jsii.compat.TypedDict):
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleSetProps")
class ReceiptRuleSetProps(jsii.compat.TypedDict, total=False):
    dropSpam: bool
    name: str
    rules: typing.List["ReceiptRuleOptions"]

@jsii.implements(IReceiptRuleAction)
class ReceiptRuleSnsAction(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRuleSnsAction"):
    def __init__(self, *, topic: aws_cdk.aws_sns.ITopic, encoding: typing.Optional["EmailEncoding"]=None) -> None:
        props: ReceiptRuleSnsActionProps = {"topic": topic}

        if encoding is not None:
            props["encoding"] = encoding

        jsii.create(ReceiptRuleSnsAction, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> "ReceiptRuleActionProps":
        return jsii.invoke(self, "render", [])

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "ReceiptRuleSnsActionProps":
        return jsii.get(self, "props")


class _ReceiptRuleSnsActionProps(jsii.compat.TypedDict, total=False):
    encoding: "EmailEncoding"

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleSnsActionProps")
class ReceiptRuleSnsActionProps(_ReceiptRuleSnsActionProps):
    topic: aws_cdk.aws_sns.ITopic

@jsii.implements(IReceiptRuleAction)
class ReceiptRuleStopAction(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRuleStopAction"):
    def __init__(self, *, topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None) -> None:
        props: ReceiptRuleStopActionProps = {}

        if topic is not None:
            props["topic"] = topic

        jsii.create(ReceiptRuleStopAction, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> "ReceiptRuleActionProps":
        return jsii.invoke(self, "render", [])

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> typing.Optional["ReceiptRuleStopActionProps"]:
        return jsii.get(self, "props")


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleStopActionProps")
class ReceiptRuleStopActionProps(jsii.compat.TypedDict, total=False):
    topic: aws_cdk.aws_sns.ITopic

@jsii.enum(jsii_type="@aws-cdk/aws-ses.TlsPolicy")
class TlsPolicy(enum.Enum):
    Optional = "Optional"
    Require = "Require"

class WhiteListReceiptFilter(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.WhiteListReceiptFilter"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, ips: typing.List[str]) -> None:
        props: WhiteListReceiptFilterProps = {"ips": ips}

        jsii.create(WhiteListReceiptFilter, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.WhiteListReceiptFilterProps")
class WhiteListReceiptFilterProps(jsii.compat.TypedDict):
    ips: typing.List[str]

__all__ = ["CfnConfigurationSet", "CfnConfigurationSetEventDestination", "CfnConfigurationSetEventDestinationProps", "CfnConfigurationSetProps", "CfnReceiptFilter", "CfnReceiptFilterProps", "CfnReceiptRule", "CfnReceiptRuleProps", "CfnReceiptRuleSet", "CfnReceiptRuleSetProps", "CfnTemplate", "CfnTemplateProps", "DropSpamReceiptRule", "EmailEncoding", "IReceiptRule", "IReceiptRuleAction", "IReceiptRuleSet", "LambdaInvocationType", "ReceiptFilter", "ReceiptFilterPolicy", "ReceiptFilterProps", "ReceiptRule", "ReceiptRuleActionProps", "ReceiptRuleAddHeaderAction", "ReceiptRuleAddHeaderActionProps", "ReceiptRuleBounceAction", "ReceiptRuleBounceActionProps", "ReceiptRuleBounceActionTemplate", "ReceiptRuleBounceActionTemplateProps", "ReceiptRuleImportProps", "ReceiptRuleLambdaAction", "ReceiptRuleLambdaActionProps", "ReceiptRuleOptions", "ReceiptRuleProps", "ReceiptRuleS3Action", "ReceiptRuleS3ActionProps", "ReceiptRuleSet", "ReceiptRuleSetBase", "ReceiptRuleSetImportProps", "ReceiptRuleSetProps", "ReceiptRuleSnsAction", "ReceiptRuleSnsActionProps", "ReceiptRuleStopAction", "ReceiptRuleStopActionProps", "TlsPolicy", "WhiteListReceiptFilter", "WhiteListReceiptFilterProps", "__jsii_assembly__"]

publication.publish()
