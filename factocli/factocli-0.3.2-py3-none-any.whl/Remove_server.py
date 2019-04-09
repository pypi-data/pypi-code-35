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








def ask_path_to_remove_server():
    where_to_remove_prompt = {
        'type': 'input',
        'name': 'remove_path',
        'message': 'Where is factorio installed? # Usually in /opt/factorio',
    }
    answers = prompt(where_to_remove_prompt)
    return answers['remove_path']

def ask_to_really_remove_server(path):
    really_remove_server = {
        'type': 'confirm',
        'name': 'confirm_remove_server',
        'message': 'Are you sure you want to remove factorio in ' + path + " ? This will remove all the files in factorio directory including save files, mods, the factorio user ,group and factorio.service file in /etc/systemd/system/. Please don't interrupt the removing process",
    }
    answers = prompt(really_remove_server)
    return answers['confirm_remove_server']



def remove_server_directory(remove_path):
    print("Removing directory " + remove_path)
    shutil.rmtree(remove_path)
    if(os.path.isdir(remove_path)):
        print("Something went wrong removing the directory " + remove_path )
    elif(os.path.isdir(remove_path) == False):
        print("Directory removed")
        print("Proceeding with removing factorio user and group")
        stop_factorio_service_if_running()
        remove_user_and_group_factorio()


def remove_user_and_group_factorio():
    print("Removing factorio user and group")
    subprocess.run(['userdel', 'factorio'])
    # print("Removing factorio group")
    # subprocess.run(['groupdel', 'factorio'])
    print("Done")
    remove_factorio_service_file()


def stop_factorio_service_if_running():
    print("Stopping factorio service if running")
    subprocess.run(["systemctl", "stop", "factorio.service"])


def remove_factorio_service_file():
    service_file_path = "/etc/systemd/system/factorio.service"
    if(os.path.isfile(service_file_path)):
        print("Service File exists")
        print("Removing factorio service file in " + service_file_path)
        os.remove(service_file_path)
        if(os.path.isfile(service_file_path) == False):
            print("Factorio service file removed")
            remove_process_finished()
    elif(os.path.isfile(service_file_path) == False):
        print("No factorio service file found in /etc/systemd/system")
        print("Please remove your own service file")
        print("Proceeding with the removing process...")
        remove_process_finished()


def reload_daemon():
    #systemctl daemon-reload
    print("Reloading daemon")
    subprocess.run(["systemctl", "daemon-reload"])
    


def remove_process_finished():
    reload_daemon()
    print("Removing process is finished. Factorio server is removed")



def remove_server_main():
    remove_path = ask_path_to_remove_server()
    remove_path_factorio = remove_path[-8:]
    if(remove_path_factorio == 'factorio'):
        directory_exists = os.path.isdir(remove_path)
        if(directory_exists):
            print("Directory factorio exists")
            yesorno = ask_to_really_remove_server(remove_path)
            if(yesorno):
                print("Removing Process Started")
                remove_server_directory(remove_path)        
            else:
                print("Canceled")    
        else:
            print("The directory " + remove_path + " doesn't exist")
    else:
        print("There is no factorio name provided with the giving path")