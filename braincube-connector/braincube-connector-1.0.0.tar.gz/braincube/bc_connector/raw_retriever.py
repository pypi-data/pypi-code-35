#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from datetime import datetime

from braincube.bc_connector.braincube_requests import get_data_defs, get_memorybase, get_references, request_data
from braincube.bc_connector.entities.braincube import Braincube
from braincube.bc_connector.entities.memorybase import Memorybase


class RawRetriever:  # Class giving access to functions communicating with the braincube API
    def __init__(self, sso_token, braincubes):
        self.__sso_token = sso_token
        self.__braincubes = braincubes

    def get_braincube_list(self):
        # Return a dataframe containing the braincubes accessible
        return self.__braincubes

    def get_memorybase_list(self, braincube_name):
        # Return a dataframe containing the memorybases available for the braincube selected
        try:
            return get_memorybase(braincube_name, self.__sso_token)
        except json.decoder.JSONDecodeError:
            print("Invalid parameters, please check spelling or access rights")

    def get_memorybase_order_variable(self, braincube_name, mb_id):
        # Return the id of the variable which is used to order the memorybase
        try:
            return get_references(braincube_name, mb_id, self.__sso_token)
        except json.decoder.JSONDecodeError:
            print("Invalid parameters, please check spelling or access rights")

    def get_variable_list(self, braincube_name, mb_id):
        # Return a dataframe containing the variables available for the memorybase selected
        try:
            return get_data_defs(braincube_name, mb_id, self.__sso_token)
        except json.decoder.JSONDecodeError:
            print("Invalid parameters, please check spelling or access rights")

    def retrieve_all_variables_from_memory_base(self, braincube_name, mb_id, start_date, end_date=datetime.now()):
        # Return a dataframe containing the datas of all the variables of the selected memorybase
        # Indexed with the order variable, a column represents a variable
        variable_list = self.get_variable_list(braincube_name, mb_id)
        selected_variables = []
        for var in variable_list:
            selected_variables.append(var['id'])
        return self.retrieve_data(braincube_name, mb_id, selected_variables, start_date, end_date)

    def retrieve_data(self, braincube_name, mb_id, variable_list, start_date, end_date=datetime.now()):
        # Return a dataframe containing the datas of the seelcted variables for the selected memorybase
        # Indexed with the order variable, a column represents a variable
        try:
            print('Braincube selected : ' + braincube_name)
            print('MemoryBase selected : ' + str(mb_id))
            ref = get_references(braincube_name, mb_id, self.__sso_token)
            selected_variables = []
            for var in variable_list:
                selected_variables.append(ref['name'] + '/d' + str(var))
            return request_data(ref, selected_variables,
                                braincube_name, start_date.strftime("%Y%m%d_%H%M%S"),
                                end_date.strftime("%Y%m%d_%H%M%S"), self.__sso_token)['datadefs']
        except json.decoder.JSONDecodeError:
            print("Invalid parameters, please check spelling or access rights")

    def get_braincube(self, braincube_name):
        return Braincube(braincube_name, self)

    def get_memorybase(self, braincube_name, mb_id):
        return Memorybase(braincube_name, mb_id, self)
