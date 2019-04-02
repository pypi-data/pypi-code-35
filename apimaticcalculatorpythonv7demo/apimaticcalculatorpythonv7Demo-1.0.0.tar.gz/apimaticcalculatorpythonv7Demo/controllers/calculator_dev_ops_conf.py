# -*- coding: utf-8 -*-

"""
    apimaticcalculatorpythonv7Demo

    This file was automatically generated for testing by APIMATIC v2.0 ( https://apimatic.io ).
"""

from apimaticcalculatorpythonv7Demo.api_helper import APIHelper
from apimaticcalculatorpythonv7Demo.configuration import Configuration
from apimaticcalculatorpythonv7Demo.controllers.base_controller import BaseController

class CalculatorDevOpsConf(BaseController):

    """A Controller to access Endpoints in the apimaticcalculatorpythonv7Demo API."""


    def calculate_dev_ops_stamford(self,
                                   operation,
                                   x,
                                   y):
        """Does a GET request to /{operation}.

        Calculates the expression using the specified operation..

        Args:
            operation (OperationType): The operator to apply on the variables
            x (float): The LHS value
            y (float): The RHS value

        Returns:
            float: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/{operation}'
        _url_path = APIHelper.append_url_with_template_parameters(_url_path, { 
            'operation': operation
        })
        _query_builder = Configuration.base_uri
        _query_builder += _url_path
        _query_parameters = {
            'x': x,
            'y': y
        }
        _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
            _query_parameters, Configuration.array_serialization)
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare and execute request
        _request = self.http_client.get(_query_url)
        _context = self.execute_request(_request)
        self.validate_response(_context)

        # Return appropriate type
        return float(_context.response.raw_body)
