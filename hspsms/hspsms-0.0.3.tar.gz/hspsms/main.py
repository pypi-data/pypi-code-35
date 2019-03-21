class HSPConnector:
    base_url = "http://sms.hspsms.com/"
    key_username = 'username'
    key_api = 'apikey'
    key_numbers = 'numbers'
    key_smstype = 'smstype'
    key_sendername = 'sendername'
    key_message = 'message'
    key_scheduled = 'scheduled'
    key_group = 'gname'
    key_from = 'from'
    key_to = 'to'
    key_query = '?'
    key_query_separater = '&'
    key_msgid = 'msgid'
    msgid = None
    response = None

    def __init__(self, username: str, apikey: str, sender: str, smstype: str):
        self.username = username
        self.api_key = apikey
        self.sender = sender
        self.sms_type = smstype

    def __send_request(self, url: str):
        import requests

        self.response = requests.get(url)

    def send_sms(self, recipient: list, message: str, sendername: str = None,
                 smstype: str = None,
                 scheduled: str = None):
        from urllib import parse

        endpoint = 'sendSMS'

        params = {self.key_username: self.username,
                  self.key_api: self.api_key, self.key_message: message,
                  self.key_sendername: sendername or self.sender,
                  self.key_smstype: smstype or self.sms_type}

        if scheduled:
            params[self.key_scheduled] = scheduled

        self.__send_request(self.base_url + endpoint + self.key_query +
                            parse.urlencode(params) + '&' + self.key_numbers +
                            '=' + ','.join(recipient))

        return self.__parse_response()

    def delivery_report(self, msgid: str):
        from urllib import parse

        url = 'getDLR'

        params = {self.key_username: self.username,
                  self.key_api: self.api_key, self.key_msgid: msgid}

        self.__send_request(self.base_url + url +
                            self.key_query +
                            parse.urlencode(params))

        return self.__parse_response()

    def __parse_response(self):
        import logging

        logger = logging.getLogger(__name__)

        if 200 <= self.response.status_code < 300:
            data = self.response.json()
            for some_data in data:
                if 'msgid' in some_data.keys():
                    self.msgid = some_data['msgid']
                    return self.msgid
            logger.error('MSGID was not found! ' +
                         str(self.response.text) +
                         '. Status Code: ' + str(self.response.status_code))
            raise ConnectionError('MSGID not found')
        else:
            logger.error('MSGID was not found! ' +
                         str(self.response.text) +
                         '. Status Code: ' + str(self.response.status_code))
            raise ConnectionError('Error code responded')
