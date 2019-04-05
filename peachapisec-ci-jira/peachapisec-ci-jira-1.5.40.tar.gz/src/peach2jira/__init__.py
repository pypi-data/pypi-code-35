#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

"""
Peach API Security Jira issue importer

This tool is used to publish faults into a Jira issue tracker.
See the Peach API Security user guide for information on usage.
"""

'''
Copyright 2017 Peach Tech

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

try:
    import click
    import requests
    from requests.exceptions import HTTPError
    import peachapisec
    import pystache
    import hexdump
except:
    print("Error, missing dependencies.")
    print("Use 'pip install -r requirements.txt'")
    exit(-1)

import sys
import os
import io
import json
import base64
import hashlib
import pkg_resources

class Jira2Peach:
    def __init__(self, api, api_token, flag_unicode, settings, comment, description):

        self._unicode = flag_unicode

        if settings == 'PEACH_DEFAULT':
            settings = pkg_resources.resource_filename(
                __name__, "settings.json")
        if comment == 'PEACH_DEFAULT':
            comment = pkg_resources.resource_filename(
                __name__, "comment.mustache")
        if description == 'PEACH_DEFAULT':
            description = pkg_resources.resource_filename(
                __name__, "description.mustache")

        if not os.path.isfile(settings):
            print("Error, settings file not found '%s'"%settings)
            exit(-1)
        if not os.path.isfile(comment):
            print("Error, comment template not found '%s'"%comment)
            exit(-1)
        if not os.path.isfile(description):
            print("Error, description template not found '%s'"%description)
            exit(-1)
        
        print(" - Settings file: %s" % settings)
        print(" - Comment template: %s" % comment)
        print(" - Description template: %s" % description)

        with io.open(settings, 'r', encoding='utf-8') as f:
            self._settings = pystache.parse(f.read())

        if self._unicode:
            print(" - Uncode in description: Enabled")
        else:
            print(" - Unicode in description: Disabled")

        if not api:
            print("Error, missing --api argument, or PEACH_API environment variable")
        if not api_token:
            print("Error, missing --api_token argument, or PEACH_API_TOKEN environment variable")

        os.environ['PEACH_API'] = api
        os.environ['PEACH_API_TOKEN'] = api_token
    
        peachapisec.set_peach_api(api)
        peachapisec.set_peach_api_token(api_token)

        self._renderer = pystache.Renderer(escape=self._json_escape)

        self._opts = { 
            'Env' : dict(os.environ),
            'Comment': comment,
            'Description':description
            }

        self._seen_buckets = set()

    def run(self):
        all_jobs = peachapisec.get_jobs()
        if len(all_jobs) == 0:
            print(" - No jobs found, exiting")
            return 1

        # Use the most recent job
        self._opts['Job'] = all_jobs[0]

        faults = peachapisec.get_faults(self._opts['Job']['Id'])
        if len(faults) == 0:
            print(" - No faults found, exiting")
            return 0

        print(" - %d faults found for processing" % len(faults))

        for fault in faults:
            print("  - Fault: %s" % fault["Title"])

            if fault['Visibility'] == 'Hidden':
                print("     Skipping, marked as hidden.")
            else:
                self._export(fault)

    def _jiraJsonRequestGet(self, opts, url):
        self._debug(">> _jiraJsonRequestGet: %s" % url)

        try:
            url = (opts['url'] + url).encode("ascii")
            response = requests.get(url,
                headers={'Content-Type':'application/json'},
                auth=(opts['user'], opts['pass']))
        except UnicodeError:
            print("Error, please verify url is correctly formated: '%s'" % url)
            raise

        try:
            faults = response.json()
            response.raise_for_status()

            return faults
        except:
            self._debug("_jiraJsonRequestGet: %s" % response)

        response.raise_for_status()
        return None

    def _jiraGetCustomFieldId(self, opts, bucket_name):

        try:
            url = (opts['url'] + "/rest/api/2/field").encode("ascii")
            response = requests.get(url,
                headers={'Content-Type':'application/json'},
                auth=(opts['user'], opts['pass']))
        except UnicodeError:
            print("Error, please verify url is correctly formated: '%s'" % url)
            raise

        response.raise_for_status()

        try:
            fields = response.json()

            for field in fields:
                if field["name"] == opts['bucket_field']:
                    return field["id"]

            return None
        except:
            self._debug("_jiraJsonRequestGet: %s" % response)
            return None

    def _jiraCreateIssue(self, opts):
        try:
            url = (opts['url'] + "/rest/api/2/issue").encode("ascii")
            response = requests.post(url,
                json=opts['issue'],
                headers={'Content-Type':'application/json'},
                auth=(opts['user'], opts['pass']))
        except UnicodeError:
            print("Error, please verify url is correctly formated: '%s'" % url)
            raise

        response.raise_for_status()

        try:
            result = response.json()
            return result["self"]
        except:
            self._debug("_jiraCreateIssue: %s" % response)

    def _jiraBucketCheck(self, opts):
        bucket_field = opts.get('bucket_field', None)
        bucket = opts.get('bucket', None)

        self._debug(">> _jiraBucketCheck(%s)" % bucket)

        if not bucket_field:
            self._debug("<< _jiraBucketCheck: No bucket_field speficied")
            return None

        if not hasattr(self, '_bucket_field_id'):
            self._bucket_field_id = self._jiraGetCustomFieldId(opts, bucket_field)
            self._debug("Resolved bucket_field '%s' to id '%s'" % (bucket_field, self._bucket_field_id))

        if not bucket:
            self._debug("<< _jiraBucketCheck: No bucket speficied")
            return None

        bucket_hash = hashlib.md5(bucket.encode('utf-8')).hexdigest()[0:8]

        if bucket_hash in self._seen_buckets:
            self._debug("<< _jiraBucketCheck: Already seen")
            return None

        # Add bucket information to issue
        opts['issue']['fields'][self._bucket_field_id] = '%s (%s)' % (bucket, bucket_hash)

        project = opts['issue']['fields']['project']['key']
        jql = 'jql=project=%s+AND+status!=done+AND+"%s"+~+"%s"' % (project, bucket_field, bucket_hash)

        search = self._jiraJsonRequestGet(opts, "/rest/api/2/search?"+jql)

        self._debug("<< _jiraBucketCheck: total: %d" % search["total"])

        self._seen_buckets.add(bucket_hash)

        if search["total"] > 0:
            return search["issues"][0]

        return None

    def _jiraAttachFileToIssue(self, opts, issue, name, data):

        payload = {"file":(name, data)}

        response = requests.post(issue + "/attachments",
            files=payload,
            headers={'X-Atlassian-Token': 'no-check'},
            auth=(opts['user'], opts['pass']))

        response.raise_for_status()

        try:
            result = response.json()
            return result
        except:
            self._debug("_jiraAttachFileToIssue: %s" % response)
        
        return None
    
    def _jiraAddComment(self, opts, issue, comment):
        response = requests.post(issue["self"]+"/comment",
            json={"body":comment},
            headers={'Content-Type':'application/json'},
            auth=(opts['user'], opts['pass']))

        response.raise_for_status()

        return None

    def _replace_str_index(self, text, index, replacement):
        return u'%s%s%s'%(text[:index],replacement,text[index+1:])

    def _newIssue(self, opts):
        # Replace fault with fault details
        job_id = self._opts['Job']['Id']
        fault_id = self._opts['Fault']['Id']
        self._opts['Fault'] = peachapisec.get_fault(job_id, fault_id)
        
        # Turn fault data into strings
        fault_data = self._opts['Fault']['FaultData']
        self._opts['FaultData'] = {
            'OriginalRequest' : self._as_str(fault_data['OriginalRequest']),
            'ActualRequest' : self._as_str(fault_data['ActualRequest']),
            'ActualResponse' : self._as_str(fault_data['ActualResponse']),
            'RecordedRequest' : self._as_str(fault_data['RecordedRequest']),
            'RecordedResponse' : self._as_str(fault_data['RecordedResponse']),
        }

        with io.open(opts['description'], 'r', encoding='utf-8') as f:
            desc_str = pystache.render(f.read(), self._opts)
            opts['issue']['fields']['description'] = desc_str

        if not self._unicode:
            # remove any unicode characters
            description = opts['issue']['fields']['description']
            
            for i in xrange(len(description)):
                chr_ord = ord(description[i])
                if chr_ord == ord('\n') or chr_ord == ord('\r'):
                    continue
                elif chr_ord > 126 or chr_ord < 32:
                    description = self._replace_str_index(description, i, u'?')
            
            opts['issue']['fields']['description'] = description

        if len(opts['issue']['fields']['description']) > 32000:
            opts['issue']['fields']['description'] = opts['issue']['fields']['description'][:32000]

        issueUrl = self._jiraCreateIssue(opts)

        for i in ['OriginalRequest', 'ActualRequest', 'ActualResponse', 'RecordedRequest', 'RecordedResponse']:
            data = fault_data[i]

            if not data:
                continue

            data = bytearray(base64.b64decode(data))

            self._print("    - Adding file %s.bin" % i)
            self._jiraAttachFileToIssue(opts, issueUrl, '%s.bin' % i, data)

    def _commentIssue(self, issue, opts):
        with io.open(opts['comment'], 'r', encoding='utf-8') as f:
            comment = pystache.render(f.read(), self._opts)
        self._jiraAddComment(opts, issue, comment)

    def _debug(self, msg):
        #print(msg)
        pass

    def _print(self, msg):
        print(msg)
        pass

    def _json_escape(self, value):
        return json.dumps(value)[1:-1]

    def _as_str(self, data):
        if not data:
            return ''

        buf = base64.b64decode(data)
        boundary = self._find_boundary(buf)
        headers = buf[0:boundary].decode('utf-8')
        body = hexdump.hexdump(buf[boundary:], result='return')
        return headers + body

    def _find_boundary(self, buf):
        last = 0
        state = 0
        for i in range(0, len(buf)):
            octet = buf[i]
            if last == '\r' and octet == '\n':
                if state > 0:
                    return i+1
                state += 1
            elif last != '\n':
                state = 0
            last = octet
        return len(buf)

    def _export(self, fault):
        self._opts['Fault'] = fault

        json_str = self._renderer.render(self._settings, self._opts)
        opts = json.loads(json_str)

        issue = self._jiraBucketCheck(opts)

        if issue:
            self._commentIssue(issue, opts)
        else:
            self._newIssue(opts)

        # Impact, Detection, Assertion, Description, Title, Owasp, Cwe,
        # FaultDetails, FaultData, Visibility, JobId, TestCase, Job,
        # CweUrl, OwaspUrl, Operation, Exploitability, Parameter, Id, Check


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-a", "--api", help="Peach API Security API URL. Defaults to PEACH_API environ.")
@click.option("-t", "--api_token", help="Peach API Security API Token. Defaults to PEACH_API_TOKEN environ.")
@click.option('-u', '--unicode', 'flag_unicode', is_flag=True, default=False, help="Enable Uncode support in JIRA descriptions. Defaults to disabled.")
@click.option("-s", "--settings", help="Settings file, defaults to package version", default='PEACH_DEFAULT')
@click.option("-c", "--comment", help="Comment template file, defaults to package version", default='PEACH_DEFAULT')
@click.option("-d", "--description", help="Description template file, defaults to package version", default='PEACH_DEFAULT')
def cli(api, api_token, flag_unicode, settings, comment, description, **kwargs):
    worker = Jira2Peach(api, api_token, flag_unicode, settings, comment, description)
    return worker.run()

def run():
    cli(auto_envvar_prefix='PEACH')

if __name__ == '__main__':
    run()

# end
