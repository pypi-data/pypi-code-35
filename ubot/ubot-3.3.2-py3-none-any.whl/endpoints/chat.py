from . import TelegramEndpoint
from .commons import DisableNotification


class ExportChatInviteLink(TelegramEndpoint):
    def __init__(self, chat_id):
        super().__init__()
        self.args = {
            'chat_id': chat_id
        }


class SetChatPhoto(TelegramEndpoint):
    method = 'POST'

    def __init__(self, chat_id, photo):
        super().__init__()
        self.args = {
            'chat_id': chat_id
        }

        with open(photo, 'r') as f:
            content = f.read()

        # todo
        # ALERT: Must be changed
        # not working
        self.fields = {
            **self.args,
            'photo': content
        }


class DeleteChatPhoto(TelegramEndpoint):
    def __init__(self, chat_id):
        super().__init__()
        self.args = {
            'chat_id': chat_id
        }


class SetChatTitle(TelegramEndpoint):
    def __init__(self, chat_id, title):
        super().__init__()
        self.args = {
            'chat_id': chat_id,
            'title': title
        }


class SetChatDescription(TelegramEndpoint):
    def __init__(self, chat_id, description):
        super().__init__()
        self.args = {
            'chat_id': chat_id,
            'description': description
        }


class PinChatMessage(TelegramEndpoint, DisableNotification):
    def __init__(self, chat_id, message_id):
        super().__init__()
        self.args = {
            'chat_id': chat_id,
            'message_id': message_id
        }


class UnpinChatMessage(TelegramEndpoint):
    def __init__(self, chat_id):
        super().__init__()
        self.args = {
            'chat_id': chat_id
        }


class LeaveChat(TelegramEndpoint):
    def __init__(self, chat_id):
        super().__init__()
        self.args = {
            'chat_id': chat_id
        }


class GetChat(TelegramEndpoint):
    def __init__(self, chat_id):
        super().__init__()
        self.args = {
            'chat_id': chat_id
        }


class GetChatAdministrators(TelegramEndpoint):
    def __init__(self, chat_id):
        super().__init__()
        self.args = {
            'chat_id': chat_id
        }


class GetChatMemberCount(TelegramEndpoint):
    def __init__(self, chat_id):
        super().__init__()
        self.args = {
            'chat_id': chat_id
        }


class GetChatMember(TelegramEndpoint):
    def __init__(self, chat_id, user_id):
        super().__init__()
        self.args = {
            'chat_id': chat_id,
            'user_id': user_id
        }


class SetChatStickerSet(TelegramEndpoint):
    def __init__(self, chat_id, sticker_set_name):
        super().__init__()
        self.args = {
            'chat_id': chat_id,
            'sticker_set_name': sticker_set_name
        }


class DeleteChatStickerSet(TelegramEndpoint):
    def __init__(self, chat_id):
        super().__init__()
        self.args = {
            'chat_id': chat_id
        }
