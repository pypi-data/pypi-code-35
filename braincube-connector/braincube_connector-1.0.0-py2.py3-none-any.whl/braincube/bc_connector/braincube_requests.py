#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import traceback

import requests
import logging

__sso_token_uri = "https://mybraincube.com/sso-server/rest/session/openWithToken"


def get_sso_token(oauth2_acces_token):
    # Return a sso_token thanks to the token, which allows the access to the REST API
    if str(oauth2_acces_token):
        headers = {'Authorization': 'Bearer ' + str(oauth2_acces_token)}

        try:
            result = requests.get(__sso_token_uri, headers=headers)
            if result.status_code != 200:
                print("Authentication failure: try again with other credentials")
            else:
                print("Successful authentication, you can now access your data")
                return json.loads(result.text)
        except Exception as e:
            logging.debug(traceback.format_exc())


def request_data(ref, selected_variables, braincube_name, start_date, end_date, sso_token):
    # Return the result of the request of data retrieving, construct with the params of the user
    if ref['referenceDate'] not in selected_variables:
        selected_variables.append(ref['referenceDate'])
    url = "https://api.mybraincube.com/braincube/" \
          + braincube_name + "/braindata/" \
          + ref['name'] + "/LF"
    headers = {'Content-Type': 'application/json', 'Accept': "application/json", 'IPLSSOTOKEN': sso_token}
    filters = [ref['order'], start_date, end_date]
    content = {
        "order": ref['referenceDate'],
        "definitions": selected_variables,
        "context":
            {
                "dataSource": ref['name'],
                "filter":
                    {
                        "BETWEEN": filters
                    }
            }
    }
    result = requests.post(url, data=json.dumps(content), headers=headers)
    return json.loads(result.text)


def get_references(braincube_name, mb_id, sso_token):
    # Return the reference of the memorybase selected
    ref_url = "https://api.mybraincube.com/braincube/" + braincube_name + "/braindata/mb" + str(mb_id) + "/simple"
    ref_headers = {'IPLSSOTOKEN': sso_token}
    res = requests.get(ref_url, headers=ref_headers)
    return json.loads(res.text)


def get_data_defs(braincube_name, mb_id, sso_token):
    # Return the definitions of the variables for the selected memorybase
    url = "https://api.mybraincube.com/braincube/" + braincube_name + "/braincube/mb/" \
          + str(mb_id) + "/variables/selector"
    headers = {'IPLSSOTOKEN': sso_token}
    result = requests.get(url, headers=headers)
    # print(json.loads(result.text))
    return json.loads(result.text)['items']


def get_memorybase(braincube_name, sso_token):
    # Return the memorybases available for the selected braincube
    url = "https://api.mybraincube.com/braincube/" + braincube_name + "/braincube/mb/all/selector"
    headers = {'IPLSSOTOKEN': sso_token}
    result = requests.get(url, headers=headers)
    # print(json.loads(result.text))
    return json.loads(result.text)['items']
