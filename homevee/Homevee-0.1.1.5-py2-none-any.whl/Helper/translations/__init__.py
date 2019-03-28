#!/usr/bin/env python
# -*- coding: utf-8 -*-
from homevee import constants
from homevee.Helper.translations import german

LANGUAGE = "en"
#LANGUAGE = "de"

def translate(key, language=None):
    translations = {
        'en': get_translations(),
        'de': german.get_translations()
    }

    if language is None or language not in translations:
        language = LANGUAGE

    return translations[language][key]

def get_translations():
    translations = {
        'no_users_create_admin': "You have not created any users yet.\nYou can create an administrator-account now.",
        'enter_password': 'Please enter a password: ',
        'password_dont_match': 'The given passwords dont match',
        'enter_username': 'Please enter a username: ',
        'your_remote_id_is': 'Your remote-id is: ',
        'homevee_server_started': "Homevee-Server (Version: "+constants.HOMEVEE_SERVER_VERSION+") has been started..."
    }
    return translations