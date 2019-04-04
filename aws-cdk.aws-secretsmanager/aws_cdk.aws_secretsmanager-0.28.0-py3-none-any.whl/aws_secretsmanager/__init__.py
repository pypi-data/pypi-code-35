import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-secretsmanager", "0.28.0", __name__, "aws-secretsmanager@0.28.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.AttachedSecretOptions")
class AttachedSecretOptions(jsii.compat.TypedDict):
    target: "ISecretAttachmentTarget"

@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.AttachedSecretProps")
class AttachedSecretProps(AttachedSecretOptions, jsii.compat.TypedDict):
    secret: "ISecret"

@jsii.enum(jsii_type="@aws-cdk/aws-secretsmanager.AttachmentTargetType")
class AttachmentTargetType(enum.Enum):
    Instance = "Instance"
    Cluster = "Cluster"

class CfnResourcePolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.CfnResourcePolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, resource_policy: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], secret_id: str) -> None:
        props: CfnResourcePolicyProps = {"resourcePolicy": resource_policy, "secretId": secret_id}

        jsii.create(CfnResourcePolicy, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnResourcePolicyProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="resourcePolicySecretArn")
    def resource_policy_secret_arn(self) -> str:
        return jsii.get(self, "resourcePolicySecretArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnResourcePolicyProps")
class CfnResourcePolicyProps(jsii.compat.TypedDict):
    resourcePolicy: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    secretId: str

