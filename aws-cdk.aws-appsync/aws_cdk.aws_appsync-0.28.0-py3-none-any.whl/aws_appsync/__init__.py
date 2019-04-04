import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-appsync", "0.28.0", __name__, "aws-appsync@0.28.0.jsii.tgz")
class CfnApiKey(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appsync.CfnApiKey"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api_id: str, description: typing.Optional[str]=None, expires: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnApiKeyProps = {"apiId": api_id}

        if description is not None:
            props["description"] = description

        if expires is not None:
            props["expires"] = expires

        jsii.create(CfnApiKey, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> str:
        return jsii.get(self, "apiKey")

    @property
    @jsii.member(jsii_name="apiKeyArn")
    def api_key_arn(self) -> str:
        return jsii.get(self, "apiKeyArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApiKeyProps":
        return jsii.get(self, "propertyOverrides")


class _CfnApiKeyProps(jsii.compat.TypedDict, total=False):
    description: str
    expires: typing.Union[jsii.Number, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnApiKeyProps")
class CfnApiKeyProps(_CfnApiKeyProps):
    apiId: str

class CfnDataSource(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appsync.CfnDataSource"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api_id: str, name: str, type: str, description: typing.Optional[str]=None, dynamo_db_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "DynamoDBConfigProperty"]]=None, elasticsearch_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ElasticsearchConfigProperty"]]=None, http_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "HttpConfigProperty"]]=None, lambda_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LambdaConfigProperty"]]=None, relational_database_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "RelationalDatabaseConfigProperty"]]=None, service_role_arn: typing.Optional[str]=None) -> None:
        props: CfnDataSourceProps = {"apiId": api_id, "name": name, "type": type}

        if description is not None:
            props["description"] = description

        if dynamo_db_config is not None:
            props["dynamoDbConfig"] = dynamo_db_config

        if elasticsearch_config is not None:
            props["elasticsearchConfig"] = elasticsearch_config

        if http_config is not None:
            props["httpConfig"] = http_config

        if lambda_config is not None:
            props["lambdaConfig"] = lambda_config

        if relational_database_config is not None:
            props["relationalDatabaseConfig"] = relational_database_config

        if service_role_arn is not None:
            props["serviceRoleArn"] = service_role_arn

        jsii.create(CfnDataSource, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="dataSourceArn")
    def data_source_arn(self) -> str:
        return jsii.get(self, "dataSourceArn")

    @property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> str:
        return jsii.get(self, "dataSourceName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDataSourceProps":
        return jsii.get(self, "propertyOverrides")

    class _AuthorizationConfigProperty(jsii.compat.TypedDict, total=False):
        awsIamConfig: typing.Union[aws_cdk.cdk.Token, "CfnDataSource.AwsIamConfigProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnDataSource.AuthorizationConfigProperty")
    class AuthorizationConfigProperty(_AuthorizationConfigProperty):
        authorizationType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnDataSource.AwsIamConfigProperty")
    class AwsIamConfigProperty(jsii.compat.TypedDict, total=False):
        signingRegion: str
        signingServiceName: str

    class _DynamoDBConfigProperty(jsii.compat.TypedDict, total=False):
        useCallerCredentials: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnDataSource.DynamoDBConfigProperty")
    class DynamoDBConfigProperty(_DynamoDBConfigProperty):
        awsRegion: str
        tableName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnDataSource.ElasticsearchConfigProperty")
    class ElasticsearchConfigProperty(jsii.compat.TypedDict):
        awsRegion: str
        endpoint: str

    class _HttpConfigProperty(jsii.compat.TypedDict, total=False):
        authorizationConfig: typing.Union[aws_cdk.cdk.Token, "CfnDataSource.AuthorizationConfigProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnDataSource.HttpConfigProperty")
    class HttpConfigProperty(_HttpConfigProperty):
        endpoint: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnDataSource.LambdaConfigProperty")
    class LambdaConfigProperty(jsii.compat.TypedDict):
        lambdaFunctionArn: str

    class _RdsHttpEndpointConfigProperty(jsii.compat.TypedDict, total=False):
        databaseName: str
        schema: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnDataSource.RdsHttpEndpointConfigProperty")
    class RdsHttpEndpointConfigProperty(_RdsHttpEndpointConfigProperty):
        awsRegion: str
        awsSecretStoreArn: str
        dbClusterIdentifier: str

    class _RelationalDatabaseConfigProperty(jsii.compat.TypedDict, total=False):
        rdsHttpEndpointConfig: typing.Union[aws_cdk.cdk.Token, "CfnDataSource.RdsHttpEndpointConfigProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnDataSource.RelationalDatabaseConfigProperty")
    class RelationalDatabaseConfigProperty(_RelationalDatabaseConfigProperty):
        relationalDatabaseSourceType: str


class _CfnDataSourceProps(jsii.compat.TypedDict, total=False):
    description: str
    dynamoDbConfig: typing.Union[aws_cdk.cdk.Token, "CfnDataSource.DynamoDBConfigProperty"]
    elasticsearchConfig: typing.Union[aws_cdk.cdk.Token, "CfnDataSource.ElasticsearchConfigProperty"]
    httpConfig: typing.Union[aws_cdk.cdk.Token, "CfnDataSource.HttpConfigProperty"]
    lambdaConfig: typing.Union[aws_cdk.cdk.Token, "CfnDataSource.LambdaConfigProperty"]
    relationalDatabaseConfig: typing.Union[aws_cdk.cdk.Token, "CfnDataSource.RelationalDatabaseConfigProperty"]
    serviceRoleArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnDataSourceProps")
class CfnDataSourceProps(_CfnDataSourceProps):
    apiId: str
    name: str
    type: str

class CfnFunctionConfiguration(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appsync.CfnFunctionConfiguration"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api_id: str, data_source_name: typing.Optional[str]=None, description: typing.Optional[str]=None, function_version: typing.Optional[str]=None, name: typing.Optional[str]=None, request_mapping_template: typing.Optional[str]=None, request_mapping_template_s3_location: typing.Optional[str]=None, response_mapping_template: typing.Optional[str]=None, response_mapping_template_s3_location: typing.Optional[str]=None) -> None:
        props: CfnFunctionConfigurationProps = {"apiId": api_id}

        if data_source_name is not None:
            props["dataSourceName"] = data_source_name

        if description is not None:
            props["description"] = description

        if function_version is not None:
            props["functionVersion"] = function_version

        if name is not None:
            props["name"] = name

        if request_mapping_template is not None:
            props["requestMappingTemplate"] = request_mapping_template

        if request_mapping_template_s3_location is not None:
            props["requestMappingTemplateS3Location"] = request_mapping_template_s3_location

        if response_mapping_template is not None:
            props["responseMappingTemplate"] = response_mapping_template

        if response_mapping_template_s3_location is not None:
            props["responseMappingTemplateS3Location"] = response_mapping_template_s3_location

        jsii.create(CfnFunctionConfiguration, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="functionConfigurationArn")
    def function_configuration_arn(self) -> str:
        return jsii.get(self, "functionConfigurationArn")

    @property
    @jsii.member(jsii_name="functionConfigurationDataSourceName")
    def function_configuration_data_source_name(self) -> str:
        return jsii.get(self, "functionConfigurationDataSourceName")

    @property
    @jsii.member(jsii_name="functionConfigurationFunctionArn")
    def function_configuration_function_arn(self) -> str:
        return jsii.get(self, "functionConfigurationFunctionArn")

    @property
    @jsii.member(jsii_name="functionConfigurationFunctionId")
    def function_configuration_function_id(self) -> str:
        return jsii.get(self, "functionConfigurationFunctionId")

    @property
    @jsii.member(jsii_name="functionConfigurationName")
    def function_configuration_name(self) -> str:
        return jsii.get(self, "functionConfigurationName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnFunctionConfigurationProps":
        return jsii.get(self, "propertyOverrides")


class _CfnFunctionConfigurationProps(jsii.compat.TypedDict, total=False):
    dataSourceName: str
    description: str
    functionVersion: str
    name: str
    requestMappingTemplate: str
    requestMappingTemplateS3Location: str
    responseMappingTemplate: str
    responseMappingTemplateS3Location: str

@jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnFunctionConfigurationProps")
class CfnFunctionConfigurationProps(_CfnFunctionConfigurationProps):
    apiId: str

class CfnGraphQLApi(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appsync.CfnGraphQLApi"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, authentication_type: str, name: str, log_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LogConfigProperty"]]=None, open_id_connect_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "OpenIDConnectConfigProperty"]]=None, user_pool_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "UserPoolConfigProperty"]]=None) -> None:
        props: CfnGraphQLApiProps = {"authenticationType": authentication_type, "name": name}

        if log_config is not None:
            props["logConfig"] = log_config

        if open_id_connect_config is not None:
            props["openIdConnectConfig"] = open_id_connect_config

        if user_pool_config is not None:
            props["userPoolConfig"] = user_pool_config

        jsii.create(CfnGraphQLApi, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="graphQlApiApiId")
    def graph_ql_api_api_id(self) -> str:
        return jsii.get(self, "graphQlApiApiId")

    @property
    @jsii.member(jsii_name="graphQlApiArn")
    def graph_ql_api_arn(self) -> str:
        return jsii.get(self, "graphQlApiArn")

    @property
    @jsii.member(jsii_name="graphQlApiGraphQlUrl")
    def graph_ql_api_graph_ql_url(self) -> str:
        return jsii.get(self, "graphQlApiGraphQlUrl")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnGraphQLApiProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnGraphQLApi.LogConfigProperty")
    class LogConfigProperty(jsii.compat.TypedDict, total=False):
        cloudWatchLogsRoleArn: str
        fieldLogLevel: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnGraphQLApi.OpenIDConnectConfigProperty")
    class OpenIDConnectConfigProperty(jsii.compat.TypedDict, total=False):
        authTtl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        clientId: str
        iatTtl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        issuer: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnGraphQLApi.UserPoolConfigProperty")
    class UserPoolConfigProperty(jsii.compat.TypedDict, total=False):
        appIdClientRegex: str
        awsRegion: str
        defaultAction: str
        userPoolId: str


