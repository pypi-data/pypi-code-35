#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import traceback
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import random

import homevee.VoiceAssistant
from homevee.VoiceAssistant import helper
from homevee.VoiceAssistant.voice_patterns import PATTERN_JOKE


def get_pattern(db):
    return PATTERN_JOKE

def get_label():
    return "joke"

def run_command(username, text, context, db):
    return get_joke(username, text, context, db)

def get_joke(username, text, context, db):
    try:
        url = helper.SMART_API_PATH + "/?action=joke&text=" + urllib.parse.quote(text.encode('utf8'))
        Logger.log(url)
        data = urllib.request.urlopen(url).read()
    except Exception as e:
        traceback.print_exc()
        data = None

    if data is not None:
        return {'msg_speech': data, 'msg_text': data}
    else:
        result = get_error()
        return {'msg_speech': result, 'msg_text': result}

def get_error():
    return random.choice([
        'Mir fällt gerade kein Witz ein.'
    ])