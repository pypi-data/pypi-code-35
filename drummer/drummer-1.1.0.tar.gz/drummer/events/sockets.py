#!/usr/bin/python3
# -*- coding: utf-8 -*-
from drummer.foundation.messages import Response, StatusCode, FollowUp

class SocketTestEvent:
    """ simple event to check socket connection """

    def __init__(self, config):

        self.config = config


    def execute(self, request):

        config = self.config

        response = Response()

        follow_up = FollowUp(None)

        try:
            response.set_status(StatusCode.STATUS_OK)

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)

        return response, follow_up
