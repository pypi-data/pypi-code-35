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

    def get_checklist(self):
        resp = rq.get(self.module_api + "/" + self._activity_url + "/checklist",
                      headers=self.session.header)
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to get checklist for activity {}: access denied"
                                       .format(self.activity_id))
        elif resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to get checklist for activity {}: not found".format(self.activity_id))
        return resp.json()

    def add_checklist(self, data):
        resp = rq.post(self.module_api + "/" + self._activity_url + "/checklist", json=data,
                       headers=self.session.header)
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to add checklist for activity {}: access denied"
                                       .format(self.activity_id))
        elif resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to add checklist for activity {}: not found".format(self.activity_id))
        elif resp.status_code == 400:
            raise EtnaAPI.NotFound("Unable to add checklist for activity {}: bad request".format(self.activity_id))
        return resp.json()
