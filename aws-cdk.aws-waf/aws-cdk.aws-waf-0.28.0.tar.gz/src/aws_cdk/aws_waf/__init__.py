import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-waf", "0.28.0", __name__, "aws-waf@0.28.0.jsii.tgz")
class CfnByteMatchSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnByteMatchSet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, byte_match_tuples: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["ByteMatchTupleProperty", aws_cdk.cdk.Token]]]]=None) -> None:
        props: CfnByteMatchSetProps = {"name": name}

        if byte_match_tuples is not None:
            props["byteMatchTuples"] = byte_match_tuples

        jsii.create(CfnByteMatchSet, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="byteMatchSetId")
    def byte_match_set_id(self) -> str:
        return jsii.get(self, "byteMatchSetId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnByteMatchSetProps":
        return jsii.get(self, "propertyOverrides")

    class _ByteMatchTupleProperty(jsii.compat.TypedDict, total=False):
        targetString: str
        targetStringBase64: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnByteMatchSet.ByteMatchTupleProperty")
    class ByteMatchTupleProperty(_ByteMatchTupleProperty):
        fieldToMatch: typing.Union[aws_cdk.cdk.Token, "CfnByteMatchSet.FieldToMatchProperty"]
        positionalConstraint: str
        textTransformation: str

    class _FieldToMatchProperty(jsii.compat.TypedDict, total=False):
        data: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnByteMatchSet.FieldToMatchProperty")
    class FieldToMatchProperty(_FieldToMatchProperty):
        type: str


class _CfnByteMatchSetProps(jsii.compat.TypedDict, total=False):
    byteMatchTuples: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnByteMatchSet.ByteMatchTupleProperty", aws_cdk.cdk.Token]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnByteMatchSetProps")
class CfnByteMatchSetProps(_CfnByteMatchSetProps):
    name: str

class CfnIPSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnIPSet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, ip_set_descriptors: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "IPSetDescriptorProperty"]]]]=None) -> None:
        props: CfnIPSetProps = {"name": name}

        if ip_set_descriptors is not None:
            props["ipSetDescriptors"] = ip_set_descriptors

        jsii.create(CfnIPSet, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="ipSetId")
    def ip_set_id(self) -> str:
        return jsii.get(self, "ipSetId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnIPSetProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.interface(jsii_type="@aws-cdk/aws-waf.CfnIPSet.IPSetDescriptorProperty")
    class IPSetDescriptorProperty(jsii.compat.Protocol):
        @staticmethod
        def __jsii_proxy_class__():
            return _IPSetDescriptorPropertyProxy

        @property
        @jsii.member(jsii_name="type")
        def type(self) -> str:
            ...

        @property
        @jsii.member(jsii_name="value")
        def value(self) -> str:
            ...


    class _IPSetDescriptorPropertyProxy():
        __jsii_type__ = "@aws-cdk/aws-waf.CfnIPSet.IPSetDescriptorProperty"
        @property
        @jsii.member(jsii_name="type")
        def type(self) -> str:
            return jsii.get(self, "type")

        @property
        @jsii.member(jsii_name="value")
        def value(self) -> str:
            return jsii.get(self, "value")



class _CfnIPSetProps(jsii.compat.TypedDict, total=False):
    ipSetDescriptors: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnIPSet.IPSetDescriptorProperty"]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnIPSetProps")
class CfnIPSetProps(_CfnIPSetProps):
    name: str

class CfnRule(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnRule"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, metric_name: str, name: str, predicates: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "PredicateProperty"]]]]=None) -> None:
        props: CfnRuleProps = {"metricName": metric_name, "name": name}

        if predicates is not None:
            props["predicates"] = predicates

        jsii.create(CfnRule, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRuleProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="ruleId")
    def rule_id(self) -> str:
        return jsii.get(self, "ruleId")

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnRule.PredicateProperty")
    class PredicateProperty(jsii.compat.TypedDict):
        dataId: str
        negated: typing.Union[bool, aws_cdk.cdk.Token]
        type: str


class _CfnRuleProps(jsii.compat.TypedDict, total=False):
    predicates: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnRule.PredicateProperty"]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnRuleProps")
class CfnRuleProps(_CfnRuleProps):
    metricName: str
    name: str

class CfnSizeConstraintSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnSizeConstraintSet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, size_constraints: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "SizeConstraintProperty"]]]) -> None:
        props: CfnSizeConstraintSetProps = {"name": name, "sizeConstraints": size_constraints}

        jsii.create(CfnSizeConstraintSet, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSizeConstraintSetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="sizeConstraintSetId")
    def size_constraint_set_id(self) -> str:
        return jsii.get(self, "sizeConstraintSetId")

    class _FieldToMatchProperty(jsii.compat.TypedDict, total=False):
        data: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSizeConstraintSet.FieldToMatchProperty")
    class FieldToMatchProperty(_FieldToMatchProperty):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSizeConstraintSet.SizeConstraintProperty")
    class SizeConstraintProperty(jsii.compat.TypedDict):
        comparisonOperator: str
        fieldToMatch: typing.Union[aws_cdk.cdk.Token, "CfnSizeConstraintSet.FieldToMatchProperty"]
        size: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        textTransformation: str


