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
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-kms", "0.28.0", __name__, "aws-kms@0.28.0.jsii.tgz")
class CfnAlias(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kms.CfnAlias"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, alias_name: str, target_key_id: str) -> None:
        props: CfnAliasProps = {"aliasName": alias_name, "targetKeyId": target_key_id}

        jsii.create(CfnAlias, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> str:
        return jsii.get(self, "aliasName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAliasProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-kms.CfnAliasProps")
class CfnAliasProps(jsii.compat.TypedDict):
    aliasName: str
    targetKeyId: str

class CfnKey(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kms.CfnKey"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, key_policy: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], description: typing.Optional[str]=None, enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, enable_key_rotation: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, key_usage: typing.Optional[str]=None, pending_window_in_days: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnKeyProps = {"keyPolicy": key_policy}

        if description is not None:
            props["description"] = description

        if enabled is not None:
            props["enabled"] = enabled

        if enable_key_rotation is not None:
            props["enableKeyRotation"] = enable_key_rotation

        if key_usage is not None:
            props["keyUsage"] = key_usage

        if pending_window_in_days is not None:
            props["pendingWindowInDays"] = pending_window_in_days

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnKey, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> str:
        return jsii.get(self, "keyArn")

    @property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> str:
        return jsii.get(self, "keyId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnKeyProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnKeyProps(jsii.compat.TypedDict, total=False):
    description: str
    enabled: typing.Union[bool, aws_cdk.cdk.Token]
    enableKeyRotation: typing.Union[bool, aws_cdk.cdk.Token]
    keyUsage: str
    pendingWindowInDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-kms.CfnKeyProps")
class CfnKeyProps(_CfnKeyProps):
    keyPolicy: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

class EncryptionKeyAlias(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kms.EncryptionKeyAlias"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, alias: str, key: "IEncryptionKey") -> None:
        props: EncryptionKeyAliasProps = {"alias": alias, "key": key}

        jsii.create(EncryptionKeyAlias, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> str:
        return jsii.get(self, "aliasName")

    @alias_name.setter
    def alias_name(self, value: str):
        return jsii.set(self, "aliasName", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-kms.EncryptionKeyAliasProps")
class EncryptionKeyAliasProps(jsii.compat.TypedDict):
    alias: str
    key: "IEncryptionKey"

@jsii.data_type(jsii_type="@aws-cdk/aws-kms.EncryptionKeyImportProps")
class EncryptionKeyImportProps(jsii.compat.TypedDict):
    keyArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-kms.EncryptionKeyProps")
class EncryptionKeyProps(jsii.compat.TypedDict, total=False):
    description: str
    enabled: bool
    enableKeyRotation: bool
    policy: aws_cdk.aws_iam.PolicyDocument
    retain: bool

@jsii.interface(jsii_type="@aws-cdk/aws-kms.IEncryptionKey")
class IEncryptionKey(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IEncryptionKeyProxy

    @property
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> str:
        ...

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias: str) -> "EncryptionKeyAlias":
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement, allow_no_op: typing.Optional[bool]=None) -> None:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "EncryptionKeyImportProps":
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantDecrypt")
    def grant_decrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantEncrypt")
    def grant_encrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantEncryptDecrypt")
    def grant_encrypt_decrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...


class _IEncryptionKeyProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-kms.IEncryptionKey"
    @property
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> str:
        return jsii.get(self, "keyArn")

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias: str) -> "EncryptionKeyAlias":
        return jsii.invoke(self, "addAlias", [alias])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement, allow_no_op: typing.Optional[bool]=None) -> None:
        return jsii.invoke(self, "addToResourcePolicy", [statement, allow_no_op])

    @jsii.member(jsii_name="export")
    def export(self) -> "EncryptionKeyImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grant", [grantee, actions])

    @jsii.member(jsii_name="grantDecrypt")
    def grant_decrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantDecrypt", [grantee])

    @jsii.member(jsii_name="grantEncrypt")
    def grant_encrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantEncrypt", [grantee])

    @jsii.member(jsii_name="grantEncryptDecrypt")
    def grant_encrypt_decrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantEncryptDecrypt", [grantee])


@jsii.implements(IEncryptionKey)
class EncryptionKeyBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-kms.EncryptionKeyBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _EncryptionKeyBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(EncryptionKeyBase, self, [scope, id])

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias: str) -> "EncryptionKeyAlias":
        return jsii.invoke(self, "addAlias", [alias])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement, allow_no_op: typing.Optional[bool]=None) -> None:
        return jsii.invoke(self, "addToResourcePolicy", [statement, allow_no_op])

    @jsii.member(jsii_name="export")
    @abc.abstractmethod
    def export(self) -> "EncryptionKeyImportProps":
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grant", [grantee, actions])

    @jsii.member(jsii_name="grantDecrypt")
    def grant_decrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantDecrypt", [grantee])

    @jsii.member(jsii_name="grantEncrypt")
    def grant_encrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantEncrypt", [grantee])

    @jsii.member(jsii_name="grantEncryptDecrypt")
    def grant_encrypt_decrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantEncryptDecrypt", [grantee])

    @property
    @jsii.member(jsii_name="keyArn")
    @abc.abstractmethod
    def key_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="policy")
    @abc.abstractmethod
    def _policy(self) -> typing.Optional[aws_cdk.aws_iam.PolicyDocument]:
        ...


