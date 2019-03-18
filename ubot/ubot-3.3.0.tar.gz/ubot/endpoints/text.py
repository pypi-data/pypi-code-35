from . import TelegramEndpoint
from .commons import DisableNotification, ParseMode, ReplyToMessageId, _ChatOrInlineMessage
from .reply_markup import ReplyMarkup


class SendMessage(TelegramEndpoint, DisableNotification, ParseMode, ReplyMarkup, ReplyToMessageId):
    def __init__(self, chat_id, text):
        super().__init__()
        self.args = {
            'chat_id': chat_id,
            'text': text
        }

    def disable_web_page_overview(self):
        self.args['disable_web_page_overview'] = True
        return self


class EditMessageText(TelegramEndpoint, ParseMode, ReplyMarkup, _ChatOrInlineMessage):
    def __init__(self, chat_or_inline_message_id, message_id, text):
        super().__init__()
        self.args = {
            'text': text
        }
        self.__chat_or_inline_message(chat_or_inline_message_id, message_id)

    def disable_web_page_overview(self):
        self.args['disable_web_page_overview'] = True
        return self
