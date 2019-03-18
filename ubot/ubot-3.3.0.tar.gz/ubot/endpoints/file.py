from . import TelegramEndpoint
from .commons import DisableNotification, ParseMode, ReplyToMessageId, _ChatOrInlineMessage
from .reply_markup import ReplyMarkup
from ..multipart_form_data import MultipartEncoder


class FileEndpoint(TelegramEndpoint, DisableNotification, ReplyMarkup, ReplyToMessageId):
    file_type = None
    attributes = []

    def __init__(self, chat_id, file, is_path=True):
        # note: chat_id is mandatory but is not put as argument in the constructor to allow easier caching

        super().__init__()
        self.args = {}

        if is_path is True:
            self.method = 'POST'
            self.multipart_encoder = MultipartEncoder()
            self.multipart_encoder.add_file(self.file_type, file)
            self.headers = {}
        else:
            self.method = 'GET'
            self.args[self.file_type] = file

    def chat_id(self, chat_id):
        self.args['chat_id'] = chat_id
        return self

    def finalize_data(self):
        # call this method after you're sure that you inserted every file you want to upload
        # useful e.g. for adding the thumbnail (when it'll be implemented) but leaving the chat_id dynamic

        if self.method == 'POST':
            boundary, data = self.multipart_encoder.encode()
            self.headers['Content-Type'] = 'multipart/form-data; boundary=%s' % boundary
            self.data = data

    def serialize(self):
        if 'chat_id' not in self.args:
            raise Exception('FileEndpoint without chat_id')

        if self.method == 'POST':
            return self.method, self.endpoint, self.args, self.data, self.headers
        return self.method, self.endpoint, self.args, None, self.headers


class SerializableToInputMedia:
    serialized_fields = []

    def to_input_media(self):

        serialized = {
            'type': self.file_type,
        }

        # todo
        # upload + attach
        # warning: doesn't work
        if self.method == 'POST':
            raise Exception('Must target updated file')
            pass

        serialized['media'] = self.args[self.file_type]

        attributes = self.attributes + self.serialized_fields
        for attribute in attributes:
            if attribute in self.args:
                serialized[attribute] = self.args[attribute]

        return serialized


class Caption:
    def caption(self, caption):
        self.args['caption'] = caption
        return self


# todo
class Thumb:
    pass


class SendPhoto(FileEndpoint, Caption, ParseMode, SerializableToInputMedia):
    file_type = 'photo'
    serialized_fields = ['caption', 'parse_mode']


class SendAudio(FileEndpoint, Caption, ParseMode, Thumb, SerializableToInputMedia):
    file_type = 'audio'
    attributes = ['duration', 'performer', 'title']
    serialized_fields = ['caption', 'parse_mode', 'thumb']


class SendDocument(FileEndpoint, Caption, ParseMode, Thumb, SerializableToInputMedia):
    file_type = 'document'
    serialized_fields = ['caption', 'parse_mode', 'thumb']


class SendVideo(FileEndpoint, Caption, ParseMode, Thumb, SerializableToInputMedia):
    file_type = 'video'
    attributes = ['duration', 'width', 'height']
    serialized_fields = ['caption', 'parse_mode', 'thumb', 'supports_streaming']

    def supports_streaming(self):
        self.args = {
            **self.args,
            'supports_streaming': True
        }
        return self


class SendAnimation(FileEndpoint, Caption, ParseMode, Thumb, SerializableToInputMedia):
    file_type = 'animation'
    attributes = ['duration', 'width', 'height']
    serialized_fields = ['caption', 'parse_mode', 'thumb']


class SendVoice(FileEndpoint, Caption, ParseMode):
    file_type = 'animation'
    attributes = ['duration']


class SendVideoNote(FileEndpoint, Thumb):
    file_type = 'video_note'
    attributes = ['duration', 'length']


class SendMediaGroup(TelegramEndpoint, DisableNotification, ReplyToMessageId):
    def __init__(self, chat_id, media_array):
        super().__init__()
        self.args = {
            'chat_id': chat_id,
            'media': [x.to_input_media() for x in media_array]
        }


class GetFile(TelegramEndpoint):
    # https://api.telegram.org/file/bot<token>/<file_path>
    def __init__(self, file_id):
        super().__init__()
        self.args = {
            'file_id': file_id
        }


class EditMessageCaption(TelegramEndpoint, Caption, ParseMode, ReplyMarkup, _ChatOrInlineMessage):
    def __init__(self, chat_or_inline_message_id, message_id):
        super().__init__()
        self.__chat_or_inline_message(chat_or_inline_message_id, message_id)


class EditMessageMedia(TelegramEndpoint, ReplyMarkup, _ChatOrInlineMessage):
    def __init__(self, chat_or_inline_message_id, message_id, media):
        super().__init__()
        self.args = {
            'media': media.to_input_media()
        }
        self.__chat_or_inline_message(chat_or_inline_message_id, message_id)
