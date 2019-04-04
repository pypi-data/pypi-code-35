import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
import aws_cdk.region_info
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-iam", "0.28.0", __name__, "aws-iam@0.28.0.jsii.tgz")
class AwsManagedPolicy(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.AwsManagedPolicy"):
    def __init__(self, managed_policy_name: str, scope: aws_cdk.cdk.IConstruct) -> None:
        jsii.create(AwsManagedPolicy, self, [managed_policy_name, scope])

    @property
    @jsii.member(jsii_name="managedPolicyName")
    def managed_policy_name(self) -> str:
        return jsii.get(self, "managedPolicyName")

    @property
    @jsii.member(jsii_name="policyArn")
    def policy_arn(self) -> str:
        return jsii.get(self, "policyArn")

    @property
    @jsii.member(jsii_name="scope")
    def scope(self) -> aws_cdk.cdk.IConstruct:
        return jsii.get(self, "scope")


class CfnAccessKey(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnAccessKey"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, user_name: str, serial: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, status: typing.Optional[str]=None) -> None:
        props: CfnAccessKeyProps = {"userName": user_name}

        if serial is not None:
            props["serial"] = serial

        if status is not None:
            props["status"] = status

        jsii.create(CfnAccessKey, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> str:
        return jsii.get(self, "accessKeyId")

    @property
    @jsii.member(jsii_name="accessKeySecretAccessKey")
    def access_key_secret_access_key(self) -> str:
        return jsii.get(self, "accessKeySecretAccessKey")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAccessKeyProps":
        return jsii.get(self, "propertyOverrides")


class _CfnAccessKeyProps(jsii.compat.TypedDict, total=False):
    serial: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    status: str

@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnAccessKeyProps")
class CfnAccessKeyProps(_CfnAccessKeyProps):
    userName: str

class CfnGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, group_name: typing.Optional[str]=None, managed_policy_arns: typing.Optional[typing.List[str]]=None, path: typing.Optional[str]=None, policies: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "PolicyProperty"]]]]=None) -> None:
        props: CfnGroupProps = {}

        if group_name is not None:
            props["groupName"] = group_name

        if managed_policy_arns is not None:
            props["managedPolicyArns"] = managed_policy_arns

        if path is not None:
            props["path"] = path

        if policies is not None:
            props["policies"] = policies

        jsii.create(CfnGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> str:
        return jsii.get(self, "groupArn")

    @property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> str:
        return jsii.get(self, "groupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnGroupProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnGroup.PolicyProperty")
    class PolicyProperty(jsii.compat.TypedDict):
        policyDocument: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        policyName: str


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnGroupProps")
class CfnGroupProps(jsii.compat.TypedDict, total=False):
    groupName: str
    managedPolicyArns: typing.List[str]
    path: str
    policies: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnGroup.PolicyProperty"]]]

class CfnInstanceProfile(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnInstanceProfile"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, roles: typing.List[str], instance_profile_name: typing.Optional[str]=None, path: typing.Optional[str]=None) -> None:
        props: CfnInstanceProfileProps = {"roles": roles}

        if instance_profile_name is not None:
            props["instanceProfileName"] = instance_profile_name

        if path is not None:
            props["path"] = path

        jsii.create(CfnInstanceProfile, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="instanceProfileArn")
    def instance_profile_arn(self) -> str:
        return jsii.get(self, "instanceProfileArn")

    @property
    @jsii.member(jsii_name="instanceProfileName")
    def instance_profile_name(self) -> str:
        return jsii.get(self, "instanceProfileName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnInstanceProfileProps":
        return jsii.get(self, "propertyOverrides")


class _CfnInstanceProfileProps(jsii.compat.TypedDict, total=False):
    instanceProfileName: str
    path: str

@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnInstanceProfileProps")
class CfnInstanceProfileProps(_CfnInstanceProfileProps):
    roles: typing.List[str]

class CfnManagedPolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnManagedPolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, policy_document: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], description: typing.Optional[str]=None, groups: typing.Optional[typing.List[str]]=None, managed_policy_name: typing.Optional[str]=None, path: typing.Optional[str]=None, roles: typing.Optional[typing.List[str]]=None, users: typing.Optional[typing.List[str]]=None) -> None:
        props: CfnManagedPolicyProps = {"policyDocument": policy_document}

        if description is not None:
            props["description"] = description

        if groups is not None:
            props["groups"] = groups

        if managed_policy_name is not None:
            props["managedPolicyName"] = managed_policy_name

        if path is not None:
            props["path"] = path

        if roles is not None:
            props["roles"] = roles

        if users is not None:
            props["users"] = users

        jsii.create(CfnManagedPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="managedPolicyArn")
    def managed_policy_arn(self) -> str:
        return jsii.get(self, "managedPolicyArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnManagedPolicyProps":
        return jsii.get(self, "propertyOverrides")


class _CfnManagedPolicyProps(jsii.compat.TypedDict, total=False):
    description: str
    groups: typing.List[str]
    managedPolicyName: str
    path: str
    roles: typing.List[str]
    users: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnManagedPolicyProps")
class CfnManagedPolicyProps(_CfnManagedPolicyProps):
    policyDocument: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

class CfnPolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnPolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, policy_document: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], policy_name: str, groups: typing.Optional[typing.List[str]]=None, roles: typing.Optional[typing.List[str]]=None, users: typing.Optional[typing.List[str]]=None) -> None:
        props: CfnPolicyProps = {"policyDocument": policy_document, "policyName": policy_name}

        if groups is not None:
            props["groups"] = groups

        if roles is not None:
            props["roles"] = roles

        if users is not None:
            props["users"] = users

        jsii.create(CfnPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> str:
        return jsii.get(self, "policyName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPolicyProps":
        return jsii.get(self, "propertyOverrides")


class _CfnPolicyProps(jsii.compat.TypedDict, total=False):
    groups: typing.List[str]
    roles: typing.List[str]
    users: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnPolicyProps")
class CfnPolicyProps(_CfnPolicyProps):
    policyDocument: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    policyName: str

class CfnRole(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnRole"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, assume_role_policy_document: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], managed_policy_arns: typing.Optional[typing.List[str]]=None, max_session_duration: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, path: typing.Optional[str]=None, permissions_boundary: typing.Optional[str]=None, policies: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "PolicyProperty"]]]]=None, role_name: typing.Optional[str]=None) -> None:
        props: CfnRoleProps = {"assumeRolePolicyDocument": assume_role_policy_document}

        if managed_policy_arns is not None:
            props["managedPolicyArns"] = managed_policy_arns

        if max_session_duration is not None:
            props["maxSessionDuration"] = max_session_duration

        if path is not None:
            props["path"] = path

        if permissions_boundary is not None:
            props["permissionsBoundary"] = permissions_boundary

        if policies is not None:
            props["policies"] = policies

        if role_name is not None:
            props["roleName"] = role_name

        jsii.create(CfnRole, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRoleProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        return jsii.get(self, "roleArn")

    @property
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> str:
        return jsii.get(self, "roleId")

    @property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> str:
        return jsii.get(self, "roleName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnRole.PolicyProperty")
    class PolicyProperty(jsii.compat.TypedDict):
        policyDocument: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        policyName: str


class _CfnRoleProps(jsii.compat.TypedDict, total=False):
    managedPolicyArns: typing.List[str]
    maxSessionDuration: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    path: str
    permissionsBoundary: str
    policies: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnRole.PolicyProperty"]]]
    roleName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnRoleProps")
class CfnRoleProps(_CfnRoleProps):
    assumeRolePolicyDocument: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

class CfnServiceLinkedRole(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnServiceLinkedRole"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, aws_service_name: str, custom_suffix: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        props: CfnServiceLinkedRoleProps = {"awsServiceName": aws_service_name}

        if custom_suffix is not None:
            props["customSuffix"] = custom_suffix

        if description is not None:
            props["description"] = description

        jsii.create(CfnServiceLinkedRole, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnServiceLinkedRoleProps":
        return jsii.get(self, "propertyOverrides")


class _CfnServiceLinkedRoleProps(jsii.compat.TypedDict, total=False):
    customSuffix: str
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnServiceLinkedRoleProps")
class CfnServiceLinkedRoleProps(_CfnServiceLinkedRoleProps):
    awsServiceName: str

class CfnUser(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnUser"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, groups: typing.Optional[typing.List[str]]=None, login_profile: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LoginProfileProperty"]]=None, managed_policy_arns: typing.Optional[typing.List[str]]=None, path: typing.Optional[str]=None, permissions_boundary: typing.Optional[str]=None, policies: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "PolicyProperty"]]]]=None, user_name: typing.Optional[str]=None) -> None:
        props: CfnUserProps = {}

        if groups is not None:
            props["groups"] = groups

        if login_profile is not None:
            props["loginProfile"] = login_profile

        if managed_policy_arns is not None:
            props["managedPolicyArns"] = managed_policy_arns

        if path is not None:
            props["path"] = path

        if permissions_boundary is not None:
            props["permissionsBoundary"] = permissions_boundary

        if policies is not None:
            props["policies"] = policies

        if user_name is not None:
            props["userName"] = user_name

        jsii.create(CfnUser, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnUserProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="userArn")
    def user_arn(self) -> str:
        return jsii.get(self, "userArn")

    @property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> str:
        return jsii.get(self, "userName")

    class _LoginProfileProperty(jsii.compat.TypedDict, total=False):
        passwordResetRequired: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnUser.LoginProfileProperty")
    class LoginProfileProperty(_LoginProfileProperty):
        password: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnUser.PolicyProperty")
    class PolicyProperty(jsii.compat.TypedDict):
        policyDocument: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        policyName: str


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnUserProps")
class CfnUserProps(jsii.compat.TypedDict, total=False):
    groups: typing.List[str]
    loginProfile: typing.Union[aws_cdk.cdk.Token, "CfnUser.LoginProfileProperty"]
    managedPolicyArns: typing.List[str]
    path: str
    permissionsBoundary: str
    policies: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnUser.PolicyProperty"]]]
    userName: str

