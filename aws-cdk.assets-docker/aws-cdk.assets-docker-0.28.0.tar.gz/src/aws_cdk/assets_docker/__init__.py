import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_cloudformation
import aws_cdk.aws_ecr
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.cdk
import aws_cdk.cx_api
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/assets-docker", "0.28.0", __name__, "assets-docker@0.28.0.jsii.tgz")
class DockerImageAsset(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/assets-docker.DockerImageAsset"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, directory: str, repository_name: typing.Optional[str]=None) -> None:
        props: DockerImageAssetProps = {"directory": directory}

        if repository_name is not None:
            props["repositoryName"] = repository_name

        jsii.create(DockerImageAsset, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> str:
        return jsii.get(self, "imageUri")

    @image_uri.setter
    def image_uri(self, value: str):
        return jsii.set(self, "imageUri", value)

    @property
    @jsii.member(jsii_name="repository")
    def repository(self) -> aws_cdk.aws_ecr.IRepository:
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: aws_cdk.aws_ecr.IRepository):
        return jsii.set(self, "repository", value)


class _DockerImageAssetProps(jsii.compat.TypedDict, total=False):
    repositoryName: str

@jsii.data_type(jsii_type="@aws-cdk/assets-docker.DockerImageAssetProps")
class DockerImageAssetProps(_DockerImageAssetProps):
    directory: str

__all__ = ["DockerImageAsset", "DockerImageAssetProps", "__jsii_assembly__"]

publication.publish()
