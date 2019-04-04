import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-cognito", "0.28.0", __name__, "aws-cognito@0.28.0.jsii.tgz")
@jsii.enum(jsii_type="@aws-cdk/aws-cognito.AuthFlow")
class AuthFlow(enum.Enum):
    AdminNoSrp = "AdminNoSrp"
    CustomFlowOnly = "CustomFlowOnly"
    UserPassword = "UserPassword"

class CfnIdentityPool(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnIdentityPool"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, allow_unauthenticated_identities: typing.Union[bool, aws_cdk.cdk.Token], cognito_events: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, cognito_identity_providers: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CognitoIdentityProviderProperty"]]]]=None, cognito_streams: typing.Optional[typing.Union[aws_cdk.cdk.Token, "CognitoStreamsProperty"]]=None, developer_provider_name: typing.Optional[str]=None, identity_pool_name: typing.Optional[str]=None, open_id_connect_provider_arns: typing.Optional[typing.List[str]]=None, push_sync: typing.Optional[typing.Union[aws_cdk.cdk.Token, "PushSyncProperty"]]=None, saml_provider_arns: typing.Optional[typing.List[str]]=None, supported_login_providers: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None) -> None:
        props: CfnIdentityPoolProps = {"allowUnauthenticatedIdentities": allow_unauthenticated_identities}

        if cognito_events is not None:
            props["cognitoEvents"] = cognito_events

        if cognito_identity_providers is not None:
            props["cognitoIdentityProviders"] = cognito_identity_providers

        if cognito_streams is not None:
            props["cognitoStreams"] = cognito_streams

        if developer_provider_name is not None:
            props["developerProviderName"] = developer_provider_name

        if identity_pool_name is not None:
            props["identityPoolName"] = identity_pool_name

        if open_id_connect_provider_arns is not None:
            props["openIdConnectProviderArns"] = open_id_connect_provider_arns

        if push_sync is not None:
            props["pushSync"] = push_sync

        if saml_provider_arns is not None:
            props["samlProviderArns"] = saml_provider_arns

        if supported_login_providers is not None:
            props["supportedLoginProviders"] = supported_login_providers

        jsii.create(CfnIdentityPool, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="identityPoolId")
    def identity_pool_id(self) -> str:
        return jsii.get(self, "identityPoolId")

    @property
    @jsii.member(jsii_name="identityPoolName")
    def identity_pool_name(self) -> str:
        return jsii.get(self, "identityPoolName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnIdentityPoolProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnIdentityPool.CognitoIdentityProviderProperty")
    class CognitoIdentityProviderProperty(jsii.compat.TypedDict, total=False):
        clientId: str
        providerName: str
        serverSideTokenCheck: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnIdentityPool.CognitoStreamsProperty")
    class CognitoStreamsProperty(jsii.compat.TypedDict, total=False):
        roleArn: str
        streamingStatus: str
        streamName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnIdentityPool.PushSyncProperty")
    class PushSyncProperty(jsii.compat.TypedDict, total=False):
        applicationArns: typing.List[str]
        roleArn: str


class _CfnIdentityPoolProps(jsii.compat.TypedDict, total=False):
    cognitoEvents: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    cognitoIdentityProviders: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnIdentityPool.CognitoIdentityProviderProperty"]]]
    cognitoStreams: typing.Union[aws_cdk.cdk.Token, "CfnIdentityPool.CognitoStreamsProperty"]
    developerProviderName: str
    identityPoolName: str
    openIdConnectProviderArns: typing.List[str]
    pushSync: typing.Union[aws_cdk.cdk.Token, "CfnIdentityPool.PushSyncProperty"]
    samlProviderArns: typing.List[str]
    supportedLoginProviders: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolProps")
class CfnIdentityPoolProps(_CfnIdentityPoolProps):
    allowUnauthenticatedIdentities: typing.Union[bool, aws_cdk.cdk.Token]

class CfnIdentityPoolRoleAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolRoleAttachment"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, identity_pool_id: str, role_mappings: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,typing.Union[aws_cdk.cdk.Token, "RoleMappingProperty"]]]]=None, roles: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None) -> None:
        props: CfnIdentityPoolRoleAttachmentProps = {"identityPoolId": identity_pool_id}

        if role_mappings is not None:
            props["roleMappings"] = role_mappings

        if roles is not None:
            props["roles"] = roles

        jsii.create(CfnIdentityPoolRoleAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="identityPoolRoleAttachmentId")
    def identity_pool_role_attachment_id(self) -> str:
        return jsii.get(self, "identityPoolRoleAttachmentId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnIdentityPoolRoleAttachmentProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolRoleAttachment.MappingRuleProperty")
    class MappingRuleProperty(jsii.compat.TypedDict):
        claim: str
        matchType: str
        roleArn: str
        value: str

    class _RoleMappingProperty(jsii.compat.TypedDict, total=False):
        ambiguousRoleResolution: str
        rulesConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnIdentityPoolRoleAttachment.RulesConfigurationTypeProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolRoleAttachment.RoleMappingProperty")
    class RoleMappingProperty(_RoleMappingProperty):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolRoleAttachment.RulesConfigurationTypeProperty")
    class RulesConfigurationTypeProperty(jsii.compat.TypedDict):
        rules: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnIdentityPoolRoleAttachment.MappingRuleProperty"]]]


class _CfnIdentityPoolRoleAttachmentProps(jsii.compat.TypedDict, total=False):
    roleMappings: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,typing.Union[aws_cdk.cdk.Token, "CfnIdentityPoolRoleAttachment.RoleMappingProperty"]]]
    roles: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolRoleAttachmentProps")
class CfnIdentityPoolRoleAttachmentProps(_CfnIdentityPoolRoleAttachmentProps):
    identityPoolId: str

