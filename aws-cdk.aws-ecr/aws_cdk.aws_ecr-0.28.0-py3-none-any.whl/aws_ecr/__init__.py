import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-ecr", "0.28.0", __name__, "aws-ecr@0.28.0.jsii.tgz")
class CfnRepository(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecr.CfnRepository"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, lifecycle_policy: typing.Optional[typing.Union["LifecyclePolicyProperty", aws_cdk.cdk.Token]]=None, repository_name: typing.Optional[str]=None, repository_policy_text: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None) -> None:
        props: CfnRepositoryProps = {}

        if lifecycle_policy is not None:
            props["lifecyclePolicy"] = lifecycle_policy

        if repository_name is not None:
            props["repositoryName"] = repository_name

        if repository_policy_text is not None:
            props["repositoryPolicyText"] = repository_policy_text

        jsii.create(CfnRepository, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRepositoryProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        return jsii.get(self, "repositoryArn")

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        return jsii.get(self, "repositoryName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecr.CfnRepository.LifecyclePolicyProperty")
    class LifecyclePolicyProperty(jsii.compat.TypedDict, total=False):
        lifecyclePolicyText: str
        registryId: str


@jsii.data_type(jsii_type="@aws-cdk/aws-ecr.CfnRepositoryProps")
class CfnRepositoryProps(jsii.compat.TypedDict, total=False):
    lifecyclePolicy: typing.Union["CfnRepository.LifecyclePolicyProperty", aws_cdk.cdk.Token]
    repositoryName: str
    repositoryPolicyText: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

@jsii.enum(jsii_type="@aws-cdk/aws-ecr.CountType")
class CountType(enum.Enum):
    ImageCountMoreThan = "ImageCountMoreThan"
    SinceImagePushed = "SinceImagePushed"

@jsii.interface(jsii_type="@aws-cdk/aws-ecr.IRepository")
class IRepository(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IRepositoryProxy

    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> str:
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "RepositoryImportProps":
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="onImagePushed")
    def on_image_pushed(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, image_tag: typing.Optional[str]=None) -> aws_cdk.aws_events.EventRule:
        ...

    @jsii.member(jsii_name="repositoryUriForTag")
    def repository_uri_for_tag(self, tag: typing.Optional[str]=None) -> str:
        ...


class _IRepositoryProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-ecr.IRepository"
    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        return jsii.get(self, "repositoryArn")

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        return jsii.get(self, "repositoryName")

    @property
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> str:
        return jsii.get(self, "repositoryUri")

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="export")
    def export(self) -> "RepositoryImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grant", [grantee, actions])

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantPull", [grantee])

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantPullPush", [grantee])

    @jsii.member(jsii_name="onImagePushed")
    def on_image_pushed(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, image_tag: typing.Optional[str]=None) -> aws_cdk.aws_events.EventRule:
        return jsii.invoke(self, "onImagePushed", [name, target, image_tag])

    @jsii.member(jsii_name="repositoryUriForTag")
    def repository_uri_for_tag(self, tag: typing.Optional[str]=None) -> str:
        return jsii.invoke(self, "repositoryUriForTag", [tag])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecr.LifecycleRule")
class LifecycleRule(jsii.compat.TypedDict, total=False):
    description: str
    maxImageAgeDays: jsii.Number
    maxImageCount: jsii.Number
    rulePriority: jsii.Number
    tagPrefixList: typing.List[str]
    tagStatus: "TagStatus"

