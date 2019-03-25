# -*- coding=utf-8
from .helper import get_code_msg


class PaperlessException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


def get_error_msg(data):
    """获取错误code与描述"""
    try:
        code, msg, _ = get_code_msg(data)
        return code, msg
    except Exception:
        return "", "Response Error Msg Is INVALID"


class PaperlessClientError(PaperlessException):
    """PaperlessClient端错误"""

    def __init__(self, message):
        PaperlessException.__init__(self, message)


class PaperlessosServiceError(PaperlessException):
    """Paperless Server端错误，可以获取特定的错误信息"""

    def __init__(self, message):
        self._origin_msg = message
        code, msg = get_error_msg(message)
        self._error_msg = msg
        self._error_code = code

    def get_origin_msg(self):
        """获取原始的XML格式错误信息"""
        return self._origin_msg

    def get_error_msg(self):
        """获取经过处理的dict格式的错误信息"""
        return self._error_msg

    def get_error_code(self):
        """获取error code"""
        return self._error_code
