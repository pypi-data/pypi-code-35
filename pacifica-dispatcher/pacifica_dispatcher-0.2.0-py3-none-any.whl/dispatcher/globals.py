#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher: pacifica/dispatcher/globals.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE for details.
"""
Globals module.

Contains globals for the source of and event types of Pacifica
Events.
"""
CLOUDEVENTS_DEFAULT_EVENT_TYPE_ = 'org.pacifica.metadata.ingest'

CLOUDEVENTS_DEFAULT_SOURCE_ = '/pacifica/metadata/ingest'

__all__ = ('CLOUDEVENTS_DEFAULT_EVENT_TYPE_', 'CLOUDEVENTS_DEFAULT_SOURCE_', )
