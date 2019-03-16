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

    def request_global_moulinette(self, stage_name, dry_run=False):
        """
        Request a moulinette on a given stage for every registered group

        :param stage_name:      the name of the stage

        :return:                a dictionary containing information about the moulinette jobs

        :raises:                EtnaAPI.BadRequest if the given stage does not have an associated moulinette
                                EtnaAPI.AccessDenied if the user does not have the required permissions
                                EtnaAPI.NotFound if the module or activity cannot be found
        """
        if dry_run is True:
            resp = rq.post(self.module_api + "/" + self._activity_url + "/stages" + "/" + stage_name + "/moulinette",
                           headers=self.session.header, json={"dry_run": True})
        else:
            resp = rq.post(self.module_api + "/" + self._activity_url + "/stages" + "/" + stage_name + "/moulinette",
                           headers=self.session.header)
        if resp.status_code == 400:
            raise EtnaAPI.BadRequest("The stage '{}' does not have nay associated moulinette".format(stage_name))
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to request moulinette for stage '{}': access denied".format(stage_name))
        if resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to request moulinette for stage '{}': not found".format(stage_name))
        return resp.json()

    def request_moulinette(self, stage_name, group_id, dry_run=False):
        """
        Request a moulinette on a given stage of the activity, for a given group

        :param stage_name:      the name of the stage
        :param group_id:        the ID of the group
        :param dry_run:         whether the results should be private or sent to the student

        :return:                a dictionary containing information about the moulinette jobs

        :raises:                EtnaAPI.BadRequest if the given stage does not have an associated moulinette
                                EtnaAPI.AccessDenied if the user does not have the required permissions
                                EtnaAPI.NotFound if the module or activity cannot be found
        """
        json_data = {"group_id": group_id}
        if dry_run is True:
            json_data["dry_run"] = True
        resp = rq.post(self.module_api + "/" + self._activity_url + "/stages" + "/" + stage_name + "/moulinette",
                       headers=self.session.header, json=json_data)
        if resp.status_code == 400:
            raise EtnaAPI.BadRequest("The stage '{}' does not have nay associated moulinette".format(stage_name))
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to request moulinette for stage '{}': access denied".format(stage_name))
        if resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to request moulinette for stage '{}': not found".format(stage_name))
        return resp.json()
