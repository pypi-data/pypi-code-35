#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests as rq
import EtnaAPI


class Controller(EtnaAPI.BasicController):
    def __init__(self, session, stud_login):
        super().__init__(session)
        self.student = stud_login

    def get_current_activities(self):
        """
        Get the student's current activities

        :return:        a dictionary sorting the activities by module, then by type
        """
        resp = rq.get(self.module_api + "/students" + "/" + self.student + "/currentactivities",
                      headers=self.session.header)
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to get the current activities for student '{}'"
                                       ": access denied".format(self.student))
        if resp.status_code == 404:
            raise EtnaAPI.AccessDenied("Unable to find student")
        return resp.json()
