# coding: utf-8

"""
    Assetic Integration API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: v2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from assetic.api_client import ApiClient


class DataExchangeJobApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def data_exchange_job_post(self, data_exchange_job, **kwargs):  # noqa: E501
        """data_exchange_job_post  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_exchange_job_post(data_exchange_job, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param Assetic3IntegrationRepresentationsDataExchangeJobRepresentation data_exchange_job: (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.data_exchange_job_post_with_http_info(data_exchange_job, **kwargs)  # noqa: E501
        else:
            (data) = self.data_exchange_job_post_with_http_info(data_exchange_job, **kwargs)  # noqa: E501
            return data

    def data_exchange_job_post_with_http_info(self, data_exchange_job, **kwargs):  # noqa: E501
        """data_exchange_job_post  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_exchange_job_post_with_http_info(data_exchange_job, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param Assetic3IntegrationRepresentationsDataExchangeJobRepresentation data_exchange_job: (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['data_exchange_job']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method data_exchange_job_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'data_exchange_job' is set
        if ('data_exchange_job' not in params or
                params['data_exchange_job'] is None):
            raise ValueError("Missing the required parameter `data_exchange_job` when calling `data_exchange_job_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'data_exchange_job' in params:
            body_params = params['data_exchange_job']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/json', 'application/octet-stream'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json', 'application/octet-stream', 'application/x-www-form-urlencoded', 'application/hal+json', 'application/hal+xml'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/api/v2/dataexchangejob', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='str',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def data_exchange_job_post_0(self, data_exchange_job_no_profile_representation, **kwargs):  # noqa: E501
        """Create data exchange jobs without having to create a profile  # noqa: E501

        <p>Sample Request Payload: </p>  <pre>               {                  \"DocumentId\": \"cd6544b3-3031-e711-80bc-005056947279\",                  \"Module\": \"Assets\",                  \"Category\": \"Land\"              }              </pre>  <br />  <p>For Module and Category, please use identifier values instead of display values. E.g.: </p>  <pre> \"Module\" : \"NetworkEntity\" </pre>  <p>instead of</p>  <pre> \"Module\" : \"Simple Asset Groups\" </pre>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_exchange_job_post_0(data_exchange_job_no_profile_representation, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param Assetic3IntegrationRepresentationsDataExchangeJobNoProfileRepresentation data_exchange_job_no_profile_representation:  (required)
        :return: Assetic3IntegrationRepresentationsDataExchangeTask
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.data_exchange_job_post_0_with_http_info(data_exchange_job_no_profile_representation, **kwargs)  # noqa: E501
        else:
            (data) = self.data_exchange_job_post_0_with_http_info(data_exchange_job_no_profile_representation, **kwargs)  # noqa: E501
            return data

    def data_exchange_job_post_0_with_http_info(self, data_exchange_job_no_profile_representation, **kwargs):  # noqa: E501
        """Create data exchange jobs without having to create a profile  # noqa: E501

        <p>Sample Request Payload: </p>  <pre>               {                  \"DocumentId\": \"cd6544b3-3031-e711-80bc-005056947279\",                  \"Module\": \"Assets\",                  \"Category\": \"Land\"              }              </pre>  <br />  <p>For Module and Category, please use identifier values instead of display values. E.g.: </p>  <pre> \"Module\" : \"NetworkEntity\" </pre>  <p>instead of</p>  <pre> \"Module\" : \"Simple Asset Groups\" </pre>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_exchange_job_post_0_with_http_info(data_exchange_job_no_profile_representation, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param Assetic3IntegrationRepresentationsDataExchangeJobNoProfileRepresentation data_exchange_job_no_profile_representation:  (required)
        :return: Assetic3IntegrationRepresentationsDataExchangeTask
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['data_exchange_job_no_profile_representation']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method data_exchange_job_post_0" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'data_exchange_job_no_profile_representation' is set
        if ('data_exchange_job_no_profile_representation' not in params or
                params['data_exchange_job_no_profile_representation'] is None):
            raise ValueError("Missing the required parameter `data_exchange_job_no_profile_representation` when calling `data_exchange_job_post_0`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'data_exchange_job_no_profile_representation' in params:
            body_params = params['data_exchange_job_no_profile_representation']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/json', 'application/octet-stream'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json', 'application/octet-stream', 'application/x-www-form-urlencoded', 'application/hal+json', 'application/hal+xml'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/api/v2/dataexchangejobnoprofile', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Assetic3IntegrationRepresentationsDataExchangeTask',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
