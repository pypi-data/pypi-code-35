import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-quickstarts",
    "version": "0.28.0",
    "description": "AWS Quickstarts for the CDK",
    "url": "https://github.com/awslabs/aws-cdk",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "project_urls": {
        "Source": "https://github.com/awslabs/aws-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.aws_quickstarts",
        "aws_cdk.aws_quickstarts._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_quickstarts._jsii": [
            "aws-quickstarts@0.28.0.jsii.tgz"
        ],
        "aws_cdk.aws_quickstarts": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii",
        "publication>=0.0.3",
        "aws-cdk.aws-ec2~=0.28.0",
        "aws-cdk.cdk~=0.28.0"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
