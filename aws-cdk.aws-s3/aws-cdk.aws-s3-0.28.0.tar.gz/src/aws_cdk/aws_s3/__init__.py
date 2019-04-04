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
import aws_cdk.aws_kms
import aws_cdk.aws_s3_notifications
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-s3", "0.28.0", __name__, "aws-s3@0.28.0.jsii.tgz")
class BlockPublicAccess(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3.BlockPublicAccess"):
    def __init__(self, *, block_public_acls: typing.Optional[bool]=None, block_public_policy: typing.Optional[bool]=None, ignore_public_acls: typing.Optional[bool]=None, restrict_public_buckets: typing.Optional[bool]=None) -> None:
        options: BlockPublicAccessOptions = {}

        if block_public_acls is not None:
            options["blockPublicAcls"] = block_public_acls

        if block_public_policy is not None:
            options["blockPublicPolicy"] = block_public_policy

        if ignore_public_acls is not None:
            options["ignorePublicAcls"] = ignore_public_acls

        if restrict_public_buckets is not None:
            options["restrictPublicBuckets"] = restrict_public_buckets

        jsii.create(BlockPublicAccess, self, [options])

    @classproperty
    @jsii.member(jsii_name="BlockAcls")
    def BLOCK_ACLS(cls) -> "BlockPublicAccess":
        return jsii.sget(cls, "BlockAcls")

    @classproperty
    @jsii.member(jsii_name="BlockAll")
    def BLOCK_ALL(cls) -> "BlockPublicAccess":
        return jsii.sget(cls, "BlockAll")

    @property
    @jsii.member(jsii_name="blockPublicAcls")
    def block_public_acls(self) -> typing.Optional[bool]:
        return jsii.get(self, "blockPublicAcls")

    @block_public_acls.setter
    def block_public_acls(self, value: typing.Optional[bool]):
        return jsii.set(self, "blockPublicAcls", value)

    @property
    @jsii.member(jsii_name="blockPublicPolicy")
    def block_public_policy(self) -> typing.Optional[bool]:
        return jsii.get(self, "blockPublicPolicy")

    @block_public_policy.setter
    def block_public_policy(self, value: typing.Optional[bool]):
        return jsii.set(self, "blockPublicPolicy", value)

    @property
    @jsii.member(jsii_name="ignorePublicAcls")
    def ignore_public_acls(self) -> typing.Optional[bool]:
        return jsii.get(self, "ignorePublicAcls")

    @ignore_public_acls.setter
    def ignore_public_acls(self, value: typing.Optional[bool]):
        return jsii.set(self, "ignorePublicAcls", value)

    @property
    @jsii.member(jsii_name="restrictPublicBuckets")
    def restrict_public_buckets(self) -> typing.Optional[bool]:
        return jsii.get(self, "restrictPublicBuckets")

    @restrict_public_buckets.setter
    def restrict_public_buckets(self, value: typing.Optional[bool]):
        return jsii.set(self, "restrictPublicBuckets", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.BlockPublicAccessOptions")
class BlockPublicAccessOptions(jsii.compat.TypedDict, total=False):
    blockPublicAcls: bool
    blockPublicPolicy: bool
    ignorePublicAcls: bool
    restrictPublicBuckets: bool

@jsii.enum(jsii_type="@aws-cdk/aws-s3.BucketEncryption")
class BucketEncryption(enum.Enum):
    Unencrypted = "Unencrypted"
    KmsManaged = "KmsManaged"
    S3Managed = "S3Managed"
    Kms = "Kms"

@jsii.data_type(jsii_type="@aws-cdk/aws-s3.BucketImportProps")
class BucketImportProps(jsii.compat.TypedDict, total=False):
    bucketArn: str
    bucketDomainName: str
    bucketName: str
    bucketWebsiteNewUrlFormat: bool
    bucketWebsiteUrl: str

class BucketPolicy(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3.BucketPolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, bucket: "IBucket") -> None:
        props: BucketPolicyProps = {"bucket": bucket}

        jsii.create(BucketPolicy, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="document")
    def document(self) -> aws_cdk.aws_iam.PolicyDocument:
        return jsii.get(self, "document")


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.BucketPolicyProps")
class BucketPolicyProps(jsii.compat.TypedDict):
    bucket: "IBucket"

@jsii.data_type(jsii_type="@aws-cdk/aws-s3.BucketProps")
class BucketProps(jsii.compat.TypedDict, total=False):
    blockPublicAccess: "BlockPublicAccess"
    bucketName: str
    encryption: "BucketEncryption"
    encryptionKey: aws_cdk.aws_kms.IEncryptionKey
    lifecycleRules: typing.List["LifecycleRule"]
    publicReadAccess: bool
    removalPolicy: aws_cdk.cdk.RemovalPolicy
    versioned: bool
    websiteErrorDocument: str
    websiteIndexDocument: str

class CfnBucket(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3.CfnBucket"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, accelerate_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "AccelerateConfigurationProperty"]]=None, access_control: typing.Optional[str]=None, analytics_configurations: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "AnalyticsConfigurationProperty"]]]]=None, bucket_encryption: typing.Optional[typing.Union[aws_cdk.cdk.Token, "BucketEncryptionProperty"]]=None, bucket_name: typing.Optional[str]=None, cors_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "CorsConfigurationProperty"]]=None, inventory_configurations: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "InventoryConfigurationProperty"]]]]=None, lifecycle_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LifecycleConfigurationProperty"]]=None, logging_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LoggingConfigurationProperty"]]=None, metrics_configurations: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "MetricsConfigurationProperty"]]]]=None, notification_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "NotificationConfigurationProperty"]]=None, public_access_block_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "PublicAccessBlockConfigurationProperty"]]=None, replication_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ReplicationConfigurationProperty"]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, versioning_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "VersioningConfigurationProperty"]]=None, website_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "WebsiteConfigurationProperty"]]=None) -> None:
        props: CfnBucketProps = {}

        if accelerate_configuration is not None:
            props["accelerateConfiguration"] = accelerate_configuration

        if access_control is not None:
            props["accessControl"] = access_control

        if analytics_configurations is not None:
            props["analyticsConfigurations"] = analytics_configurations

        if bucket_encryption is not None:
            props["bucketEncryption"] = bucket_encryption

        if bucket_name is not None:
            props["bucketName"] = bucket_name

        if cors_configuration is not None:
            props["corsConfiguration"] = cors_configuration

        if inventory_configurations is not None:
            props["inventoryConfigurations"] = inventory_configurations

        if lifecycle_configuration is not None:
            props["lifecycleConfiguration"] = lifecycle_configuration

        if logging_configuration is not None:
            props["loggingConfiguration"] = logging_configuration

        if metrics_configurations is not None:
            props["metricsConfigurations"] = metrics_configurations

        if notification_configuration is not None:
            props["notificationConfiguration"] = notification_configuration

        if public_access_block_configuration is not None:
            props["publicAccessBlockConfiguration"] = public_access_block_configuration

        if replication_configuration is not None:
            props["replicationConfiguration"] = replication_configuration

        if tags is not None:
            props["tags"] = tags

        if versioning_configuration is not None:
            props["versioningConfiguration"] = versioning_configuration

        if website_configuration is not None:
            props["websiteConfiguration"] = website_configuration

        jsii.create(CfnBucket, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> str:
        return jsii.get(self, "bucketArn")

    @property
    @jsii.member(jsii_name="bucketDomainName")
    def bucket_domain_name(self) -> str:
        return jsii.get(self, "bucketDomainName")

    @property
    @jsii.member(jsii_name="bucketDualStackDomainName")
    def bucket_dual_stack_domain_name(self) -> str:
        return jsii.get(self, "bucketDualStackDomainName")

    @property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> str:
        return jsii.get(self, "bucketName")

    @property
    @jsii.member(jsii_name="bucketRegionalDomainName")
    def bucket_regional_domain_name(self) -> str:
        return jsii.get(self, "bucketRegionalDomainName")

    @property
    @jsii.member(jsii_name="bucketWebsiteUrl")
    def bucket_website_url(self) -> str:
        return jsii.get(self, "bucketWebsiteUrl")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnBucketProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.AbortIncompleteMultipartUploadProperty")
    class AbortIncompleteMultipartUploadProperty(jsii.compat.TypedDict):
        daysAfterInitiation: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.AccelerateConfigurationProperty")
    class AccelerateConfigurationProperty(jsii.compat.TypedDict):
        accelerationStatus: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.AccessControlTranslationProperty")
    class AccessControlTranslationProperty(jsii.compat.TypedDict):
        owner: str

    class _AnalyticsConfigurationProperty(jsii.compat.TypedDict, total=False):
        prefix: str
        tagFilters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.TagFilterProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.AnalyticsConfigurationProperty")
    class AnalyticsConfigurationProperty(_AnalyticsConfigurationProperty):
        id: str
        storageClassAnalysis: typing.Union[aws_cdk.cdk.Token, "CfnBucket.StorageClassAnalysisProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.BucketEncryptionProperty")
    class BucketEncryptionProperty(jsii.compat.TypedDict):
        serverSideEncryptionConfiguration: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.ServerSideEncryptionRuleProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.CorsConfigurationProperty")
    class CorsConfigurationProperty(jsii.compat.TypedDict):
        corsRules: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.CorsRuleProperty"]]]

    class _CorsRuleProperty(jsii.compat.TypedDict, total=False):
        allowedHeaders: typing.List[str]
        exposedHeaders: typing.List[str]
        id: str
        maxAge: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.CorsRuleProperty")
    class CorsRuleProperty(_CorsRuleProperty):
        allowedMethods: typing.List[str]
        allowedOrigins: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.DataExportProperty")
    class DataExportProperty(jsii.compat.TypedDict):
        destination: typing.Union[aws_cdk.cdk.Token, "CfnBucket.DestinationProperty"]
        outputSchemaVersion: str

    class _DestinationProperty(jsii.compat.TypedDict, total=False):
        bucketAccountId: str
        prefix: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.DestinationProperty")
    class DestinationProperty(_DestinationProperty):
        bucketArn: str
        format: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.EncryptionConfigurationProperty")
    class EncryptionConfigurationProperty(jsii.compat.TypedDict):
        replicaKmsKeyId: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.FilterRuleProperty")
    class FilterRuleProperty(jsii.compat.TypedDict):
        name: str
        value: str

    class _InventoryConfigurationProperty(jsii.compat.TypedDict, total=False):
        optionalFields: typing.List[str]
        prefix: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.InventoryConfigurationProperty")
    class InventoryConfigurationProperty(_InventoryConfigurationProperty):
        destination: typing.Union[aws_cdk.cdk.Token, "CfnBucket.DestinationProperty"]
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        id: str
        includedObjectVersions: str
        scheduleFrequency: str

    class _LambdaConfigurationProperty(jsii.compat.TypedDict, total=False):
        filter: typing.Union[aws_cdk.cdk.Token, "CfnBucket.NotificationFilterProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.LambdaConfigurationProperty")
    class LambdaConfigurationProperty(_LambdaConfigurationProperty):
        event: str
        function: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.LifecycleConfigurationProperty")
    class LifecycleConfigurationProperty(jsii.compat.TypedDict):
        rules: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.RuleProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.LoggingConfigurationProperty")
    class LoggingConfigurationProperty(jsii.compat.TypedDict, total=False):
        destinationBucketName: str
        logFilePrefix: str

    class _MetricsConfigurationProperty(jsii.compat.TypedDict, total=False):
        prefix: str
        tagFilters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.TagFilterProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.MetricsConfigurationProperty")
    class MetricsConfigurationProperty(_MetricsConfigurationProperty):
        id: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.NoncurrentVersionTransitionProperty")
    class NoncurrentVersionTransitionProperty(jsii.compat.TypedDict):
        storageClass: str
        transitionInDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.NotificationConfigurationProperty")
    class NotificationConfigurationProperty(jsii.compat.TypedDict, total=False):
        lambdaConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.LambdaConfigurationProperty"]]]
        queueConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.QueueConfigurationProperty"]]]
        topicConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.TopicConfigurationProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.NotificationFilterProperty")
    class NotificationFilterProperty(jsii.compat.TypedDict):
        s3Key: typing.Union[aws_cdk.cdk.Token, "CfnBucket.S3KeyFilterProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.PublicAccessBlockConfigurationProperty")
    class PublicAccessBlockConfigurationProperty(jsii.compat.TypedDict, total=False):
        blockPublicAcls: typing.Union[bool, aws_cdk.cdk.Token]
        blockPublicPolicy: typing.Union[bool, aws_cdk.cdk.Token]
        ignorePublicAcls: typing.Union[bool, aws_cdk.cdk.Token]
        restrictPublicBuckets: typing.Union[bool, aws_cdk.cdk.Token]

    class _QueueConfigurationProperty(jsii.compat.TypedDict, total=False):
        filter: typing.Union[aws_cdk.cdk.Token, "CfnBucket.NotificationFilterProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.QueueConfigurationProperty")
    class QueueConfigurationProperty(_QueueConfigurationProperty):
        event: str
        queue: str

    class _RedirectAllRequestsToProperty(jsii.compat.TypedDict, total=False):
        protocol: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.RedirectAllRequestsToProperty")
    class RedirectAllRequestsToProperty(_RedirectAllRequestsToProperty):
        hostName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.RedirectRuleProperty")
    class RedirectRuleProperty(jsii.compat.TypedDict, total=False):
        hostName: str
        httpRedirectCode: str
        protocol: str
        replaceKeyPrefixWith: str
        replaceKeyWith: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.ReplicationConfigurationProperty")
    class ReplicationConfigurationProperty(jsii.compat.TypedDict):
        role: str
        rules: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.ReplicationRuleProperty"]]]

    class _ReplicationDestinationProperty(jsii.compat.TypedDict, total=False):
        accessControlTranslation: typing.Union[aws_cdk.cdk.Token, "CfnBucket.AccessControlTranslationProperty"]
        account: str
        encryptionConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnBucket.EncryptionConfigurationProperty"]
        storageClass: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.ReplicationDestinationProperty")
    class ReplicationDestinationProperty(_ReplicationDestinationProperty):
        bucket: str

    class _ReplicationRuleProperty(jsii.compat.TypedDict, total=False):
        id: str
        sourceSelectionCriteria: typing.Union[aws_cdk.cdk.Token, "CfnBucket.SourceSelectionCriteriaProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.ReplicationRuleProperty")
    class ReplicationRuleProperty(_ReplicationRuleProperty):
        destination: typing.Union[aws_cdk.cdk.Token, "CfnBucket.ReplicationDestinationProperty"]
        prefix: str
        status: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.RoutingRuleConditionProperty")
    class RoutingRuleConditionProperty(jsii.compat.TypedDict, total=False):
        httpErrorCodeReturnedEquals: str
        keyPrefixEquals: str

    class _RoutingRuleProperty(jsii.compat.TypedDict, total=False):
        routingRuleCondition: typing.Union[aws_cdk.cdk.Token, "CfnBucket.RoutingRuleConditionProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.RoutingRuleProperty")
    class RoutingRuleProperty(_RoutingRuleProperty):
        redirectRule: typing.Union[aws_cdk.cdk.Token, "CfnBucket.RedirectRuleProperty"]

    class _RuleProperty(jsii.compat.TypedDict, total=False):
        abortIncompleteMultipartUpload: typing.Union[aws_cdk.cdk.Token, "CfnBucket.AbortIncompleteMultipartUploadProperty"]
        expirationDate: typing.Union[aws_cdk.cdk.Token, datetime.datetime]
        expirationInDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        id: str
        noncurrentVersionExpirationInDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        noncurrentVersionTransition: typing.Union[aws_cdk.cdk.Token, "CfnBucket.NoncurrentVersionTransitionProperty"]
        noncurrentVersionTransitions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.NoncurrentVersionTransitionProperty"]]]
        prefix: str
        tagFilters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.TagFilterProperty"]]]
        transition: typing.Union[aws_cdk.cdk.Token, "CfnBucket.TransitionProperty"]
        transitions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.TransitionProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.RuleProperty")
    class RuleProperty(_RuleProperty):
        status: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.S3KeyFilterProperty")
    class S3KeyFilterProperty(jsii.compat.TypedDict):
        rules: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.FilterRuleProperty"]]]

    class _ServerSideEncryptionByDefaultProperty(jsii.compat.TypedDict, total=False):
        kmsMasterKeyId: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.ServerSideEncryptionByDefaultProperty")
    class ServerSideEncryptionByDefaultProperty(_ServerSideEncryptionByDefaultProperty):
        sseAlgorithm: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.ServerSideEncryptionRuleProperty")
    class ServerSideEncryptionRuleProperty(jsii.compat.TypedDict, total=False):
        serverSideEncryptionByDefault: typing.Union[aws_cdk.cdk.Token, "CfnBucket.ServerSideEncryptionByDefaultProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.SourceSelectionCriteriaProperty")
    class SourceSelectionCriteriaProperty(jsii.compat.TypedDict):
        sseKmsEncryptedObjects: typing.Union[aws_cdk.cdk.Token, "CfnBucket.SseKmsEncryptedObjectsProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.SseKmsEncryptedObjectsProperty")
    class SseKmsEncryptedObjectsProperty(jsii.compat.TypedDict):
        status: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.StorageClassAnalysisProperty")
    class StorageClassAnalysisProperty(jsii.compat.TypedDict, total=False):
        dataExport: typing.Union[aws_cdk.cdk.Token, "CfnBucket.DataExportProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.TagFilterProperty")
    class TagFilterProperty(jsii.compat.TypedDict):
        key: str
        value: str

    class _TopicConfigurationProperty(jsii.compat.TypedDict, total=False):
        filter: typing.Union[aws_cdk.cdk.Token, "CfnBucket.NotificationFilterProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.TopicConfigurationProperty")
    class TopicConfigurationProperty(_TopicConfigurationProperty):
        event: str
        topic: str

    class _TransitionProperty(jsii.compat.TypedDict, total=False):
        transitionDate: typing.Union[aws_cdk.cdk.Token, datetime.datetime]
        transitionInDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.TransitionProperty")
    class TransitionProperty(_TransitionProperty):
        storageClass: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.VersioningConfigurationProperty")
    class VersioningConfigurationProperty(jsii.compat.TypedDict):
        status: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.WebsiteConfigurationProperty")
    class WebsiteConfigurationProperty(jsii.compat.TypedDict, total=False):
        errorDocument: str
        indexDocument: str
        redirectAllRequestsTo: typing.Union[aws_cdk.cdk.Token, "CfnBucket.RedirectAllRequestsToProperty"]
        routingRules: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.RoutingRuleProperty"]]]


class CfnBucketPolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3.CfnBucketPolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, bucket: str, policy_document: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]) -> None:
        props: CfnBucketPolicyProps = {"bucket": bucket, "policyDocument": policy_document}

        jsii.create(CfnBucketPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnBucketPolicyProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucketPolicyProps")
class CfnBucketPolicyProps(jsii.compat.TypedDict):
    bucket: str
    policyDocument: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucketProps")
class CfnBucketProps(jsii.compat.TypedDict, total=False):
    accelerateConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnBucket.AccelerateConfigurationProperty"]
    accessControl: str
    analyticsConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.AnalyticsConfigurationProperty"]]]
    bucketEncryption: typing.Union[aws_cdk.cdk.Token, "CfnBucket.BucketEncryptionProperty"]
    bucketName: str
    corsConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnBucket.CorsConfigurationProperty"]
    inventoryConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.InventoryConfigurationProperty"]]]
    lifecycleConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnBucket.LifecycleConfigurationProperty"]
    loggingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnBucket.LoggingConfigurationProperty"]
    metricsConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBucket.MetricsConfigurationProperty"]]]
    notificationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnBucket.NotificationConfigurationProperty"]
    publicAccessBlockConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnBucket.PublicAccessBlockConfigurationProperty"]
    replicationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnBucket.ReplicationConfigurationProperty"]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    versioningConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnBucket.VersioningConfigurationProperty"]
    websiteConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnBucket.WebsiteConfigurationProperty"]

