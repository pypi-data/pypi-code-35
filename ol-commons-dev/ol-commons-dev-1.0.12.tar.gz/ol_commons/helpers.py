import os
import string
import requests
import json
import logging
import yaml
from ol_commons.constants.http_codes import HTTP_200_OK
from ol_commons.constants.messages import SECURITY_RESPONSE_MSG
from ol_commons.errors import AttributeControllerError, AppSecurityControllerError


def is_informational(code) -> bool:
    return 100 <= code <= 199


def is_success(code) -> bool:
    return 200 <= code <= 299


def is_redirect(code) -> bool:
    return 300 <= code <= 399


def is_client_error(code) -> bool:
    return 400 <= code <= 499


def is_server_error(code) -> bool:
    return 500 <= code <= 599


def standard_response(http_status, content, message) -> dict:
    response = {'status': http_status,
                'content': content,
                'message': message}
    return response


def get_attributes(str_attribute_name) -> dict:
    logging.info('Obteniendo listado de atributos generales con filtro de --> ' + str_attribute_name)
    json_in = None
    url = os.environ.get('URL_ATTRIBUTES_SERVICE') + '?str_attribute_name=' + str_attribute_name

    service_resp = requests.get(url, json=json_in)
    json_out = json.loads(service_resp.text)

    if json_out.get('status') is not HTTP_200_OK:
        raise AttributeControllerError(json_out.get('message'), json_out.get('status'))

    content = json_out.get('content')

    logging.info('Generando dictionario de atributos')
    result_dic = dict()

    if content is not None:
        attr_list = content.get('attributes')
        result_dic = dict([i.get('num_attr_member_id'), i.get('str_attr_member_value')] for i in attr_list)

    logging.info('Retornando listado de dictionario de atributos')

    return result_dic


def get_auth_password(user_auth) -> string:
    try:
        json_in = {'oauth_user': {'user': user_auth, 'password': None}}
        logging.info('Validando credenciales para usuario --> ' + user_auth)
        logging.info('Obteniendo password para usuario --> ' + user_auth)
        service_resp = requests.post(os.environ.get('URL_OAUTH_SECURITY_SERVICE'), json=json_in)

        if service_resp.status_code is not HTTP_200_OK:
            raise AppSecurityControllerError(service_resp.status_code)

        json_out = json.loads(service_resp.text)
        content = json_out.get('content')

        if content is None:
            raise AppSecurityControllerError(SECURITY_RESPONSE_MSG)

        oauth_user = content.get('oauth_user')

        if oauth_user is None:
            raise AppSecurityControllerError(SECURITY_RESPONSE_MSG)

        logging.info('Retornando password para usuario --> ' + user_auth)

        return oauth_user.get('str_oauth_cred_password')
    except requests.RequestException as e:
        raise AppSecurityControllerError(e)


def setup_logging(default_path='configs/logging.yaml', default_level=logging.DEBUG, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)

    if value:
        path = value
    if os.path.exists(path):
        logging.debug("Si existe archivo de configuracicon de logs")
        logging.info("Cargando configuracion para LOGS")
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
        logging.info("Definiendo nivel LOGS : " + default_level)
        logging.getLogger().setLevel(level=default_level)
    else:
        logging.debug("No existe archivo de configuracicon de logs")
        logging.info("Cargando configuracion para LOGS")
        logging.info("Definiendo nivel LOGS : " + default_level)
        logging.basicConfig(level=default_level)


def setup_application(default_config='DBA', flask_app=None):
    logging.info('Obteniendo configuraciones de la aplicacion para ' + default_config)
    json_in = None
    url = os.environ.get('URL_CONFIG_SERVER') + '/' + default_config

    service_resp = requests.get(url, json=json_in)
    result_dic = dict(json.loads(service_resp.text))

    logging.info('Cargando configuraciones a variables de entorno')

    for k, v in result_dic.items():
        logging.info('Variable --> k: ' + str(k) + ', v:' + str(v))
        os.environ[k] = v

    logging.info('Setting up configuraciones de BD')

    db_string_connection = str(os.environ.get('STRING_CONNECTION'))

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_string_connection.format(
        username=os.environ.get('DBUSERNAME'),
        password=os.environ.get('DBPASSWORD'),
        hostname=os.environ.get('DBHOSTNAME'),
        port=os.environ.get('DBPORT'),
        database=os.environ.get('DBNAME')
    )

    flask_app.config['SQLALCHEMY_ECHO'] = False
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    flask_app.config['SQLALCHEMY_POOL_SIZE'] = int(os.environ.get('DBPOOL_SIZE'))
    flask_app.config['SQLALCHEMY_POOL_TIMEOUT'] = int(os.environ.get('DBPOOL_TIMEOUT'))
    flask_app.config['SQLALCHEMY_RECORD_QUERIES'] = True
