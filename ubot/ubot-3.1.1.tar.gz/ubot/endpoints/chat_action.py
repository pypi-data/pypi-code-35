from . import TelegramEndpoint
from .exceptions import InvalidChatAction


class SendChatAction(TelegramEndpoint):
    def __init__(self, chat_id, action):
        super().__init__()
        if action not in ['typing', 'upload_photo', 'record_video', 'upload_video', 'record_audio', 'upload_audio',
                          'upload_document', 'find_location', 'record_video_note', 'upload_video_note']:
            raise InvalidChatAction

        self.args = {
            'chat_id': chat_id,
            'action': action  # noqa: S001
        }