class _EncryptionKeyBaseProxy(EncryptionKeyBase):
    @jsii.member(jsii_name="export")
    def export(self) -> "EncryptionKeyImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> str:
        return jsii.get(self, "keyArn")

    @property
    @jsii.member(jsii_name="policy")
    def _policy(self) -> typing.Optional[aws_cdk.aws_iam.PolicyDocument]:
        return jsii.get(self, "policy")


class EncryptionKey(EncryptionKeyBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kms.EncryptionKey"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, enable_key_rotation: typing.Optional[bool]=None, policy: typing.Optional[aws_cdk.aws_iam.PolicyDocument]=None, retain: typing.Optional[bool]=None) -> None:
        props: EncryptionKeyProps = {}

        if description is not None:
            props["description"] = description

        if enabled is not None:
            props["enabled"] = enabled

        if enable_key_rotation is not None:
            props["enableKeyRotation"] = enable_key_rotation

        if policy is not None:
            props["policy"] = policy

        if retain is not None:
            props["retain"] = retain

        jsii.create(EncryptionKey, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, key_arn: str) -> "IEncryptionKey":
        props: EncryptionKeyImportProps = {"keyArn": key_arn}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "EncryptionKeyImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> str:
        return jsii.get(self, "keyArn")

    @property
    @jsii.member(jsii_name="policy")
    def _policy(self) -> typing.Optional[aws_cdk.aws_iam.PolicyDocument]:
        return jsii.get(self, "policy")


class ViaServicePrincipal(aws_cdk.aws_iam.PrincipalBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kms.ViaServicePrincipal"):
    def __init__(self, service_name: str, base_principal: typing.Optional[aws_cdk.aws_iam.IPrincipal]=None) -> None:
        jsii.create(ViaServicePrincipal, self, [service_name, base_principal])

    @property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> aws_cdk.aws_iam.PrincipalPolicyFragment:
        return jsii.get(self, "policyFragment")

    @property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> str:
        return jsii.get(self, "serviceName")


__all__ = ["CfnAlias", "CfnAliasProps", "CfnKey", "CfnKeyProps", "EncryptionKey", "EncryptionKeyAlias", "EncryptionKeyAliasProps", "EncryptionKeyBase", "EncryptionKeyImportProps", "EncryptionKeyProps", "IEncryptionKey", "ViaServicePrincipal", "__jsii_assembly__"]

publication.publish()
