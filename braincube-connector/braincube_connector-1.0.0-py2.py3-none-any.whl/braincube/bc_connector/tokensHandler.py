import json as __json
import os
import re as __research
import webbrowser

import requests
from flask import Flask as __Flask, send_from_directory, render_template
from flask import redirect
from flask import request
from flask_cors import CORS as __CORS
from flask_cors import cross_origin
from gevent import pywsgi

from braincube.bc_connector.braincube_requests import get_sso_token
from braincube.bc_connector.config_handler import get_client_id, get_client_secret

file_path = os.path.expanduser('~/.braincube') + '/OAuth2AccessToken'

__app = __Flask(__name__)
__app.config['CORS_HEADERS'] = 'Content-Type'
__cors = __CORS(__app, resources={r"/*": {"origins": "https://mybraincube.com/*"}})

cert_file = os.path.expanduser('~/.braincube/cert.pem')
key_file = os.path.expanduser('~/.braincube/key.pem')

http_server = pywsgi.WSGIServer(('localhost', 5000), __app, certfile=cert_file, keyfile=key_file)

authorize_uri = "https://mybraincube.com/sso-server/vendors/braincube/authorize.jsp"
token_uri = "https://mybraincube.com/sso-server/ws/oauth2/token"
redirect_uri = "https://localhost:5000/token"

scopes = "BASE%20API"


@__app.route('/')
@cross_origin()
# Code executed when launching the local server
# Opens the Braincube authorization page or the React page according to the parameter passed in query
def launch_connector():
    url = authorize_uri \
          + '?client_id=' + get_client_id() \
          + '&response_type=code' \
          + '&scope=' + scopes \
          + '&redirect_uri=' + redirect_uri
    print("url " + url)
    return redirect(url)  # -> /token


@__app.route('/token')
@cross_origin()
# Code executed when returning from the Braincube authorization page
# Allows to recover a token thanks to the received code
def get_token_from_code():
    code = __research.search('code=(.*)', request.url).group(1)
    content = {"grant_type": "authorization_code",
               "code": code,
               "redirect_uri": redirect_uri,
               "client_id": get_client_id(),
               "client_secret": get_client_secret()
               }
    print("Pending recovery attempt, please wait")
    retrieve_token = requests.post(token_uri, data=content)
    global TOKEN  # The only way to return a result from a flask app
    TOKEN = __json.loads(retrieve_token.text)['access_token']
    return render_template("closing.html")


@__app.route('/closing')
@cross_origin()
def closing():
    shutdown_server()
    return "server closed"


def shutdown_server():
    """ Close the local server"""
    print("Shutting down the local serveur.")
    http_server.close()


def retrieve_tokens(oauth2_acces_token=None):
    """ Try to get an sso token from an OAuth2 access token"""
    sso_token = None
    if oauth2_acces_token is not None:  # if we have a specified token
        print("Trying with specified oauth2 access token")
        sso_token = get_sso_token(oauth2_acces_token)
    if sso_token is None:
        print("Trying with locally saved oauth2 access token")
        oauth2_acces_token = read_local_oauth_access_token()  # Try to read local written token
        sso_token = get_sso_token(oauth2_acces_token)
    if sso_token is None:
        print("Trying by calling SSO to acquire an oauth2 access token ")
        oauth2_acces_token = get_token_from_web()  # Retrieve a token from web
        sso_token = get_sso_token(oauth2_acces_token)
    return oauth2_acces_token, sso_token


def get_token_from_web():
    """ Redirect to the sso server to get an oauth2 token """
    webbrowser.open('https://localhost:5000/')
    try:
        http_server.serve_forever()

    except OSError:
        print('The port 5000 of the machine is already open, please close your activity before restarting it')
    token = TOKEN
    write_local_oauth_access_token(token)
    return token


def read_local_oauth_access_token():
    """ Try to read the OAuth access token on disk """
    if os.path.isfile(file_path):
        with open(file_path) as token:
            return token.read()


def write_local_oauth_access_token(sso_token):
    """ write the OAuth access token on disk """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as outfile:
        outfile.write(sso_token)
