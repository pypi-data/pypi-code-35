#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests as rq
import EtnaAPI


class Controller(EtnaAPI.BasicController):
    def __init__(self, session, module_id):
        super().__init__(session)
        self.module_id = module_id
        self.module_id_str = str(module_id)

    def get_module_activities(self):
        """
        Get a list of all the activities in a module

        :return:                        a list containing information about each activity in the module

        :raise EtnaAPI.AccessDenied:    if the user does not have the required permissions
        """
        resp = rq.get(self.module_api + "/" + self.module_id_str + "/activities", headers=self.session.header)
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to get the activities in the module "
                                       "with ID {}: permission denied".format(self.module_id))
        return resp.json()

    def get_activity(self, activity_id):
        """
        Get the information associated with a single activity

        :param activity_id:             the activity ID

        :return:                        the information associated with the given activity

        :raise EtnaAPI.AccessDenied:    if the user does not have the required permissions
        :raise EtnaAPI.NotFound:        if the module or activity cannot be found
        """

        resp = rq.get(self.module_api + "/" + self.module_id_str + "/activities" + "/" + str(activity_id),
                      headers=self.session.header)
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to get the activity with ID {} in the module "
                                       "with ID {}: access denied".format(activity_id, self.module_id))
        if resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to list files for activity with ID {}: not found"
                                   .format(activity_id))
        return resp.json()

    # ToDo: Move this to the student module
    def get_student_activities(self, student_login):
        resp = rq.get(self.module_api + "/students" + "/" + student_login + "/currentactivities",
                      headers=self.session.header)
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to get the current activities for '{}'"
                                       ": access denied".format(student_login))
        if resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to find student")
        return resp.json()

    def delete_activity(self, activity_id):
        raise NotImplemented()  # The documentation doesn't show any successful example of deleting an activity

    def get_activity_marks(self, activity_id):
        """
        Get the marks for a given activity

        :param activity_id:             the activity ID

        :return:                        a list of objects representing the sessions of the activity

        :raise EtnaAPI.AccessDenied:    if the user does not have the required permissions
        :raise EtnaAPI.NotFound:        if the module or activity cannot be found
        """
        resp = rq.get(
            self.module_api + "/" + self.module_id_str + "/activities" + "/" + str(activity_id) + "/marks_list",
            headers=self.session.header)
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to get marks for the activity with ID {} in the module "
                                       "with ID {}: access denied".format(activity_id, self.module_id))
        if resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to get marks for the activity with ID {} in the module "
                                   "with ID {}: not found".format(activity_id, self.module_id))
        return resp.json()

    def get_activity_global_svn(self, activity_id=None, activity_info=None):
        """
        Extract the global SVN repo for a given activity

        :param activity_id:             the activity ID
        :param activity_info:           the activity full information, as returned by get_activity or get_activities

        :return:                        a string containing the repo URL or None if none was found

        :raise EtnaAPI.AccessDenied:    if the user does not have the required permissions
        :raise EtnaAPI.NotFound:        if the module or activity cannot be found
        """
        if activity_info is not None:
            if activity_info["rendu"] is None:
                return None
            return activity_info["rendu"] \
                       .replace("$$session$$", activity_info["module"]["name"]) \
                       .replace("$$session_id$$", str(activity_info["module"]["id"])).rpartition('/')[0] + '/'
        elif activity_id is not None:
            acti = self.get_activity(activity_id)
            return self.get_activity_global_svn(activity_info=acti)

    def add_activity(self, activity_info):
        """
        Add an activity to the module

        :param activity_info:           a dictionary containing the activity metadata

        :return:                        a dictionary representing the newly-created activity

        :raise EtnaAPI.AccessDenied:    if the user does not have the required permissions
        :raise EtnaAPI.NotFound:        if the module cannot be found
        """
        resp = rq.post(self.module_api + "/" + self.module_id_str + "/activities", json=activity_info,
                       headers=self.session.header)
        # ToDo: handle multiple 400-error case
        return resp.json()