class CfnUserPool(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnUserPool"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, admin_create_user_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "AdminCreateUserConfigProperty"]]=None, alias_attributes: typing.Optional[typing.List[str]]=None, auto_verified_attributes: typing.Optional[typing.List[str]]=None, device_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "DeviceConfigurationProperty"]]=None, email_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "EmailConfigurationProperty"]]=None, email_verification_message: typing.Optional[str]=None, email_verification_subject: typing.Optional[str]=None, lambda_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LambdaConfigProperty"]]=None, mfa_configuration: typing.Optional[str]=None, policies: typing.Optional[typing.Union[aws_cdk.cdk.Token, "PoliciesProperty"]]=None, schema: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "SchemaAttributeProperty"]]]]=None, sms_authentication_message: typing.Optional[str]=None, sms_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "SmsConfigurationProperty"]]=None, sms_verification_message: typing.Optional[str]=None, username_attributes: typing.Optional[typing.List[str]]=None, user_pool_name: typing.Optional[str]=None, user_pool_tags: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None) -> None:
        props: CfnUserPoolProps = {}

        if admin_create_user_config is not None:
            props["adminCreateUserConfig"] = admin_create_user_config

        if alias_attributes is not None:
            props["aliasAttributes"] = alias_attributes

        if auto_verified_attributes is not None:
            props["autoVerifiedAttributes"] = auto_verified_attributes

        if device_configuration is not None:
            props["deviceConfiguration"] = device_configuration

        if email_configuration is not None:
            props["emailConfiguration"] = email_configuration

        if email_verification_message is not None:
            props["emailVerificationMessage"] = email_verification_message

        if email_verification_subject is not None:
            props["emailVerificationSubject"] = email_verification_subject

        if lambda_config is not None:
            props["lambdaConfig"] = lambda_config

        if mfa_configuration is not None:
            props["mfaConfiguration"] = mfa_configuration

        if policies is not None:
            props["policies"] = policies

        if schema is not None:
            props["schema"] = schema

        if sms_authentication_message is not None:
            props["smsAuthenticationMessage"] = sms_authentication_message

        if sms_configuration is not None:
            props["smsConfiguration"] = sms_configuration

        if sms_verification_message is not None:
            props["smsVerificationMessage"] = sms_verification_message

        if username_attributes is not None:
            props["usernameAttributes"] = username_attributes

        if user_pool_name is not None:
            props["userPoolName"] = user_pool_name

        if user_pool_tags is not None:
            props["userPoolTags"] = user_pool_tags

        jsii.create(CfnUserPool, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnUserPoolProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="userPoolArn")
    def user_pool_arn(self) -> str:
        return jsii.get(self, "userPoolArn")

    @property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> str:
        return jsii.get(self, "userPoolId")

    @property
    @jsii.member(jsii_name="userPoolProviderName")
    def user_pool_provider_name(self) -> str:
        return jsii.get(self, "userPoolProviderName")

    @property
    @jsii.member(jsii_name="userPoolProviderUrl")
    def user_pool_provider_url(self) -> str:
        return jsii.get(self, "userPoolProviderUrl")

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.AdminCreateUserConfigProperty")
    class AdminCreateUserConfigProperty(jsii.compat.TypedDict, total=False):
        allowAdminCreateUserOnly: typing.Union[bool, aws_cdk.cdk.Token]
        inviteMessageTemplate: typing.Union[aws_cdk.cdk.Token, "CfnUserPool.InviteMessageTemplateProperty"]
        unusedAccountValidityDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.DeviceConfigurationProperty")
    class DeviceConfigurationProperty(jsii.compat.TypedDict, total=False):
        challengeRequiredOnNewDevice: typing.Union[bool, aws_cdk.cdk.Token]
        deviceOnlyRememberedOnUserPrompt: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.EmailConfigurationProperty")
    class EmailConfigurationProperty(jsii.compat.TypedDict, total=False):
        replyToEmailAddress: str
        sourceArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.InviteMessageTemplateProperty")
    class InviteMessageTemplateProperty(jsii.compat.TypedDict, total=False):
        emailMessage: str
        emailSubject: str
        smsMessage: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.LambdaConfigProperty")
    class LambdaConfigProperty(jsii.compat.TypedDict, total=False):
        createAuthChallenge: str
        customMessage: str
        defineAuthChallenge: str
        postAuthentication: str
        postConfirmation: str
        preAuthentication: str
        preSignUp: str
        verifyAuthChallengeResponse: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.NumberAttributeConstraintsProperty")
    class NumberAttributeConstraintsProperty(jsii.compat.TypedDict, total=False):
        maxValue: str
        minValue: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.PasswordPolicyProperty")
    class PasswordPolicyProperty(jsii.compat.TypedDict, total=False):
        minimumLength: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        requireLowercase: typing.Union[bool, aws_cdk.cdk.Token]
        requireNumbers: typing.Union[bool, aws_cdk.cdk.Token]
        requireSymbols: typing.Union[bool, aws_cdk.cdk.Token]
        requireUppercase: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.PoliciesProperty")
    class PoliciesProperty(jsii.compat.TypedDict, total=False):
        passwordPolicy: typing.Union[aws_cdk.cdk.Token, "CfnUserPool.PasswordPolicyProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.SchemaAttributeProperty")
    class SchemaAttributeProperty(jsii.compat.TypedDict, total=False):
        attributeDataType: str
        developerOnlyAttribute: typing.Union[bool, aws_cdk.cdk.Token]
        mutable: typing.Union[bool, aws_cdk.cdk.Token]
        name: str
        numberAttributeConstraints: typing.Union[aws_cdk.cdk.Token, "CfnUserPool.NumberAttributeConstraintsProperty"]
        required: typing.Union[bool, aws_cdk.cdk.Token]
        stringAttributeConstraints: typing.Union[aws_cdk.cdk.Token, "CfnUserPool.StringAttributeConstraintsProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.SmsConfigurationProperty")
    class SmsConfigurationProperty(jsii.compat.TypedDict, total=False):
        externalId: str
        snsCallerArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPool.StringAttributeConstraintsProperty")
    class StringAttributeConstraintsProperty(jsii.compat.TypedDict, total=False):
        maxLength: str
        minLength: str


