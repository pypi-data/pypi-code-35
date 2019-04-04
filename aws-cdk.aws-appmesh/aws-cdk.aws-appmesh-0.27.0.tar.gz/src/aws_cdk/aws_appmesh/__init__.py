import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-appmesh", "0.27.0", __name__, "aws-appmesh@0.27.0.jsii.tgz")
class CfnMesh(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appmesh.CfnMesh"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, mesh_name: str, spec: typing.Optional[typing.Union["MeshSpecProperty", aws_cdk.cdk.Token]]=None, tags: typing.Optional[typing.List["TagRefProperty"]]=None) -> None:
        props: CfnMeshProps = {"meshName": mesh_name}

        if spec is not None:
            props["spec"] = spec

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnMesh, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="meshArn")
    def mesh_arn(self) -> str:
        return jsii.get(self, "meshArn")

    @property
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> str:
        return jsii.get(self, "meshName")

    @property
    @jsii.member(jsii_name="meshUid")
    def mesh_uid(self) -> str:
        return jsii.get(self, "meshUid")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnMeshProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnMesh.EgressFilterProperty")
    class EgressFilterProperty(jsii.compat.TypedDict):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnMesh.MeshSpecProperty")
    class MeshSpecProperty(jsii.compat.TypedDict, total=False):
        egressFilter: typing.Union[aws_cdk.cdk.Token, "CfnMesh.EgressFilterProperty"]

    class _TagRefProperty(jsii.compat.TypedDict, total=False):
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnMesh.TagRefProperty")
    class TagRefProperty(_TagRefProperty):
        key: str


class _CfnMeshProps(jsii.compat.TypedDict, total=False):
    spec: typing.Union["CfnMesh.MeshSpecProperty", aws_cdk.cdk.Token]
    tags: typing.List["CfnMesh.TagRefProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnMeshProps")
class CfnMeshProps(_CfnMeshProps):
    meshName: str

class CfnRoute(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appmesh.CfnRoute"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, mesh_name: str, route_name: str, spec: typing.Union[aws_cdk.cdk.Token, "RouteSpecProperty"], virtual_router_name: str, tags: typing.Optional[typing.List["TagRefProperty"]]=None) -> None:
        props: CfnRouteProps = {"meshName": mesh_name, "routeName": route_name, "spec": spec, "virtualRouterName": virtual_router_name}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnRoute, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRouteProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="routeArn")
    def route_arn(self) -> str:
        return jsii.get(self, "routeArn")

    @property
    @jsii.member(jsii_name="routeMeshName")
    def route_mesh_name(self) -> str:
        return jsii.get(self, "routeMeshName")

    @property
    @jsii.member(jsii_name="routeName")
    def route_name(self) -> str:
        return jsii.get(self, "routeName")

    @property
    @jsii.member(jsii_name="routeUid")
    def route_uid(self) -> str:
        return jsii.get(self, "routeUid")

    @property
    @jsii.member(jsii_name="routeVirtualRouterName")
    def route_virtual_router_name(self) -> str:
        return jsii.get(self, "routeVirtualRouterName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRoute.HttpRouteActionProperty")
    class HttpRouteActionProperty(jsii.compat.TypedDict):
        weightedTargets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnRoute.WeightedTargetProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRoute.HttpRouteMatchProperty")
    class HttpRouteMatchProperty(jsii.compat.TypedDict):
        prefix: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRoute.HttpRouteProperty")
    class HttpRouteProperty(jsii.compat.TypedDict):
        action: typing.Union[aws_cdk.cdk.Token, "CfnRoute.HttpRouteActionProperty"]
        match: typing.Union[aws_cdk.cdk.Token, "CfnRoute.HttpRouteMatchProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRoute.RouteSpecProperty")
    class RouteSpecProperty(jsii.compat.TypedDict, total=False):
        httpRoute: typing.Union[aws_cdk.cdk.Token, "CfnRoute.HttpRouteProperty"]
        tcpRoute: typing.Union[aws_cdk.cdk.Token, "CfnRoute.TcpRouteProperty"]

    class _TagRefProperty(jsii.compat.TypedDict, total=False):
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRoute.TagRefProperty")
    class TagRefProperty(_TagRefProperty):
        key: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRoute.TcpRouteActionProperty")
    class TcpRouteActionProperty(jsii.compat.TypedDict):
        weightedTargets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnRoute.WeightedTargetProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRoute.TcpRouteProperty")
    class TcpRouteProperty(jsii.compat.TypedDict):
        action: typing.Union[aws_cdk.cdk.Token, "CfnRoute.TcpRouteActionProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRoute.WeightedTargetProperty")
    class WeightedTargetProperty(jsii.compat.TypedDict):
        virtualNode: str
        weight: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class _CfnRouteProps(jsii.compat.TypedDict, total=False):
    tags: typing.List["CfnRoute.TagRefProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRouteProps")
