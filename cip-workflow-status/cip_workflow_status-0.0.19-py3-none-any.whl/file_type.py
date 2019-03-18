from enum import Enum


class FileType(Enum):
    VIDEO = 0
    THUMBNAIL = 1
    SUBTITLE = 2

    TYPE_TO_STR = [
        'video',
        'thumb',
        'subtitle'
    ]

    NAME_TO_FRIENDLY_SRT = [
        'video',
        'thumbnail',
        'legenda'
    ]

    def to_friendly_string(self):
        return FileType.NAME_TO_FRIENDLY_SRT.value[self.value]

    @staticmethod
    def string_to_friendly_string(status_string):
        job_status = FileType.TYPE_TO_STR.value.index(status_string)
        return FileType.NAME_TO_FRIENDLY_SRT.value[job_status]

    def to_string(self):
        return FileType.TYPE_TO_STR.value[self.value]

    @staticmethod
    def from_string(status_string):
        return FileType(FileType.TYPE_TO_STR.value.index(status_string))