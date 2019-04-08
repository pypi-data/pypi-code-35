#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import traceback
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse

from . import VoiceAssistant
from .constants import HOMEVEE_DIR
from .db_utils import get_database_con

CURRENT_VERSION = "0.0";

def check_for_updates():
    try:
        url = VoiceAssistant.SMART_API_PATH + "/?action=check_for_updates&current_version=" + urllib.parse.quote(CURRENT_VERSION.encode('utf8'))
        Logger.log(url)
        data = urllib.request.urlopen(url).read()
    except Exception as e:
        traceback.print_exc()
        data = None

def update_system():
    update_database()
    update_files()

def update_database():

    commands = []

    db = get_database_con()

    with db:
        cur = db.cursor()

        for command in commands:
            cur.execute(command)

    return

def update_files():
    #os.system("sudo rm -r "+HOMEVEE_DIR)

    #Neue Homevee-Version mit "git clone" herunterladen
    #os.chdir(os.path.dirname(HOMEVEE_DIR))

    #HOMEVEE_REPOSITORY = 'https://bitbucket.org/smarthomeblogger/shacos.git'

    #os.system("sudo git clone " + HOMEVEE_REPOSITORY)

    #os.system("sudo reboot")
	
	return