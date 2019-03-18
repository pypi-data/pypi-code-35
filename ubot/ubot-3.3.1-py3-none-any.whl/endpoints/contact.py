from . import TelegramEndpoint
from .commons import DisableNotification, ReplyToMessageId
from .reply_markup import ReplyMarkup


class SendContact(TelegramEndpoint, DisableNotification, ReplyMarkup, ReplyToMessageId):
    def __init__(self, chat_id, phone_number, first_name):
        super().__init__()
        self.args = {
            'chat_id': chat_id,
            'phone_number': phone_number,
            'first_name': first_name  # noqa: S001
        }

    def last_name(self, _last_name):
        self.args = {
            **self.args,
            'last_name': _last_name
        }
        return self

    def vcard(self, vcard):
        self.args = {
            **self.args,
            'vcard': vcard
        }
        return self
