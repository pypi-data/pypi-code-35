# -*- coding: UTF-8 -*-
#! python3

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging

# 3rd party
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

ISOGEO_API_URL_BASE = "https://api.isogeo.com/"

client_id = "isogeo-legacy-scripts-ab1b9920af95422595782fee5c5b8786"
client_secret = "NUbkbXmGlm2mvHlkn7sqjqJZosPCuho1wPt4NUXPd37ARQliV70pWtgIlRiyeQVO"
username = "julien.moura@isogeo.com"
password = "20Izoge@14"
uri_token = "https://id.api.isogeo.com/oauth/token"

md_1 = "2313f3f7e0f540c3ad2850d7c9c4c04d"
md_2 = "43e8f4a6f0e04b4a87ff45f8431220dd"


# AUTH #################
# for workgroup applications

# client = BackendApplicationClient(client_id="csw-65468859dd254121bfd781645203af61")
# oauth = OAuth2Session(client=client)
# token = oauth.fetch_token(
#     token_url='https://id.api.isogeo.com/oauth/token',
#     client_id="csw-65468859dd254121bfd781645203af61",
#     client_secret="T9mToPsnxdwP009vUH0JJuxDrsox88zp1HhTaeaLUzAS1YcXLindUi879dWnj5PD"
#     )

# print(token)

# for legacy scripts (password flow legacy)
isogeo = OAuth2Session(client=LegacyApplicationClient(client_id=client_id),
                       auto_refresh_url=uri_token)
token = isogeo.fetch_token(token_url=uri_token,
                           username=username,
                           password=password,
                           client_id=client_id,
                           client_secret=client_secret)


# OPERATIONS #################
# memberships
url_memberships = "{}/account/memberships".format(ISOGEO_API_URL_BASE)
req_memberships = isogeo.get(url_memberships,
                             # headers=head,
                             # params=payload,
                            #  verify=1
                            )

user_memberships = req_memberships.json()
print(len(user_memberships))

# feature attributes
data = {
    "name": "TEST ATTRIBUTyh",
    "alias": "ATTR_TEST",
    "dataType": "Char",
    "description": "Hop hop **hop**",
    "language": "fr"
}
url_md_add_attributes = "{}/resources/{}/feature-attributes"\
    .format(
        ISOGEO_API_URL_BASE,
        "2313f3f7e0f540c3ad2850d7c9c4c04d"
    )

req_md_add_attributes = isogeo.post(url=url_md_add_attributes,
                                    #  headers=head,
                                    #  payload=payload,
                                    data=data,
                                    # verify=ssl_opt
                                    )

print(req_md_add_attributes.status_code)


# events - creation date
# data = {
#     "date": "2019-02-01",
#     "kind": "creation",
#     "waitForSync": 1
# }

# url_md_add_event = "{}/resources/{}/events"\
#     .format(
#         ISOGEO_API_URL_BASE,
#         "2313f3f7e0f540c3ad2850d7c9c4c04d"
#     )

# req_md_add_creation_date = isogeo.post(url=url_md_add_event,
#                                        #  headers=head,
#                                        #  payload=payload,
#                                        data=data,
#                                        # verify=ssl_opt
#                                       )

# print(req_md_add_creation_date.status_code)

# remove it
# data = {
#     "date": "2019-02-01",
#     "kind": "creation",
#     "waitForSync": 1
# }

url_md_del_event = "{}/resources/{}/events/9e8a28d2d4df4b43843198410b84781c"\
    .format(
        ISOGEO_API_URL_BASE,
        "2313f3f7e0f540c3ad2850d7c9c4c04d"
    )

req_md_add_creation_date = isogeo.delete(url=url_md_del_event,
                                       #  headers=head,
                                       #  payload=payload,
                                    #    data=data,
                                       # verify=ssl_opt
                                       )