@jsii.implements(IRepository)
class RepositoryBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecr.RepositoryBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _RepositoryBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(RepositoryBase, self, [scope, id])

    @jsii.member(jsii_name="arnForLocalRepository")
    @classmethod
    def arn_for_local_repository(cls, repository_name: str, scope: aws_cdk.cdk.IConstruct) -> str:
        return jsii.sinvoke(cls, "arnForLocalRepository", [repository_name, scope])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, repository_arn: typing.Optional[str]=None, repository_name: typing.Optional[str]=None) -> "IRepository":
        props: RepositoryImportProps = {}

        if repository_arn is not None:
            props["repositoryArn"] = repository_arn

        if repository_name is not None:
            props["repositoryName"] = repository_name

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addToResourcePolicy")
    @abc.abstractmethod
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        ...

    @jsii.member(jsii_name="export")
    @abc.abstractmethod
    def export(self) -> "RepositoryImportProps":
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grant", [grantee, actions])

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantPull", [grantee])

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantPullPush", [grantee])

    @jsii.member(jsii_name="onImagePushed")
    def on_image_pushed(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, image_tag: typing.Optional[str]=None) -> aws_cdk.aws_events.EventRule:
        return jsii.invoke(self, "onImagePushed", [name, target, image_tag])

    @jsii.member(jsii_name="repositoryUriForTag")
    def repository_uri_for_tag(self, tag: typing.Optional[str]=None) -> str:
        return jsii.invoke(self, "repositoryUriForTag", [tag])

    @property
    @jsii.member(jsii_name="repositoryArn")
    @abc.abstractmethod
    def repository_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="repositoryName")
    @abc.abstractmethod
    def repository_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> str:
        return jsii.get(self, "repositoryUri")


class _RepositoryBaseProxy(RepositoryBase):
    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="export")
    def export(self) -> "RepositoryImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        return jsii.get(self, "repositoryArn")

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        return jsii.get(self, "repositoryName")


class Repository(RepositoryBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecr.Repository"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, lifecycle_registry_id: typing.Optional[str]=None, lifecycle_rules: typing.Optional[typing.List["LifecycleRule"]]=None, repository_name: typing.Optional[str]=None, retain: typing.Optional[bool]=None) -> None:
        props: RepositoryProps = {}

        if lifecycle_registry_id is not None:
            props["lifecycleRegistryId"] = lifecycle_registry_id

        if lifecycle_rules is not None:
            props["lifecycleRules"] = lifecycle_rules

        if repository_name is not None:
            props["repositoryName"] = repository_name

        if retain is not None:
            props["retain"] = retain

        jsii.create(Repository, self, [scope, id, props])

    @jsii.member(jsii_name="addLifecycleRule")
    def add_lifecycle_rule(self, *, description: typing.Optional[str]=None, max_image_age_days: typing.Optional[jsii.Number]=None, max_image_count: typing.Optional[jsii.Number]=None, rule_priority: typing.Optional[jsii.Number]=None, tag_prefix_list: typing.Optional[typing.List[str]]=None, tag_status: typing.Optional["TagStatus"]=None) -> None:
        rule: LifecycleRule = {}

        if description is not None:
            rule["description"] = description

        if max_image_age_days is not None:
            rule["maxImageAgeDays"] = max_image_age_days

        if max_image_count is not None:
            rule["maxImageCount"] = max_image_count

        if rule_priority is not None:
            rule["rulePriority"] = rule_priority

        if tag_prefix_list is not None:
            rule["tagPrefixList"] = tag_prefix_list

        if tag_status is not None:
            rule["tagStatus"] = tag_status

        return jsii.invoke(self, "addLifecycleRule", [rule])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="export")
    def export(self) -> "RepositoryImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        return jsii.get(self, "repositoryArn")

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        return jsii.get(self, "repositoryName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecr.RepositoryImportProps")
class RepositoryImportProps(jsii.compat.TypedDict, total=False):
    repositoryArn: str
    repositoryName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ecr.RepositoryProps")
class RepositoryProps(jsii.compat.TypedDict, total=False):
    lifecycleRegistryId: str
    lifecycleRules: typing.List["LifecycleRule"]
    repositoryName: str
    retain: bool

@jsii.enum(jsii_type="@aws-cdk/aws-ecr.TagStatus")
class TagStatus(enum.Enum):
    Any = "Any"
    Tagged = "Tagged"
    Untagged = "Untagged"

__all__ = ["CfnRepository", "CfnRepositoryProps", "CountType", "IRepository", "LifecycleRule", "Repository", "RepositoryBase", "RepositoryImportProps", "RepositoryProps", "TagStatus", "__jsii_assembly__"]

publication.publish()
