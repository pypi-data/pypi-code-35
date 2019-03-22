# -*- coding: utf-8 -*-

from sanic.exceptions import SanicException


class FactureException(SanicException):
    def __init__(self, *args, **kwargs):
        self.log_message = kwargs.pop('write_log', False)

        super(FactureException, self).__init__(*args, **kwargs)
