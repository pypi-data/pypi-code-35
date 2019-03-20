#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher: pacifica/dispatcher/exceptions.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE for details.
"""
Exceptions module.

This module contains specific exceptions that can happen during the
dispatching process.
"""
from cloudevents.model import Event

from .globals import CLOUDEVENTS_DEFAULT_EVENT_TYPE_, CLOUDEVENTS_DEFAULT_SOURCE_


class EventError(BaseException):
    """
    Base event dispatcher error class.

    This the base event class used by all other error classes.
    """

    def __init__(self, event: Event) -> None:
        """Save the event for later use."""
        super(EventError, self).__init__()

        self.event = event


class InvalidEventTypeValueError(EventError):
    """
    Invalid event type error.

    This error is raised when events are received that have an
    invalid ``event_type`` attribute.
    """

    def __str__(self) -> str:  # pragma: no cover
        """Stringify the invalid type."""
        return 'field \'event_type\' is invalid (expected: \'{0}\')'.format(
            CLOUDEVENTS_DEFAULT_EVENT_TYPE_.replace('\'', '\\\''))


class InvalidSourceValueError(EventError):
    """
    Invalid event source error.

    This error is raised when events are received that have an
    invalid ``source`` attribute.
    """

    def __str__(self) -> str:  # pragma: no cover
        """Stringify the invalid source."""
        return 'field \'source\' is invalid (expected: \'{0}\')'.format(
            CLOUDEVENTS_DEFAULT_SOURCE_.replace('\'', '\\\''))


class TransactionDuplicateAttributeError(EventError):
    """
    Duplicate event error.

    Events can be sent multiple times, this error is raised if a
    transaction event has already been seen.
    """

    def __init__(self, event: Event, name: str) -> None:
        """Add the name of the event as well."""
        super(TransactionDuplicateAttributeError, self).__init__(event)

        self.name = name

    def __str__(self) -> str:  # pragma: no cover
        """Stringify the duplicate transaction."""
        return 'field \'Transactions.{0}\' is already defined'.format(self.name.replace('\'', '\\\''))


__all__ = ('EventError', 'InvalidEventTypeValueError',
           'InvalidSourceValueError', 'TransactionDuplicateAttributeError', )
