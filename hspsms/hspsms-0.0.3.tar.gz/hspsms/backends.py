from sendsms.backends.base import BaseSmsBackend


class DjangoSendSMSBackend(BaseSmsBackend):
    """
    Django SendSMS HSPSMS backend

    Custom backend for hspsms based on Django SendSMS
    """

    def __init__(self, fail_silently=False, **kwargs):
        from django.conf import settings
        from django.core.exceptions import ImproperlyConfigured

        from . import HSPConnector

        super(DjangoSendSMSBackend, self).__init__(fail_silently=fail_silently,
                                                   **kwargs)
        try:
            hspsms = getattr(settings, "HSPSMS", None)
            username = hspsms['USER']
            apikey = hspsms['APIKEY']
            sender = hspsms['SENDER']
            smstype = hspsms['DEFAULT_SMSTYPE']
        except (KeyError, TypeError):
            if not fail_silently:
                raise ImproperlyConfigured("HSPSMS API config improperly "
                                           "configured.")
        else:
            self.hsp = HSPConnector(username=username, apikey=apikey,
                                    sender=sender, smstype=smstype)

    def send_messages(self, messages):
        for message in messages:
            try:
                self.hsp.send_sms(recipient=list(message.to),
                                  message=message.body,
                                  sendername=message.from_phone)
            except:
                if not self.fail_silently:
                    raise
