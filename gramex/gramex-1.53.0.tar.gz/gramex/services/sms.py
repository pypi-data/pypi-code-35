from __future__ import unicode_literals

import boto3
import requests
from gramex.http import OK
from gramex.config import app_log


class Notifier(object):
    def send(self, to, subject, sender):
        '''
        Send an SMS to the ``to`` mobile with ``subject`` as the contents. ``sender`` optional.

        Return API-specific response object.
        Raise Exception if API access fails. (This does not guarantee SMS delivery.)
        '''
        raise NotImplementedError()

    def status(self, result):
        '''
        Returns the delivery status of the SMS. The ``result`` is the output from ``.send()``.
        '''
        raise NotImplementedError()


class AmazonSNS(Notifier):
    '''
    Send messages via AmazonSNS::

        >>> notifier = AmazonSNS(
        ...     aws_access_key_id='...',
        ...     aws_secret_access_key='...',
        ...     region_name='ap-southeast-1',
        ...     smstype='Transactional')
        >>> notifier.send(
        ...     to='+919741552552',
        ...     subject='This is the content of the message',
        ...     sender='gramex')
    '''

    def __init__(self, aws_access_key_id, aws_secret_access_key,
                 smstype='Transactional', **kwargs):
        self.client = boto3.client(
            'sns',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            **kwargs)
        self.smstype = smstype

    def send(self, to, subject, sender):
        result = self.client.publish(
            PhoneNumber=to,
            Message=subject,
            MessageAttributes={
                'AWS.SNS.SMS.SenderID': {
                    'DataType': 'String',
                    'StringValue': sender,
                },
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': self.smstype,
                }
            }
        )
        app_log.info('SMS sent. SNS MessageId: %s', result['MessageId'])
        return result


class Exotel(Notifier):
    '''
    Send messages via Exotel::

        >>> notifier = Exotel(
        ...     sid='...',
        ...     token='...',
        ...     priority='high',
        ... )
        >>> notifier.send(
        ...     to='+919741552552',
        ...     subject='This is the content of the message',
        ...     sender='gramex')
    '''
    def __init__(self, sid, token, priority='high'):
        self.sid = sid
        self.token = token
        self.priority = priority
        self.send_url = 'https://{}:{}@api.exotel.com/v1/Accounts/{}/Sms/send.json'.format(
            self.sid, self.token, self.sid)
        self.stat_url = 'https://{}:{}@api.exotel.com/v1/Accounts/{}/SMS/Messages/%s.json'.format(
            self.sid, self.token, self.sid)

    def _handle_response(self, r):
        if r.status_code != OK:
            raise RuntimeError('Exotel API failed: %s' % r.text)
        result = r.json()
        return result['SMSMessage']

    def send(self, to, subject, sender=None):
        r = requests.post(self.send_url, {
            'From': sender or self.sid,
            'To': to,
            'Body': subject,
            'Priority': self.priority,
        })
        return self._handle_response(r)

    def status(self, result):
        r = requests.get(self.stat_url % result['Sid'])
        return self._handle_response(r)


class Twilio(Notifier):
    def __init__(self, account_sid, auth_token, **kwargs):
        raise NotImplementedError()
