from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
from examples import custom_style_1
from examples import custom_style_2
from examples import custom_style_3
from pprint import pprint
import os, errno
import wget
import urllib.request
import shutil
from pathlib import Path
import subprocess







def ask_path_to_update_server():
    path_to_update_server = {
        'type': 'input',
        'name': 'update_path',
        'message': 'Where is factorio installed? ',
    }
    answers = prompt(path_to_update_server)
    return answers['update_path']


def confirm_where_to_update_server(path):
    confirm_where_to_update = {
        'type': 'confirm',
        'name': 'confirm_where_to_update',
        'message': 'Are you sure you want to update factorio in ' + path + " ?",
    }
    answers = prompt(confirm_where_to_update)
    return answers['confirm_where_to_update']



def update_main():
    update_path = ask_path_to_update_server()
    print(update_path)
    yesorno = confirm_where_to_update_server(update_path)
    if(yesorno):
        print("Aright updating factorio")
    if(yesorno == False):
        print("please try again")