class CfnUserPoolClient(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnUserPoolClient"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, user_pool_id: str, client_name: typing.Optional[str]=None, explicit_auth_flows: typing.Optional[typing.List[str]]=None, generate_secret: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, read_attributes: typing.Optional[typing.List[str]]=None, refresh_token_validity: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, write_attributes: typing.Optional[typing.List[str]]=None) -> None:
        props: CfnUserPoolClientProps = {"userPoolId": user_pool_id}

        if client_name is not None:
            props["clientName"] = client_name

        if explicit_auth_flows is not None:
            props["explicitAuthFlows"] = explicit_auth_flows

        if generate_secret is not None:
            props["generateSecret"] = generate_secret

        if read_attributes is not None:
            props["readAttributes"] = read_attributes

        if refresh_token_validity is not None:
            props["refreshTokenValidity"] = refresh_token_validity

        if write_attributes is not None:
            props["writeAttributes"] = write_attributes

        jsii.create(CfnUserPoolClient, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnUserPoolClientProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="userPoolClientClientSecret")
    def user_pool_client_client_secret(self) -> str:
        return jsii.get(self, "userPoolClientClientSecret")

    @property
    @jsii.member(jsii_name="userPoolClientId")
    def user_pool_client_id(self) -> str:
        return jsii.get(self, "userPoolClientId")

    @property
    @jsii.member(jsii_name="userPoolClientName")
    def user_pool_client_name(self) -> str:
        return jsii.get(self, "userPoolClientName")


class _CfnUserPoolClientProps(jsii.compat.TypedDict, total=False):
    clientName: str
    explicitAuthFlows: typing.List[str]
    generateSecret: typing.Union[bool, aws_cdk.cdk.Token]
    readAttributes: typing.List[str]
    refreshTokenValidity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    writeAttributes: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolClientProps")
class CfnUserPoolClientProps(_CfnUserPoolClientProps):
    userPoolId: str

class CfnUserPoolGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnUserPoolGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, user_pool_id: str, description: typing.Optional[str]=None, group_name: typing.Optional[str]=None, precedence: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, role_arn: typing.Optional[str]=None) -> None:
        props: CfnUserPoolGroupProps = {"userPoolId": user_pool_id}

        if description is not None:
            props["description"] = description

        if group_name is not None:
            props["groupName"] = group_name

        if precedence is not None:
            props["precedence"] = precedence

        if role_arn is not None:
            props["roleArn"] = role_arn

        jsii.create(CfnUserPoolGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnUserPoolGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="userPoolGroupName")
    def user_pool_group_name(self) -> str:
        return jsii.get(self, "userPoolGroupName")


class _CfnUserPoolGroupProps(jsii.compat.TypedDict, total=False):
    description: str
    groupName: str
    precedence: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    roleArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolGroupProps")
class CfnUserPoolGroupProps(_CfnUserPoolGroupProps):
    userPoolId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolProps")
class CfnUserPoolProps(jsii.compat.TypedDict, total=False):
    adminCreateUserConfig: typing.Union[aws_cdk.cdk.Token, "CfnUserPool.AdminCreateUserConfigProperty"]
    aliasAttributes: typing.List[str]
    autoVerifiedAttributes: typing.List[str]
    deviceConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnUserPool.DeviceConfigurationProperty"]
    emailConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnUserPool.EmailConfigurationProperty"]
    emailVerificationMessage: str
    emailVerificationSubject: str
    lambdaConfig: typing.Union[aws_cdk.cdk.Token, "CfnUserPool.LambdaConfigProperty"]
    mfaConfiguration: str
    policies: typing.Union[aws_cdk.cdk.Token, "CfnUserPool.PoliciesProperty"]
    schema: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnUserPool.SchemaAttributeProperty"]]]
    smsAuthenticationMessage: str
    smsConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnUserPool.SmsConfigurationProperty"]
    smsVerificationMessage: str
    usernameAttributes: typing.List[str]
    userPoolName: str
    userPoolTags: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

