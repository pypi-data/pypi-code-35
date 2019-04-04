import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-apigateway", "0.28.0", __name__, "aws-apigateway@0.28.0.jsii.tgz")
@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.ApiKeySourceType")
class ApiKeySourceType(enum.Enum):
    Header = "Header"
    Authorizer = "Authorizer"

@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.AuthorizationType")
class AuthorizationType(enum.Enum):
    None_ = "None"
    IAM = "IAM"
    Custom = "Custom"
    Cognito = "Cognito"

class _AwsIntegrationProps(jsii.compat.TypedDict, total=False):
    action: str
    actionParameters: typing.Mapping[str,str]
    options: "IntegrationOptions"
    path: str
    proxy: bool
    subdomain: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.AwsIntegrationProps")
class AwsIntegrationProps(_AwsIntegrationProps):
    service: str

class CfnAccount(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnAccount"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cloud_watch_role_arn: typing.Optional[str]=None) -> None:
        props: CfnAccountProps = {}

        if cloud_watch_role_arn is not None:
            props["cloudWatchRoleArn"] = cloud_watch_role_arn

        jsii.create(CfnAccount, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> str:
        return jsii.get(self, "accountId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAccountProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnAccountProps")
class CfnAccountProps(jsii.compat.TypedDict, total=False):
    cloudWatchRoleArn: str

class CfnApiKey(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnApiKey"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, customer_id: typing.Optional[str]=None, description: typing.Optional[str]=None, enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, generate_distinct_id: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, name: typing.Optional[str]=None, stage_keys: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "StageKeyProperty"]]]]=None, value: typing.Optional[str]=None) -> None:
        props: CfnApiKeyProps = {}

        if customer_id is not None:
            props["customerId"] = customer_id

        if description is not None:
            props["description"] = description

        if enabled is not None:
            props["enabled"] = enabled

        if generate_distinct_id is not None:
            props["generateDistinctId"] = generate_distinct_id

        if name is not None:
            props["name"] = name

        if stage_keys is not None:
            props["stageKeys"] = stage_keys

        if value is not None:
            props["value"] = value

        jsii.create(CfnApiKey, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="apiKeyId")
    def api_key_id(self) -> str:
        return jsii.get(self, "apiKeyId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApiKeyProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnApiKey.StageKeyProperty")
    class StageKeyProperty(jsii.compat.TypedDict, total=False):
        restApiId: str
        stageName: str


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnApiKeyProps")
class CfnApiKeyProps(jsii.compat.TypedDict, total=False):
    customerId: str
    description: str
    enabled: typing.Union[bool, aws_cdk.cdk.Token]
    generateDistinctId: typing.Union[bool, aws_cdk.cdk.Token]
    name: str
    stageKeys: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApiKey.StageKeyProperty"]]]
    value: str

class CfnApiV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnApiV2"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, protocol_type: str, route_selection_expression: str, api_key_selection_expression: typing.Optional[str]=None, description: typing.Optional[str]=None, disable_schema_validation: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, version: typing.Optional[str]=None) -> None:
        props: CfnApiV2Props = {"name": name, "protocolType": protocol_type, "routeSelectionExpression": route_selection_expression}

        if api_key_selection_expression is not None:
            props["apiKeySelectionExpression"] = api_key_selection_expression

        if description is not None:
            props["description"] = description

        if disable_schema_validation is not None:
            props["disableSchemaValidation"] = disable_schema_validation

        if version is not None:
            props["version"] = version

        jsii.create(CfnApiV2, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        return jsii.get(self, "apiId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApiV2Props":
        return jsii.get(self, "propertyOverrides")


class _CfnApiV2Props(jsii.compat.TypedDict, total=False):
    apiKeySelectionExpression: str
    description: str
    disableSchemaValidation: typing.Union[bool, aws_cdk.cdk.Token]
    version: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnApiV2Props")
class CfnApiV2Props(_CfnApiV2Props):
    name: str
    protocolType: str
    routeSelectionExpression: str

class CfnAuthorizer(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnAuthorizer"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, rest_api_id: str, type: str, authorizer_credentials: typing.Optional[str]=None, authorizer_result_ttl_in_seconds: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, authorizer_uri: typing.Optional[str]=None, auth_type: typing.Optional[str]=None, identity_source: typing.Optional[str]=None, identity_validation_expression: typing.Optional[str]=None, name: typing.Optional[str]=None, provider_arns: typing.Optional[typing.List[str]]=None) -> None:
        props: CfnAuthorizerProps = {"restApiId": rest_api_id, "type": type}

        if authorizer_credentials is not None:
            props["authorizerCredentials"] = authorizer_credentials

        if authorizer_result_ttl_in_seconds is not None:
            props["authorizerResultTtlInSeconds"] = authorizer_result_ttl_in_seconds

        if authorizer_uri is not None:
            props["authorizerUri"] = authorizer_uri

        if auth_type is not None:
            props["authType"] = auth_type

        if identity_source is not None:
            props["identitySource"] = identity_source

        if identity_validation_expression is not None:
            props["identityValidationExpression"] = identity_validation_expression

        if name is not None:
            props["name"] = name

        if provider_arns is not None:
            props["providerArns"] = provider_arns

        jsii.create(CfnAuthorizer, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> str:
        return jsii.get(self, "authorizerId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAuthorizerProps":
        return jsii.get(self, "propertyOverrides")


class _CfnAuthorizerProps(jsii.compat.TypedDict, total=False):
    authorizerCredentials: str
    authorizerResultTtlInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    authorizerUri: str
    authType: str
    identitySource: str
    identityValidationExpression: str
    name: str
    providerArns: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnAuthorizerProps")
class CfnAuthorizerProps(_CfnAuthorizerProps):
    restApiId: str
    type: str

class CfnAuthorizerV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnAuthorizerV2"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api_id: str, authorizer_type: str, authorizer_uri: str, identity_source: typing.List[str], name: str, authorizer_credentials_arn: typing.Optional[str]=None, authorizer_result_ttl_in_seconds: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, identity_validation_expression: typing.Optional[str]=None) -> None:
        props: CfnAuthorizerV2Props = {"apiId": api_id, "authorizerType": authorizer_type, "authorizerUri": authorizer_uri, "identitySource": identity_source, "name": name}

        if authorizer_credentials_arn is not None:
            props["authorizerCredentialsArn"] = authorizer_credentials_arn

        if authorizer_result_ttl_in_seconds is not None:
            props["authorizerResultTtlInSeconds"] = authorizer_result_ttl_in_seconds

        if identity_validation_expression is not None:
            props["identityValidationExpression"] = identity_validation_expression

        jsii.create(CfnAuthorizerV2, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> str:
        return jsii.get(self, "authorizerId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAuthorizerV2Props":
        return jsii.get(self, "propertyOverrides")


class _CfnAuthorizerV2Props(jsii.compat.TypedDict, total=False):
    authorizerCredentialsArn: str
    authorizerResultTtlInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    identityValidationExpression: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnAuthorizerV2Props")
class CfnAuthorizerV2Props(_CfnAuthorizerV2Props):
    apiId: str
    authorizerType: str
    authorizerUri: str
    identitySource: typing.List[str]
    name: str

class CfnBasePathMapping(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnBasePathMapping"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, domain_name: str, base_path: typing.Optional[str]=None, rest_api_id: typing.Optional[str]=None, stage: typing.Optional[str]=None) -> None:
        props: CfnBasePathMappingProps = {"domainName": domain_name}

        if base_path is not None:
            props["basePath"] = base_path

        if rest_api_id is not None:
            props["restApiId"] = rest_api_id

        if stage is not None:
            props["stage"] = stage

        jsii.create(CfnBasePathMapping, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="basePathMappingId")
    def base_path_mapping_id(self) -> str:
        return jsii.get(self, "basePathMappingId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnBasePathMappingProps":
        return jsii.get(self, "propertyOverrides")


class _CfnBasePathMappingProps(jsii.compat.TypedDict, total=False):
    basePath: str
    restApiId: str
    stage: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnBasePathMappingProps")
class CfnBasePathMappingProps(_CfnBasePathMappingProps):
    domainName: str

class CfnClientCertificate(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnClientCertificate"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: typing.Optional[str]=None) -> None:
        props: CfnClientCertificateProps = {}

        if description is not None:
            props["description"] = description

        jsii.create(CfnClientCertificate, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="clientCertificateName")
    def client_certificate_name(self) -> str:
        return jsii.get(self, "clientCertificateName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnClientCertificateProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnClientCertificateProps")
class CfnClientCertificateProps(jsii.compat.TypedDict, total=False):
    description: str

class CfnDeployment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnDeployment"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, rest_api_id: str, deployment_canary_settings: typing.Optional[typing.Union[aws_cdk.cdk.Token, "DeploymentCanarySettingsProperty"]]=None, description: typing.Optional[str]=None, stage_description: typing.Optional[typing.Union[aws_cdk.cdk.Token, "StageDescriptionProperty"]]=None, stage_name: typing.Optional[str]=None) -> None:
        props: CfnDeploymentProps = {"restApiId": rest_api_id}

        if deployment_canary_settings is not None:
            props["deploymentCanarySettings"] = deployment_canary_settings

        if description is not None:
            props["description"] = description

        if stage_description is not None:
            props["stageDescription"] = stage_description

        if stage_name is not None:
            props["stageName"] = stage_name

        jsii.create(CfnDeployment, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> str:
        return jsii.get(self, "deploymentId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDeploymentProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDeployment.AccessLogSettingProperty")
    class AccessLogSettingProperty(jsii.compat.TypedDict, total=False):
        destinationArn: str
        format: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDeployment.CanarySettingProperty")
    class CanarySettingProperty(jsii.compat.TypedDict, total=False):
        percentTraffic: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        stageVariableOverrides: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        useStageCache: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDeployment.DeploymentCanarySettingsProperty")
    class DeploymentCanarySettingsProperty(jsii.compat.TypedDict, total=False):
        percentTraffic: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        stageVariableOverrides: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        useStageCache: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDeployment.MethodSettingProperty")
    class MethodSettingProperty(jsii.compat.TypedDict, total=False):
        cacheDataEncrypted: typing.Union[bool, aws_cdk.cdk.Token]
        cacheTtlInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        cachingEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        dataTraceEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        httpMethod: str
        loggingLevel: str
        metricsEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        resourcePath: str
        throttlingBurstLimit: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        throttlingRateLimit: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDeployment.StageDescriptionProperty")
    class StageDescriptionProperty(jsii.compat.TypedDict, total=False):
        accessLogSetting: typing.Union[aws_cdk.cdk.Token, "CfnDeployment.AccessLogSettingProperty"]
        cacheClusterEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        cacheClusterSize: str
        cacheDataEncrypted: typing.Union[bool, aws_cdk.cdk.Token]
        cacheTtlInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        cachingEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        canarySetting: typing.Union[aws_cdk.cdk.Token, "CfnDeployment.CanarySettingProperty"]
        clientCertificateId: str
        dataTraceEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        description: str
        documentationVersion: str
        loggingLevel: str
        methodSettings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeployment.MethodSettingProperty"]]]
        metricsEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        tags: typing.List[aws_cdk.cdk.CfnTag]
        throttlingBurstLimit: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        throttlingRateLimit: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        tracingEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        variables: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]


class _CfnDeploymentProps(jsii.compat.TypedDict, total=False):
    deploymentCanarySettings: typing.Union[aws_cdk.cdk.Token, "CfnDeployment.DeploymentCanarySettingsProperty"]
    description: str
    stageDescription: typing.Union[aws_cdk.cdk.Token, "CfnDeployment.StageDescriptionProperty"]
    stageName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDeploymentProps")
class CfnDeploymentProps(_CfnDeploymentProps):
    restApiId: str

class CfnDeploymentV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnDeploymentV2"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api_id: str, description: typing.Optional[str]=None, stage_name: typing.Optional[str]=None) -> None:
        props: CfnDeploymentV2Props = {"apiId": api_id}

        if description is not None:
            props["description"] = description

        if stage_name is not None:
            props["stageName"] = stage_name

        jsii.create(CfnDeploymentV2, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> str:
        return jsii.get(self, "deploymentId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDeploymentV2Props":
        return jsii.get(self, "propertyOverrides")


class _CfnDeploymentV2Props(jsii.compat.TypedDict, total=False):
    description: str
    stageName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDeploymentV2Props")
class CfnDeploymentV2Props(_CfnDeploymentV2Props):
    apiId: str

class CfnDocumentationPart(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnDocumentationPart"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, location: typing.Union[aws_cdk.cdk.Token, "LocationProperty"], properties: str, rest_api_id: str) -> None:
        props: CfnDocumentationPartProps = {"location": location, "properties": properties, "restApiId": rest_api_id}

        jsii.create(CfnDocumentationPart, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="documentationPartId")
    def documentation_part_id(self) -> str:
        return jsii.get(self, "documentationPartId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDocumentationPartProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDocumentationPart.LocationProperty")
    class LocationProperty(jsii.compat.TypedDict, total=False):
        method: str
        name: str
        path: str
        statusCode: str
        type: str


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDocumentationPartProps")
class CfnDocumentationPartProps(jsii.compat.TypedDict):
    location: typing.Union[aws_cdk.cdk.Token, "CfnDocumentationPart.LocationProperty"]
    properties: str
    restApiId: str

class CfnDocumentationVersion(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnDocumentationVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, documentation_version: str, rest_api_id: str, description: typing.Optional[str]=None) -> None:
        props: CfnDocumentationVersionProps = {"documentationVersion": documentation_version, "restApiId": rest_api_id}

        if description is not None:
            props["description"] = description

        jsii.create(CfnDocumentationVersion, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="documentationVersionId")
    def documentation_version_id(self) -> str:
        return jsii.get(self, "documentationVersionId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDocumentationVersionProps":
        return jsii.get(self, "propertyOverrides")


class _CfnDocumentationVersionProps(jsii.compat.TypedDict, total=False):
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDocumentationVersionProps")
class CfnDocumentationVersionProps(_CfnDocumentationVersionProps):
    documentationVersion: str
    restApiId: str

class CfnDomainName(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnDomainName"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, domain_name: str, certificate_arn: typing.Optional[str]=None, endpoint_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "EndpointConfigurationProperty"]]=None, regional_certificate_arn: typing.Optional[str]=None) -> None:
        props: CfnDomainNameProps = {"domainName": domain_name}

        if certificate_arn is not None:
            props["certificateArn"] = certificate_arn

        if endpoint_configuration is not None:
            props["endpointConfiguration"] = endpoint_configuration

        if regional_certificate_arn is not None:
            props["regionalCertificateArn"] = regional_certificate_arn

        jsii.create(CfnDomainName, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="domainNameDistributionDomainName")
    def domain_name_distribution_domain_name(self) -> str:
        return jsii.get(self, "domainNameDistributionDomainName")

    @property
    @jsii.member(jsii_name="domainNameDistributionHostedZoneId")
    def domain_name_distribution_hosted_zone_id(self) -> str:
        return jsii.get(self, "domainNameDistributionHostedZoneId")

    @property
    @jsii.member(jsii_name="domainNameName")
    def domain_name_name(self) -> str:
        return jsii.get(self, "domainNameName")

    @property
    @jsii.member(jsii_name="domainNameRegionalDomainName")
    def domain_name_regional_domain_name(self) -> str:
        return jsii.get(self, "domainNameRegionalDomainName")

    @property
    @jsii.member(jsii_name="domainNameRegionalHostedZoneId")
    def domain_name_regional_hosted_zone_id(self) -> str:
        return jsii.get(self, "domainNameRegionalHostedZoneId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDomainNameProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDomainName.EndpointConfigurationProperty")
    class EndpointConfigurationProperty(jsii.compat.TypedDict, total=False):
        types: typing.List[str]


class _CfnDomainNameProps(jsii.compat.TypedDict, total=False):
    certificateArn: str
    endpointConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDomainName.EndpointConfigurationProperty"]
    regionalCertificateArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDomainNameProps")
class CfnDomainNameProps(_CfnDomainNameProps):
    domainName: str

class CfnGatewayResponse(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnGatewayResponse"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, response_type: str, rest_api_id: str, response_parameters: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]]=None, response_templates: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]]=None, status_code: typing.Optional[str]=None) -> None:
        props: CfnGatewayResponseProps = {"responseType": response_type, "restApiId": rest_api_id}

        if response_parameters is not None:
            props["responseParameters"] = response_parameters

        if response_templates is not None:
            props["responseTemplates"] = response_templates

        if status_code is not None:
            props["statusCode"] = status_code

        jsii.create(CfnGatewayResponse, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="gatewayResponseId")
    def gateway_response_id(self) -> str:
        return jsii.get(self, "gatewayResponseId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnGatewayResponseProps":
        return jsii.get(self, "propertyOverrides")


class _CfnGatewayResponseProps(jsii.compat.TypedDict, total=False):
    responseParameters: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
    responseTemplates: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
    statusCode: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnGatewayResponseProps")
class CfnGatewayResponseProps(_CfnGatewayResponseProps):
    responseType: str
    restApiId: str

class CfnIntegrationResponseV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnIntegrationResponseV2"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api_id: str, integration_id: str, integration_response_key: str, content_handling_strategy: typing.Optional[str]=None, response_parameters: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, response_templates: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, template_selection_expression: typing.Optional[str]=None) -> None:
        props: CfnIntegrationResponseV2Props = {"apiId": api_id, "integrationId": integration_id, "integrationResponseKey": integration_response_key}

        if content_handling_strategy is not None:
            props["contentHandlingStrategy"] = content_handling_strategy

        if response_parameters is not None:
            props["responseParameters"] = response_parameters

        if response_templates is not None:
            props["responseTemplates"] = response_templates

        if template_selection_expression is not None:
            props["templateSelectionExpression"] = template_selection_expression

        jsii.create(CfnIntegrationResponseV2, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="integrationResponseId")
    def integration_response_id(self) -> str:
        return jsii.get(self, "integrationResponseId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnIntegrationResponseV2Props":
        return jsii.get(self, "propertyOverrides")


class _CfnIntegrationResponseV2Props(jsii.compat.TypedDict, total=False):
    contentHandlingStrategy: str
    responseParameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    responseTemplates: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    templateSelectionExpression: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnIntegrationResponseV2Props")
class CfnIntegrationResponseV2Props(_CfnIntegrationResponseV2Props):
    apiId: str
    integrationId: str
    integrationResponseKey: str

class CfnIntegrationV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnIntegrationV2"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api_id: str, integration_type: str, connection_type: typing.Optional[str]=None, content_handling_strategy: typing.Optional[str]=None, credentials_arn: typing.Optional[str]=None, description: typing.Optional[str]=None, integration_method: typing.Optional[str]=None, integration_uri: typing.Optional[str]=None, passthrough_behavior: typing.Optional[str]=None, request_parameters: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, request_templates: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, template_selection_expression: typing.Optional[str]=None, timeout_in_millis: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnIntegrationV2Props = {"apiId": api_id, "integrationType": integration_type}

        if connection_type is not None:
            props["connectionType"] = connection_type

        if content_handling_strategy is not None:
            props["contentHandlingStrategy"] = content_handling_strategy

        if credentials_arn is not None:
            props["credentialsArn"] = credentials_arn

        if description is not None:
            props["description"] = description

        if integration_method is not None:
            props["integrationMethod"] = integration_method

        if integration_uri is not None:
            props["integrationUri"] = integration_uri

        if passthrough_behavior is not None:
            props["passthroughBehavior"] = passthrough_behavior

        if request_parameters is not None:
            props["requestParameters"] = request_parameters

        if request_templates is not None:
            props["requestTemplates"] = request_templates

        if template_selection_expression is not None:
            props["templateSelectionExpression"] = template_selection_expression

        if timeout_in_millis is not None:
            props["timeoutInMillis"] = timeout_in_millis

        jsii.create(CfnIntegrationV2, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> str:
        return jsii.get(self, "integrationId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnIntegrationV2Props":
        return jsii.get(self, "propertyOverrides")


class _CfnIntegrationV2Props(jsii.compat.TypedDict, total=False):
    connectionType: str
    contentHandlingStrategy: str
    credentialsArn: str
    description: str
    integrationMethod: str
    integrationUri: str
    passthroughBehavior: str
    requestParameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    requestTemplates: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    templateSelectionExpression: str
    timeoutInMillis: typing.Union[jsii.Number, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnIntegrationV2Props")
class CfnIntegrationV2Props(_CfnIntegrationV2Props):
    apiId: str
    integrationType: str

class CfnMethod(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnMethod"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, http_method: str, resource_id: str, rest_api_id: str, api_key_required: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, authorization_scopes: typing.Optional[typing.List[str]]=None, authorization_type: typing.Optional[str]=None, authorizer_id: typing.Optional[str]=None, integration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "IntegrationProperty"]]=None, method_responses: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "MethodResponseProperty"]]]]=None, operation_name: typing.Optional[str]=None, request_models: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]]=None, request_parameters: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,typing.Union[bool, aws_cdk.cdk.Token]]]]=None, request_validator_id: typing.Optional[str]=None) -> None:
        props: CfnMethodProps = {"httpMethod": http_method, "resourceId": resource_id, "restApiId": rest_api_id}

        if api_key_required is not None:
            props["apiKeyRequired"] = api_key_required

        if authorization_scopes is not None:
            props["authorizationScopes"] = authorization_scopes

        if authorization_type is not None:
            props["authorizationType"] = authorization_type

        if authorizer_id is not None:
            props["authorizerId"] = authorizer_id

        if integration is not None:
            props["integration"] = integration

        if method_responses is not None:
            props["methodResponses"] = method_responses

        if operation_name is not None:
            props["operationName"] = operation_name

        if request_models is not None:
            props["requestModels"] = request_models

        if request_parameters is not None:
            props["requestParameters"] = request_parameters

        if request_validator_id is not None:
            props["requestValidatorId"] = request_validator_id

        jsii.create(CfnMethod, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="methodId")
    def method_id(self) -> str:
        return jsii.get(self, "methodId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnMethodProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnMethod.IntegrationProperty")
    class IntegrationProperty(jsii.compat.TypedDict, total=False):
        cacheKeyParameters: typing.List[str]
        cacheNamespace: str
        connectionId: str
        connectionType: str
        contentHandling: str
        credentials: str
        integrationHttpMethod: str
        integrationResponses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnMethod.IntegrationResponseProperty"]]]
        passthroughBehavior: str
        requestParameters: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        requestTemplates: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        timeoutInMillis: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        type: str
        uri: str

    class _IntegrationResponseProperty(jsii.compat.TypedDict, total=False):
        contentHandling: str
        responseParameters: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        responseTemplates: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        selectionPattern: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnMethod.IntegrationResponseProperty")
    class IntegrationResponseProperty(_IntegrationResponseProperty):
        statusCode: str

    class _MethodResponseProperty(jsii.compat.TypedDict, total=False):
        responseModels: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        responseParameters: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,typing.Union[bool, aws_cdk.cdk.Token]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnMethod.MethodResponseProperty")
    class MethodResponseProperty(_MethodResponseProperty):
        statusCode: str


class _CfnMethodProps(jsii.compat.TypedDict, total=False):
    apiKeyRequired: typing.Union[bool, aws_cdk.cdk.Token]
    authorizationScopes: typing.List[str]
    authorizationType: str
    authorizerId: str
    integration: typing.Union[aws_cdk.cdk.Token, "CfnMethod.IntegrationProperty"]
    methodResponses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnMethod.MethodResponseProperty"]]]
    operationName: str
    requestModels: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
    requestParameters: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,typing.Union[bool, aws_cdk.cdk.Token]]]
    requestValidatorId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnMethodProps")
class CfnMethodProps(_CfnMethodProps):
    httpMethod: str
    resourceId: str
    restApiId: str

class CfnModel(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnModel"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, rest_api_id: str, content_type: typing.Optional[str]=None, description: typing.Optional[str]=None, name: typing.Optional[str]=None, schema: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None) -> None:
        props: CfnModelProps = {"restApiId": rest_api_id}

        if content_type is not None:
            props["contentType"] = content_type

        if description is not None:
            props["description"] = description

        if name is not None:
            props["name"] = name

        if schema is not None:
            props["schema"] = schema

        jsii.create(CfnModel, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="modelName")
    def model_name(self) -> str:
        return jsii.get(self, "modelName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnModelProps":
        return jsii.get(self, "propertyOverrides")


class _CfnModelProps(jsii.compat.TypedDict, total=False):
    contentType: str
    description: str
    name: str
    schema: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnModelProps")
class CfnModelProps(_CfnModelProps):
    restApiId: str

class CfnModelV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnModelV2"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api_id: str, name: str, schema: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], content_type: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        props: CfnModelV2Props = {"apiId": api_id, "name": name, "schema": schema}

        if content_type is not None:
            props["contentType"] = content_type

        if description is not None:
            props["description"] = description

        jsii.create(CfnModelV2, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> str:
        return jsii.get(self, "modelId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnModelV2Props":
        return jsii.get(self, "propertyOverrides")


class _CfnModelV2Props(jsii.compat.TypedDict, total=False):
    contentType: str
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnModelV2Props")
class CfnModelV2Props(_CfnModelV2Props):
    apiId: str
    name: str
    schema: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

class CfnRequestValidator(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnRequestValidator"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, rest_api_id: str, name: typing.Optional[str]=None, validate_request_body: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, validate_request_parameters: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnRequestValidatorProps = {"restApiId": rest_api_id}

        if name is not None:
            props["name"] = name

        if validate_request_body is not None:
            props["validateRequestBody"] = validate_request_body

        if validate_request_parameters is not None:
            props["validateRequestParameters"] = validate_request_parameters

        jsii.create(CfnRequestValidator, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRequestValidatorProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="requestValidatorId")
    def request_validator_id(self) -> str:
        return jsii.get(self, "requestValidatorId")


class _CfnRequestValidatorProps(jsii.compat.TypedDict, total=False):
    name: str
    validateRequestBody: typing.Union[bool, aws_cdk.cdk.Token]
    validateRequestParameters: typing.Union[bool, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnRequestValidatorProps")
class CfnRequestValidatorProps(_CfnRequestValidatorProps):
    restApiId: str

class CfnResource(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnResource"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, parent_id: str, path_part: str, rest_api_id: str) -> None:
        props: CfnResourceProps = {"parentId": parent_id, "pathPart": path_part, "restApiId": rest_api_id}

        jsii.create(CfnResource, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnResourceProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> str:
        return jsii.get(self, "resourceId")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnResourceProps")
class CfnResourceProps(jsii.compat.TypedDict):
    parentId: str
    pathPart: str
    restApiId: str

class CfnRestApi(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnRestApi"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api_key_source_type: typing.Optional[str]=None, binary_media_types: typing.Optional[typing.List[str]]=None, body: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, body_s3_location: typing.Optional[typing.Union[aws_cdk.cdk.Token, "S3LocationProperty"]]=None, clone_from: typing.Optional[str]=None, description: typing.Optional[str]=None, endpoint_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "EndpointConfigurationProperty"]]=None, fail_on_warnings: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, minimum_compression_size: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, name: typing.Optional[str]=None, parameters: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]]=None, policy: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None) -> None:
        props: CfnRestApiProps = {}

        if api_key_source_type is not None:
            props["apiKeySourceType"] = api_key_source_type

        if binary_media_types is not None:
            props["binaryMediaTypes"] = binary_media_types

        if body is not None:
            props["body"] = body

        if body_s3_location is not None:
            props["bodyS3Location"] = body_s3_location

        if clone_from is not None:
            props["cloneFrom"] = clone_from

        if description is not None:
            props["description"] = description

        if endpoint_configuration is not None:
            props["endpointConfiguration"] = endpoint_configuration

        if fail_on_warnings is not None:
            props["failOnWarnings"] = fail_on_warnings

        if minimum_compression_size is not None:
            props["minimumCompressionSize"] = minimum_compression_size

        if name is not None:
            props["name"] = name

        if parameters is not None:
            props["parameters"] = parameters

        if policy is not None:
            props["policy"] = policy

        jsii.create(CfnRestApi, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRestApiProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        return jsii.get(self, "restApiId")

    @property
    @jsii.member(jsii_name="restApiRootResourceId")
    def rest_api_root_resource_id(self) -> str:
        return jsii.get(self, "restApiRootResourceId")

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnRestApi.EndpointConfigurationProperty")
    class EndpointConfigurationProperty(jsii.compat.TypedDict, total=False):
        types: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnRestApi.S3LocationProperty")
    class S3LocationProperty(jsii.compat.TypedDict, total=False):
        bucket: str
        eTag: str
        key: str
        version: str


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnRestApiProps")
class CfnRestApiProps(jsii.compat.TypedDict, total=False):
    apiKeySourceType: str
    binaryMediaTypes: typing.List[str]
    body: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    bodyS3Location: typing.Union[aws_cdk.cdk.Token, "CfnRestApi.S3LocationProperty"]
    cloneFrom: str
    description: str
    endpointConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnRestApi.EndpointConfigurationProperty"]
    failOnWarnings: typing.Union[bool, aws_cdk.cdk.Token]
    minimumCompressionSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    name: str
    parameters: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
    policy: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

class CfnRouteResponseV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnRouteResponseV2"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api_id: str, route_id: str, route_response_key: str, model_selection_expression: typing.Optional[str]=None, response_models: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, response_parameters: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None) -> None:
        props: CfnRouteResponseV2Props = {"apiId": api_id, "routeId": route_id, "routeResponseKey": route_response_key}

        if model_selection_expression is not None:
            props["modelSelectionExpression"] = model_selection_expression

        if response_models is not None:
            props["responseModels"] = response_models

        if response_parameters is not None:
            props["responseParameters"] = response_parameters

        jsii.create(CfnRouteResponseV2, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRouteResponseV2Props":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="routeResponseId")
    def route_response_id(self) -> str:
        return jsii.get(self, "routeResponseId")

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnRouteResponseV2.ParameterConstraintsProperty")
    class ParameterConstraintsProperty(jsii.compat.TypedDict):
        required: typing.Union[bool, aws_cdk.cdk.Token]


class _CfnRouteResponseV2Props(jsii.compat.TypedDict, total=False):
    modelSelectionExpression: str
    responseModels: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    responseParameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnRouteResponseV2Props")
class CfnRouteResponseV2Props(_CfnRouteResponseV2Props):
    apiId: str
    routeId: str
    routeResponseKey: str

class CfnRouteV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnRouteV2"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api_id: str, route_key: str, api_key_required: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, authorization_scopes: typing.Optional[typing.List[str]]=None, authorization_type: typing.Optional[str]=None, authorizer_id: typing.Optional[str]=None, model_selection_expression: typing.Optional[str]=None, operation_name: typing.Optional[str]=None, request_models: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, request_parameters: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, route_response_selection_expression: typing.Optional[str]=None, target: typing.Optional[str]=None) -> None:
        props: CfnRouteV2Props = {"apiId": api_id, "routeKey": route_key}

        if api_key_required is not None:
            props["apiKeyRequired"] = api_key_required

        if authorization_scopes is not None:
            props["authorizationScopes"] = authorization_scopes

        if authorization_type is not None:
            props["authorizationType"] = authorization_type

        if authorizer_id is not None:
            props["authorizerId"] = authorizer_id

        if model_selection_expression is not None:
            props["modelSelectionExpression"] = model_selection_expression

        if operation_name is not None:
            props["operationName"] = operation_name

        if request_models is not None:
            props["requestModels"] = request_models

        if request_parameters is not None:
            props["requestParameters"] = request_parameters

        if route_response_selection_expression is not None:
            props["routeResponseSelectionExpression"] = route_response_selection_expression

        if target is not None:
            props["target"] = target

        jsii.create(CfnRouteV2, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRouteV2Props":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="routeId")
    def route_id(self) -> str:
        return jsii.get(self, "routeId")

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnRouteV2.ParameterConstraintsProperty")
    class ParameterConstraintsProperty(jsii.compat.TypedDict):
        required: typing.Union[bool, aws_cdk.cdk.Token]


class _CfnRouteV2Props(jsii.compat.TypedDict, total=False):
    apiKeyRequired: typing.Union[bool, aws_cdk.cdk.Token]
    authorizationScopes: typing.List[str]
    authorizationType: str
    authorizerId: str
    modelSelectionExpression: str
    operationName: str
    requestModels: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    requestParameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    routeResponseSelectionExpression: str
    target: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnRouteV2Props")
class CfnRouteV2Props(_CfnRouteV2Props):
    apiId: str
    routeKey: str

class CfnStage(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnStage"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, rest_api_id: str, access_log_setting: typing.Optional[typing.Union[aws_cdk.cdk.Token, "AccessLogSettingProperty"]]=None, cache_cluster_enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, cache_cluster_size: typing.Optional[str]=None, canary_setting: typing.Optional[typing.Union[aws_cdk.cdk.Token, "CanarySettingProperty"]]=None, client_certificate_id: typing.Optional[str]=None, deployment_id: typing.Optional[str]=None, description: typing.Optional[str]=None, documentation_version: typing.Optional[str]=None, method_settings: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "MethodSettingProperty"]]]]=None, stage_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, tracing_enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, variables: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]]=None) -> None:
        props: CfnStageProps = {"restApiId": rest_api_id}

        if access_log_setting is not None:
            props["accessLogSetting"] = access_log_setting

        if cache_cluster_enabled is not None:
            props["cacheClusterEnabled"] = cache_cluster_enabled

        if cache_cluster_size is not None:
            props["cacheClusterSize"] = cache_cluster_size

        if canary_setting is not None:
            props["canarySetting"] = canary_setting

        if client_certificate_id is not None:
            props["clientCertificateId"] = client_certificate_id

        if deployment_id is not None:
            props["deploymentId"] = deployment_id

        if description is not None:
            props["description"] = description

        if documentation_version is not None:
            props["documentationVersion"] = documentation_version

        if method_settings is not None:
            props["methodSettings"] = method_settings

        if stage_name is not None:
            props["stageName"] = stage_name

        if tags is not None:
            props["tags"] = tags

        if tracing_enabled is not None:
            props["tracingEnabled"] = tracing_enabled

        if variables is not None:
            props["variables"] = variables

        jsii.create(CfnStage, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnStageProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> str:
        return jsii.get(self, "stageName")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnStage.AccessLogSettingProperty")
    class AccessLogSettingProperty(jsii.compat.TypedDict, total=False):
        destinationArn: str
        format: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnStage.CanarySettingProperty")
    class CanarySettingProperty(jsii.compat.TypedDict, total=False):
        deploymentId: str
        percentTraffic: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        stageVariableOverrides: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        useStageCache: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnStage.MethodSettingProperty")
    class MethodSettingProperty(jsii.compat.TypedDict, total=False):
        cacheDataEncrypted: typing.Union[bool, aws_cdk.cdk.Token]
        cacheTtlInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        cachingEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        dataTraceEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        httpMethod: str
        loggingLevel: str
        metricsEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        resourcePath: str
        throttlingBurstLimit: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        throttlingRateLimit: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class _CfnStageProps(jsii.compat.TypedDict, total=False):
    accessLogSetting: typing.Union[aws_cdk.cdk.Token, "CfnStage.AccessLogSettingProperty"]
    cacheClusterEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    cacheClusterSize: str
    canarySetting: typing.Union[aws_cdk.cdk.Token, "CfnStage.CanarySettingProperty"]
    clientCertificateId: str
    deploymentId: str
    description: str
    documentationVersion: str
    methodSettings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnStage.MethodSettingProperty"]]]
    stageName: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    tracingEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    variables: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnStageProps")
class CfnStageProps(_CfnStageProps):
    restApiId: str

class CfnStageV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnStageV2"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api_id: str, deployment_id: str, stage_name: str, access_log_settings: typing.Optional[typing.Union[aws_cdk.cdk.Token, "AccessLogSettingsProperty"]]=None, client_certificate_id: typing.Optional[str]=None, default_route_settings: typing.Optional[typing.Union[aws_cdk.cdk.Token, "RouteSettingsProperty"]]=None, description: typing.Optional[str]=None, route_settings: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, stage_variables: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None) -> None:
        props: CfnStageV2Props = {"apiId": api_id, "deploymentId": deployment_id, "stageName": stage_name}

        if access_log_settings is not None:
            props["accessLogSettings"] = access_log_settings

        if client_certificate_id is not None:
            props["clientCertificateId"] = client_certificate_id

        if default_route_settings is not None:
            props["defaultRouteSettings"] = default_route_settings

        if description is not None:
            props["description"] = description

        if route_settings is not None:
            props["routeSettings"] = route_settings

        if stage_variables is not None:
            props["stageVariables"] = stage_variables

        jsii.create(CfnStageV2, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnStageV2Props":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> str:
        return jsii.get(self, "stageName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnStageV2.AccessLogSettingsProperty")
    class AccessLogSettingsProperty(jsii.compat.TypedDict, total=False):
        destinationArn: str
        format: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnStageV2.RouteSettingsProperty")
    class RouteSettingsProperty(jsii.compat.TypedDict, total=False):
        dataTraceEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        detailedMetricsEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        loggingLevel: str
        throttlingBurstLimit: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        throttlingRateLimit: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class _CfnStageV2Props(jsii.compat.TypedDict, total=False):
    accessLogSettings: typing.Union[aws_cdk.cdk.Token, "CfnStageV2.AccessLogSettingsProperty"]
    clientCertificateId: str
    defaultRouteSettings: typing.Union[aws_cdk.cdk.Token, "CfnStageV2.RouteSettingsProperty"]
    description: str
    routeSettings: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    stageVariables: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnStageV2Props")
class CfnStageV2Props(_CfnStageV2Props):
    apiId: str
    deploymentId: str
    stageName: str

class CfnUsagePlan(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnUsagePlan"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api_stages: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ApiStageProperty"]]]]=None, description: typing.Optional[str]=None, quota: typing.Optional[typing.Union[aws_cdk.cdk.Token, "QuotaSettingsProperty"]]=None, throttle: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ThrottleSettingsProperty"]]=None, usage_plan_name: typing.Optional[str]=None) -> None:
        props: CfnUsagePlanProps = {}

        if api_stages is not None:
            props["apiStages"] = api_stages

        if description is not None:
            props["description"] = description

        if quota is not None:
            props["quota"] = quota

        if throttle is not None:
            props["throttle"] = throttle

        if usage_plan_name is not None:
            props["usagePlanName"] = usage_plan_name

        jsii.create(CfnUsagePlan, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnUsagePlanProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="usagePlanId")
    def usage_plan_id(self) -> str:
        return jsii.get(self, "usagePlanId")

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnUsagePlan.ApiStageProperty")
    class ApiStageProperty(jsii.compat.TypedDict, total=False):
        apiId: str
        stage: str
        throttle: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,typing.Union[aws_cdk.cdk.Token, "CfnUsagePlan.ThrottleSettingsProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnUsagePlan.QuotaSettingsProperty")
    class QuotaSettingsProperty(jsii.compat.TypedDict, total=False):
        limit: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        offset: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        period: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnUsagePlan.ThrottleSettingsProperty")
    class ThrottleSettingsProperty(jsii.compat.TypedDict, total=False):
        burstLimit: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        rateLimit: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class CfnUsagePlanKey(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnUsagePlanKey"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, key_id: str, key_type: str, usage_plan_id: str) -> None:
        props: CfnUsagePlanKeyProps = {"keyId": key_id, "keyType": key_type, "usagePlanId": usage_plan_id}

        jsii.create(CfnUsagePlanKey, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnUsagePlanKeyProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="usagePlanKeyId")
    def usage_plan_key_id(self) -> str:
        return jsii.get(self, "usagePlanKeyId")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnUsagePlanKeyProps")
class CfnUsagePlanKeyProps(jsii.compat.TypedDict):
    keyId: str
    keyType: str
    usagePlanId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnUsagePlanProps")
class CfnUsagePlanProps(jsii.compat.TypedDict, total=False):
    apiStages: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnUsagePlan.ApiStageProperty"]]]
    description: str
    quota: typing.Union[aws_cdk.cdk.Token, "CfnUsagePlan.QuotaSettingsProperty"]
    throttle: typing.Union[aws_cdk.cdk.Token, "CfnUsagePlan.ThrottleSettingsProperty"]
    usagePlanName: str

class CfnVpcLink(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnVpcLink"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, target_arns: typing.List[str], description: typing.Optional[str]=None) -> None:
        props: CfnVpcLinkProps = {"name": name, "targetArns": target_arns}

        if description is not None:
            props["description"] = description

        jsii.create(CfnVpcLink, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVpcLinkProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="vpcLinkId")
    def vpc_link_id(self) -> str:
        return jsii.get(self, "vpcLinkId")


class _CfnVpcLinkProps(jsii.compat.TypedDict, total=False):
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnVpcLinkProps")
class CfnVpcLinkProps(_CfnVpcLinkProps):
    name: str
    targetArns: typing.List[str]

@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.ConnectionType")
class ConnectionType(enum.Enum):
    Internet = "Internet"
    VpcLink = "VpcLink"

@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.ContentHandling")
class ContentHandling(enum.Enum):
    ConvertToBinary = "ConvertToBinary"
    ConvertToText = "ConvertToText"

class Deployment(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.Deployment"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api: "IRestApi", description: typing.Optional[str]=None, retain_deployments: typing.Optional[bool]=None) -> None:
        props: DeploymentProps = {"api": api}

        if description is not None:
            props["description"] = description

        if retain_deployments is not None:
            props["retainDeployments"] = retain_deployments

        jsii.create(Deployment, self, [scope, id, props])

    @jsii.member(jsii_name="addToLogicalId")
    def add_to_logical_id(self, data: typing.Any) -> None:
        return jsii.invoke(self, "addToLogicalId", [data])

    @property
    @jsii.member(jsii_name="api")
    def api(self) -> "IRestApi":
        return jsii.get(self, "api")

    @property
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> str:
        return jsii.get(self, "deploymentId")


class _DeploymentProps(jsii.compat.TypedDict, total=False):
    description: str
    retainDeployments: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.DeploymentProps")
class DeploymentProps(_DeploymentProps):
    api: "IRestApi"

@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.EndpointType")
class EndpointType(enum.Enum):
    Edge = "Edge"
    Regional = "Regional"
    Private = "Private"

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.HttpIntegrationProps")
class HttpIntegrationProps(jsii.compat.TypedDict, total=False):
    httpMethod: str
    options: "IntegrationOptions"
    proxy: bool

@jsii.interface(jsii_type="@aws-cdk/aws-apigateway.IModel")
class IModel(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IModelProxy

    @property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> str:
        ...


class _IModelProxy():
    __jsii_type__ = "@aws-cdk/aws-apigateway.IModel"
    @property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> str:
        return jsii.get(self, "modelId")


@jsii.implements(IModel)
class EmptyModel(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.EmptyModel"):
    def __init__(self) -> None:
        jsii.create(EmptyModel, self, [])

    @property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> str:
        return jsii.get(self, "modelId")


@jsii.implements(IModel)
class ErrorModel(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.ErrorModel"):
    def __init__(self) -> None:
        jsii.create(ErrorModel, self, [])

    @property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> str:
        return jsii.get(self, "modelId")


@jsii.interface(jsii_type="@aws-cdk/aws-apigateway.IRestApi")
class IRestApi(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IRestApiProxy

    @property
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "RestApiImportProps":
        ...


class _IRestApiProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-apigateway.IRestApi"
    @property
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        return jsii.get(self, "restApiId")

    @jsii.member(jsii_name="export")
    def export(self) -> "RestApiImportProps":
        return jsii.invoke(self, "export", [])


@jsii.interface(jsii_type="@aws-cdk/aws-apigateway.IRestApiResource")
class IRestApiResource(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IRestApiResourceProxy

    @property
    @jsii.member(jsii_name="resourceApi")
    def resource_api(self) -> "RestApi":
        ...

    @property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="resourcePath")
    def resource_path(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="defaultIntegration")
    def default_integration(self) -> typing.Optional["Integration"]:
        ...

    @property
    @jsii.member(jsii_name="defaultMethodOptions")
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        ...

    @property
    @jsii.member(jsii_name="parentResource")
    def parent_resource(self) -> typing.Optional["IRestApiResource"]:
        ...

    @jsii.member(jsii_name="addMethod")
    def add_method(self, http_method: str, target: typing.Optional["Integration"]=None, *, api_key_required: typing.Optional[bool]=None, authorization_type: typing.Optional["AuthorizationType"]=None, authorizer_id: typing.Optional[str]=None, method_responses: typing.Optional[typing.List["MethodResponse"]]=None, operation_name: typing.Optional[str]=None, request_parameters: typing.Optional[typing.Mapping[str,bool]]=None) -> "Method":
        ...

    @jsii.member(jsii_name="addProxy")
    def add_proxy(self, *, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> "ProxyResource":
        ...

    @jsii.member(jsii_name="addResource")
    def add_resource(self, path_part: str, *, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> "Resource":
        ...

    @jsii.member(jsii_name="getResource")
    def get_resource(self, path_part: str) -> typing.Optional["IRestApiResource"]:
        ...

    @jsii.member(jsii_name="resourceForPath")
    def resource_for_path(self, path: str) -> "Resource":
        ...


class _IRestApiResourceProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-apigateway.IRestApiResource"
    @property
    @jsii.member(jsii_name="resourceApi")
    def resource_api(self) -> "RestApi":
        return jsii.get(self, "resourceApi")

    @property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> str:
        return jsii.get(self, "resourceId")

    @property
    @jsii.member(jsii_name="resourcePath")
    def resource_path(self) -> str:
        return jsii.get(self, "resourcePath")

    @property
    @jsii.member(jsii_name="defaultIntegration")
    def default_integration(self) -> typing.Optional["Integration"]:
        return jsii.get(self, "defaultIntegration")

    @property
    @jsii.member(jsii_name="defaultMethodOptions")
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        return jsii.get(self, "defaultMethodOptions")

    @property
    @jsii.member(jsii_name="parentResource")
    def parent_resource(self) -> typing.Optional["IRestApiResource"]:
        return jsii.get(self, "parentResource")

    @jsii.member(jsii_name="addMethod")
    def add_method(self, http_method: str, target: typing.Optional["Integration"]=None, *, api_key_required: typing.Optional[bool]=None, authorization_type: typing.Optional["AuthorizationType"]=None, authorizer_id: typing.Optional[str]=None, method_responses: typing.Optional[typing.List["MethodResponse"]]=None, operation_name: typing.Optional[str]=None, request_parameters: typing.Optional[typing.Mapping[str,bool]]=None) -> "Method":
        options: MethodOptions = {}

        if api_key_required is not None:
            options["apiKeyRequired"] = api_key_required

        if authorization_type is not None:
            options["authorizationType"] = authorization_type

        if authorizer_id is not None:
            options["authorizerId"] = authorizer_id

        if method_responses is not None:
            options["methodResponses"] = method_responses

        if operation_name is not None:
            options["operationName"] = operation_name

        if request_parameters is not None:
            options["requestParameters"] = request_parameters

        return jsii.invoke(self, "addMethod", [http_method, target, options])

    @jsii.member(jsii_name="addProxy")
    def add_proxy(self, *, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> "ProxyResource":
        options: ResourceOptions = {}

        if default_integration is not None:
            options["defaultIntegration"] = default_integration

        if default_method_options is not None:
            options["defaultMethodOptions"] = default_method_options

        return jsii.invoke(self, "addProxy", [options])

    @jsii.member(jsii_name="addResource")
    def add_resource(self, path_part: str, *, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> "Resource":
        options: ResourceOptions = {}

        if default_integration is not None:
            options["defaultIntegration"] = default_integration

        if default_method_options is not None:
            options["defaultMethodOptions"] = default_method_options

        return jsii.invoke(self, "addResource", [path_part, options])

    @jsii.member(jsii_name="getResource")
    def get_resource(self, path_part: str) -> typing.Optional["IRestApiResource"]:
        return jsii.invoke(self, "getResource", [path_part])

    @jsii.member(jsii_name="resourceForPath")
    def resource_for_path(self, path: str) -> "Resource":
        return jsii.invoke(self, "resourceForPath", [path])


class Integration(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.Integration"):
    def __init__(self, *, type: "IntegrationType", integration_http_method: typing.Optional[str]=None, options: typing.Optional["IntegrationOptions"]=None, uri: typing.Any=None) -> None:
        props: IntegrationProps = {"type": type}

        if integration_http_method is not None:
            props["integrationHttpMethod"] = integration_http_method

        if options is not None:
            props["options"] = options

        if uri is not None:
            props["uri"] = uri

        jsii.create(Integration, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _method: "Method") -> None:
        return jsii.invoke(self, "bind", [_method])

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "IntegrationProps":
        return jsii.get(self, "props")


class AwsIntegration(Integration, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.AwsIntegration"):
    def __init__(self, *, service: str, action: typing.Optional[str]=None, action_parameters: typing.Optional[typing.Mapping[str,str]]=None, options: typing.Optional["IntegrationOptions"]=None, path: typing.Optional[str]=None, proxy: typing.Optional[bool]=None, subdomain: typing.Optional[str]=None) -> None:
        props: AwsIntegrationProps = {"service": service}

        if action is not None:
            props["action"] = action

        if action_parameters is not None:
            props["actionParameters"] = action_parameters

        if options is not None:
            props["options"] = options

        if path is not None:
            props["path"] = path

        if proxy is not None:
            props["proxy"] = proxy

        if subdomain is not None:
            props["subdomain"] = subdomain

        jsii.create(AwsIntegration, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, method: "Method") -> None:
        return jsii.invoke(self, "bind", [method])


class HttpIntegration(Integration, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.HttpIntegration"):
    def __init__(self, url: str, *, http_method: typing.Optional[str]=None, options: typing.Optional["IntegrationOptions"]=None, proxy: typing.Optional[bool]=None) -> None:
        props: HttpIntegrationProps = {}

        if http_method is not None:
            props["httpMethod"] = http_method

        if options is not None:
            props["options"] = options

        if proxy is not None:
            props["proxy"] = proxy

        jsii.create(HttpIntegration, self, [url, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.IntegrationOptions")
class IntegrationOptions(jsii.compat.TypedDict, total=False):
    cacheKeyParameters: typing.List[str]
    cacheNamespace: str
    connectionType: "ConnectionType"
    contentHandling: "ContentHandling"
    credentialsPassthrough: bool
    credentialsRole: aws_cdk.aws_iam.Role
    integrationResponses: typing.List["IntegrationResponse"]
    passthroughBehavior: "PassthroughBehavior"
    requestParameters: typing.Mapping[str,str]
    requestTemplates: typing.Mapping[str,str]
    vpcLink: "VpcLink"

class _IntegrationProps(jsii.compat.TypedDict, total=False):
    integrationHttpMethod: str
    options: "IntegrationOptions"
    uri: typing.Any

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.IntegrationProps")
class IntegrationProps(_IntegrationProps):
    type: "IntegrationType"

class _IntegrationResponse(jsii.compat.TypedDict, total=False):
    contentHandling: "ContentHandling"
    responseParameters: typing.Mapping[str,str]
    responseTemplates: typing.Mapping[str,str]
    selectionPattern: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.IntegrationResponse")
class IntegrationResponse(_IntegrationResponse):
    statusCode: str

@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.IntegrationType")
class IntegrationType(enum.Enum):
    Aws = "Aws"
    AwsProxy = "AwsProxy"
    Http = "Http"
    HttpProxy = "HttpProxy"
    Mock = "Mock"

class LambdaIntegration(AwsIntegration, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.LambdaIntegration"):
    def __init__(self, handler: aws_cdk.aws_lambda.IFunction, *, allow_test_invoke: typing.Optional[bool]=None, proxy: typing.Optional[bool]=None, cache_key_parameters: typing.Optional[typing.List[str]]=None, cache_namespace: typing.Optional[str]=None, connection_type: typing.Optional["ConnectionType"]=None, content_handling: typing.Optional["ContentHandling"]=None, credentials_passthrough: typing.Optional[bool]=None, credentials_role: typing.Optional[aws_cdk.aws_iam.Role]=None, integration_responses: typing.Optional[typing.List["IntegrationResponse"]]=None, passthrough_behavior: typing.Optional["PassthroughBehavior"]=None, request_parameters: typing.Optional[typing.Mapping[str,str]]=None, request_templates: typing.Optional[typing.Mapping[str,str]]=None, vpc_link: typing.Optional["VpcLink"]=None) -> None:
        options: LambdaIntegrationOptions = {}

        if allow_test_invoke is not None:
            options["allowTestInvoke"] = allow_test_invoke

        if proxy is not None:
            options["proxy"] = proxy

        if cache_key_parameters is not None:
            options["cacheKeyParameters"] = cache_key_parameters

        if cache_namespace is not None:
            options["cacheNamespace"] = cache_namespace

        if connection_type is not None:
            options["connectionType"] = connection_type

        if content_handling is not None:
            options["contentHandling"] = content_handling

        if credentials_passthrough is not None:
            options["credentialsPassthrough"] = credentials_passthrough

        if credentials_role is not None:
            options["credentialsRole"] = credentials_role

        if integration_responses is not None:
            options["integrationResponses"] = integration_responses

        if passthrough_behavior is not None:
            options["passthroughBehavior"] = passthrough_behavior

        if request_parameters is not None:
            options["requestParameters"] = request_parameters

        if request_templates is not None:
            options["requestTemplates"] = request_templates

        if vpc_link is not None:
            options["vpcLink"] = vpc_link

        jsii.create(LambdaIntegration, self, [handler, options])

    @jsii.member(jsii_name="bind")
    def bind(self, method: "Method") -> None:
        return jsii.invoke(self, "bind", [method])


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.LambdaIntegrationOptions")
class LambdaIntegrationOptions(IntegrationOptions, jsii.compat.TypedDict, total=False):
    allowTestInvoke: bool
    proxy: bool

class _LambdaRestApiProps(jsii.compat.TypedDict, total=False):
    options: "RestApiProps"
    proxy: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.LambdaRestApiProps")
class LambdaRestApiProps(_LambdaRestApiProps):
    handler: aws_cdk.aws_lambda.IFunction

class Method(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.Method"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, http_method: str, resource: "IRestApiResource", integration: typing.Optional["Integration"]=None, options: typing.Optional["MethodOptions"]=None) -> None:
        props: MethodProps = {"httpMethod": http_method, "resource": resource}

        if integration is not None:
            props["integration"] = integration

        if options is not None:
            props["options"] = options

        jsii.create(Method, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="httpMethod")
    def http_method(self) -> str:
        return jsii.get(self, "httpMethod")

    @property
    @jsii.member(jsii_name="methodArn")
    def method_arn(self) -> str:
        return jsii.get(self, "methodArn")

    @property
    @jsii.member(jsii_name="methodId")
    def method_id(self) -> str:
        return jsii.get(self, "methodId")

    @property
    @jsii.member(jsii_name="resource")
    def resource(self) -> "IRestApiResource":
        return jsii.get(self, "resource")

    @property
    @jsii.member(jsii_name="restApi")
    def rest_api(self) -> "RestApi":
        return jsii.get(self, "restApi")

    @property
    @jsii.member(jsii_name="testMethodArn")
    def test_method_arn(self) -> str:
        return jsii.get(self, "testMethodArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.MethodDeploymentOptions")
class MethodDeploymentOptions(jsii.compat.TypedDict, total=False):
    cacheDataEncrypted: bool
    cacheTtlSeconds: jsii.Number
    cachingEnabled: bool
    dataTraceEnabled: bool
    loggingLevel: "MethodLoggingLevel"
    metricsEnabled: bool
    throttlingBurstLimit: jsii.Number
    throttlingRateLimit: jsii.Number

@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.MethodLoggingLevel")
class MethodLoggingLevel(enum.Enum):
    Off = "Off"
    Error = "Error"
    Info = "Info"

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.MethodOptions")
class MethodOptions(jsii.compat.TypedDict, total=False):
    apiKeyRequired: bool
    authorizationType: "AuthorizationType"
    authorizerId: str
    methodResponses: typing.List["MethodResponse"]
    operationName: str
    requestParameters: typing.Mapping[str,bool]

class _MethodProps(jsii.compat.TypedDict, total=False):
    integration: "Integration"
    options: "MethodOptions"

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.MethodProps")
class MethodProps(_MethodProps):
    httpMethod: str
    resource: "IRestApiResource"

class _MethodResponse(jsii.compat.TypedDict, total=False):
    responseModels: typing.Mapping[str,"IModel"]
    responseParameters: typing.Mapping[str,bool]

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.MethodResponse")
class MethodResponse(_MethodResponse):
    statusCode: str

class MockIntegration(Integration, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.MockIntegration"):
    def __init__(self, *, cache_key_parameters: typing.Optional[typing.List[str]]=None, cache_namespace: typing.Optional[str]=None, connection_type: typing.Optional["ConnectionType"]=None, content_handling: typing.Optional["ContentHandling"]=None, credentials_passthrough: typing.Optional[bool]=None, credentials_role: typing.Optional[aws_cdk.aws_iam.Role]=None, integration_responses: typing.Optional[typing.List["IntegrationResponse"]]=None, passthrough_behavior: typing.Optional["PassthroughBehavior"]=None, request_parameters: typing.Optional[typing.Mapping[str,str]]=None, request_templates: typing.Optional[typing.Mapping[str,str]]=None, vpc_link: typing.Optional["VpcLink"]=None) -> None:
        options: IntegrationOptions = {}

        if cache_key_parameters is not None:
            options["cacheKeyParameters"] = cache_key_parameters

        if cache_namespace is not None:
            options["cacheNamespace"] = cache_namespace

        if connection_type is not None:
            options["connectionType"] = connection_type

        if content_handling is not None:
            options["contentHandling"] = content_handling

        if credentials_passthrough is not None:
            options["credentialsPassthrough"] = credentials_passthrough

        if credentials_role is not None:
            options["credentialsRole"] = credentials_role

        if integration_responses is not None:
            options["integrationResponses"] = integration_responses

        if passthrough_behavior is not None:
            options["passthroughBehavior"] = passthrough_behavior

        if request_parameters is not None:
            options["requestParameters"] = request_parameters

        if request_templates is not None:
            options["requestTemplates"] = request_templates

        if vpc_link is not None:
            options["vpcLink"] = vpc_link

        jsii.create(MockIntegration, self, [options])


@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.PassthroughBehavior")
class PassthroughBehavior(enum.Enum):
    WhenNoMatch = "WhenNoMatch"
    Never = "Never"
    WhenNoTemplates = "WhenNoTemplates"

@jsii.implements(IRestApiResource)
class ResourceBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-apigateway.ResourceBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _ResourceBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(ResourceBase, self, [scope, id])

    @jsii.member(jsii_name="addMethod")
    def add_method(self, http_method: str, integration: typing.Optional["Integration"]=None, *, api_key_required: typing.Optional[bool]=None, authorization_type: typing.Optional["AuthorizationType"]=None, authorizer_id: typing.Optional[str]=None, method_responses: typing.Optional[typing.List["MethodResponse"]]=None, operation_name: typing.Optional[str]=None, request_parameters: typing.Optional[typing.Mapping[str,bool]]=None) -> "Method":
        options: MethodOptions = {}

        if api_key_required is not None:
            options["apiKeyRequired"] = api_key_required

        if authorization_type is not None:
            options["authorizationType"] = authorization_type

        if authorizer_id is not None:
            options["authorizerId"] = authorizer_id

        if method_responses is not None:
            options["methodResponses"] = method_responses

        if operation_name is not None:
            options["operationName"] = operation_name

        if request_parameters is not None:
            options["requestParameters"] = request_parameters

        return jsii.invoke(self, "addMethod", [http_method, integration, options])

    @jsii.member(jsii_name="addProxy")
    def add_proxy(self, *, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> "ProxyResource":
        options: ResourceOptions = {}

        if default_integration is not None:
            options["defaultIntegration"] = default_integration

        if default_method_options is not None:
            options["defaultMethodOptions"] = default_method_options

        return jsii.invoke(self, "addProxy", [options])

    @jsii.member(jsii_name="addResource")
    def add_resource(self, path_part: str, *, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> "Resource":
        options: ResourceOptions = {}

        if default_integration is not None:
            options["defaultIntegration"] = default_integration

        if default_method_options is not None:
            options["defaultMethodOptions"] = default_method_options

        return jsii.invoke(self, "addResource", [path_part, options])

    @jsii.member(jsii_name="getResource")
    def get_resource(self, path_part: str) -> typing.Optional["IRestApiResource"]:
        return jsii.invoke(self, "getResource", [path_part])

    @jsii.member(jsii_name="resourceForPath")
    def resource_for_path(self, path: str) -> "Resource":
        return jsii.invoke(self, "resourceForPath", [path])

    @jsii.member(jsii_name="trackChild")
    def track_child(self, path_part: str, resource: "Resource") -> None:
        return jsii.invoke(self, "trackChild", [path_part, resource])

    @property
    @jsii.member(jsii_name="resourceApi")
    @abc.abstractmethod
    def resource_api(self) -> "RestApi":
        ...

    @property
    @jsii.member(jsii_name="resourceId")
    @abc.abstractmethod
    def resource_id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="resourcePath")
    @abc.abstractmethod
    def resource_path(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="defaultIntegration")
    @abc.abstractmethod
    def default_integration(self) -> typing.Optional["Integration"]:
        ...

    @property
    @jsii.member(jsii_name="defaultMethodOptions")
    @abc.abstractmethod
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        ...

    @property
    @jsii.member(jsii_name="parentResource")
    @abc.abstractmethod
    def parent_resource(self) -> typing.Optional["IRestApiResource"]:
        ...


class _ResourceBaseProxy(ResourceBase):
    @property
    @jsii.member(jsii_name="resourceApi")
    def resource_api(self) -> "RestApi":
        return jsii.get(self, "resourceApi")

    @property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> str:
        return jsii.get(self, "resourceId")

    @property
    @jsii.member(jsii_name="resourcePath")
    def resource_path(self) -> str:
        return jsii.get(self, "resourcePath")

    @property
    @jsii.member(jsii_name="defaultIntegration")
    def default_integration(self) -> typing.Optional["Integration"]:
        return jsii.get(self, "defaultIntegration")

    @property
    @jsii.member(jsii_name="defaultMethodOptions")
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        return jsii.get(self, "defaultMethodOptions")

    @property
    @jsii.member(jsii_name="parentResource")
    def parent_resource(self) -> typing.Optional["IRestApiResource"]:
        return jsii.get(self, "parentResource")


class Resource(ResourceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.Resource"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, parent: "IRestApiResource", path_part: str, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> None:
        props: ResourceProps = {"parent": parent, "pathPart": path_part}

        if default_integration is not None:
            props["defaultIntegration"] = default_integration

        if default_method_options is not None:
            props["defaultMethodOptions"] = default_method_options

        jsii.create(Resource, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="resourceApi")
    def resource_api(self) -> "RestApi":
        return jsii.get(self, "resourceApi")

    @property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> str:
        return jsii.get(self, "resourceId")

    @property
    @jsii.member(jsii_name="resourcePath")
    def resource_path(self) -> str:
        return jsii.get(self, "resourcePath")

    @property
    @jsii.member(jsii_name="defaultIntegration")
    def default_integration(self) -> typing.Optional["Integration"]:
        return jsii.get(self, "defaultIntegration")

    @property
    @jsii.member(jsii_name="defaultMethodOptions")
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        return jsii.get(self, "defaultMethodOptions")

    @property
    @jsii.member(jsii_name="parentResource")
    def parent_resource(self) -> typing.Optional["IRestApiResource"]:
        return jsii.get(self, "parentResource")


class ProxyResource(Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.ProxyResource"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, parent: "IRestApiResource", any_method: typing.Optional[bool]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> None:
        props: ProxyResourceProps = {"parent": parent}

        if any_method is not None:
            props["anyMethod"] = any_method

        if default_integration is not None:
            props["defaultIntegration"] = default_integration

        if default_method_options is not None:
            props["defaultMethodOptions"] = default_method_options

        jsii.create(ProxyResource, self, [scope, id, props])

    @jsii.member(jsii_name="addMethod")
    def add_method(self, http_method: str, integration: typing.Optional["Integration"]=None, *, api_key_required: typing.Optional[bool]=None, authorization_type: typing.Optional["AuthorizationType"]=None, authorizer_id: typing.Optional[str]=None, method_responses: typing.Optional[typing.List["MethodResponse"]]=None, operation_name: typing.Optional[str]=None, request_parameters: typing.Optional[typing.Mapping[str,bool]]=None) -> "Method":
        options: MethodOptions = {}

        if api_key_required is not None:
            options["apiKeyRequired"] = api_key_required

        if authorization_type is not None:
            options["authorizationType"] = authorization_type

        if authorizer_id is not None:
            options["authorizerId"] = authorizer_id

        if method_responses is not None:
            options["methodResponses"] = method_responses

        if operation_name is not None:
            options["operationName"] = operation_name

        if request_parameters is not None:
            options["requestParameters"] = request_parameters

        return jsii.invoke(self, "addMethod", [http_method, integration, options])

    @property
    @jsii.member(jsii_name="anyMethod")
    def any_method(self) -> typing.Optional["Method"]:
        return jsii.get(self, "anyMethod")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.ResourceOptions")
class ResourceOptions(jsii.compat.TypedDict, total=False):
    defaultIntegration: "Integration"
    defaultMethodOptions: "MethodOptions"

class _ProxyResourceProps(ResourceOptions, jsii.compat.TypedDict, total=False):
    anyMethod: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.ProxyResourceProps")
class ProxyResourceProps(_ProxyResourceProps):
    parent: "IRestApiResource"

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.ResourceProps")
class ResourceProps(ResourceOptions, jsii.compat.TypedDict):
    parent: "IRestApiResource"
    pathPart: str

@jsii.implements(IRestApi)
class RestApi(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.RestApi"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api_key_source_type: typing.Optional["ApiKeySourceType"]=None, binary_media_types: typing.Optional[typing.List[str]]=None, clone_from: typing.Optional["IRestApi"]=None, cloud_watch_role: typing.Optional[bool]=None, deploy: typing.Optional[bool]=None, deploy_options: typing.Optional["StageOptions"]=None, description: typing.Optional[str]=None, endpoint_types: typing.Optional[typing.List["EndpointType"]]=None, fail_on_warnings: typing.Optional[bool]=None, minimum_compression_size: typing.Optional[jsii.Number]=None, parameters: typing.Optional[typing.Mapping[str,str]]=None, policy: typing.Optional[aws_cdk.aws_iam.PolicyDocument]=None, rest_api_name: typing.Optional[str]=None, retain_deployments: typing.Optional[bool]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> None:
        props: RestApiProps = {}

        if api_key_source_type is not None:
            props["apiKeySourceType"] = api_key_source_type

        if binary_media_types is not None:
            props["binaryMediaTypes"] = binary_media_types

        if clone_from is not None:
            props["cloneFrom"] = clone_from

        if cloud_watch_role is not None:
            props["cloudWatchRole"] = cloud_watch_role

        if deploy is not None:
            props["deploy"] = deploy

        if deploy_options is not None:
            props["deployOptions"] = deploy_options

        if description is not None:
            props["description"] = description

        if endpoint_types is not None:
            props["endpointTypes"] = endpoint_types

        if fail_on_warnings is not None:
            props["failOnWarnings"] = fail_on_warnings

        if minimum_compression_size is not None:
            props["minimumCompressionSize"] = minimum_compression_size

        if parameters is not None:
            props["parameters"] = parameters

        if policy is not None:
            props["policy"] = policy

        if rest_api_name is not None:
            props["restApiName"] = rest_api_name

        if retain_deployments is not None:
            props["retainDeployments"] = retain_deployments

        if default_integration is not None:
            props["defaultIntegration"] = default_integration

        if default_method_options is not None:
            props["defaultMethodOptions"] = default_method_options

        jsii.create(RestApi, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, rest_api_id: str) -> "IRestApi":
        props: RestApiImportProps = {"restApiId": rest_api_id}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="executeApiArn")
    def execute_api_arn(self, method: typing.Optional[str]=None, path: typing.Optional[str]=None, stage: typing.Optional[str]=None) -> str:
        return jsii.invoke(self, "executeApiArn", [method, path, stage])

    @jsii.member(jsii_name="export")
    def export(self) -> "RestApiImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="urlForPath")
    def url_for_path(self, path: typing.Optional[str]=None) -> str:
        return jsii.invoke(self, "urlForPath", [path])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        return jsii.get(self, "restApiId")

    @property
    @jsii.member(jsii_name="root")
    def root(self) -> "IRestApiResource":
        return jsii.get(self, "root")

    @property
    @jsii.member(jsii_name="url")
    def url(self) -> str:
        return jsii.get(self, "url")

    @property
    @jsii.member(jsii_name="deploymentStage")
    def deployment_stage(self) -> typing.Optional["Stage"]:
        return jsii.get(self, "deploymentStage")

    @deployment_stage.setter
    def deployment_stage(self, value: typing.Optional["Stage"]):
        return jsii.set(self, "deploymentStage", value)

    @property
    @jsii.member(jsii_name="latestDeployment")
    def latest_deployment(self) -> typing.Optional["Deployment"]:
        return jsii.get(self, "latestDeployment")

    @latest_deployment.setter
    def latest_deployment(self, value: typing.Optional["Deployment"]):
        return jsii.set(self, "latestDeployment", value)


class LambdaRestApi(RestApi, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.LambdaRestApi"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, handler: aws_cdk.aws_lambda.IFunction, options: typing.Optional["RestApiProps"]=None, proxy: typing.Optional[bool]=None) -> None:
        props: LambdaRestApiProps = {"handler": handler}

        if options is not None:
            props["options"] = options

        if proxy is not None:
            props["proxy"] = proxy

        jsii.create(LambdaRestApi, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.RestApiImportProps")
class RestApiImportProps(jsii.compat.TypedDict):
    restApiId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.RestApiProps")
class RestApiProps(ResourceOptions, jsii.compat.TypedDict, total=False):
    apiKeySourceType: "ApiKeySourceType"
    binaryMediaTypes: typing.List[str]
    cloneFrom: "IRestApi"
    cloudWatchRole: bool
    deploy: bool
    deployOptions: "StageOptions"
    description: str
    endpointTypes: typing.List["EndpointType"]
    failOnWarnings: bool
    minimumCompressionSize: jsii.Number
    parameters: typing.Mapping[str,str]
    policy: aws_cdk.aws_iam.PolicyDocument
    restApiName: str
    retainDeployments: bool

class Stage(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.Stage"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, deployment: "Deployment", cache_cluster_enabled: typing.Optional[bool]=None, cache_cluster_size: typing.Optional[str]=None, client_certificate_id: typing.Optional[str]=None, description: typing.Optional[str]=None, documentation_version: typing.Optional[str]=None, method_options: typing.Optional[typing.Mapping[str,"MethodDeploymentOptions"]]=None, stage_name: typing.Optional[str]=None, tracing_enabled: typing.Optional[bool]=None, variables: typing.Optional[typing.Mapping[str,str]]=None, cache_data_encrypted: typing.Optional[bool]=None, cache_ttl_seconds: typing.Optional[jsii.Number]=None, caching_enabled: typing.Optional[bool]=None, data_trace_enabled: typing.Optional[bool]=None, logging_level: typing.Optional["MethodLoggingLevel"]=None, metrics_enabled: typing.Optional[bool]=None, throttling_burst_limit: typing.Optional[jsii.Number]=None, throttling_rate_limit: typing.Optional[jsii.Number]=None) -> None:
        props: StageProps = {"deployment": deployment}

        if cache_cluster_enabled is not None:
            props["cacheClusterEnabled"] = cache_cluster_enabled

        if cache_cluster_size is not None:
            props["cacheClusterSize"] = cache_cluster_size

        if client_certificate_id is not None:
            props["clientCertificateId"] = client_certificate_id

        if description is not None:
            props["description"] = description

        if documentation_version is not None:
            props["documentationVersion"] = documentation_version

        if method_options is not None:
            props["methodOptions"] = method_options

        if stage_name is not None:
            props["stageName"] = stage_name

        if tracing_enabled is not None:
            props["tracingEnabled"] = tracing_enabled

        if variables is not None:
            props["variables"] = variables

        if cache_data_encrypted is not None:
            props["cacheDataEncrypted"] = cache_data_encrypted

        if cache_ttl_seconds is not None:
            props["cacheTtlSeconds"] = cache_ttl_seconds

        if caching_enabled is not None:
            props["cachingEnabled"] = caching_enabled

        if data_trace_enabled is not None:
            props["dataTraceEnabled"] = data_trace_enabled

        if logging_level is not None:
            props["loggingLevel"] = logging_level

        if metrics_enabled is not None:
            props["metricsEnabled"] = metrics_enabled

        if throttling_burst_limit is not None:
            props["throttlingBurstLimit"] = throttling_burst_limit

        if throttling_rate_limit is not None:
            props["throttlingRateLimit"] = throttling_rate_limit

        jsii.create(Stage, self, [scope, id, props])

    @jsii.member(jsii_name="urlForPath")
    def url_for_path(self, path: typing.Optional[str]=None) -> str:
        return jsii.invoke(self, "urlForPath", [path])

    @property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> str:
        return jsii.get(self, "stageName")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.StageOptions")
class StageOptions(MethodDeploymentOptions, jsii.compat.TypedDict, total=False):
    cacheClusterEnabled: bool
    cacheClusterSize: str
    clientCertificateId: str
    description: str
    documentationVersion: str
    methodOptions: typing.Mapping[str,"MethodDeploymentOptions"]
    stageName: str
    tracingEnabled: bool
    variables: typing.Mapping[str,str]

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.StageProps")
class StageProps(StageOptions, jsii.compat.TypedDict):
    deployment: "Deployment"

class VpcLink(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.VpcLink"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, targets: typing.List[aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancer], description: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
        props: VpcLinkProps = {"targets": targets}

        if description is not None:
            props["description"] = description

        if name is not None:
            props["name"] = name

        jsii.create(VpcLink, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="vpcLinkId")
    def vpc_link_id(self) -> str:
        return jsii.get(self, "vpcLinkId")


class _VpcLinkProps(jsii.compat.TypedDict, total=False):
    description: str
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.VpcLinkProps")
class VpcLinkProps(_VpcLinkProps):
    targets: typing.List[aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancer]

__all__ = ["ApiKeySourceType", "AuthorizationType", "AwsIntegration", "AwsIntegrationProps", "CfnAccount", "CfnAccountProps", "CfnApiKey", "CfnApiKeyProps", "CfnApiV2", "CfnApiV2Props", "CfnAuthorizer", "CfnAuthorizerProps", "CfnAuthorizerV2", "CfnAuthorizerV2Props", "CfnBasePathMapping", "CfnBasePathMappingProps", "CfnClientCertificate", "CfnClientCertificateProps", "CfnDeployment", "CfnDeploymentProps", "CfnDeploymentV2", "CfnDeploymentV2Props", "CfnDocumentationPart", "CfnDocumentationPartProps", "CfnDocumentationVersion", "CfnDocumentationVersionProps", "CfnDomainName", "CfnDomainNameProps", "CfnGatewayResponse", "CfnGatewayResponseProps", "CfnIntegrationResponseV2", "CfnIntegrationResponseV2Props", "CfnIntegrationV2", "CfnIntegrationV2Props", "CfnMethod", "CfnMethodProps", "CfnModel", "CfnModelProps", "CfnModelV2", "CfnModelV2Props", "CfnRequestValidator", "CfnRequestValidatorProps", "CfnResource", "CfnResourceProps", "CfnRestApi", "CfnRestApiProps", "CfnRouteResponseV2", "CfnRouteResponseV2Props", "CfnRouteV2", "CfnRouteV2Props", "CfnStage", "CfnStageProps", "CfnStageV2", "CfnStageV2Props", "CfnUsagePlan", "CfnUsagePlanKey", "CfnUsagePlanKeyProps", "CfnUsagePlanProps", "CfnVpcLink", "CfnVpcLinkProps", "ConnectionType", "ContentHandling", "Deployment", "DeploymentProps", "EmptyModel", "EndpointType", "ErrorModel", "HttpIntegration", "HttpIntegrationProps", "IModel", "IRestApi", "IRestApiResource", "Integration", "IntegrationOptions", "IntegrationProps", "IntegrationResponse", "IntegrationType", "LambdaIntegration", "LambdaIntegrationOptions", "LambdaRestApi", "LambdaRestApiProps", "Method", "MethodDeploymentOptions", "MethodLoggingLevel", "MethodOptions", "MethodProps", "MethodResponse", "MockIntegration", "PassthroughBehavior", "ProxyResource", "ProxyResourceProps", "Resource", "ResourceBase", "ResourceOptions", "ResourceProps", "RestApi", "RestApiImportProps", "RestApiProps", "Stage", "StageOptions", "StageProps", "VpcLink", "VpcLinkProps", "__jsii_assembly__"]

publication.publish()
