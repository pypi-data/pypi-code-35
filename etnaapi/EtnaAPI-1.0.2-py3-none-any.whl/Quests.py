#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests as rq
import EtnaAPI


class Controller(EtnaAPI.BasicController):
    def __init__(self, session, module_id, activity_id):
        super().__init__(session)
        self.module_id = module_id
        self.activity_id = activity_id
        self._activity_url = str(module_id) + "/activities" + "/" + str(activity_id)

    def get_stages(self):
        """
        Get a list of stages for the quest

        :return:
        """
        resp = rq.get(self.module_api + "/" + self._activity_url + "/stages", headers=self.session.header)
        if resp.status_code == 400:
            raise EtnaAPI.BadRequest("Unable to get stages for activity with ID {}".format(self.activity_id))
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to get stages for activity with ID {}".format(self.activity_id))
        if resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to get stages for activity with ID {}: access denied".format(self.activity_id))
        return resp.json()