class CfnUserPoolUser(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUser"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, user_pool_id: str, desired_delivery_mediums: typing.Optional[typing.List[str]]=None, force_alias_creation: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, message_action: typing.Optional[str]=None, user_attributes: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "AttributeTypeProperty"]]]]=None, username: typing.Optional[str]=None, validation_data: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "AttributeTypeProperty"]]]]=None) -> None:
        props: CfnUserPoolUserProps = {"userPoolId": user_pool_id}

        if desired_delivery_mediums is not None:
            props["desiredDeliveryMediums"] = desired_delivery_mediums

        if force_alias_creation is not None:
            props["forceAliasCreation"] = force_alias_creation

        if message_action is not None:
            props["messageAction"] = message_action

        if user_attributes is not None:
            props["userAttributes"] = user_attributes

        if username is not None:
            props["username"] = username

        if validation_data is not None:
            props["validationData"] = validation_data

        jsii.create(CfnUserPoolUser, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnUserPoolUserProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="userPoolUserName")
    def user_pool_user_name(self) -> str:
        return jsii.get(self, "userPoolUserName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUser.AttributeTypeProperty")
    class AttributeTypeProperty(jsii.compat.TypedDict, total=False):
        name: str
        value: str


class _CfnUserPoolUserProps(jsii.compat.TypedDict, total=False):
    desiredDeliveryMediums: typing.List[str]
    forceAliasCreation: typing.Union[bool, aws_cdk.cdk.Token]
    messageAction: str
    userAttributes: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnUserPoolUser.AttributeTypeProperty"]]]
    username: str
    validationData: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnUserPoolUser.AttributeTypeProperty"]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUserProps")
class CfnUserPoolUserProps(_CfnUserPoolUserProps):
    userPoolId: str

class CfnUserPoolUserToGroupAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUserToGroupAttachment"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, group_name: str, username: str, user_pool_id: str) -> None:
        props: CfnUserPoolUserToGroupAttachmentProps = {"groupName": group_name, "username": username, "userPoolId": user_pool_id}

        jsii.create(CfnUserPoolUserToGroupAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnUserPoolUserToGroupAttachmentProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="userPoolUserToGroupAttachmentId")
    def user_pool_user_to_group_attachment_id(self) -> str:
        return jsii.get(self, "userPoolUserToGroupAttachmentId")


@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUserToGroupAttachmentProps")
class CfnUserPoolUserToGroupAttachmentProps(jsii.compat.TypedDict):
    groupName: str
    username: str
    userPoolId: str

