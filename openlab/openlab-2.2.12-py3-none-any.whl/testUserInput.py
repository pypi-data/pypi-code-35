import os
import inspect
import time
import json

import keyring

service = 'openlab_prod'
default_username = 'testOpenLabUser'
username = 'andrew'

actual_email = "a.holsaeter@gmail.com"
actual_api_key = "ABF17DFB6AB178674A95F60DDB276EDF855362B58D9CD498E1B2CB21E62B56A5"

def request_user_credentials():
    """
    Asks user for email and api_key
    """
    print("email: ")
    name = input()
    print("api_key:")
    api_key = input()
    keyring.set_password(service, name, api_key)
    return [name, api_key]

def get_keyring_username(service, username):
    #Treating username like a password
    email = keyring.get_password(service, username)
    if email is None:
        print("No OpenLab username exists yet. Input email:")
        email = input()
        keyring.set_password(service, username, email)
        return email
    else:
        return email

#get email address since we treat it like a password
email = get_keyring_username(service, default_username)

print("email is: {}".format(email))

#get actual password
password = keyring.get_password(service, email)

if password is None:
    credentials = request_user_credentials()
    print(credentials)
else:
    print("Keyring existed: {}".format(password))