class CfnUserToGroupAddition(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnUserToGroupAddition"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, group_name: str, users: typing.List[str]) -> None:
        props: CfnUserToGroupAdditionProps = {"groupName": group_name, "users": users}

        jsii.create(CfnUserToGroupAddition, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnUserToGroupAdditionProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnUserToGroupAdditionProps")
class CfnUserToGroupAdditionProps(jsii.compat.TypedDict):
    groupName: str
    users: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CommonGrantOptions")
class CommonGrantOptions(jsii.compat.TypedDict):
    actions: typing.List[str]
    grantee: "IGrantable"
    resourceArns: typing.List[str]

class Grant(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.Grant"):
    @jsii.member(jsii_name="addToPrincipal")
    @classmethod
    def add_to_principal(cls, *, scope: typing.Optional[aws_cdk.cdk.IConstruct]=None, actions: typing.List[str], grantee: "IGrantable", resource_arns: typing.List[str]) -> "Grant":
        options: GrantOnPrincipalOptions = {"actions": actions, "grantee": grantee, "resourceArns": resource_arns}

        if scope is not None:
            options["scope"] = scope

        return jsii.sinvoke(cls, "addToPrincipal", [options])

    @jsii.member(jsii_name="addToPrincipalAndResource")
    @classmethod
    def add_to_principal_and_resource(cls, *, resource: "IResourceWithPolicy", resource_self_arns: typing.Optional[typing.List[str]]=None, actions: typing.List[str], grantee: "IGrantable", resource_arns: typing.List[str]) -> "Grant":
        options: GrantOnPrincipalAndResourceOptions = {"resource": resource, "actions": actions, "grantee": grantee, "resourceArns": resource_arns}

        if resource_self_arns is not None:
            options["resourceSelfArns"] = resource_self_arns

        return jsii.sinvoke(cls, "addToPrincipalAndResource", [options])

    @jsii.member(jsii_name="addToPrincipalOrResource")
    @classmethod
    def add_to_principal_or_resource(cls, *, resource: "IResourceWithPolicy", resource_self_arns: typing.Optional[typing.List[str]]=None, actions: typing.List[str], grantee: "IGrantable", resource_arns: typing.List[str]) -> "Grant":
        options: GrantWithResourceOptions = {"resource": resource, "actions": actions, "grantee": grantee, "resourceArns": resource_arns}

        if resource_self_arns is not None:
            options["resourceSelfArns"] = resource_self_arns

        return jsii.sinvoke(cls, "addToPrincipalOrResource", [options])

    @jsii.member(jsii_name="assertSuccess")
    def assert_success(self) -> None:
        return jsii.invoke(self, "assertSuccess", [])

    @property
    @jsii.member(jsii_name="success")
    def success(self) -> bool:
        return jsii.get(self, "success")

    @property
    @jsii.member(jsii_name="principalStatement")
    def principal_statement(self) -> typing.Optional["PolicyStatement"]:
        return jsii.get(self, "principalStatement")

    @property
    @jsii.member(jsii_name="resourceStatement")
    def resource_statement(self) -> typing.Optional["PolicyStatement"]:
        return jsii.get(self, "resourceStatement")


class _GrantOnPrincipalAndResourceOptions(CommonGrantOptions, jsii.compat.TypedDict, total=False):
    resourceSelfArns: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-iam.GrantOnPrincipalAndResourceOptions")
class GrantOnPrincipalAndResourceOptions(_GrantOnPrincipalAndResourceOptions):
    resource: "IResourceWithPolicy"

@jsii.data_type(jsii_type="@aws-cdk/aws-iam.GrantOnPrincipalOptions")
class GrantOnPrincipalOptions(CommonGrantOptions, jsii.compat.TypedDict, total=False):
    scope: aws_cdk.cdk.IConstruct

class _GrantWithResourceOptions(CommonGrantOptions, jsii.compat.TypedDict, total=False):
    resourceSelfArns: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-iam.GrantWithResourceOptions")
class GrantWithResourceOptions(_GrantWithResourceOptions):
    resource: "IResourceWithPolicy"

@jsii.data_type(jsii_type="@aws-cdk/aws-iam.GroupProps")
class GroupProps(jsii.compat.TypedDict, total=False):
    groupName: str
    managedPolicyArns: typing.List[typing.Any]
    path: str

@jsii.interface(jsii_type="@aws-cdk/aws-iam.IGrantable")
class IGrantable(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IGrantableProxy

    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        ...


class _IGrantableProxy():
    __jsii_type__ = "@aws-cdk/aws-iam.IGrantable"
    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        return jsii.get(self, "grantPrincipal")


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IPrincipal")
class IPrincipal(IGrantable, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IPrincipalProxy

    @property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        ...

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> bool:
        ...


class _IPrincipalProxy(jsii.proxy_for(IGrantable)):
    __jsii_type__ = "@aws-cdk/aws-iam.IPrincipal"
    @property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        return jsii.get(self, "assumeRoleAction")

    @property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        return jsii.get(self, "policyFragment")

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> bool:
        return jsii.invoke(self, "addToPolicy", [statement])


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IIdentity")
class IIdentity(IPrincipal, aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IIdentityProxy

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: "Policy") -> None:
        ...

    @jsii.member(jsii_name="attachManagedPolicy")
    def attach_managed_policy(self, arn: str) -> None:
        ...


class _IIdentityProxy(jsii.proxy_for(IPrincipal), jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-iam.IIdentity"
    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: "Policy") -> None:
        return jsii.invoke(self, "attachInlinePolicy", [policy])

    @jsii.member(jsii_name="attachManagedPolicy")
    def attach_managed_policy(self, arn: str) -> None:
        return jsii.invoke(self, "attachManagedPolicy", [arn])


@jsii.implements(IIdentity)
class Group(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.Group"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, group_name: typing.Optional[str]=None, managed_policy_arns: typing.Optional[typing.List[typing.Any]]=None, path: typing.Optional[str]=None) -> None:
        props: GroupProps = {}

        if group_name is not None:
            props["groupName"] = group_name

        if managed_policy_arns is not None:
            props["managedPolicyArns"] = managed_policy_arns

        if path is not None:
            props["path"] = path

        jsii.create(Group, self, [scope, id, props])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> bool:
        return jsii.invoke(self, "addToPolicy", [statement])

    @jsii.member(jsii_name="addUser")
    def add_user(self, user: "User") -> None:
        return jsii.invoke(self, "addUser", [user])

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: "Policy") -> None:
        return jsii.invoke(self, "attachInlinePolicy", [policy])

    @jsii.member(jsii_name="attachManagedPolicy")
    def attach_managed_policy(self, arn: str) -> None:
        return jsii.invoke(self, "attachManagedPolicy", [arn])

    @property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        return jsii.get(self, "assumeRoleAction")

    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        return jsii.get(self, "grantPrincipal")

    @property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> str:
        return jsii.get(self, "groupArn")

    @property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> str:
        return jsii.get(self, "groupName")

    @property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        return jsii.get(self, "policyFragment")


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IResourceWithPolicy")
class IResourceWithPolicy(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IResourceWithPolicyProxy

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: "PolicyStatement") -> None:
        ...


class _IResourceWithPolicyProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-iam.IResourceWithPolicy"
    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: "PolicyStatement") -> None:
        return jsii.invoke(self, "addToResourcePolicy", [statement])


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IRole")
class IRole(IIdentity, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IRoleProxy

    @property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "RoleImportProps":
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: "IPrincipal", *actions: str) -> "Grant":
        ...

    @jsii.member(jsii_name="grantPassRole")
    def grant_pass_role(self, grantee: "IPrincipal") -> "Grant":
        ...


class _IRoleProxy(jsii.proxy_for(IIdentity)):
    __jsii_type__ = "@aws-cdk/aws-iam.IRole"
    @property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        return jsii.get(self, "roleArn")

    @property
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> str:
        return jsii.get(self, "roleId")

    @property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> str:
        return jsii.get(self, "roleName")

    @jsii.member(jsii_name="export")
    def export(self) -> "RoleImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: "IPrincipal", *actions: str) -> "Grant":
        return jsii.invoke(self, "grant", [grantee, actions])

    @jsii.member(jsii_name="grantPassRole")
    def grant_pass_role(self, grantee: "IPrincipal") -> "Grant":
        return jsii.invoke(self, "grantPassRole", [grantee])


@jsii.implements(IPrincipal)
class ImportedResourcePrincipal(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.ImportedResourcePrincipal"):
    def __init__(self, *, resource: aws_cdk.cdk.IConstruct) -> None:
        props: ImportedResourcePrincipalProps = {"resource": resource}

        jsii.create(ImportedResourcePrincipal, self, [props])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> bool:
        return jsii.invoke(self, "addToPolicy", [statement])

    @property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        return jsii.get(self, "assumeRoleAction")

    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        return jsii.get(self, "grantPrincipal")

    @property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        return jsii.get(self, "policyFragment")


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.ImportedResourcePrincipalProps")
class ImportedResourcePrincipalProps(jsii.compat.TypedDict):
    resource: aws_cdk.cdk.IConstruct

@jsii.implements(IRole)
class LazyRole(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.LazyRole"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, assumed_by: "IPrincipal", external_id: typing.Optional[str]=None, inline_policies: typing.Optional[typing.Mapping[str,"PolicyDocument"]]=None, managed_policy_arns: typing.Optional[typing.List[str]]=None, max_session_duration_sec: typing.Optional[jsii.Number]=None, path: typing.Optional[str]=None, role_name: typing.Optional[str]=None) -> None:
        props: RoleProps = {"assumedBy": assumed_by}

        if external_id is not None:
            props["externalId"] = external_id

        if inline_policies is not None:
            props["inlinePolicies"] = inline_policies

        if managed_policy_arns is not None:
            props["managedPolicyArns"] = managed_policy_arns

        if max_session_duration_sec is not None:
            props["maxSessionDurationSec"] = max_session_duration_sec

        if path is not None:
            props["path"] = path

        if role_name is not None:
            props["roleName"] = role_name

        jsii.create(LazyRole, self, [scope, id, props])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> bool:
        return jsii.invoke(self, "addToPolicy", [statement])

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: "Policy") -> None:
        return jsii.invoke(self, "attachInlinePolicy", [policy])

    @jsii.member(jsii_name="attachManagedPolicy")
    def attach_managed_policy(self, arn: str) -> None:
        return jsii.invoke(self, "attachManagedPolicy", [arn])

    @jsii.member(jsii_name="export")
    def export(self) -> "RoleImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grant")
    def grant(self, identity: "IPrincipal", *actions: str) -> "Grant":
        return jsii.invoke(self, "grant", [identity, actions])

    @jsii.member(jsii_name="grantPassRole")
    def grant_pass_role(self, identity: "IPrincipal") -> "Grant":
        return jsii.invoke(self, "grantPassRole", [identity])

    @property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        return jsii.get(self, "assumeRoleAction")

    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        return jsii.get(self, "grantPrincipal")

    @property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        return jsii.get(self, "policyFragment")

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "RoleProps":
        return jsii.get(self, "props")

    @property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        return jsii.get(self, "roleArn")

    @property
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> str:
        return jsii.get(self, "roleId")

    @property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> str:
        return jsii.get(self, "roleName")


class Policy(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.Policy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, groups: typing.Optional[typing.List["Group"]]=None, policy_name: typing.Optional[str]=None, roles: typing.Optional[typing.List["IRole"]]=None, statements: typing.Optional[typing.List["PolicyStatement"]]=None, users: typing.Optional[typing.List["User"]]=None) -> None:
        props: PolicyProps = {}

        if groups is not None:
            props["groups"] = groups

        if policy_name is not None:
            props["policyName"] = policy_name

        if roles is not None:
            props["roles"] = roles

        if statements is not None:
            props["statements"] = statements

        if users is not None:
            props["users"] = users

        jsii.create(Policy, self, [scope, id, props])

    @jsii.member(jsii_name="addStatement")
    def add_statement(self, statement: "PolicyStatement") -> None:
        return jsii.invoke(self, "addStatement", [statement])

    @jsii.member(jsii_name="attachToGroup")
    def attach_to_group(self, group: "Group") -> None:
        return jsii.invoke(self, "attachToGroup", [group])

    @jsii.member(jsii_name="attachToRole")
    def attach_to_role(self, role: "IRole") -> None:
        return jsii.invoke(self, "attachToRole", [role])

    @jsii.member(jsii_name="attachToUser")
    def attach_to_user(self, user: "User") -> None:
        return jsii.invoke(self, "attachToUser", [user])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="document")
    def document(self) -> "PolicyDocument":
        return jsii.get(self, "document")

    @property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> str:
        return jsii.get(self, "policyName")


class PolicyDocument(aws_cdk.cdk.Token, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.PolicyDocument"):
    def __init__(self, base_document: typing.Any=None) -> None:
        jsii.create(PolicyDocument, self, [base_document])

    @jsii.member(jsii_name="addStatement")
    def add_statement(self, statement: "PolicyStatement") -> "PolicyDocument":
        return jsii.invoke(self, "addStatement", [statement])

    @jsii.member(jsii_name="resolve")
    def resolve(self, *, prefix: typing.List[str], scope: aws_cdk.cdk.IConstruct) -> typing.Any:
        _context: aws_cdk.cdk.ResolveContext = {"prefix": prefix, "scope": scope}

        return jsii.invoke(self, "resolve", [_context])

    @property
    @jsii.member(jsii_name="isEmpty")
    def is_empty(self) -> bool:
        return jsii.get(self, "isEmpty")

    @property
    @jsii.member(jsii_name="statementCount")
    def statement_count(self) -> jsii.Number:
        return jsii.get(self, "statementCount")

    @property
    @jsii.member(jsii_name="baseDocument")
    def base_document(self) -> typing.Any:
        return jsii.get(self, "baseDocument")


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.PolicyProps")
class PolicyProps(jsii.compat.TypedDict, total=False):
    groups: typing.List["Group"]
    policyName: str
    roles: typing.List["IRole"]
    statements: typing.List["PolicyStatement"]
    users: typing.List["User"]

class PolicyStatement(aws_cdk.cdk.Token, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.PolicyStatement"):
    def __init__(self, effect: typing.Optional["PolicyStatementEffect"]=None) -> None:
        jsii.create(PolicyStatement, self, [effect])

    @jsii.member(jsii_name="addAccountRootPrincipal")
    def add_account_root_principal(self) -> "PolicyStatement":
        return jsii.invoke(self, "addAccountRootPrincipal", [])

    @jsii.member(jsii_name="addAction")
    def add_action(self, action: str) -> "PolicyStatement":
        return jsii.invoke(self, "addAction", [action])

    @jsii.member(jsii_name="addActions")
    def add_actions(self, *actions: str) -> "PolicyStatement":
        return jsii.invoke(self, "addActions", [actions])

    @jsii.member(jsii_name="addAllResources")
    def add_all_resources(self) -> "PolicyStatement":
        return jsii.invoke(self, "addAllResources", [])

    @jsii.member(jsii_name="addAnyPrincipal")
    def add_any_principal(self) -> "PolicyStatement":
        return jsii.invoke(self, "addAnyPrincipal", [])

    @jsii.member(jsii_name="addArnPrincipal")
    def add_arn_principal(self, arn: str) -> "PolicyStatement":
        return jsii.invoke(self, "addArnPrincipal", [arn])

    @jsii.member(jsii_name="addAwsAccountPrincipal")
    def add_aws_account_principal(self, account_id: str) -> "PolicyStatement":
        return jsii.invoke(self, "addAwsAccountPrincipal", [account_id])

    @jsii.member(jsii_name="addAwsPrincipal")
    def add_aws_principal(self, arn: str) -> "PolicyStatement":
        return jsii.invoke(self, "addAwsPrincipal", [arn])

    @jsii.member(jsii_name="addCanonicalUserPrincipal")
    def add_canonical_user_principal(self, canonical_user_id: str) -> "PolicyStatement":
        return jsii.invoke(self, "addCanonicalUserPrincipal", [canonical_user_id])

    @jsii.member(jsii_name="addCondition")
    def add_condition(self, key: str, value: typing.Any) -> "PolicyStatement":
        return jsii.invoke(self, "addCondition", [key, value])

    @jsii.member(jsii_name="addConditions")
    def add_conditions(self, conditions: typing.Mapping[str,typing.Any]) -> "PolicyStatement":
        return jsii.invoke(self, "addConditions", [conditions])

    @jsii.member(jsii_name="addFederatedPrincipal")
    def add_federated_principal(self, federated: typing.Any, conditions: typing.Mapping[str,typing.Any]) -> "PolicyStatement":
        return jsii.invoke(self, "addFederatedPrincipal", [federated, conditions])

    @jsii.member(jsii_name="addPrincipal")
    def add_principal(self, principal: "IPrincipal") -> "PolicyStatement":
        return jsii.invoke(self, "addPrincipal", [principal])

    @jsii.member(jsii_name="addResource")
    def add_resource(self, arn: str) -> "PolicyStatement":
        return jsii.invoke(self, "addResource", [arn])

    @jsii.member(jsii_name="addResources")
    def add_resources(self, *arns: str) -> "PolicyStatement":
        return jsii.invoke(self, "addResources", [arns])

    @jsii.member(jsii_name="addServicePrincipal")
    def add_service_principal(self, service: str, *, region: typing.Optional[str]=None) -> "PolicyStatement":
        opts: ServicePrincipalOpts = {}

        if region is not None:
            opts["region"] = region

        return jsii.invoke(self, "addServicePrincipal", [service, opts])

    @jsii.member(jsii_name="allow")
    def allow(self) -> "PolicyStatement":
        return jsii.invoke(self, "allow", [])

    @jsii.member(jsii_name="deny")
    def deny(self) -> "PolicyStatement":
        return jsii.invoke(self, "deny", [])

    @jsii.member(jsii_name="describe")
    def describe(self, sid: str) -> "PolicyStatement":
        return jsii.invoke(self, "describe", [sid])

    @jsii.member(jsii_name="limitToAccount")
    def limit_to_account(self, account_id: str) -> "PolicyStatement":
        return jsii.invoke(self, "limitToAccount", [account_id])

    @jsii.member(jsii_name="resolve")
    def resolve(self, *, prefix: typing.List[str], scope: aws_cdk.cdk.IConstruct) -> typing.Any:
        _context: aws_cdk.cdk.ResolveContext = {"prefix": prefix, "scope": scope}

        return jsii.invoke(self, "resolve", [_context])

    @jsii.member(jsii_name="setCondition")
    def set_condition(self, key: str, value: typing.Any) -> "PolicyStatement":
        return jsii.invoke(self, "setCondition", [key, value])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.Any:
        return jsii.invoke(self, "toJson", [])

    @property
    @jsii.member(jsii_name="hasPrincipal")
    def has_principal(self) -> bool:
        return jsii.get(self, "hasPrincipal")

    @property
    @jsii.member(jsii_name="hasResource")
    def has_resource(self) -> bool:
        return jsii.get(self, "hasResource")


@jsii.enum(jsii_type="@aws-cdk/aws-iam.PolicyStatementEffect")
class PolicyStatementEffect(enum.Enum):
    Allow = "Allow"
    Deny = "Deny"

@jsii.implements(IPrincipal)
class PrincipalBase(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-iam.PrincipalBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _PrincipalBaseProxy

    def __init__(self) -> None:
        jsii.create(PrincipalBase, self, [])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, _statement: "PolicyStatement") -> bool:
        return jsii.invoke(self, "addToPolicy", [_statement])

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Mapping[str,typing.List[str]]:
        return jsii.invoke(self, "toJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        return jsii.get(self, "assumeRoleAction")

    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        return jsii.get(self, "grantPrincipal")

    @property
    @jsii.member(jsii_name="policyFragment")
    @abc.abstractmethod
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        ...


class _PrincipalBaseProxy(PrincipalBase):
    @property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        return jsii.get(self, "policyFragment")


class ArnPrincipal(PrincipalBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.ArnPrincipal"):
    def __init__(self, arn: str) -> None:
        jsii.create(ArnPrincipal, self, [arn])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="arn")
    def arn(self) -> str:
        return jsii.get(self, "arn")

    @property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        return jsii.get(self, "policyFragment")


class AccountPrincipal(ArnPrincipal, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.AccountPrincipal"):
    def __init__(self, account_id: typing.Any) -> None:
        jsii.create(AccountPrincipal, self, [account_id])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> typing.Any:
        return jsii.get(self, "accountId")


class AccountRootPrincipal(AccountPrincipal, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.AccountRootPrincipal"):
    def __init__(self) -> None:
        jsii.create(AccountRootPrincipal, self, [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])


class AnyPrincipal(ArnPrincipal, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.AnyPrincipal"):
    def __init__(self) -> None:
        jsii.create(AnyPrincipal, self, [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])


class Anyone(AnyPrincipal, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.Anyone"):
    def __init__(self) -> None:
        jsii.create(Anyone, self, [])


class CanonicalUserPrincipal(PrincipalBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CanonicalUserPrincipal"):
    def __init__(self, canonical_user_id: str) -> None:
        jsii.create(CanonicalUserPrincipal, self, [canonical_user_id])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canonicalUserId")
    def canonical_user_id(self) -> str:
        return jsii.get(self, "canonicalUserId")

    @property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        return jsii.get(self, "policyFragment")


class CompositePrincipal(PrincipalBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CompositePrincipal"):
    def __init__(self, principal: "PrincipalBase", *additional_principals: "PrincipalBase") -> None:
        jsii.create(CompositePrincipal, self, [principal, additional_principals])

    @jsii.member(jsii_name="addPrincipals")
    def add_principals(self, *principals: "PrincipalBase") -> "CompositePrincipal":
        return jsii.invoke(self, "addPrincipals", [principals])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        return jsii.get(self, "assumeRoleAction")

    @property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        return jsii.get(self, "policyFragment")


class FederatedPrincipal(PrincipalBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.FederatedPrincipal"):
    def __init__(self, federated: str, conditions: typing.Mapping[str,typing.Any], assume_role_action: typing.Optional[str]=None) -> None:
        jsii.create(FederatedPrincipal, self, [federated, conditions, assume_role_action])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        return jsii.get(self, "assumeRoleAction")

    @property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "conditions")

    @property
    @jsii.member(jsii_name="federated")
    def federated(self) -> str:
        return jsii.get(self, "federated")

    @property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        return jsii.get(self, "policyFragment")


class OrganizationPrincipal(PrincipalBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.OrganizationPrincipal"):
    def __init__(self, organization_id: str) -> None:
        jsii.create(OrganizationPrincipal, self, [organization_id])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> str:
        return jsii.get(self, "organizationId")

    @property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        return jsii.get(self, "policyFragment")


class PrincipalPolicyFragment(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.PrincipalPolicyFragment"):
    def __init__(self, principal_json: typing.Mapping[str,typing.List[str]], conditions: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        jsii.create(PrincipalPolicyFragment, self, [principal_json, conditions])

    @property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "conditions")

    @property
    @jsii.member(jsii_name="principalJson")
    def principal_json(self) -> typing.Mapping[str,typing.List[str]]:
        return jsii.get(self, "principalJson")


@jsii.implements(IRole)
class Role(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.Role"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, assumed_by: "IPrincipal", external_id: typing.Optional[str]=None, inline_policies: typing.Optional[typing.Mapping[str,"PolicyDocument"]]=None, managed_policy_arns: typing.Optional[typing.List[str]]=None, max_session_duration_sec: typing.Optional[jsii.Number]=None, path: typing.Optional[str]=None, role_name: typing.Optional[str]=None) -> None:
        props: RoleProps = {"assumedBy": assumed_by}

        if external_id is not None:
            props["externalId"] = external_id

        if inline_policies is not None:
            props["inlinePolicies"] = inline_policies

        if managed_policy_arns is not None:
            props["managedPolicyArns"] = managed_policy_arns

        if max_session_duration_sec is not None:
            props["maxSessionDurationSec"] = max_session_duration_sec

        if path is not None:
            props["path"] = path

        if role_name is not None:
            props["roleName"] = role_name

        jsii.create(Role, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, role_arn: str, role_id: typing.Optional[str]=None) -> "IRole":
        props: RoleImportProps = {"roleArn": role_arn}

        if role_id is not None:
            props["roleId"] = role_id

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> bool:
        return jsii.invoke(self, "addToPolicy", [statement])

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: "Policy") -> None:
        return jsii.invoke(self, "attachInlinePolicy", [policy])

    @jsii.member(jsii_name="attachManagedPolicy")
    def attach_managed_policy(self, arn: str) -> None:
        return jsii.invoke(self, "attachManagedPolicy", [arn])

    @jsii.member(jsii_name="export")
    def export(self) -> "RoleImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: "IPrincipal", *actions: str) -> "Grant":
        return jsii.invoke(self, "grant", [grantee, actions])

    @jsii.member(jsii_name="grantPassRole")
    def grant_pass_role(self, identity: "IPrincipal") -> "Grant":
        return jsii.invoke(self, "grantPassRole", [identity])

    @property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        return jsii.get(self, "assumeRoleAction")

    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        return jsii.get(self, "grantPrincipal")

    @property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        return jsii.get(self, "policyFragment")

    @property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        return jsii.get(self, "roleArn")

    @property
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> str:
        return jsii.get(self, "roleId")

    @property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> str:
        return jsii.get(self, "roleName")

    @property
    @jsii.member(jsii_name="assumeRolePolicy")
    def assume_role_policy(self) -> typing.Optional["PolicyDocument"]:
        return jsii.get(self, "assumeRolePolicy")


class _RoleImportProps(jsii.compat.TypedDict, total=False):
    roleId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-iam.RoleImportProps")
class RoleImportProps(_RoleImportProps):
    roleArn: str

class _RoleProps(jsii.compat.TypedDict, total=False):
    externalId: str
    inlinePolicies: typing.Mapping[str,"PolicyDocument"]
    managedPolicyArns: typing.List[str]
    maxSessionDurationSec: jsii.Number
    path: str
    roleName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-iam.RoleProps")
class RoleProps(_RoleProps):
    assumedBy: "IPrincipal"

class ServicePrincipal(PrincipalBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.ServicePrincipal"):
    def __init__(self, service: str, *, region: typing.Optional[str]=None) -> None:
        opts: ServicePrincipalOpts = {}

        if region is not None:
            opts["region"] = region

        jsii.create(ServicePrincipal, self, [service, opts])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="opts")
    def opts(self) -> "ServicePrincipalOpts":
        return jsii.get(self, "opts")

    @property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        return jsii.get(self, "policyFragment")

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> str:
        return jsii.get(self, "service")


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.ServicePrincipalOpts")
class ServicePrincipalOpts(jsii.compat.TypedDict, total=False):
    region: str

@jsii.implements(IIdentity)
class User(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.User"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, groups: typing.Optional[typing.List["Group"]]=None, managed_policy_arns: typing.Optional[typing.List[typing.Any]]=None, password: typing.Optional[aws_cdk.cdk.SecretValue]=None, password_reset_required: typing.Optional[bool]=None, path: typing.Optional[str]=None, user_name: typing.Optional[str]=None) -> None:
        props: UserProps = {}

        if groups is not None:
            props["groups"] = groups

        if managed_policy_arns is not None:
            props["managedPolicyArns"] = managed_policy_arns

        if password is not None:
            props["password"] = password

        if password_reset_required is not None:
            props["passwordResetRequired"] = password_reset_required

        if path is not None:
            props["path"] = path

        if user_name is not None:
            props["userName"] = user_name

        jsii.create(User, self, [scope, id, props])

    @jsii.member(jsii_name="addToGroup")
    def add_to_group(self, group: "Group") -> None:
        return jsii.invoke(self, "addToGroup", [group])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> bool:
        return jsii.invoke(self, "addToPolicy", [statement])

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: "Policy") -> None:
        return jsii.invoke(self, "attachInlinePolicy", [policy])

    @jsii.member(jsii_name="attachManagedPolicy")
    def attach_managed_policy(self, arn: str) -> None:
        return jsii.invoke(self, "attachManagedPolicy", [arn])

    @property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        return jsii.get(self, "assumeRoleAction")

    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        return jsii.get(self, "grantPrincipal")

    @property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        return jsii.get(self, "policyFragment")

    @property
    @jsii.member(jsii_name="userArn")
    def user_arn(self) -> str:
        return jsii.get(self, "userArn")

    @property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> str:
        return jsii.get(self, "userName")


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.UserProps")
class UserProps(jsii.compat.TypedDict, total=False):
    groups: typing.List["Group"]
    managedPolicyArns: typing.List[typing.Any]
    password: aws_cdk.cdk.SecretValue
    passwordResetRequired: bool
    path: str
    userName: str

__all__ = ["AccountPrincipal", "AccountRootPrincipal", "AnyPrincipal", "Anyone", "ArnPrincipal", "AwsManagedPolicy", "CanonicalUserPrincipal", "CfnAccessKey", "CfnAccessKeyProps", "CfnGroup", "CfnGroupProps", "CfnInstanceProfile", "CfnInstanceProfileProps", "CfnManagedPolicy", "CfnManagedPolicyProps", "CfnPolicy", "CfnPolicyProps", "CfnRole", "CfnRoleProps", "CfnServiceLinkedRole", "CfnServiceLinkedRoleProps", "CfnUser", "CfnUserProps", "CfnUserToGroupAddition", "CfnUserToGroupAdditionProps", "CommonGrantOptions", "CompositePrincipal", "FederatedPrincipal", "Grant", "GrantOnPrincipalAndResourceOptions", "GrantOnPrincipalOptions", "GrantWithResourceOptions", "Group", "GroupProps", "IGrantable", "IIdentity", "IPrincipal", "IResourceWithPolicy", "IRole", "ImportedResourcePrincipal", "ImportedResourcePrincipalProps", "LazyRole", "OrganizationPrincipal", "Policy", "PolicyDocument", "PolicyProps", "PolicyStatement", "PolicyStatementEffect", "PrincipalBase", "PrincipalPolicyFragment", "Role", "RoleImportProps", "RoleProps", "ServicePrincipal", "ServicePrincipalOpts", "User", "UserProps", "__jsii_assembly__"]

publication.publish()