@jsii.interface(jsii_type="@aws-cdk/aws-cognito.IUserPool")
class IUserPool(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IUserPoolProxy

    @property
    @jsii.member(jsii_name="userPoolArn")
    def user_pool_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="userPoolProviderName")
    def user_pool_provider_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="userPoolProviderUrl")
    def user_pool_provider_url(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "UserPoolImportProps":
        ...


class _IUserPoolProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-cognito.IUserPool"
    @property
    @jsii.member(jsii_name="userPoolArn")
    def user_pool_arn(self) -> str:
        return jsii.get(self, "userPoolArn")

    @property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> str:
        return jsii.get(self, "userPoolId")

    @property
    @jsii.member(jsii_name="userPoolProviderName")
    def user_pool_provider_name(self) -> str:
        return jsii.get(self, "userPoolProviderName")

    @property
    @jsii.member(jsii_name="userPoolProviderUrl")
    def user_pool_provider_url(self) -> str:
        return jsii.get(self, "userPoolProviderUrl")

    @jsii.member(jsii_name="export")
    def export(self) -> "UserPoolImportProps":
        return jsii.invoke(self, "export", [])


@jsii.enum(jsii_type="@aws-cdk/aws-cognito.SignInType")
class SignInType(enum.Enum):
    Username = "Username"
    Email = "Email"
    Phone = "Phone"
    EmailOrPhone = "EmailOrPhone"

@jsii.implements(IUserPool)
class UserPool(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.UserPool"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_verified_attributes: typing.Optional[typing.List["UserPoolAttribute"]]=None, lambda_triggers: typing.Optional["UserPoolTriggers"]=None, pool_name: typing.Optional[str]=None, sign_in_type: typing.Optional["SignInType"]=None, username_alias_attributes: typing.Optional[typing.List["UserPoolAttribute"]]=None) -> None:
        props: UserPoolProps = {}

        if auto_verified_attributes is not None:
            props["autoVerifiedAttributes"] = auto_verified_attributes

        if lambda_triggers is not None:
            props["lambdaTriggers"] = lambda_triggers

        if pool_name is not None:
            props["poolName"] = pool_name

        if sign_in_type is not None:
            props["signInType"] = sign_in_type

        if username_alias_attributes is not None:
            props["usernameAliasAttributes"] = username_alias_attributes

        jsii.create(UserPool, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, user_pool_arn: str, user_pool_id: str, user_pool_provider_name: str, user_pool_provider_url: str) -> "IUserPool":
        props: UserPoolImportProps = {"userPoolArn": user_pool_arn, "userPoolId": user_pool_id, "userPoolProviderName": user_pool_provider_name, "userPoolProviderUrl": user_pool_provider_url}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "UserPoolImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="onCreateAuthChallenge")
    def on_create_auth_challenge(self, fn: aws_cdk.aws_lambda.IFunction) -> None:
        return jsii.invoke(self, "onCreateAuthChallenge", [fn])

    @jsii.member(jsii_name="onCustomMessage")
    def on_custom_message(self, fn: aws_cdk.aws_lambda.IFunction) -> None:
        return jsii.invoke(self, "onCustomMessage", [fn])

    @jsii.member(jsii_name="onDefineAuthChallenge")
    def on_define_auth_challenge(self, fn: aws_cdk.aws_lambda.IFunction) -> None:
        return jsii.invoke(self, "onDefineAuthChallenge", [fn])

    @jsii.member(jsii_name="onPostAuthentication")
    def on_post_authentication(self, fn: aws_cdk.aws_lambda.IFunction) -> None:
        return jsii.invoke(self, "onPostAuthentication", [fn])

    @jsii.member(jsii_name="onPostConfirmation")
    def on_post_confirmation(self, fn: aws_cdk.aws_lambda.IFunction) -> None:
        return jsii.invoke(self, "onPostConfirmation", [fn])

    @jsii.member(jsii_name="onPreAuthentication")
    def on_pre_authentication(self, fn: aws_cdk.aws_lambda.IFunction) -> None:
        return jsii.invoke(self, "onPreAuthentication", [fn])

    @jsii.member(jsii_name="onPreSignUp")
    def on_pre_sign_up(self, fn: aws_cdk.aws_lambda.IFunction) -> None:
        return jsii.invoke(self, "onPreSignUp", [fn])

    @jsii.member(jsii_name="onVerifyAuthChallengeResponse")
    def on_verify_auth_challenge_response(self, fn: aws_cdk.aws_lambda.IFunction) -> None:
        return jsii.invoke(self, "onVerifyAuthChallengeResponse", [fn])

    @property
    @jsii.member(jsii_name="userPoolArn")
    def user_pool_arn(self) -> str:
        return jsii.get(self, "userPoolArn")

    @property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> str:
        return jsii.get(self, "userPoolId")

    @property
    @jsii.member(jsii_name="userPoolProviderName")
    def user_pool_provider_name(self) -> str:
        return jsii.get(self, "userPoolProviderName")

    @property
    @jsii.member(jsii_name="userPoolProviderUrl")
    def user_pool_provider_url(self) -> str:
        return jsii.get(self, "userPoolProviderUrl")


@jsii.enum(jsii_type="@aws-cdk/aws-cognito.UserPoolAttribute")
class UserPoolAttribute(enum.Enum):
    Address = "Address"
    Birthdate = "Birthdate"
    Email = "Email"
    FamilyName = "FamilyName"
    Gender = "Gender"
    GivenName = "GivenName"
    Locale = "Locale"
    MiddleName = "MiddleName"
    Name = "Name"
    Nickname = "Nickname"
    PhoneNumber = "PhoneNumber"
    Picture = "Picture"
    PreferredUsername = "PreferredUsername"
    Profile = "Profile"
    Timezone = "Timezone"
    UpdatedAt = "UpdatedAt"
    Website = "Website"

class UserPoolClient(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.UserPoolClient"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, user_pool: "IUserPool", client_name: typing.Optional[str]=None, enabled_auth_flows: typing.Optional[typing.List["AuthFlow"]]=None, generate_secret: typing.Optional[bool]=None) -> None:
        props: UserPoolClientProps = {"userPool": user_pool}

        if client_name is not None:
            props["clientName"] = client_name

        if enabled_auth_flows is not None:
            props["enabledAuthFlows"] = enabled_auth_flows

        if generate_secret is not None:
            props["generateSecret"] = generate_secret

        jsii.create(UserPoolClient, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> str:
        return jsii.get(self, "clientId")


class _UserPoolClientProps(jsii.compat.TypedDict, total=False):
    clientName: str
    enabledAuthFlows: typing.List["AuthFlow"]
    generateSecret: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.UserPoolClientProps")
class UserPoolClientProps(_UserPoolClientProps):
    userPool: "IUserPool"

@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.UserPoolImportProps")
class UserPoolImportProps(jsii.compat.TypedDict):
    userPoolArn: str
    userPoolId: str
    userPoolProviderName: str
    userPoolProviderUrl: str

@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.UserPoolProps")
class UserPoolProps(jsii.compat.TypedDict, total=False):
    autoVerifiedAttributes: typing.List["UserPoolAttribute"]
    lambdaTriggers: "UserPoolTriggers"
    poolName: str
    signInType: "SignInType"
    usernameAliasAttributes: typing.List["UserPoolAttribute"]

@jsii.data_type(jsii_type="@aws-cdk/aws-cognito.UserPoolTriggers")
class UserPoolTriggers(jsii.compat.TypedDict, total=False):
    createAuthChallenge: aws_cdk.aws_lambda.IFunction
    customMessage: aws_cdk.aws_lambda.IFunction
    defineAuthChallenge: aws_cdk.aws_lambda.IFunction
    postAuthentication: aws_cdk.aws_lambda.IFunction
    postConfirmation: aws_cdk.aws_lambda.IFunction
    preAuthentication: aws_cdk.aws_lambda.IFunction
    preSignUp: aws_cdk.aws_lambda.IFunction
    verifyAuthChallengeResponse: aws_cdk.aws_lambda.IFunction

__all__ = ["AuthFlow", "CfnIdentityPool", "CfnIdentityPoolProps", "CfnIdentityPoolRoleAttachment", "CfnIdentityPoolRoleAttachmentProps", "CfnUserPool", "CfnUserPoolClient", "CfnUserPoolClientProps", "CfnUserPoolGroup", "CfnUserPoolGroupProps", "CfnUserPoolProps", "CfnUserPoolUser", "CfnUserPoolUserProps", "CfnUserPoolUserToGroupAttachment", "CfnUserPoolUserToGroupAttachmentProps", "IUserPool", "SignInType", "UserPool", "UserPoolAttribute", "UserPoolClient", "UserPoolClientProps", "UserPoolImportProps", "UserPoolProps", "UserPoolTriggers", "__jsii_assembly__"]

publication.publish()
