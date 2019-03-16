#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests as rq
from urllib.parse import quote
import EtnaAPI


class Controller(EtnaAPI.BasicController):
    def get_module_by_id(self, module_id):
        """
        Retrieve module information given a module ID

        :param module_id:               the module ID, as a number

        :return:                        a JSON object describing the module

        :raises EtnaAPI.AccessDenied:   if the user does not have permissions to view the module
        :raises EtnaAPI.NotFound:       if no module is found with the given ID
        """
        resp = rq.get(self.module_api + "/" + str(module_id), headers=self.session.header)
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to get module with ID {}: access denied".format(module_id))
        if resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to get module with ID {}: no such module".format(module_id))
        return resp.json()

    def search_module(self, with_module_info=None, with_activity=None):
        """
        Search modules matching given criteria

        :param with_module_info:        a dictionary whose keys and values will be passed in the query
                                        (for example, "uv_name": "FDI-DVC1", or "version": 3)
        :param with_activity:           not implemented yet

        :return:                        a list containing information about each matching module

        :raises EtnaAPI.AccessDenied:   if the user does not have the required permissions
        """
        search_query = ""
        if with_module_info is not None:
            for info_key, info_value in with_module_info.items():
                if isinstance(info_value, str):
                    search_query += '+{}:"{}" '.format(info_key, info_value)
                else:
                    search_query += '+{}:{} '.format(info_key, info_value)
            search_query = quote(search_query.rstrip())
        if with_activity is not None:
            raise NotImplemented()
        resp = rq.get(self.module_api + "/search?archive=true&q={}".format(search_query), headers=self.session.header)
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to browse modules: access denied")
        return resp.json()["modules"]["hits"]

    def get_current_modules(self):
        """
        Get a list of all the ongoing modules

        :return:                        a list containing information about each ongoing module

        :raises EtnaAPI.AccessDenied:   if the user does not have the required permissions
        """
        resp = rq.get(self.module_api + "/uvs", headers=self.session.header)
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to get a list of the current modules: access denied")
        return resp.json()
