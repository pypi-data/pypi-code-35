import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-servicecatalog", "0.28.0", __name__, "aws-servicecatalog@0.28.0.jsii.tgz")
class CfnAcceptedPortfolioShare(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnAcceptedPortfolioShare"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, portfolio_id: str, accept_language: typing.Optional[str]=None) -> None:
        props: CfnAcceptedPortfolioShareProps = {"portfolioId": portfolio_id}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        jsii.create(CfnAcceptedPortfolioShare, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="acceptedPortfolioShareId")
    def accepted_portfolio_share_id(self) -> str:
        return jsii.get(self, "acceptedPortfolioShareId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAcceptedPortfolioShareProps":
        return jsii.get(self, "propertyOverrides")


class _CfnAcceptedPortfolioShareProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnAcceptedPortfolioShareProps")
class CfnAcceptedPortfolioShareProps(_CfnAcceptedPortfolioShareProps):
    portfolioId: str

class CfnCloudFormationProduct(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnCloudFormationProduct"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, owner: str, provisioning_artifact_parameters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["ProvisioningArtifactPropertiesProperty", aws_cdk.cdk.Token]]], accept_language: typing.Optional[str]=None, description: typing.Optional[str]=None, distributor: typing.Optional[str]=None, support_description: typing.Optional[str]=None, support_email: typing.Optional[str]=None, support_url: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnCloudFormationProductProps = {"name": name, "owner": owner, "provisioningArtifactParameters": provisioning_artifact_parameters}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        if description is not None:
            props["description"] = description

        if distributor is not None:
            props["distributor"] = distributor

        if support_description is not None:
            props["supportDescription"] = support_description

        if support_email is not None:
            props["supportEmail"] = support_email

        if support_url is not None:
            props["supportUrl"] = support_url

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnCloudFormationProduct, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="cloudFormationProductId")
    def cloud_formation_product_id(self) -> str:
        return jsii.get(self, "cloudFormationProductId")

    @property
    @jsii.member(jsii_name="cloudFormationProductProductName")
    def cloud_formation_product_product_name(self) -> str:
        return jsii.get(self, "cloudFormationProductProductName")

    @property
    @jsii.member(jsii_name="cloudFormationProductProvisioningArtifactIds")
    def cloud_formation_product_provisioning_artifact_ids(self) -> str:
        return jsii.get(self, "cloudFormationProductProvisioningArtifactIds")

    @property
    @jsii.member(jsii_name="cloudFormationProductProvisioningArtifactNames")
    def cloud_formation_product_provisioning_artifact_names(self) -> str:
        return jsii.get(self, "cloudFormationProductProvisioningArtifactNames")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCloudFormationProductProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    class _ProvisioningArtifactPropertiesProperty(jsii.compat.TypedDict, total=False):
        description: str
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty")
    class ProvisioningArtifactPropertiesProperty(_ProvisioningArtifactPropertiesProperty):
        info: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]


class _CfnCloudFormationProductProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    description: str
    distributor: str
    supportDescription: str
    supportEmail: str
    supportUrl: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnCloudFormationProductProps")
class CfnCloudFormationProductProps(_CfnCloudFormationProductProps):
    name: str
    owner: str
    provisioningArtifactParameters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty", aws_cdk.cdk.Token]]]

class CfnCloudFormationProvisionedProduct(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnCloudFormationProvisionedProduct"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, accept_language: typing.Optional[str]=None, notification_arns: typing.Optional[typing.List[str]]=None, path_id: typing.Optional[str]=None, product_id: typing.Optional[str]=None, product_name: typing.Optional[str]=None, provisioned_product_name: typing.Optional[str]=None, provisioning_artifact_id: typing.Optional[str]=None, provisioning_artifact_name: typing.Optional[str]=None, provisioning_parameters: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ProvisioningParameterProperty"]]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnCloudFormationProvisionedProductProps = {}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        if notification_arns is not None:
            props["notificationArns"] = notification_arns

        if path_id is not None:
            props["pathId"] = path_id

        if product_id is not None:
            props["productId"] = product_id

        if product_name is not None:
            props["productName"] = product_name

        if provisioned_product_name is not None:
            props["provisionedProductName"] = provisioned_product_name

        if provisioning_artifact_id is not None:
            props["provisioningArtifactId"] = provisioning_artifact_id

        if provisioning_artifact_name is not None:
            props["provisioningArtifactName"] = provisioning_artifact_name

        if provisioning_parameters is not None:
            props["provisioningParameters"] = provisioning_parameters

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnCloudFormationProvisionedProduct, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="cloudFormationProvisionedProductCloudformationStackArn")
    def cloud_formation_provisioned_product_cloudformation_stack_arn(self) -> str:
        return jsii.get(self, "cloudFormationProvisionedProductCloudformationStackArn")

    @property
    @jsii.member(jsii_name="cloudFormationProvisionedProductId")
    def cloud_formation_provisioned_product_id(self) -> str:
        return jsii.get(self, "cloudFormationProvisionedProductId")

    @property
    @jsii.member(jsii_name="cloudFormationProvisionedProductRecordId")
    def cloud_formation_provisioned_product_record_id(self) -> str:
        return jsii.get(self, "cloudFormationProvisionedProductRecordId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCloudFormationProvisionedProductProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty")
    class ProvisioningParameterProperty(jsii.compat.TypedDict, total=False):
        key: str
        value: str