class CfnRotationSchedule(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.CfnRotationSchedule"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, secret_id: str, rotation_lambda_arn: typing.Optional[str]=None, rotation_rules: typing.Optional[typing.Union[aws_cdk.cdk.Token, "RotationRulesProperty"]]=None) -> None:
        props: CfnRotationScheduleProps = {"secretId": secret_id}

        if rotation_lambda_arn is not None:
            props["rotationLambdaArn"] = rotation_lambda_arn

        if rotation_rules is not None:
            props["rotationRules"] = rotation_rules

        jsii.create(CfnRotationSchedule, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRotationScheduleProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="rotationScheduleSecretArn")
    def rotation_schedule_secret_arn(self) -> str:
        return jsii.get(self, "rotationScheduleSecretArn")

    @jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnRotationSchedule.RotationRulesProperty")
    class RotationRulesProperty(jsii.compat.TypedDict, total=False):
        automaticallyAfterDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class _CfnRotationScheduleProps(jsii.compat.TypedDict, total=False):
    rotationLambdaArn: str
    rotationRules: typing.Union[aws_cdk.cdk.Token, "CfnRotationSchedule.RotationRulesProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnRotationScheduleProps")
class CfnRotationScheduleProps(_CfnRotationScheduleProps):
    secretId: str

class CfnSecret(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.CfnSecret"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: typing.Optional[str]=None, generate_secret_string: typing.Optional[typing.Union[aws_cdk.cdk.Token, "GenerateSecretStringProperty"]]=None, kms_key_id: typing.Optional[str]=None, name: typing.Optional[str]=None, secret_string: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnSecretProps = {}

        if description is not None:
            props["description"] = description

        if generate_secret_string is not None:
            props["generateSecretString"] = generate_secret_string

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if name is not None:
            props["name"] = name

        if secret_string is not None:
            props["secretString"] = secret_string

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnSecret, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSecretProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        return jsii.get(self, "secretArn")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnSecret.GenerateSecretStringProperty")
    class GenerateSecretStringProperty(jsii.compat.TypedDict, total=False):
        excludeCharacters: str
        excludeLowercase: typing.Union[bool, aws_cdk.cdk.Token]
        excludeNumbers: typing.Union[bool, aws_cdk.cdk.Token]
        excludePunctuation: typing.Union[bool, aws_cdk.cdk.Token]
        excludeUppercase: typing.Union[bool, aws_cdk.cdk.Token]
        generateStringKey: str
        includeSpace: typing.Union[bool, aws_cdk.cdk.Token]
        passwordLength: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        requireEachIncludedType: typing.Union[bool, aws_cdk.cdk.Token]
        secretStringTemplate: str


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnSecretProps")
class CfnSecretProps(jsii.compat.TypedDict, total=False):
    description: str
    generateSecretString: typing.Union[aws_cdk.cdk.Token, "CfnSecret.GenerateSecretStringProperty"]
    kmsKeyId: str
    name: str
    secretString: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

class CfnSecretTargetAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.CfnSecretTargetAttachment"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, secret_id: str, target_id: str, target_type: str) -> None:
        props: CfnSecretTargetAttachmentProps = {"secretId": secret_id, "targetId": target_id, "targetType": target_type}

        jsii.create(CfnSecretTargetAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSecretTargetAttachmentProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> str:
        return jsii.get(self, "secretTargetAttachmentSecretArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnSecretTargetAttachmentProps")
class CfnSecretTargetAttachmentProps(jsii.compat.TypedDict):
    secretId: str
    targetId: str
    targetType: str

@jsii.interface(jsii_type="@aws-cdk/aws-secretsmanager.ISecret")
class ISecret(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ISecretProxy

    @property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> aws_cdk.cdk.SecretValue:
        ...

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        ...

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(self, id: str, *, rotation_lambda: aws_cdk.aws_lambda.IFunction, automatically_after_days: typing.Optional[jsii.Number]=None) -> "RotationSchedule":
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "SecretImportProps":
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable, version_stages: typing.Optional[typing.List[str]]=None) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="secretJsonValue")
    def secret_json_value(self, key: str) -> aws_cdk.cdk.SecretValue:
        ...


class _ISecretProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-secretsmanager.ISecret"
    @property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        return jsii.get(self, "secretArn")

    @property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> aws_cdk.cdk.SecretValue:
        return jsii.get(self, "secretValue")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        return jsii.get(self, "encryptionKey")

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(self, id: str, *, rotation_lambda: aws_cdk.aws_lambda.IFunction, automatically_after_days: typing.Optional[jsii.Number]=None) -> "RotationSchedule":
        options: RotationScheduleOptions = {"rotationLambda": rotation_lambda}

        if automatically_after_days is not None:
            options["automaticallyAfterDays"] = automatically_after_days

        return jsii.invoke(self, "addRotationSchedule", [id, options])

    @jsii.member(jsii_name="export")
    def export(self) -> "SecretImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable, version_stages: typing.Optional[typing.List[str]]=None) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantRead", [grantee, version_stages])

    @jsii.member(jsii_name="secretJsonValue")
    def secret_json_value(self, key: str) -> aws_cdk.cdk.SecretValue:
        return jsii.invoke(self, "secretJsonValue", [key])


@jsii.interface(jsii_type="@aws-cdk/aws-secretsmanager.ISecretAttachmentTarget")
class ISecretAttachmentTarget(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ISecretAttachmentTargetProxy

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> "SecretAttachmentTargetProps":
        ...


class _ISecretAttachmentTargetProxy():
    __jsii_type__ = "@aws-cdk/aws-secretsmanager.ISecretAttachmentTarget"
    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> "SecretAttachmentTargetProps":
        return jsii.invoke(self, "asSecretAttachmentTarget", [])


class RotationSchedule(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.RotationSchedule"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, secret: "ISecret", rotation_lambda: aws_cdk.aws_lambda.IFunction, automatically_after_days: typing.Optional[jsii.Number]=None) -> None:
        props: RotationScheduleProps = {"secret": secret, "rotationLambda": rotation_lambda}

        if automatically_after_days is not None:
            props["automaticallyAfterDays"] = automatically_after_days

        jsii.create(RotationSchedule, self, [scope, id, props])


class _RotationScheduleOptions(jsii.compat.TypedDict, total=False):
    automaticallyAfterDays: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.RotationScheduleOptions")
class RotationScheduleOptions(_RotationScheduleOptions):
    rotationLambda: aws_cdk.aws_lambda.IFunction

@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.RotationScheduleProps")
class RotationScheduleProps(RotationScheduleOptions, jsii.compat.TypedDict):
    secret: "ISecret"

@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.SecretAttachmentTargetProps")
class SecretAttachmentTargetProps(jsii.compat.TypedDict):
    targetId: str
    targetType: "AttachmentTargetType"

@jsii.implements(ISecret)
class SecretBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-secretsmanager.SecretBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _SecretBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(SecretBase, self, [scope, id])

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(self, id: str, *, rotation_lambda: aws_cdk.aws_lambda.IFunction, automatically_after_days: typing.Optional[jsii.Number]=None) -> "RotationSchedule":
        options: RotationScheduleOptions = {"rotationLambda": rotation_lambda}

        if automatically_after_days is not None:
            options["automaticallyAfterDays"] = automatically_after_days

        return jsii.invoke(self, "addRotationSchedule", [id, options])

    @jsii.member(jsii_name="export")
    @abc.abstractmethod
    def export(self) -> "SecretImportProps":
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable, version_stages: typing.Optional[typing.List[str]]=None) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantRead", [grantee, version_stages])

    @jsii.member(jsii_name="secretJsonValue")
    def secret_json_value(self, json_field: str) -> aws_cdk.cdk.SecretValue:
        return jsii.invoke(self, "secretJsonValue", [json_field])

    @property
    @jsii.member(jsii_name="secretArn")
    @abc.abstractmethod
    def secret_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> aws_cdk.cdk.SecretValue:
        return jsii.get(self, "secretValue")

    @property
    @jsii.member(jsii_name="encryptionKey")
    @abc.abstractmethod
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        ...


class _SecretBaseProxy(SecretBase):
    @jsii.member(jsii_name="export")
    def export(self) -> "SecretImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        return jsii.get(self, "secretArn")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        return jsii.get(self, "encryptionKey")


@jsii.implements(ISecret)
class AttachedSecret(SecretBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.AttachedSecret"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, secret: "ISecret", target: "ISecretAttachmentTarget") -> None:
        props: AttachedSecretProps = {"secret": secret, "target": target}

        jsii.create(AttachedSecret, self, [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "SecretImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        return jsii.get(self, "secretArn")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        return jsii.get(self, "encryptionKey")


class Secret(SecretBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.Secret"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: typing.Optional[str]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IEncryptionKey]=None, generate_secret_string: typing.Optional["SecretStringGenerator"]=None, name: typing.Optional[str]=None) -> None:
        props: SecretProps = {}

        if description is not None:
            props["description"] = description

        if encryption_key is not None:
            props["encryptionKey"] = encryption_key

        if generate_secret_string is not None:
            props["generateSecretString"] = generate_secret_string

        if name is not None:
            props["name"] = name

        jsii.create(Secret, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, secret_arn: str, encryption_key: typing.Optional[aws_cdk.aws_kms.IEncryptionKey]=None) -> "ISecret":
        props: SecretImportProps = {"secretArn": secret_arn}

        if encryption_key is not None:
            props["encryptionKey"] = encryption_key

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addTargetAttachment")
    def add_target_attachment(self, id: str, *, target: "ISecretAttachmentTarget") -> "AttachedSecret":
        options: AttachedSecretOptions = {"target": target}

        return jsii.invoke(self, "addTargetAttachment", [id, options])

    @jsii.member(jsii_name="export")
    def export(self) -> "SecretImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        return jsii.get(self, "secretArn")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        return jsii.get(self, "encryptionKey")


class _SecretImportProps(jsii.compat.TypedDict, total=False):
    encryptionKey: aws_cdk.aws_kms.IEncryptionKey

@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.SecretImportProps")
class SecretImportProps(_SecretImportProps):
    secretArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.SecretProps")
class SecretProps(jsii.compat.TypedDict, total=False):
    description: str
    encryptionKey: aws_cdk.aws_kms.IEncryptionKey
    generateSecretString: "SecretStringGenerator"
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.SecretStringGenerator")
class SecretStringGenerator(jsii.compat.TypedDict, total=False):
    excludeCharacters: str
    excludeLowercase: bool
    excludeNumbers: bool
    excludePunctuation: bool
    excludeUppercase: bool
    generateStringKey: str
    includeSpace: bool
    passwordLength: jsii.Number
    requireEachIncludedType: bool
    secretStringTemplate: str

__all__ = ["AttachedSecret", "AttachedSecretOptions", "AttachedSecretProps", "AttachmentTargetType", "CfnResourcePolicy", "CfnResourcePolicyProps", "CfnRotationSchedule", "CfnRotationScheduleProps", "CfnSecret", "CfnSecretProps", "CfnSecretTargetAttachment", "CfnSecretTargetAttachmentProps", "ISecret", "ISecretAttachmentTarget", "RotationSchedule", "RotationScheduleOptions", "RotationScheduleProps", "Secret", "SecretAttachmentTargetProps", "SecretBase", "SecretImportProps", "SecretProps", "SecretStringGenerator", "__jsii_assembly__"]

publication.publish()
