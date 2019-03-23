from frogtips.api import Credentials
from frogtips import constants
import json
import requests
from io import StringIO
import sys


class Tip:
    id = 0
    tip = ''

    def __init__(self, id = 0, tip = ''):
        self.set_id(id)
        self.set_tip(tip)

        if (id > 0) & (tip == ''):
            self.download_tip(id)

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_tip(self):
        return self.tip

    def get_formatted_tip(self):
        tip_string = "TIP " + str(self.get_id()) + ": " + self.get_tip()
        return tip_string

    def set_tip(self, tip):
        self.tip = tip

    def serialize(self):
        temp_tip = {}
        temp_tip['id'] = self.get_id()
        temp_tip['tip'] = self.get_tip()
        return json.dumps(temp_tip)

    def download_tip(self, id):
        """Download tip [id] from the frog.tips API server. Sets self.id and
        self.tip upon successful download."""
        credentials = Credentials()
        url = 'https://' + constants.FROG_TIPS_DOMAIN + \
              '/api/3/tips/' + str(id)
        headers = {'Content-type': 'application/json',
                   'Accept': 'application/json',
                   'Authorization': 'Basic ' +
                                    credentials.get_http_basic_auth()}
        response = requests.get(url=url,
                                headers=headers)

        if (response.status_code == 200) or (response.status_code == 201):
            # is all of this truly necessary?
            tip_io = StringIO(str(response.content.decode('utf-8')))
            temp_tip = json.load(tip_io)

            self.set_id(temp_tip['id'])
            self.set_tip(temp_tip['tip'])
        elif response.status_code == 404:
            self.set_tip(constants.ERROR_MSG_404)

    def submit_tip(self, tip_text):
        """Submits tip_text to the frog.tips API server. Upon success, sets
        self.tip to tip_text and self.id to the new tip ID returned from the
        API server."""
        if not self.validator(tip_text):
            sys.exit("Invalid FROG tip: %s" % tip_text)

        credentials = Credentials()
        if credentials.get_username() == '':
            sys.exit("Your API key must have an associated username for " +
                     "you to be able to submit FROG tips.")

        url = 'https://' + constants.FROG_TIPS_DOMAIN + '/api/3/tips/add'
        temp_tip = {'tip': tip_text}
        http_headers = {'Content-type': 'application/json',
                        'Accept': 'application/json',
                        'Authorization': 'Basic ' +
                                         credentials.get_http_basic_auth()}
        response = requests.post(url=url,
                                 data=json.dumps(temp_tip),
                                 headers=http_headers)
        self.set_tip(tip_text)
        self.set_id(response.json()['id'])

    def validator(self,tip_text = ''):
        """Returns True if and only if:
        - the tip is less than constants.MAX_TIP_LENGTH
        - the tip contains the word FROG
        - the tip is in all upper case
        - the tip ends with a period"""
        is_valid = True

        if len(tip_text) > constants.MAX_TIP_LENGNTH:
            is_valid = False

        if not 'FROG' in tip_text:
            is_valid = False

        if not tip_text.isupper():
            is_valid = False

        if not tip_text.endswith('.'):
            is_valid = False

        return is_valid