@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnCloudFormationProvisionedProductProps")
class CfnCloudFormationProvisionedProductProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    notificationArns: typing.List[str]
    pathId: str
    productId: str
    productName: str
    provisionedProductName: str
    provisioningArtifactId: str
    provisioningArtifactName: str
    provisioningParameters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty"]]]
    tags: typing.List[aws_cdk.cdk.CfnTag]

class CfnLaunchNotificationConstraint(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnLaunchNotificationConstraint"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, notification_arns: typing.List[str], portfolio_id: str, product_id: str, accept_language: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        props: CfnLaunchNotificationConstraintProps = {"notificationArns": notification_arns, "portfolioId": portfolio_id, "productId": product_id}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        if description is not None:
            props["description"] = description

        jsii.create(CfnLaunchNotificationConstraint, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="launchNotificationConstraintId")
    def launch_notification_constraint_id(self) -> str:
        return jsii.get(self, "launchNotificationConstraintId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLaunchNotificationConstraintProps":
        return jsii.get(self, "propertyOverrides")


class _CfnLaunchNotificationConstraintProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnLaunchNotificationConstraintProps")
class CfnLaunchNotificationConstraintProps(_CfnLaunchNotificationConstraintProps):
    notificationArns: typing.List[str]
    portfolioId: str
    productId: str

class CfnLaunchRoleConstraint(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnLaunchRoleConstraint"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, portfolio_id: str, product_id: str, role_arn: str, accept_language: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        props: CfnLaunchRoleConstraintProps = {"portfolioId": portfolio_id, "productId": product_id, "roleArn": role_arn}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        if description is not None:
            props["description"] = description

        jsii.create(CfnLaunchRoleConstraint, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="launchRoleConstraintId")
    def launch_role_constraint_id(self) -> str:
        return jsii.get(self, "launchRoleConstraintId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLaunchRoleConstraintProps":
        return jsii.get(self, "propertyOverrides")


class _CfnLaunchRoleConstraintProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnLaunchRoleConstraintProps")
class CfnLaunchRoleConstraintProps(_CfnLaunchRoleConstraintProps):
    portfolioId: str
    productId: str
    roleArn: str

class CfnLaunchTemplateConstraint(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnLaunchTemplateConstraint"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, portfolio_id: str, product_id: str, rules: str, accept_language: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        props: CfnLaunchTemplateConstraintProps = {"portfolioId": portfolio_id, "productId": product_id, "rules": rules}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        if description is not None:
            props["description"] = description

        jsii.create(CfnLaunchTemplateConstraint, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="launchTemplateConstraintId")
    def launch_template_constraint_id(self) -> str:
        return jsii.get(self, "launchTemplateConstraintId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLaunchTemplateConstraintProps":
        return jsii.get(self, "propertyOverrides")


class _CfnLaunchTemplateConstraintProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnLaunchTemplateConstraintProps")
class CfnLaunchTemplateConstraintProps(_CfnLaunchTemplateConstraintProps):
    portfolioId: str
    productId: str
    rules: str

class CfnPortfolio(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnPortfolio"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, display_name: str, provider_name: str, accept_language: typing.Optional[str]=None, description: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnPortfolioProps = {"displayName": display_name, "providerName": provider_name}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        if description is not None:
            props["description"] = description

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnPortfolio, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="portfolioId")
    def portfolio_id(self) -> str:
        return jsii.get(self, "portfolioId")

    @property
    @jsii.member(jsii_name="portfolioName")
    def portfolio_name(self) -> str:
        return jsii.get(self, "portfolioName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPortfolioProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class CfnPortfolioPrincipalAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnPortfolioPrincipalAssociation"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, portfolio_id: str, principal_arn: str, principal_type: str, accept_language: typing.Optional[str]=None) -> None:
        props: CfnPortfolioPrincipalAssociationProps = {"portfolioId": portfolio_id, "principalArn": principal_arn, "principalType": principal_type}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        jsii.create(CfnPortfolioPrincipalAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="portfolioPrincipalAssociationId")
    def portfolio_principal_association_id(self) -> str:
        return jsii.get(self, "portfolioPrincipalAssociationId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPortfolioPrincipalAssociationProps":
        return jsii.get(self, "propertyOverrides")


class _CfnPortfolioPrincipalAssociationProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnPortfolioPrincipalAssociationProps")
class CfnPortfolioPrincipalAssociationProps(_CfnPortfolioPrincipalAssociationProps):
    portfolioId: str
    principalArn: str
    principalType: str

class CfnPortfolioProductAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnPortfolioProductAssociation"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, portfolio_id: str, product_id: str, accept_language: typing.Optional[str]=None, source_portfolio_id: typing.Optional[str]=None) -> None:
        props: CfnPortfolioProductAssociationProps = {"portfolioId": portfolio_id, "productId": product_id}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        if source_portfolio_id is not None:
            props["sourcePortfolioId"] = source_portfolio_id

        jsii.create(CfnPortfolioProductAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="portfolioProductAssociationId")
    def portfolio_product_association_id(self) -> str:
        return jsii.get(self, "portfolioProductAssociationId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPortfolioProductAssociationProps":
        return jsii.get(self, "propertyOverrides")


class _CfnPortfolioProductAssociationProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    sourcePortfolioId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnPortfolioProductAssociationProps")
class CfnPortfolioProductAssociationProps(_CfnPortfolioProductAssociationProps):
    portfolioId: str
    productId: str

class _CfnPortfolioProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    description: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnPortfolioProps")
class CfnPortfolioProps(_CfnPortfolioProps):
    displayName: str
    providerName: str

class CfnPortfolioShare(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnPortfolioShare"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, account_id: str, portfolio_id: str, accept_language: typing.Optional[str]=None) -> None:
        props: CfnPortfolioShareProps = {"accountId": account_id, "portfolioId": portfolio_id}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        jsii.create(CfnPortfolioShare, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="portfolioShareId")
    def portfolio_share_id(self) -> str:
        return jsii.get(self, "portfolioShareId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPortfolioShareProps":
        return jsii.get(self, "propertyOverrides")


class _CfnPortfolioShareProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnPortfolioShareProps")
class CfnPortfolioShareProps(_CfnPortfolioShareProps):
    accountId: str
    portfolioId: str

class CfnTagOption(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnTagOption"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, key: str, value: str, active: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnTagOptionProps = {"key": key, "value": value}

        if active is not None:
            props["active"] = active

        jsii.create(CfnTagOption, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTagOptionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tagOptionId")
    def tag_option_id(self) -> str:
        return jsii.get(self, "tagOptionId")


class CfnTagOptionAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnTagOptionAssociation"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, resource_id: str, tag_option_id: str) -> None:
        props: CfnTagOptionAssociationProps = {"resourceId": resource_id, "tagOptionId": tag_option_id}

        jsii.create(CfnTagOptionAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTagOptionAssociationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tagOptionAssociationId")
    def tag_option_association_id(self) -> str:
        return jsii.get(self, "tagOptionAssociationId")


@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnTagOptionAssociationProps")
class CfnTagOptionAssociationProps(jsii.compat.TypedDict):
    resourceId: str
    tagOptionId: str

class _CfnTagOptionProps(jsii.compat.TypedDict, total=False):
    active: typing.Union[bool, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnTagOptionProps")
class CfnTagOptionProps(_CfnTagOptionProps):
    key: str
    value: str

__all__ = ["CfnAcceptedPortfolioShare", "CfnAcceptedPortfolioShareProps", "CfnCloudFormationProduct", "CfnCloudFormationProductProps", "CfnCloudFormationProvisionedProduct", "CfnCloudFormationProvisionedProductProps", "CfnLaunchNotificationConstraint", "CfnLaunchNotificationConstraintProps", "CfnLaunchRoleConstraint", "CfnLaunchRoleConstraintProps", "CfnLaunchTemplateConstraint", "CfnLaunchTemplateConstraintProps", "CfnPortfolio", "CfnPortfolioPrincipalAssociation", "CfnPortfolioPrincipalAssociationProps", "CfnPortfolioProductAssociation", "CfnPortfolioProductAssociationProps", "CfnPortfolioProps", "CfnPortfolioShare", "CfnPortfolioShareProps", "CfnTagOption", "CfnTagOptionAssociation", "CfnTagOptionAssociationProps", "CfnTagOptionProps", "__jsii_assembly__"]

publication.publish()
