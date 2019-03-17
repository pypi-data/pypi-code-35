from . import TelegramEndpoint
from .commons import _ChatOrInlineMessage
from .reply_markup import ReplyMarkup


class GetMe(TelegramEndpoint):
    pass


class GetUserProfilePhotos(TelegramEndpoint):
    def __init__(self, user_id):
        super().__init__()
        self.args = {
            'user_id': user_id
        }

    def offset(self, offset):
        self.args['offset'] = offset
        return self

    def limit(self, limit):
        self.args['limit'] = limit
        return self


class EditMessageReplyMarkup(TelegramEndpoint, _ChatOrInlineMessage, ReplyMarkup):
    def __init__(self, chat_or_inline_message_id, message_id):
        super().__init__()
        self.__chat_or_inline_message(chat_or_inline_message_id, message_id)


class DeleteMessage(TelegramEndpoint):
    def __init__(self, chat_id, message_id):
        super().__init__()
        self.args = {
            'chat_id': chat_id,
            'message_id': message_id
        }
