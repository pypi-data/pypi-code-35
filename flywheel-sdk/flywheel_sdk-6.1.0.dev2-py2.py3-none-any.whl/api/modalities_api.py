# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 6.1.0-dev.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from flywheel.api_client import ApiClient
import flywheel.models

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.

class ModalitiesApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def add_modality(self, body, **kwargs):  # noqa: E501
        """Create a new modality.

        This method makes a synchronous HTTP request by default.

        :param Modality body: (required)
        :param bool async_: Perform the request asynchronously
        :return: ContainerNewOutput
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.add_modality_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.add_modality_with_http_info(body, **kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def add_modality_with_http_info(self, body, **kwargs):  # noqa: E501
        """Create a new modality.

        This method makes a synchronous HTTP request by default.

        :param Modality body: (required)
        :param bool async: Perform the request asynchronously
        :return: ContainerNewOutput
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method add_modality" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `add_modality`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = flywheel.models.Modality.positional_to_model(params['body'])
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/modalities', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ContainerNewOutput',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def delete_modality(self, modality_id, **kwargs):  # noqa: E501
        """Delete a modality

        This method makes a synchronous HTTP request by default.

        :param str modality_id: (required)
        :param bool async_: Perform the request asynchronously
        :return: None
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.delete_modality_with_http_info(modality_id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_modality_with_http_info(modality_id, **kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def delete_modality_with_http_info(self, modality_id, **kwargs):  # noqa: E501
        """Delete a modality

        This method makes a synchronous HTTP request by default.

        :param str modality_id: (required)
        :param bool async: Perform the request asynchronously
        :return: None
        """

        all_params = ['modality_id']  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_modality" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'modality_id' is set
        if ('modality_id' not in params or
                params['modality_id'] is None):
            raise ValueError("Missing the required parameter `modality_id` when calling `delete_modality`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'modality_id' in params:
            path_params['ModalityId'] = params['modality_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/modalities/{ModalityId}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def get_all_modalities(self, **kwargs):  # noqa: E501
        """List all modalities.

        Requires login.
        This method makes a synchronous HTTP request by default.

        :param bool async_: Perform the request asynchronously
        :return: list[Modality]
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.get_all_modalities_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_all_modalities_with_http_info(**kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def get_all_modalities_with_http_info(self, **kwargs):  # noqa: E501
        """List all modalities.

        Requires login.
        This method makes a synchronous HTTP request by default.

        :param bool async: Perform the request asynchronously
        :return: list[Modality]
        """

        all_params = []  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_modalities" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/modalities', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[Modality]',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def get_modality(self, modality_id, **kwargs):  # noqa: E501
        """Get a modality&#39;s classification specification

        This method makes a synchronous HTTP request by default.

        :param str modality_id: (required)
        :param bool async_: Perform the request asynchronously
        :return: Modality
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.get_modality_with_http_info(modality_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_modality_with_http_info(modality_id, **kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def get_modality_with_http_info(self, modality_id, **kwargs):  # noqa: E501
        """Get a modality&#39;s classification specification

        This method makes a synchronous HTTP request by default.

        :param str modality_id: (required)
        :param bool async: Perform the request asynchronously
        :return: Modality
        """

        all_params = ['modality_id']  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_modality" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'modality_id' is set
        if ('modality_id' not in params or
                params['modality_id'] is None):
            raise ValueError("Missing the required parameter `modality_id` when calling `get_modality`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'modality_id' in params:
            path_params['ModalityId'] = params['modality_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/modalities/{ModalityId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Modality',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def replace_modality(self, modality_id, body, **kwargs):  # noqa: E501
        """Replace modality

        This method makes a synchronous HTTP request by default.

        :param str modality_id: (required)
        :param Modality body: (required)
        :param bool async_: Perform the request asynchronously
        :return: None
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.replace_modality_with_http_info(modality_id, body, **kwargs)  # noqa: E501
        else:
            (data) = self.replace_modality_with_http_info(modality_id, body, **kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def replace_modality_with_http_info(self, modality_id, body, **kwargs):  # noqa: E501
        """Replace modality

        This method makes a synchronous HTTP request by default.

        :param str modality_id: (required)
        :param Modality body: (required)
        :param bool async: Perform the request asynchronously
        :return: None
        """

        all_params = ['modality_id', 'body']  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method replace_modality" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'modality_id' is set
        if ('modality_id' not in params or
                params['modality_id'] is None):
            raise ValueError("Missing the required parameter `modality_id` when calling `replace_modality`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `replace_modality`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'modality_id' in params:
            path_params['ModalityId'] = params['modality_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = flywheel.models.Modality.positional_to_model(params['body'])
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/modalities/{ModalityId}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)
