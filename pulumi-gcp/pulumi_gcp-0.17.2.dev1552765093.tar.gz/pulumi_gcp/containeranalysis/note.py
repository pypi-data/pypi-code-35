# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Note(pulumi.CustomResource):
    attestation_authority: pulumi.Output[dict]
    name: pulumi.Output[str]
    project: pulumi.Output[str]
    def __init__(__self__, resource_name, opts=None, attestation_authority=None, name=None, project=None, __name__=None, __opts__=None):
        """
        Provides a detailed description of a Note.
        
        > **Warning:** This resource is in beta, and should be used with the terraform-provider-google-beta provider.
        See [Provider Versions](https://terraform.io/docs/providers/google/provider_versions.html) for more details on beta resources.
        
        To get more information about Note, see:
        
        * [API documentation](https://cloud.google.com/container-analysis/api/reference/rest/)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/container-analysis/)
        
        <div class = "oics-button" style="float: right; margin: 0 0 -15px">
          <a href="https://console.cloud.google.com/cloudshell/open?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fterraform-google-modules%2Fdocs-examples.git&cloudshell_working_dir=container_analysis_note_basic&cloudshell_image=gcr.io%2Fgraphite-cloud-shell-images%2Fterraform%3Alatest&open_in_editor=main.tf&cloudshell_print=.%2Fmotd&cloudshell_tutorial=.%2Ftutorial.md" target="_blank">
            <img alt="Open in Cloud Shell" src="//gstatic.com/cloudssh/images/open-btn.svg" style="max-height: 44px; margin: 32px auto; max-width: 100%;">
          </a>
        </div>
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if not resource_name:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(resource_name, str):
            raise TypeError('Expected resource name to be a string')
        if opts and not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if attestation_authority is None:
            raise TypeError('Missing required property attestation_authority')
        __props__['attestation_authority'] = attestation_authority

        __props__['name'] = name

        __props__['project'] = project

        super(Note, __self__).__init__(
            'gcp:containeranalysis/note:Note',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

