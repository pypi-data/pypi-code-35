#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests as rq
import EtnaAPI


class Controller(EtnaAPI.BasicController):
    def __init__(self, session, module_id, activity_id):
        super(Controller, self).__init__(session)
        self.module_id = module_id
        self.activity_id = activity_id
        self._activity_url = str(module_id) + "/activities" + "/" + str(activity_id)

    def get_groups(self):
        """
        Get a list of the registered groups for the activity

        :return:                        a list of objects, each containing information about a group

        :raises EtnaAPI.AccessDenied:   if the user does not have the required permissions
        :raises EtnaAPI.NotFound:       if the module or activity cannot be found
        """
        resp = rq.get(self.module_api + "/" + self._activity_url + "/groups", headers=self.session.header)
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to list groups for activity {}: access denied".format(self.activity_id))
        if resp.status_code == 404:
            raise EtnaAPI.AccessDenied("Unable to list groups for activity {}: not found".format(self.activity_id))
        return resp.json()

    def get_unregistered_students(self):
        """
        Get a list of the unregistered students for the activity

        :return:                        a list of objects, each containing information about an unregistered student

        :raises EtnaAPI.AccessDenied:   if the user does not have the required permissions
        :raises EtnaAPI.NotFound:       if the module or activity cannot be found
        """
        resp = rq.get(self.module_api + "/" + self._activity_url + "/unregistered", headers=self.session.header)
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to list unregistered students for activity {}: access denied"
                                       .format(self.activity_id))
        if resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to list unregisteted students for activity {}: not found"
                                       .format(self.activity_id))
        return resp.json()

    def get_group_by_id(self, group_id):
        """
        Get a group's information given its ID

        :param group_id:                the group ID

        :return:                        an dictionary describing the group

        :raises EtnaAPI.AccessDenied:   if the user does not have the required permissions
        :raises EtnaAPI.NotFound:       if the module, activity or group cannot be found
        """
        resp = rq.get(self.module_api + "/" + self._activity_url + "/groups" + "/" + str(group_id),
                      headers=self.session.header)
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to get group for activity {}: access denied".format(self.activity_id))
        if resp.status_code == 404:
            raise EtnaAPI.AccessDenied("Unable to get group for activity {}: not found".format(self.activity_id))
        return resp.json()