@jsii.enum(jsii_type="@aws-cdk/aws-s3.EventType")
class EventType(enum.Enum):
    ObjectCreated = "ObjectCreated"
    ObjectCreatedPut = "ObjectCreatedPut"
    ObjectCreatedPost = "ObjectCreatedPost"
    ObjectCreatedCopy = "ObjectCreatedCopy"
    ObjectCreatedCompleteMultipartUpload = "ObjectCreatedCompleteMultipartUpload"
    ObjectRemoved = "ObjectRemoved"
    ObjectRemovedDelete = "ObjectRemovedDelete"
    ObjectRemovedDeleteMarkerCreated = "ObjectRemovedDeleteMarkerCreated"
    ReducedRedundancyLostObject = "ReducedRedundancyLostObject"

@jsii.interface(jsii_type="@aws-cdk/aws-s3.IBucket")
class IBucket(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IBucketProxy

    @property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="bucketUrl")
    def bucket_url(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        ...

    @property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional["BucketPolicy"]:
        ...

    @policy.setter
    def policy(self, value: typing.Optional["BucketPolicy"]):
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, permission: aws_cdk.aws_iam.PolicyStatement) -> None:
        ...

    @jsii.member(jsii_name="arnForObjects")
    def arn_for_objects(self, *key_pattern: str) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "BucketImportProps":
        ...

    @jsii.member(jsii_name="grantDelete")
    def grant_delete(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantPublicAccess")
    def grant_public_access(self, key_prefix: typing.Optional[str], *allowed_actions: str) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantPut")
    def grant_put(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="onPutObject")
    def on_put_object(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, path: typing.Optional[str]=None) -> aws_cdk.aws_events.EventRule:
        ...

    @jsii.member(jsii_name="urlForObject")
    def url_for_object(self, key: typing.Optional[str]=None) -> str:
        ...


class _IBucketProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-s3.IBucket"
    @property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> str:
        return jsii.get(self, "bucketArn")

    @property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> str:
        return jsii.get(self, "bucketName")

    @property
    @jsii.member(jsii_name="bucketUrl")
    def bucket_url(self) -> str:
        return jsii.get(self, "bucketUrl")

    @property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        return jsii.get(self, "domainName")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        return jsii.get(self, "encryptionKey")

    @property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional["BucketPolicy"]:
        return jsii.get(self, "policy")

    @policy.setter
    def policy(self, value: typing.Optional["BucketPolicy"]):
        return jsii.set(self, "policy", value)

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, permission: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToResourcePolicy", [permission])

    @jsii.member(jsii_name="arnForObjects")
    def arn_for_objects(self, *key_pattern: str) -> str:
        return jsii.invoke(self, "arnForObjects", [key_pattern])

    @jsii.member(jsii_name="export")
    def export(self) -> "BucketImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grantDelete")
    def grant_delete(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantDelete", [identity, objects_key_pattern])

    @jsii.member(jsii_name="grantPublicAccess")
    def grant_public_access(self, key_prefix: typing.Optional[str], *allowed_actions: str) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantPublicAccess", [key_prefix, allowed_actions])

    @jsii.member(jsii_name="grantPut")
    def grant_put(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantPut", [identity, objects_key_pattern])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantRead", [identity, objects_key_pattern])

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantReadWrite", [identity, objects_key_pattern])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantWrite", [identity, objects_key_pattern])

    @jsii.member(jsii_name="onPutObject")
    def on_put_object(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, path: typing.Optional[str]=None) -> aws_cdk.aws_events.EventRule:
        return jsii.invoke(self, "onPutObject", [name, target, path])

    @jsii.member(jsii_name="urlForObject")
    def url_for_object(self, key: typing.Optional[str]=None) -> str:
        return jsii.invoke(self, "urlForObject", [key])