class CfnRouteProps(_CfnRouteProps):
    meshName: str
    routeName: str
    spec: typing.Union[aws_cdk.cdk.Token, "CfnRoute.RouteSpecProperty"]
    virtualRouterName: str

class CfnVirtualNode(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, mesh_name: str, spec: typing.Union[aws_cdk.cdk.Token, "VirtualNodeSpecProperty"], virtual_node_name: str, tags: typing.Optional[typing.List["TagRefProperty"]]=None) -> None:
        props: CfnVirtualNodeProps = {"meshName": mesh_name, "spec": spec, "virtualNodeName": virtual_node_name}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnVirtualNode, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVirtualNodeProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="virtualNodeArn")
    def virtual_node_arn(self) -> str:
        return jsii.get(self, "virtualNodeArn")

    @property
    @jsii.member(jsii_name="virtualNodeMeshName")
    def virtual_node_mesh_name(self) -> str:
        return jsii.get(self, "virtualNodeMeshName")

    @property
    @jsii.member(jsii_name="virtualNodeName")
    def virtual_node_name(self) -> str:
        return jsii.get(self, "virtualNodeName")

    @property
    @jsii.member(jsii_name="virtualNodeUid")
    def virtual_node_uid(self) -> str:
        return jsii.get(self, "virtualNodeUid")

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.AccessLogProperty")
    class AccessLogProperty(jsii.compat.TypedDict, total=False):
        file: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.FileAccessLogProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.BackendProperty")
    class BackendProperty(jsii.compat.TypedDict, total=False):
        virtualService: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.VirtualServiceBackendProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.DnsServiceDiscoveryProperty")
    class DnsServiceDiscoveryProperty(jsii.compat.TypedDict):
        hostname: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.FileAccessLogProperty")
    class FileAccessLogProperty(jsii.compat.TypedDict):
        path: str

    class _HealthCheckProperty(jsii.compat.TypedDict, total=False):
        path: str
        port: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.HealthCheckProperty")
    class HealthCheckProperty(_HealthCheckProperty):
        healthyThreshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        intervalMillis: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        protocol: str
        timeoutMillis: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        unhealthyThreshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    class _ListenerProperty(jsii.compat.TypedDict, total=False):
        healthCheck: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.HealthCheckProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ListenerProperty")
    class ListenerProperty(_ListenerProperty):
        portMapping: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.PortMappingProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.LoggingProperty")
    class LoggingProperty(jsii.compat.TypedDict, total=False):
        accessLog: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.AccessLogProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.PortMappingProperty")
    class PortMappingProperty(jsii.compat.TypedDict):
        port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        protocol: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ServiceDiscoveryProperty")
    class ServiceDiscoveryProperty(jsii.compat.TypedDict):
        dns: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.DnsServiceDiscoveryProperty"]

    class _TagRefProperty(jsii.compat.TypedDict, total=False):
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.TagRefProperty")
    class TagRefProperty(_TagRefProperty):
        key: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.VirtualNodeSpecProperty")
    class VirtualNodeSpecProperty(jsii.compat.TypedDict, total=False):
        backends: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.BackendProperty"]]]
        listeners: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.ListenerProperty"]]]
        logging: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.LoggingProperty"]
        serviceDiscovery: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.ServiceDiscoveryProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.VirtualServiceBackendProperty")
    class VirtualServiceBackendProperty(jsii.compat.TypedDict):
        virtualServiceName: str


class _CfnVirtualNodeProps(jsii.compat.TypedDict, total=False):
    tags: typing.List["CfnVirtualNode.TagRefProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNodeProps")
class CfnVirtualNodeProps(_CfnVirtualNodeProps):
    meshName: str
    spec: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.VirtualNodeSpecProperty"]
    virtualNodeName: str

