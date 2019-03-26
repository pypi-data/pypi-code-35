import logging

from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from ol_commons.constants.http_codes import HTTP_403_FORBIDDEN
from ol_commons.constants.messages import SECURITY_UNAUTHORIZED_MSG
from ol_commons.errors import AppSecurityControllerError
from ol_commons.helpers import standard_response, get_auth_password

auth = HTTPBasicAuth()


@auth.get_password
def get_password(oauth_user):
    response = None

    try:
        logging.info('------------ INICIANDO PROCESO DE BASIC AUTHENTICATION ------------')
        logging.info('Obteniendo credenciales ingresadas')
        response = get_auth_password(oauth_user)
    except AppSecurityControllerError as e:
        logging.error('ERROR: Se encontro un error durante la ejecucion --->' + e.message)
    finally:
        logging.info('------------ FINALIZANDO PROCESO DE BASIC AUTHENTICATION ------------')
        return response


@auth.error_handler
def unauthorized():
    resp = standard_response(HTTP_403_FORBIDDEN, None, SECURITY_UNAUTHORIZED_MSG)
    return jsonify(resp)