@jsii.implements(IBucket)
class BucketBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-s3.BucketBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _BucketBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(BucketBase, self, [scope, id])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, permission: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToResourcePolicy", [permission])

    @jsii.member(jsii_name="arnForObjects")
    def arn_for_objects(self, *key_pattern: str) -> str:
        return jsii.invoke(self, "arnForObjects", [key_pattern])

    @jsii.member(jsii_name="export")
    @abc.abstractmethod
    def export(self) -> "BucketImportProps":
        ...

    @jsii.member(jsii_name="grantDelete")
    def grant_delete(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantDelete", [identity, objects_key_pattern])

    @jsii.member(jsii_name="grantPublicAccess")
    def grant_public_access(self, key_prefix: typing.Optional[str], *allowed_actions: str) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantPublicAccess", [key_prefix, allowed_actions])

    @jsii.member(jsii_name="grantPut")
    def grant_put(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantPut", [identity, objects_key_pattern])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantRead", [identity, objects_key_pattern])

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantReadWrite", [identity, objects_key_pattern])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantWrite", [identity, objects_key_pattern])

    @jsii.member(jsii_name="onPutObject")
    def on_put_object(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, path: typing.Optional[str]=None) -> aws_cdk.aws_events.EventRule:
        return jsii.invoke(self, "onPutObject", [name, target, path])

    @jsii.member(jsii_name="urlForObject")
    def url_for_object(self, key: typing.Optional[str]=None) -> str:
        return jsii.invoke(self, "urlForObject", [key])

    @property
    @jsii.member(jsii_name="bucketArn")
    @abc.abstractmethod
    def bucket_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="bucketName")
    @abc.abstractmethod
    def bucket_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="bucketUrl")
    def bucket_url(self) -> str:
        return jsii.get(self, "bucketUrl")

    @property
    @jsii.member(jsii_name="domainName")
    @abc.abstractmethod
    def domain_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="encryptionKey")
    @abc.abstractmethod
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        ...

    @property
    @jsii.member(jsii_name="autoCreatePolicy")
    @abc.abstractmethod
    def _auto_create_policy(self) -> bool:
        ...

    @_auto_create_policy.setter
    @abc.abstractmethod
    def _auto_create_policy(self, value: bool):
        ...

    @property
    @jsii.member(jsii_name="disallowPublicAccess")
    @abc.abstractmethod
    def _disallow_public_access(self) -> typing.Optional[bool]:
        ...

    @_disallow_public_access.setter
    @abc.abstractmethod
    def _disallow_public_access(self, value: typing.Optional[bool]):
        ...

    @property
    @jsii.member(jsii_name="policy")
    @abc.abstractmethod
    def policy(self) -> typing.Optional["BucketPolicy"]:
        ...

    @policy.setter
    @abc.abstractmethod
    def policy(self, value: typing.Optional["BucketPolicy"]):
        ...


