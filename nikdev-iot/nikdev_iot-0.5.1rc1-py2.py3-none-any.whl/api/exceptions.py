# -*- coding: utf-8 -*-


class GetException(Exception):

    def __init__(self, message):
        super(GetException, self).__init__(message)


class PushException(Exception):

    retained_data = None
    """
    Whether or not the data was retained. If false the uploaded data is deleted.

    :type: bool
    """

    def __init__(self, message, retained_data):
        self.retained_data = retained_data
        super(PushException, self).__init__(message)