class CfnVirtualRouter(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouter"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, mesh_name: str, spec: typing.Union[aws_cdk.cdk.Token, "VirtualRouterSpecProperty"], virtual_router_name: str, tags: typing.Optional[typing.List["TagRefProperty"]]=None) -> None:
        props: CfnVirtualRouterProps = {"meshName": mesh_name, "spec": spec, "virtualRouterName": virtual_router_name}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnVirtualRouter, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVirtualRouterProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="virtualRouterArn")
    def virtual_router_arn(self) -> str:
        return jsii.get(self, "virtualRouterArn")

    @property
    @jsii.member(jsii_name="virtualRouterMeshName")
    def virtual_router_mesh_name(self) -> str:
        return jsii.get(self, "virtualRouterMeshName")

    @property
    @jsii.member(jsii_name="virtualRouterName")
    def virtual_router_name(self) -> str:
        return jsii.get(self, "virtualRouterName")

    @property
    @jsii.member(jsii_name="virtualRouterUid")
    def virtual_router_uid(self) -> str:
        return jsii.get(self, "virtualRouterUid")

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouter.PortMappingProperty")
    class PortMappingProperty(jsii.compat.TypedDict):
        port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        protocol: str

    class _TagRefProperty(jsii.compat.TypedDict, total=False):
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouter.TagRefProperty")
    class TagRefProperty(_TagRefProperty):
        key: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouter.VirtualRouterListenerProperty")
    class VirtualRouterListenerProperty(jsii.compat.TypedDict):
        portMapping: typing.Union[aws_cdk.cdk.Token, "CfnVirtualRouter.PortMappingProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouter.VirtualRouterSpecProperty")
    class VirtualRouterSpecProperty(jsii.compat.TypedDict):
        listeners: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnVirtualRouter.VirtualRouterListenerProperty"]]]


class _CfnVirtualRouterProps(jsii.compat.TypedDict, total=False):
    tags: typing.List["CfnVirtualRouter.TagRefProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouterProps")
class CfnVirtualRouterProps(_CfnVirtualRouterProps):
    meshName: str
    spec: typing.Union[aws_cdk.cdk.Token, "CfnVirtualRouter.VirtualRouterSpecProperty"]
    virtualRouterName: str

class CfnVirtualService(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, mesh_name: str, spec: typing.Union[aws_cdk.cdk.Token, "VirtualServiceSpecProperty"], virtual_service_name: str, tags: typing.Optional[typing.List["TagRefProperty"]]=None) -> None:
        props: CfnVirtualServiceProps = {"meshName": mesh_name, "spec": spec, "virtualServiceName": virtual_service_name}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnVirtualService, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVirtualServiceProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="virtualServiceArn")
    def virtual_service_arn(self) -> str:
        return jsii.get(self, "virtualServiceArn")

    @property
    @jsii.member(jsii_name="virtualServiceMeshName")
    def virtual_service_mesh_name(self) -> str:
        return jsii.get(self, "virtualServiceMeshName")

    @property
    @jsii.member(jsii_name="virtualServiceName")
    def virtual_service_name(self) -> str:
        return jsii.get(self, "virtualServiceName")

    @property
    @jsii.member(jsii_name="virtualServiceUid")
    def virtual_service_uid(self) -> str:
        return jsii.get(self, "virtualServiceUid")

    class _TagRefProperty(jsii.compat.TypedDict, total=False):
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService.TagRefProperty")
    class TagRefProperty(_TagRefProperty):
        key: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService.VirtualNodeServiceProviderProperty")
    class VirtualNodeServiceProviderProperty(jsii.compat.TypedDict):
        virtualNodeName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService.VirtualRouterServiceProviderProperty")
    class VirtualRouterServiceProviderProperty(jsii.compat.TypedDict):
        virtualRouterName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService.VirtualServiceProviderProperty")
    class VirtualServiceProviderProperty(jsii.compat.TypedDict, total=False):
        virtualNode: typing.Union[aws_cdk.cdk.Token, "CfnVirtualService.VirtualNodeServiceProviderProperty"]
        virtualRouter: typing.Union[aws_cdk.cdk.Token, "CfnVirtualService.VirtualRouterServiceProviderProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService.VirtualServiceSpecProperty")
    class VirtualServiceSpecProperty(jsii.compat.TypedDict, total=False):
        provider: typing.Union[aws_cdk.cdk.Token, "CfnVirtualService.VirtualServiceProviderProperty"]


class _CfnVirtualServiceProps(jsii.compat.TypedDict, total=False):
    tags: typing.List["CfnVirtualService.TagRefProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualServiceProps")
class CfnVirtualServiceProps(_CfnVirtualServiceProps):
    meshName: str
    spec: typing.Union[aws_cdk.cdk.Token, "CfnVirtualService.VirtualServiceSpecProperty"]
    virtualServiceName: str

__all__ = ["CfnMesh", "CfnMeshProps", "CfnRoute", "CfnRouteProps", "CfnVirtualNode", "CfnVirtualNodeProps", "CfnVirtualRouter", "CfnVirtualRouterProps", "CfnVirtualService", "CfnVirtualServiceProps", "__jsii_assembly__"]

publication.publish()
