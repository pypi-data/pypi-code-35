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

    def delete_file(self, path):
        """
        Delete a file from the activity

        :param path:                    the path to the file to delete

        :return:                        a string containing the word "Deleted"

        :raises EtnaAPI.BadRequest:     if the activity has already started
        :raises EtnaAPI.AccessDenied:   if the user does not have the required permissions
        :raises EtnaAPI.NotFound:       if the module or activity cannot be found
        """
        resp = rq.delete(self.module_api + "/" + self._activity_url + path, headers=self.session.header)
        if resp.status_code == 400:
            raise EtnaAPI.BadRequest("Unable to delete file '{}'".format(path))
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to delete file '{}': access defined".format(path))
        if resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to delete file '{}': file not found".format(path))
        return resp.json()

    def download_file(self, path):
        """
        Download a file from the activity

        :param path:                    the path to the file to download

        :return:                        the requested file contents

        :raises EtnaAPI.AccessDenied:   if the user does not have the required permissions
        :raises EtnaAPI.AccessDenied:   if module, activity or file cannot be found
        """
        resp = rq.get(self.module_api + "/" + self._activity_url + "/download/" + path, headers=self.session.header)
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to download file '{}': access denied".format(path))
        if resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to download file '{}': file not found".format(path))
        return resp.content

    def list_files(self):
        """
        Get a list of all the files in the activity

        :return:                        a list of objects, each containing metadata about a file

        :raises EtnaAPI.AccessDenied:   if the user does not have the required permissions
        :raises EtnaAPI.NotFound:       if the module or activity cannot be found
        """
        resp = rq.get(self.module_api + "/" + self._activity_url + "/files")
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to list files for activity with ID {}: access denied"
                                       .format(self.activity_id))
        if resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to list files for activity with ID {}: not found"
                                   .format(self.activity_id))
        return resp.json()
