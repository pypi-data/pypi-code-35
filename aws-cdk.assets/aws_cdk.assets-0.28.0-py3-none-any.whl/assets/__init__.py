import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.aws_s3
import aws_cdk.cdk
import aws_cdk.cx_api
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/assets", "0.28.0", __name__, "assets@0.28.0.jsii.tgz")
class Asset(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/assets.Asset"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, packaging: "AssetPackaging", path: str, readers: typing.Optional[typing.List[aws_cdk.aws_iam.IGrantable]]=None) -> None:
        props: GenericAssetProps = {"packaging": packaging, "path": path}

        if readers is not None:
            props["readers"] = readers

        jsii.create(Asset, self, [scope, id, props])

    @jsii.member(jsii_name="addResourceMetadata")
    def add_resource_metadata(self, resource: aws_cdk.cdk.CfnResource, resource_property: str) -> None:
        return jsii.invoke(self, "addResourceMetadata", [resource, resource_property])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> None:
        return jsii.invoke(self, "grantRead", [grantee])

    @property
    @jsii.member(jsii_name="assetPath")
    def asset_path(self) -> str:
        return jsii.get(self, "assetPath")

    @property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        return jsii.get(self, "bucket")

    @property
    @jsii.member(jsii_name="isZipArchive")
    def is_zip_archive(self) -> bool:
        return jsii.get(self, "isZipArchive")

    @property
    @jsii.member(jsii_name="s3BucketName")
    def s3_bucket_name(self) -> str:
        return jsii.get(self, "s3BucketName")

    @property
    @jsii.member(jsii_name="s3ObjectKey")
    def s3_object_key(self) -> str:
        return jsii.get(self, "s3ObjectKey")

    @property
    @jsii.member(jsii_name="s3Url")
    def s3_url(self) -> str:
        return jsii.get(self, "s3Url")


@jsii.enum(jsii_type="@aws-cdk/assets.AssetPackaging")
class AssetPackaging(enum.Enum):
    ZipDirectory = "ZipDirectory"
    File = "File"

class FileAsset(Asset, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/assets.FileAsset"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, path: str, readers: typing.Optional[typing.List[aws_cdk.aws_iam.IGrantable]]=None) -> None:
        props: FileAssetProps = {"path": path}

        if readers is not None:
            props["readers"] = readers

        jsii.create(FileAsset, self, [scope, id, props])


class _FileAssetProps(jsii.compat.TypedDict, total=False):
    readers: typing.List[aws_cdk.aws_iam.IGrantable]

@jsii.data_type(jsii_type="@aws-cdk/assets.FileAssetProps")
class FileAssetProps(_FileAssetProps):
    path: str

class _GenericAssetProps(jsii.compat.TypedDict, total=False):
    readers: typing.List[aws_cdk.aws_iam.IGrantable]

@jsii.data_type(jsii_type="@aws-cdk/assets.GenericAssetProps")
class GenericAssetProps(_GenericAssetProps):
    packaging: "AssetPackaging"
    path: str

class ZipDirectoryAsset(Asset, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/assets.ZipDirectoryAsset"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, path: str, readers: typing.Optional[typing.List[aws_cdk.aws_iam.IGrantable]]=None) -> None:
        props: ZipDirectoryAssetProps = {"path": path}

        if readers is not None:
            props["readers"] = readers

        jsii.create(ZipDirectoryAsset, self, [scope, id, props])


class _ZipDirectoryAssetProps(jsii.compat.TypedDict, total=False):
    readers: typing.List[aws_cdk.aws_iam.IGrantable]

@jsii.data_type(jsii_type="@aws-cdk/assets.ZipDirectoryAssetProps")
class ZipDirectoryAssetProps(_ZipDirectoryAssetProps):
    path: str

__all__ = ["Asset", "AssetPackaging", "FileAsset", "FileAssetProps", "GenericAssetProps", "ZipDirectoryAsset", "ZipDirectoryAssetProps", "__jsii_assembly__"]

publication.publish()
