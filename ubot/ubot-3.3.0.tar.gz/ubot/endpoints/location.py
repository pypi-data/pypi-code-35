from . import TelegramEndpoint
from .commons import DisableNotification, ReplyToMessageId, _ChatOrInlineMessage
from .reply_markup import ReplyMarkup


class SendLocation(TelegramEndpoint, DisableNotification, ReplyMarkup, ReplyToMessageId):
    def __init__(self, chat_id, latitude, longitude):
        super().__init__()
        self.args = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude
        }

    def live_period(self, live_period):
        self.args['live_period'] = live_period
        return self


class EditMessageLiveLocation(TelegramEndpoint, _ChatOrInlineMessage, ReplyMarkup):
    def __init__(self, chat_or_inline_message_id, message_id, latitude, longitude):
        super().__init__()
        self.args = {
            'latitude': latitude,
            'longitude': longitude
        }
        self.__chat_or_inline_message(chat_or_inline_message_id, message_id)


class StopMessageLiveLocation(TelegramEndpoint, ReplyMarkup, _ChatOrInlineMessage):
    def __init__(self, chat_or_inline_message_id, message_id):
        super().__init__()
        self.__chat_or_inline_message(chat_or_inline_message_id, message_id)
