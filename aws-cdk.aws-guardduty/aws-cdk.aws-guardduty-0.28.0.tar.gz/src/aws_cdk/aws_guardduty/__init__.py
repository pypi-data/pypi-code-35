import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-guardduty", "0.28.0", __name__, "aws-guardduty@0.28.0.jsii.tgz")
class CfnDetector(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-guardduty.CfnDetector"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, enable: typing.Union[bool, aws_cdk.cdk.Token], finding_publishing_frequency: typing.Optional[str]=None) -> None:
        props: CfnDetectorProps = {"enable": enable}

        if finding_publishing_frequency is not None:
            props["findingPublishingFrequency"] = finding_publishing_frequency

        jsii.create(CfnDetector, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="detectorId")
    def detector_id(self) -> str:
        return jsii.get(self, "detectorId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDetectorProps":
        return jsii.get(self, "propertyOverrides")


class _CfnDetectorProps(jsii.compat.TypedDict, total=False):
    findingPublishingFrequency: str

@jsii.data_type(jsii_type="@aws-cdk/aws-guardduty.CfnDetectorProps")
class CfnDetectorProps(_CfnDetectorProps):
    enable: typing.Union[bool, aws_cdk.cdk.Token]

class CfnFilter(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-guardduty.CfnFilter"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, action: str, description: str, detector_id: str, finding_criteria: typing.Union[aws_cdk.cdk.Token, "FindingCriteriaProperty"], rank: typing.Union[jsii.Number, aws_cdk.cdk.Token], name: typing.Optional[str]=None) -> None:
        props: CfnFilterProps = {"action": action, "description": description, "detectorId": detector_id, "findingCriteria": finding_criteria, "rank": rank}

        if name is not None:
            props["name"] = name

        jsii.create(CfnFilter, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="filterName")
    def filter_name(self) -> str:
        return jsii.get(self, "filterName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnFilterProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-guardduty.CfnFilter.ConditionProperty")
    class ConditionProperty(jsii.compat.TypedDict, total=False):
        eq: typing.List[str]
        gte: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        lt: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        lte: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        neq: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-guardduty.CfnFilter.FindingCriteriaProperty")
    class FindingCriteriaProperty(jsii.compat.TypedDict, total=False):
        criterion: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        itemType: typing.Union[aws_cdk.cdk.Token, "CfnFilter.ConditionProperty"]


class _CfnFilterProps(jsii.compat.TypedDict, total=False):
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-guardduty.CfnFilterProps")
class CfnFilterProps(_CfnFilterProps):
    action: str
    description: str
    detectorId: str
    findingCriteria: typing.Union[aws_cdk.cdk.Token, "CfnFilter.FindingCriteriaProperty"]
    rank: typing.Union[jsii.Number, aws_cdk.cdk.Token]

class CfnIPSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-guardduty.CfnIPSet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, activate: typing.Union[bool, aws_cdk.cdk.Token], detector_id: str, format: str, location: str, name: typing.Optional[str]=None) -> None:
        props: CfnIPSetProps = {"activate": activate, "detectorId": detector_id, "format": format, "location": location}

        if name is not None:
            props["name"] = name

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


class _CfnIPSetProps(jsii.compat.TypedDict, total=False):
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-guardduty.CfnIPSetProps")
class CfnIPSetProps(_CfnIPSetProps):
    activate: typing.Union[bool, aws_cdk.cdk.Token]
    detectorId: str
    format: str
    location: str

class CfnMaster(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-guardduty.CfnMaster"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, detector_id: str, master_id: str, invitation_id: typing.Optional[str]=None) -> None:
        props: CfnMasterProps = {"detectorId": detector_id, "masterId": master_id}

        if invitation_id is not None:
            props["invitationId"] = invitation_id

        jsii.create(CfnMaster, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnMasterProps":
        return jsii.get(self, "propertyOverrides")


class _CfnMasterProps(jsii.compat.TypedDict, total=False):
    invitationId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-guardduty.CfnMasterProps")
class CfnMasterProps(_CfnMasterProps):
    detectorId: str
    masterId: str

class CfnMember(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-guardduty.CfnMember"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, detector_id: str, email: str, member_id: str, disable_email_notification: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, message: typing.Optional[str]=None, status: typing.Optional[str]=None) -> None:
        props: CfnMemberProps = {"detectorId": detector_id, "email": email, "memberId": member_id}

        if disable_email_notification is not None:
            props["disableEmailNotification"] = disable_email_notification

        if message is not None:
            props["message"] = message

        if status is not None:
            props["status"] = status

        jsii.create(CfnMember, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnMemberProps":
        return jsii.get(self, "propertyOverrides")


class _CfnMemberProps(jsii.compat.TypedDict, total=False):
    disableEmailNotification: typing.Union[bool, aws_cdk.cdk.Token]
    message: str
    status: str

@jsii.data_type(jsii_type="@aws-cdk/aws-guardduty.CfnMemberProps")
class CfnMemberProps(_CfnMemberProps):
    detectorId: str
    email: str
    memberId: str

class CfnThreatIntelSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-guardduty.CfnThreatIntelSet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, activate: typing.Union[bool, aws_cdk.cdk.Token], detector_id: str, format: str, location: str, name: typing.Optional[str]=None) -> None:
        props: CfnThreatIntelSetProps = {"activate": activate, "detectorId": detector_id, "format": format, "location": location}

        if name is not None:
            props["name"] = name

        jsii.create(CfnThreatIntelSet, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnThreatIntelSetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="threatIntelSetId")
    def threat_intel_set_id(self) -> str:
        return jsii.get(self, "threatIntelSetId")


class _CfnThreatIntelSetProps(jsii.compat.TypedDict, total=False):
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-guardduty.CfnThreatIntelSetProps")
class CfnThreatIntelSetProps(_CfnThreatIntelSetProps):
    activate: typing.Union[bool, aws_cdk.cdk.Token]
    detectorId: str
    format: str
    location: str

__all__ = ["CfnDetector", "CfnDetectorProps", "CfnFilter", "CfnFilterProps", "CfnIPSet", "CfnIPSetProps", "CfnMaster", "CfnMasterProps", "CfnMember", "CfnMemberProps", "CfnThreatIntelSet", "CfnThreatIntelSetProps", "__jsii_assembly__"]

publication.publish()