class _BucketBaseProxy(BucketBase):
    @jsii.member(jsii_name="export")
    def export(self) -> "BucketImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> str:
        return jsii.get(self, "bucketArn")

    @property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> str:
        return jsii.get(self, "bucketName")

    @property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        return jsii.get(self, "domainName")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        return jsii.get(self, "encryptionKey")

    @property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> bool:
        return jsii.get(self, "autoCreatePolicy")

    @_auto_create_policy.setter
    def _auto_create_policy(self, value: bool):
        return jsii.set(self, "autoCreatePolicy", value)

    @property
    @jsii.member(jsii_name="disallowPublicAccess")
    def _disallow_public_access(self) -> typing.Optional[bool]:
        return jsii.get(self, "disallowPublicAccess")

    @_disallow_public_access.setter
    def _disallow_public_access(self, value: typing.Optional[bool]):
        return jsii.set(self, "disallowPublicAccess", value)

    @property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional["BucketPolicy"]:
        return jsii.get(self, "policy")

    @policy.setter
    def policy(self, value: typing.Optional["BucketPolicy"]):
        return jsii.set(self, "policy", value)


class Bucket(BucketBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3.Bucket"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, block_public_access: typing.Optional["BlockPublicAccess"]=None, bucket_name: typing.Optional[str]=None, encryption: typing.Optional["BucketEncryption"]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IEncryptionKey]=None, lifecycle_rules: typing.Optional[typing.List["LifecycleRule"]]=None, public_read_access: typing.Optional[bool]=None, removal_policy: typing.Optional[aws_cdk.cdk.RemovalPolicy]=None, versioned: typing.Optional[bool]=None, website_error_document: typing.Optional[str]=None, website_index_document: typing.Optional[str]=None) -> None:
        props: BucketProps = {}

        if block_public_access is not None:
            props["blockPublicAccess"] = block_public_access

        if bucket_name is not None:
            props["bucketName"] = bucket_name

        if encryption is not None:
            props["encryption"] = encryption

        if encryption_key is not None:
            props["encryptionKey"] = encryption_key

        if lifecycle_rules is not None:
            props["lifecycleRules"] = lifecycle_rules

        if public_read_access is not None:
            props["publicReadAccess"] = public_read_access

        if removal_policy is not None:
            props["removalPolicy"] = removal_policy

        if versioned is not None:
            props["versioned"] = versioned

        if website_error_document is not None:
            props["websiteErrorDocument"] = website_error_document

        if website_index_document is not None:
            props["websiteIndexDocument"] = website_index_document

        jsii.create(Bucket, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, bucket_arn: typing.Optional[str]=None, bucket_domain_name: typing.Optional[str]=None, bucket_name: typing.Optional[str]=None, bucket_website_new_url_format: typing.Optional[bool]=None, bucket_website_url: typing.Optional[str]=None) -> "IBucket":
        props: BucketImportProps = {}

        if bucket_arn is not None:
            props["bucketArn"] = bucket_arn

        if bucket_domain_name is not None:
            props["bucketDomainName"] = bucket_domain_name

        if bucket_name is not None:
            props["bucketName"] = bucket_name

        if bucket_website_new_url_format is not None:
            props["bucketWebsiteNewUrlFormat"] = bucket_website_new_url_format

        if bucket_website_url is not None:
            props["bucketWebsiteUrl"] = bucket_website_url

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addLifecycleRule")
    def add_lifecycle_rule(self, *, abort_incomplete_multipart_upload_after_days: typing.Optional[jsii.Number]=None, enabled: typing.Optional[bool]=None, expiration_date: typing.Optional[datetime.datetime]=None, expiration_in_days: typing.Optional[jsii.Number]=None, id: typing.Optional[str]=None, noncurrent_version_expiration_in_days: typing.Optional[jsii.Number]=None, noncurrent_version_transitions: typing.Optional[typing.List["NoncurrentVersionTransition"]]=None, prefix: typing.Optional[str]=None, tag_filters: typing.Optional[typing.Mapping[str,typing.Any]]=None, transitions: typing.Optional[typing.List["Transition"]]=None) -> None:
        rule: LifecycleRule = {}

        if abort_incomplete_multipart_upload_after_days is not None:
            rule["abortIncompleteMultipartUploadAfterDays"] = abort_incomplete_multipart_upload_after_days

        if enabled is not None:
            rule["enabled"] = enabled

        if expiration_date is not None:
            rule["expirationDate"] = expiration_date

        if expiration_in_days is not None:
            rule["expirationInDays"] = expiration_in_days

        if id is not None:
            rule["id"] = id

        if noncurrent_version_expiration_in_days is not None:
            rule["noncurrentVersionExpirationInDays"] = noncurrent_version_expiration_in_days

        if noncurrent_version_transitions is not None:
            rule["noncurrentVersionTransitions"] = noncurrent_version_transitions

        if prefix is not None:
            rule["prefix"] = prefix

        if tag_filters is not None:
            rule["tagFilters"] = tag_filters

        if transitions is not None:
            rule["transitions"] = transitions

        return jsii.invoke(self, "addLifecycleRule", [rule])

    @jsii.member(jsii_name="export")
    def export(self) -> "BucketImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="onEvent")
    def on_event(self, event: "EventType", dest: aws_cdk.aws_s3_notifications.IBucketNotificationDestination, *, prefix: typing.Optional[str]=None, suffix: typing.Optional[str]=None) -> None:
        filters: NotificationKeyFilter = {}

        if prefix is not None:
            filters["prefix"] = prefix

        if suffix is not None:
            filters["suffix"] = suffix

        return jsii.invoke(self, "onEvent", [event, dest, filters])

    @jsii.member(jsii_name="onObjectCreated")
    def on_object_created(self, dest: aws_cdk.aws_s3_notifications.IBucketNotificationDestination, *, prefix: typing.Optional[str]=None, suffix: typing.Optional[str]=None) -> None:
        filters: NotificationKeyFilter = {}

        if prefix is not None:
            filters["prefix"] = prefix

        if suffix is not None:
            filters["suffix"] = suffix

        return jsii.invoke(self, "onObjectCreated", [dest, filters])

    @jsii.member(jsii_name="onObjectRemoved")
    def on_object_removed(self, dest: aws_cdk.aws_s3_notifications.IBucketNotificationDestination, *, prefix: typing.Optional[str]=None, suffix: typing.Optional[str]=None) -> None:
        filters: NotificationKeyFilter = {}

        if prefix is not None:
            filters["prefix"] = prefix

        if suffix is not None:
            filters["suffix"] = suffix

        return jsii.invoke(self, "onObjectRemoved", [dest, filters])

    @property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> str:
        return jsii.get(self, "bucketArn")

    @property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> str:
        return jsii.get(self, "bucketName")

    @property
    @jsii.member(jsii_name="bucketWebsiteUrl")
    def bucket_website_url(self) -> str:
        return jsii.get(self, "bucketWebsiteUrl")

    @property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        return jsii.get(self, "domainName")

    @property
    @jsii.member(jsii_name="dualstackDomainName")
    def dualstack_domain_name(self) -> str:
        return jsii.get(self, "dualstackDomainName")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        return jsii.get(self, "encryptionKey")

    @property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> bool:
        return jsii.get(self, "autoCreatePolicy")

    @_auto_create_policy.setter
    def _auto_create_policy(self, value: bool):
        return jsii.set(self, "autoCreatePolicy", value)

    @property
    @jsii.member(jsii_name="disallowPublicAccess")
    def _disallow_public_access(self) -> typing.Optional[bool]:
        return jsii.get(self, "disallowPublicAccess")

    @_disallow_public_access.setter
    def _disallow_public_access(self, value: typing.Optional[bool]):
        return jsii.set(self, "disallowPublicAccess", value)

    @property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional["BucketPolicy"]:
        return jsii.get(self, "policy")

    @policy.setter
    def policy(self, value: typing.Optional["BucketPolicy"]):
        return jsii.set(self, "policy", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.LifecycleRule")
class LifecycleRule(jsii.compat.TypedDict, total=False):
    abortIncompleteMultipartUploadAfterDays: jsii.Number
    enabled: bool
    expirationDate: datetime.datetime
    expirationInDays: jsii.Number
    id: str
    noncurrentVersionExpirationInDays: jsii.Number
    noncurrentVersionTransitions: typing.List["NoncurrentVersionTransition"]
    prefix: str
    tagFilters: typing.Mapping[str,typing.Any]
    transitions: typing.List["Transition"]

@jsii.data_type(jsii_type="@aws-cdk/aws-s3.NoncurrentVersionTransition")
class NoncurrentVersionTransition(jsii.compat.TypedDict):
    storageClass: "StorageClass"
    transitionInDays: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-s3.NotificationKeyFilter")
class NotificationKeyFilter(jsii.compat.TypedDict, total=False):
    prefix: str
    suffix: str

@jsii.enum(jsii_type="@aws-cdk/aws-s3.StorageClass")
class StorageClass(enum.Enum):
    InfrequentAccess = "InfrequentAccess"
    OneZoneInfrequentAccess = "OneZoneInfrequentAccess"
    Glacier = "Glacier"

class _Transition(jsii.compat.TypedDict, total=False):
    transitionDate: datetime.datetime
    transitionInDays: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-s3.Transition")
class Transition(_Transition):
    storageClass: "StorageClass"

__all__ = ["BlockPublicAccess", "BlockPublicAccessOptions", "Bucket", "BucketBase", "BucketEncryption", "BucketImportProps", "BucketPolicy", "BucketPolicyProps", "BucketProps", "CfnBucket", "CfnBucketPolicy", "CfnBucketPolicyProps", "CfnBucketProps", "EventType", "IBucket", "LifecycleRule", "NoncurrentVersionTransition", "NotificationKeyFilter", "StorageClass", "Transition", "__jsii_assembly__"]

publication.publish()