class _CfnGraphQLApiProps(jsii.compat.TypedDict, total=False):
    logConfig: typing.Union[aws_cdk.cdk.Token, "CfnGraphQLApi.LogConfigProperty"]
    openIdConnectConfig: typing.Union[aws_cdk.cdk.Token, "CfnGraphQLApi.OpenIDConnectConfigProperty"]
    userPoolConfig: typing.Union[aws_cdk.cdk.Token, "CfnGraphQLApi.UserPoolConfigProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnGraphQLApiProps")
class CfnGraphQLApiProps(_CfnGraphQLApiProps):
    authenticationType: str
    name: str

class CfnGraphQLSchema(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appsync.CfnGraphQLSchema"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api_id: str, definition: typing.Optional[str]=None, definition_s3_location: typing.Optional[str]=None) -> None:
        props: CfnGraphQLSchemaProps = {"apiId": api_id}

        if definition is not None:
            props["definition"] = definition

        if definition_s3_location is not None:
            props["definitionS3Location"] = definition_s3_location

        jsii.create(CfnGraphQLSchema, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="graphQlSchemaId")
    def graph_ql_schema_id(self) -> str:
        return jsii.get(self, "graphQlSchemaId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnGraphQLSchemaProps":
        return jsii.get(self, "propertyOverrides")


class _CfnGraphQLSchemaProps(jsii.compat.TypedDict, total=False):
    definition: str
    definitionS3Location: str

@jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnGraphQLSchemaProps")
class CfnGraphQLSchemaProps(_CfnGraphQLSchemaProps):
    apiId: str

class CfnResolver(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appsync.CfnResolver"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, api_id: str, field_name: str, type_name: str, data_source_name: typing.Optional[str]=None, kind: typing.Optional[str]=None, pipeline_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "PipelineConfigProperty"]]=None, request_mapping_template: typing.Optional[str]=None, request_mapping_template_s3_location: typing.Optional[str]=None, response_mapping_template: typing.Optional[str]=None, response_mapping_template_s3_location: typing.Optional[str]=None) -> None:
        props: CfnResolverProps = {"apiId": api_id, "fieldName": field_name, "typeName": type_name}

        if data_source_name is not None:
            props["dataSourceName"] = data_source_name

        if kind is not None:
            props["kind"] = kind

        if pipeline_config is not None:
            props["pipelineConfig"] = pipeline_config

        if request_mapping_template is not None:
            props["requestMappingTemplate"] = request_mapping_template

        if request_mapping_template_s3_location is not None:
            props["requestMappingTemplateS3Location"] = request_mapping_template_s3_location

        if response_mapping_template is not None:
            props["responseMappingTemplate"] = response_mapping_template

        if response_mapping_template_s3_location is not None:
            props["responseMappingTemplateS3Location"] = response_mapping_template_s3_location

        jsii.create(CfnResolver, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnResolverProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="resolverArn")
    def resolver_arn(self) -> str:
        return jsii.get(self, "resolverArn")

    @property
    @jsii.member(jsii_name="resolverFieldName")
    def resolver_field_name(self) -> str:
        return jsii.get(self, "resolverFieldName")

    @property
    @jsii.member(jsii_name="resolverTypeName")
    def resolver_type_name(self) -> str:
        return jsii.get(self, "resolverTypeName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnResolver.PipelineConfigProperty")
    class PipelineConfigProperty(jsii.compat.TypedDict, total=False):
        functions: typing.List[str]


class _CfnResolverProps(jsii.compat.TypedDict, total=False):
    dataSourceName: str
    kind: str
    pipelineConfig: typing.Union[aws_cdk.cdk.Token, "CfnResolver.PipelineConfigProperty"]
    requestMappingTemplate: str
    requestMappingTemplateS3Location: str
    responseMappingTemplate: str
    responseMappingTemplateS3Location: str

@jsii.data_type(jsii_type="@aws-cdk/aws-appsync.CfnResolverProps")
class CfnResolverProps(_CfnResolverProps):
    apiId: str
    fieldName: str
    typeName: str

__all__ = ["CfnApiKey", "CfnApiKeyProps", "CfnDataSource", "CfnDataSourceProps", "CfnFunctionConfiguration", "CfnFunctionConfigurationProps", "CfnGraphQLApi", "CfnGraphQLApiProps", "CfnGraphQLSchema", "CfnGraphQLSchemaProps", "CfnResolver", "CfnResolverProps", "__jsii_assembly__"]

publication.publish()
