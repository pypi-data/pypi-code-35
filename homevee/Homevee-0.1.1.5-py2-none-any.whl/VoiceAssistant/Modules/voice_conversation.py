#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import traceback
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse

import homevee.VoiceAssistant
from homevee.Helper import translations
from homevee.VoiceAssistant import helper
from homevee.VoiceAssistant.helper import generate_string

GREETINGS = ['hallo', 'hey', 'na', 'hi']

THANKS = ['danke', 'dank', 'dankeschön']

def get_pattern(db):
    return []

def get_label():
    return "conversation"

def run_command(username, text, context, db):
    return conversation(username, text, context, db)

def conversation(username, text, context, db):
    url = helper.SMART_API_PATH + "/?action=plaintext&language="+translations.LANGUAGE+"&text="+urllib.parse.quote(codecs.encode(text, 'utf-8'))
    #print url
    output = urllib.request.urlopen(url).read()

    #print(url)

    #print(output)

    if output is None or output == '':
        data = [
            [[['Es ', 'tut '], 'Tut '], 'mir ', ['echt ', 'sehr ', ''], ['Leid. ', 'Leid, '+username+'. '],
            ['Da ', 'Dabei ', 'Damit '], 'kann ', 'ich ', 'dir ', ['leider ', ''], ['noch ', ''], 'nicht ', ['helfen', 'weiterhelfen'], '.']
        ]
        output = generate_string(data)

    output = output.decode("utf-8")

    result = {'msg_speech': output, 'msg_text': output}

    return result

def contains(text, array):
    words = text.split(' ')

    for item in array:
        if item in words:
            return True

    return False

def get_label():
    return "conversation"