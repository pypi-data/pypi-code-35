from abc import ABC

from .commons import Caption
from ..commons import ParseMode
from ...utils import MultipartEncoder, random_string


class File(ABC):
    file_type = None
    attributes = []
    cache = {}

    def __init__(self, file, is_path=True, **kwargs):
        # cache is a dict {file_path: file_id} and should be updated with the trigger callback
        self.args = {}
        self.file = file

        if is_path is True:
            file_id = self.cache.get(self.file, None)
            if file_id is not None:
                self.method = 'GET'
                self.value = file_id
            else:
                self.method = 'POST'
                self.calls_before_get = 1
                self.value = [MultipartEncoder.encode_file(self.file_type, self.file)]
        else:
            self.method = 'GET'
            self.value = self.file

        if kwargs:
            for key, value in kwargs.items():
                method = getattr(self, key)
                method(value)

    def with_cache(self):
        if self.calls_before_get == -1:
            return self

        if self.calls_before_get != 0:
            self.calls_before_get = 0
            return self

        file_id = self.cache.get(self.file, None)
        self.calls_before_get = -1

        if file_id is not None:
            self.method = 'GET'
            self.value = file_id

        return self

    @staticmethod
    def _get_file_id(response):
        return response

    def update_cache(self, response, index=None):
        file_id = self.cache.get(self.file, None)
        if file_id is None:
            _res = response['result']
            if index is not None:
                _res = _res[index][self.file_type]
            else:
                _res = _res[self.file_type]

            self.cache[self.file] = self._get_file_id(_res)['file_id']


class ToInputMedia:
    media_types = ['photo', 'video']

    def to_input_media(self):

        serialized = {
            'type': self.file_type,
            **self.args
        }

        if self.method == 'POST':
            files = []
            for file in self.value:
                field_name = random_string()
                if file[0] in self.media_types:
                    serialized['media'] = f'attach://{field_name}'
                else:
                    serialized[file[0]] = f'attach://{field_name}'
                files.append((field_name, file[1], file[2], file[3]))
            return serialized, files
        else:
            serialized['media'] = self.value
            return serialized, None


class Thumb:
    def thumb(self, thumb):
        # thumb must be a path
        if self.method == 'POST':
            self.value.append(MultipartEncoder.encode_file('thumb', thumb))
        return self


class Photo(File, Caption, ParseMode, ToInputMedia):
    file_type = 'photo'
    serialized_fields = ['caption', 'parse_mode']

    @staticmethod
    def _get_file_id(response):
        return response[-1]


class Audio(File, Caption, ParseMode, Thumb, ToInputMedia):
    file_type = 'audio'
    attributes = ['duration', 'performer', 'title']
    serialized_fields = ['caption', 'parse_mode', 'thumb']


class Document(File, Caption, ParseMode, Thumb, ToInputMedia):
    file_type = 'document'
    serialized_fields = ['caption', 'parse_mode', 'thumb']


class Video(File, Caption, ParseMode, Thumb, ToInputMedia):
    file_type = 'video'
    attributes = ['duration', 'width', 'height']
    serialized_fields = ['caption', 'parse_mode', 'thumb', 'supports_streaming']

    def supports_streaming(self):
        self.args['supports_streaming'] = True
        return self


class Animation(File, Caption, ParseMode, Thumb, ToInputMedia):
    file_type = 'animation'
    attributes = ['duration', 'width', 'height']
    serialized_fields = ['caption', 'parse_mode', 'thumb']


class Voice(File, Caption, ParseMode):
    file_type = 'voice'
    attributes = ['duration']


class VideoNote(File, Thumb):
    file_type = 'video_note'
    attributes = ['duration', 'length']
