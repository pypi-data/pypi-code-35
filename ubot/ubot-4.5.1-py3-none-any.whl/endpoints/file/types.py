from abc import ABC

from libmediainfo_cffi import MediaInfo

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

    def read_metadata(self, json_lib=None):
        data = MediaInfo.read_metadata(self.file, Inform='JSON')

        if json_lib is None:
            import json
            _json = json
        else:
            _json = json_lib

        data = _json.loads(data)
        data_dict = {}
        for track in data['media']['track']:
            _type = track['@type']

            track_list = data_dict.get(_type, None)
            if track_list is None:
                track_list = []
                data_dict[_type] = track_list
            track_list.append(track)

        for attribute, _type, key in self.attributes:
            attribute_value = data_dict.get(_type, None)
            if attribute_value is None:
                continue

            attribute_value = attribute_value[0].get(key, None)
            if attribute_value is None:
                continue

            self.args[attribute] = attribute_value

        return self

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

    @staticmethod
    def _get_file_id(response):
        return response[-1]


class Audio(File, Caption, ParseMode, Thumb, ToInputMedia):
    file_type = 'audio'
    attributes = [
        ('duration', 'General', 'Duration'),
        ('performer', 'General', 'Performer'),
        ('title', 'General', 'Track')
    ]

    def duration(self, duration):
        self.args['duration'] = duration
        return self

    def performer(self, performer):
        self.args['performer'] = performer
        return self

    def title(self, title):
        self.args['title'] = title
        return self


class Document(File, Caption, ParseMode, Thumb, ToInputMedia):
    file_type = 'document'


class Video(File, Caption, ParseMode, Thumb, ToInputMedia):
    file_type = 'video'
    attributes = [
        ('duration', 'General', 'Duration'),
        ('width', 'Video', 'Width'),
        ('height', 'Video', 'Height')
    ]

    def supports_streaming(self):
        self.args['supports_streaming'] = True
        return self

    def duration(self, duration):
        self.args['duration'] = duration
        return self

    def width(self, width):
        self.args['width'] = width
        return self

    def height(self, height):
        self.args['height'] = height
        return self


class Animation(File, Caption, ParseMode, Thumb, ToInputMedia):
    file_type = 'animation'
    attributes = [
        ('duration', 'General', 'Duration'),
        ('width', 'Video', 'Width'),
        ('height', 'Video', 'Height')
    ]

    def duration(self, duration):
        self.args['duration'] = duration
        return self

    def width(self, width):
        self.args['width'] = width
        return self

    def height(self, height):
        self.args['height'] = height
        return self


class Voice(File, Caption, ParseMode):
    file_type = 'voice'
    attributes = [
        ('duration', 'General', 'Duration')
    ]

    def duration(self, duration):
        self.args['duration'] = duration
        return self


class VideoNote(File, Thumb):
    file_type = 'video_note'
    attributes = [
        ('duration', 'General', 'Duration'),
        ('length', ),
    ]

    def duration(self, duration):
        self.args['duration'] = duration
        return self

    def length(self, length):
        self.args['length'] = length
        return self
