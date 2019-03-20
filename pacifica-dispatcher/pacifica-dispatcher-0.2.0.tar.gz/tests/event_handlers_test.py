#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher: tests/event_handlers_test.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE for details.
"""Test event handlers."""
import unittest

from cloudevents.constants import SPEC_VERSION
from cloudevents.model import Event

from pacifica.dispatcher.event_handlers import NoopEventHandler
from pacifica.dispatcher.globals import CLOUDEVENTS_DEFAULT_EVENT_TYPE_, CLOUDEVENTS_DEFAULT_SOURCE_


class NoopEventHandlerTestCase(unittest.TestCase):
    """Test the noop event handler."""

    def test_event_handler(self):
        """Verify the noop event handler does nothing."""
        event = Event({
            'cloudEventsVersion': SPEC_VERSION,
            'eventID': 'ID',
            'eventType': CLOUDEVENTS_DEFAULT_EVENT_TYPE_,
            'source': CLOUDEVENTS_DEFAULT_SOURCE_,
            'data': [],
        })

        event_handler = NoopEventHandler()
        event_handler.handle(event)
        self.assertTrue(event_handler)


if __name__ == '__main__':
    unittest.main()