@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSizeConstraintSetProps")
class CfnSizeConstraintSetProps(jsii.compat.TypedDict):
    name: str
    sizeConstraints: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSizeConstraintSet.SizeConstraintProperty"]]]

class CfnSqlInjectionMatchSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnSqlInjectionMatchSet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, sql_injection_match_tuples: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "SqlInjectionMatchTupleProperty"]]]]=None) -> None:
        props: CfnSqlInjectionMatchSetProps = {"name": name}

        if sql_injection_match_tuples is not None:
            props["sqlInjectionMatchTuples"] = sql_injection_match_tuples

        jsii.create(CfnSqlInjectionMatchSet, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSqlInjectionMatchSetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="sqlInjectionMatchSetId")
    def sql_injection_match_set_id(self) -> str:
        return jsii.get(self, "sqlInjectionMatchSetId")

    class _FieldToMatchProperty(jsii.compat.TypedDict, total=False):
        data: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSqlInjectionMatchSet.FieldToMatchProperty")
    class FieldToMatchProperty(_FieldToMatchProperty):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty")
    class SqlInjectionMatchTupleProperty(jsii.compat.TypedDict):
        fieldToMatch: typing.Union[aws_cdk.cdk.Token, "CfnSqlInjectionMatchSet.FieldToMatchProperty"]
        textTransformation: str


class _CfnSqlInjectionMatchSetProps(jsii.compat.TypedDict, total=False):
    sqlInjectionMatchTuples: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty"]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSqlInjectionMatchSetProps")
class CfnSqlInjectionMatchSetProps(_CfnSqlInjectionMatchSetProps):
    name: str

class CfnWebACL(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnWebACL"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, default_action: typing.Union[aws_cdk.cdk.Token, "WafActionProperty"], metric_name: str, name: str, rules: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ActivatedRuleProperty"]]]]=None) -> None:
        props: CfnWebACLProps = {"defaultAction": default_action, "metricName": metric_name, "name": name}

        if rules is not None:
            props["rules"] = rules

        jsii.create(CfnWebACL, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnWebACLProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="webAclId")
    def web_acl_id(self) -> str:
        return jsii.get(self, "webAclId")

    class _ActivatedRuleProperty(jsii.compat.TypedDict, total=False):
        action: typing.Union[aws_cdk.cdk.Token, "CfnWebACL.WafActionProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnWebACL.ActivatedRuleProperty")
    class ActivatedRuleProperty(_ActivatedRuleProperty):
        priority: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        ruleId: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnWebACL.WafActionProperty")
    class WafActionProperty(jsii.compat.TypedDict):
        type: str


class _CfnWebACLProps(jsii.compat.TypedDict, total=False):
    rules: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnWebACL.ActivatedRuleProperty"]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnWebACLProps")
class CfnWebACLProps(_CfnWebACLProps):
    defaultAction: typing.Union[aws_cdk.cdk.Token, "CfnWebACL.WafActionProperty"]
    metricName: str
    name: str

class CfnXssMatchSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnXssMatchSet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, xss_match_tuples: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "XssMatchTupleProperty"]]]) -> None:
        props: CfnXssMatchSetProps = {"name": name, "xssMatchTuples": xss_match_tuples}

        jsii.create(CfnXssMatchSet, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnXssMatchSetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="xssMatchSetId")
    def xss_match_set_id(self) -> str:
        return jsii.get(self, "xssMatchSetId")

    class _FieldToMatchProperty(jsii.compat.TypedDict, total=False):
        data: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnXssMatchSet.FieldToMatchProperty")
    class FieldToMatchProperty(_FieldToMatchProperty):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnXssMatchSet.XssMatchTupleProperty")
    class XssMatchTupleProperty(jsii.compat.TypedDict):
        fieldToMatch: typing.Union[aws_cdk.cdk.Token, "CfnXssMatchSet.FieldToMatchProperty"]
        textTransformation: str


@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnXssMatchSetProps")
class CfnXssMatchSetProps(jsii.compat.TypedDict):
    name: str
    xssMatchTuples: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnXssMatchSet.XssMatchTupleProperty"]]]

__all__ = ["CfnByteMatchSet", "CfnByteMatchSetProps", "CfnIPSet", "CfnIPSetProps", "CfnRule", "CfnRuleProps", "CfnSizeConstraintSet", "CfnSizeConstraintSetProps", "CfnSqlInjectionMatchSet", "CfnSqlInjectionMatchSetProps", "CfnWebACL", "CfnWebACLProps", "CfnXssMatchSet", "CfnXssMatchSetProps", "__jsii_assembly__"]

publication.publish()
