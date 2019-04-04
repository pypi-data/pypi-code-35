import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-budgets", "0.28.0", __name__, "aws-budgets@0.28.0.jsii.tgz")
class CfnBudget(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-budgets.CfnBudget"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, budget: typing.Union["BudgetDataProperty", aws_cdk.cdk.Token], notifications_with_subscribers: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "NotificationWithSubscribersProperty"]]]]=None) -> None:
        props: CfnBudgetProps = {"budget": budget}

        if notifications_with_subscribers is not None:
            props["notificationsWithSubscribers"] = notifications_with_subscribers

        jsii.create(CfnBudget, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="budgetName")
    def budget_name(self) -> str:
        return jsii.get(self, "budgetName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnBudgetProps":
        return jsii.get(self, "propertyOverrides")

    class _BudgetDataProperty(jsii.compat.TypedDict, total=False):
        budgetLimit: typing.Union[aws_cdk.cdk.Token, "CfnBudget.SpendProperty"]
        budgetName: str
        costFilters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        costTypes: typing.Union[aws_cdk.cdk.Token, "CfnBudget.CostTypesProperty"]
        timePeriod: typing.Union[aws_cdk.cdk.Token, "CfnBudget.TimePeriodProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-budgets.CfnBudget.BudgetDataProperty")
    class BudgetDataProperty(_BudgetDataProperty):
        budgetType: str
        timeUnit: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-budgets.CfnBudget.CostTypesProperty")
    class CostTypesProperty(jsii.compat.TypedDict, total=False):
        includeCredit: typing.Union[bool, aws_cdk.cdk.Token]
        includeDiscount: typing.Union[bool, aws_cdk.cdk.Token]
        includeOtherSubscription: typing.Union[bool, aws_cdk.cdk.Token]
        includeRecurring: typing.Union[bool, aws_cdk.cdk.Token]
        includeRefund: typing.Union[bool, aws_cdk.cdk.Token]
        includeSubscription: typing.Union[bool, aws_cdk.cdk.Token]
        includeSupport: typing.Union[bool, aws_cdk.cdk.Token]
        includeTax: typing.Union[bool, aws_cdk.cdk.Token]
        includeUpfront: typing.Union[bool, aws_cdk.cdk.Token]
        useAmortized: typing.Union[bool, aws_cdk.cdk.Token]
        useBlended: typing.Union[bool, aws_cdk.cdk.Token]

    class _NotificationProperty(jsii.compat.TypedDict, total=False):
        thresholdType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-budgets.CfnBudget.NotificationProperty")
    class NotificationProperty(_NotificationProperty):
        comparisonOperator: str
        notificationType: str
        threshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-budgets.CfnBudget.NotificationWithSubscribersProperty")
    class NotificationWithSubscribersProperty(jsii.compat.TypedDict):
        notification: typing.Union[aws_cdk.cdk.Token, "CfnBudget.NotificationProperty"]
        subscribers: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBudget.SubscriberProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-budgets.CfnBudget.SpendProperty")
    class SpendProperty(jsii.compat.TypedDict):
        amount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        unit: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-budgets.CfnBudget.SubscriberProperty")
    class SubscriberProperty(jsii.compat.TypedDict):
        address: str
        subscriptionType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-budgets.CfnBudget.TimePeriodProperty")
    class TimePeriodProperty(jsii.compat.TypedDict, total=False):
        end: str
        start: str


class _CfnBudgetProps(jsii.compat.TypedDict, total=False):
    notificationsWithSubscribers: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBudget.NotificationWithSubscribersProperty"]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-budgets.CfnBudgetProps")
class CfnBudgetProps(_CfnBudgetProps):
    budget: typing.Union["CfnBudget.BudgetDataProperty", aws_cdk.cdk.Token]

__all__ = ["CfnBudget", "CfnBudgetProps", "__jsii_assembly__"]

publication.publish()
