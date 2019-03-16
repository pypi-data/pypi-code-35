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

class ReportsApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_access_log_report(self, **kwargs):  # noqa: E501
        """Get a report of access log entries for the given parameters

        This method makes a synchronous HTTP request by default.

        :param str start_date: An ISO formatted timestamp for the start time of the report
        :param str end_date: An ISO formatted timestamp for the end time of the report
        :param str uid: User id of the target user
        :param int limit: Maximum number of records to return
        :param str subject: Limit the report to the subject code of session accessed
        :param list[str] access_type: The list of access_types to filter logs
        :param bool csv: Set to download a csv file instead of json
        :param bool async_: Perform the request asynchronously
        :return: list[ReportAccessLogEntry]
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.get_access_log_report_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_access_log_report_with_http_info(**kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def get_access_log_report_with_http_info(self, **kwargs):  # noqa: E501
        """Get a report of access log entries for the given parameters

        This method makes a synchronous HTTP request by default.

        :param str start_date: An ISO formatted timestamp for the start time of the report
        :param str end_date: An ISO formatted timestamp for the end time of the report
        :param str uid: User id of the target user
        :param int limit: Maximum number of records to return
        :param str subject: Limit the report to the subject code of session accessed
        :param list[str] access_type: The list of access_types to filter logs
        :param bool csv: Set to download a csv file instead of json
        :param bool async: Perform the request asynchronously
        :return: list[ReportAccessLogEntry]
        """

        all_params = ['start_date', 'end_date', 'uid', 'limit', 'subject', 'access_type', 'csv']  # noqa: E501
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
                    " to method get_access_log_report" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'start_date' in params:
            query_params.append(('start_date', params['start_date']))  # noqa: E501
        if 'end_date' in params:
            query_params.append(('end_date', params['end_date']))  # noqa: E501
        if 'uid' in params:
            query_params.append(('uid', params['uid']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'subject' in params:
            query_params.append(('subject', params['subject']))  # noqa: E501
        if 'access_type' in params:
            query_params.append(('access_type', params['access_type']))  # noqa: E501
            collection_formats['access_type'] = 'multi'  # noqa: E501
        if 'csv' in params:
            query_params.append(('csv', params['csv']))  # noqa: E501

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
            '/report/accesslog', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[ReportAccessLogEntry]',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def get_access_log_types(self, **kwargs):  # noqa: E501
        """Get the list of types of access log entries

        This method makes a synchronous HTTP request by default.

        :param bool async_: Perform the request asynchronously
        :return: list[str]
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.get_access_log_types_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_access_log_types_with_http_info(**kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def get_access_log_types_with_http_info(self, **kwargs):  # noqa: E501
        """Get the list of types of access log entries

        This method makes a synchronous HTTP request by default.

        :param bool async: Perform the request asynchronously
        :return: list[str]
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
                    " to method get_access_log_types" % key
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
            '/report/accesslog/types', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[str]',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def get_project_report(self, **kwargs):  # noqa: E501
        """get_project_report

        This method makes a synchronous HTTP request by default.

        :param str projects: Specify multiple times to include projects in the report
        :param str start_date: Report start date
        :param str end_date: Report end date
        :param bool async_: Perform the request asynchronously
        :return: ReportProject
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.get_project_report_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_project_report_with_http_info(**kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def get_project_report_with_http_info(self, **kwargs):  # noqa: E501
        """get_project_report

        This method makes a synchronous HTTP request by default.

        :param str projects: Specify multiple times to include projects in the report
        :param str start_date: Report start date
        :param str end_date: Report end date
        :param bool async: Perform the request asynchronously
        :return: ReportProject
        """

        all_params = ['projects', 'start_date', 'end_date']  # noqa: E501
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
                    " to method get_project_report" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'projects' in params:
            query_params.append(('projects', params['projects']))  # noqa: E501
        if 'start_date' in params:
            query_params.append(('start_date', params['start_date']))  # noqa: E501
        if 'end_date' in params:
            query_params.append(('end_date', params['end_date']))  # noqa: E501

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
            '/report/project', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ReportProject',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def get_site_report(self, **kwargs):  # noqa: E501
        """get_site_report

        This method makes a synchronous HTTP request by default.

        :param bool async_: Perform the request asynchronously
        :return: ReportSite
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.get_site_report_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_site_report_with_http_info(**kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def get_site_report_with_http_info(self, **kwargs):  # noqa: E501
        """get_site_report

        This method makes a synchronous HTTP request by default.

        :param bool async: Perform the request asynchronously
        :return: ReportSite
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
                    " to method get_site_report" % key
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
            '/report/site', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ReportSite',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def get_usage_report(self, type, **kwargs):  # noqa: E501
        """Get a usage report for the site grouped by month or project

        This method makes a synchronous HTTP request by default.

        :param str type: The type of usage report to generate (required)
        :param str start_date: An ISO formatted timestamp for the start time of the report
        :param str end_date: An ISO formatted timestamp for the end time of the report
        :param bool async_: Perform the request asynchronously
        :return: list[ReportUsageEntry]
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_'):
            return self.get_usage_report_with_http_info(type, **kwargs)  # noqa: E501
        else:
            (data) = self.get_usage_report_with_http_info(type, **kwargs)  # noqa: E501
            if data and hasattr(data, 'return_value'):
                return data.return_value()
            return data


    def get_usage_report_with_http_info(self, type, **kwargs):  # noqa: E501
        """Get a usage report for the site grouped by month or project

        This method makes a synchronous HTTP request by default.

        :param str type: The type of usage report to generate (required)
        :param str start_date: An ISO formatted timestamp for the start time of the report
        :param str end_date: An ISO formatted timestamp for the end time of the report
        :param bool async: Perform the request asynchronously
        :return: list[ReportUsageEntry]
        """

        all_params = ['type', 'start_date', 'end_date']  # noqa: E501
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
                    " to method get_usage_report" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'type' is set
        if ('type' not in params or
                params['type'] is None):
            raise ValueError("Missing the required parameter `type` when calling `get_usage_report`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'type' in params:
            query_params.append(('type', params['type']))  # noqa: E501
        if 'start_date' in params:
            query_params.append(('start_date', params['start_date']))  # noqa: E501
        if 'end_date' in params:
            query_params.append(('end_date', params['end_date']))  # noqa: E501

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
            '/report/usage', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[ReportUsageEntry]',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)
