#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################ Copyrights and license ############################
#                                                                              #
# Copyright 2019 Sophian Mehboub <sophian.mehboub@gmail.com>                   #
#                                                                              #
# This file is part of google-iap.                                             #
#                                                                              #
# google-iap is free software: you can redistribute it and/or modify it under  #
# the terms of the GNU Lesser General Public License as published by the Free  #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# google-iap is distributed in the hope that it will be useful, but WITHOUT ANY#
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS    #
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more #
# details.                                                                     #
#                                                                              #
# You should have received a copy of the GNU Lesser General Public License     #
# along with google-iap. If not, see <http://www.gnu.org/licenses/>.           #
#                                                                              #
################################################################################

from .utils import GCPEXCEPTION
import json, yaml
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

class GcpIap:

    def __init__(self, SERVICE_ACCOUNT_FILE):
        SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
        try:
            self.credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        except IOError as e:
            raise GCPEXCEPTION(str(e))
        
    def getResource(self, resource, version):
        return build(resource, version, credentials=self.credentials)

    def getProject(self, projectId):
        service = self.getResource('cloudresourcemanager', 'v1')
        try:
            return service.projects().get(projectId=projectId).execute()
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def listProjects(self):
        l = []
        service = self.getResource('cloudresourcemanager', 'v1')
        try:
            for project in service.projects().list().execute()['projects']:
                l.append(project['projectId'])
            return l
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def getAllInstancesRaw(self, projectId):
        service = self.getResource('compute', 'v1')
        try:
            return service.instances().aggregatedList(project=projectId).execute()
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def listZonesUsed(self, projectId):
        l = []
        try:
            instances = self.getAllInstancesRaw(projectId)
            for k,v in instances['items'].items():
                if 'instances' in v:
                    l.append(k.replace('zones/',''))
            return l
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def listInstancesByZone(self, projectId, zone):
        l = []
        service = self.getResource('compute', 'v1')
        try:
            instances = service.instances().list(project=projectId, zone=zone).execute()
            for v in instances['items']:
                l.append(v['name'])
            return l
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def listInstances(self, projectId):
        l = []
        try:
            instances = self.getAllInstancesRaw(projectId)
            for k,v in instances['items'].items():
                if 'instances' in v:
                    for instance in v['instances']:
                        l.append(instance['name'])
            return l
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def getIapPolicy(self, project, zone=None ,instance=None, format='yaml'):
        formatSupported = ['json', 'yaml']
        if not format in formatSupported: raise GCPEXCEPTION('The supported format is yaml or json')
        service = self.getResource('iap', 'v1beta1')
        project_num = self.getProject(project)['projectNumber']
        zone = '/zones/%s' % zone if zone else ""
        instance = '/instances/%s' % instance if instance else ""
        try:
            resp = service.v1beta1().getIamPolicy(resource='projects/%s/iap_tunnel%s%s' % (project_num, zone, instance)).execute()
            if format == 'json':
                resp = { "policy" : resp }
                return json.dumps(resp, indent=4, sort_keys=True)
            elif format == 'yaml':
                js = json.loads(json.dumps(resp))
                return yaml.safe_dump({ "policy" : js }, allow_unicode=True,  default_flow_style=False)
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def setIapPolicy(self, project, policyfile, zone=None ,instance=None):
        service = self.getResource('iap', 'v1beta1')
        project_num = self.getProject(project)['projectNumber']
        zone = '/zones/%s' % zone if zone else ""
        instance = '/instances/%s' % instance if instance else ""
        try:
            body = open(policyfile).read()
        except IOError as e:
            raise GCPEXCEPTION(str(e))
        try:
            body = yaml.safe_load(body)
        except yaml.scanner.ScannerError as e:
            raise GCPEXCEPTION(str(e))

        try:
            resp = service.v1beta1().setIamPolicy(resource='projects/%s/iap_tunnel%s%s' % (project_num, zone, instance), body=body).execute()
            return json.dumps({ "policy" : resp }, indent=4, sort_keys=True)
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

