import getpass
from clint import resources
from clint.textui import prompt, validators
import re

from dccli.error_codes import *
from dccli.utils import *


def get_login_token():
    token = resources.user.read(TEMP_AUTH_TOKEN)
    if token is None:
        return None

    return TokenAuth(token)


class Login(BaseCase):
    welcome = "Login to DeepCluster"

    def execute(self, FLAGS):
        email = prompt.query("Please enter your email:")
        password = getpass.getpass("Please enter your password:")

        data = {
            'email': email,
            'password': password
        }

        return self.login(data)

    def login(self, data):
        server_url = "{}/api/v1/user/login/".format(self.master_endpoint)
        result, response, response_data, error = request_server(server_url, "post", data=data)
        if not result:
            if not response:
                console_out_error("Error: {}".format(error))
                return MASTER_FAILURE
            elif response.status_code == 401:
                console_out_error("Error: Unknown email/password combination")
                return LOGIN_NEED_REGISTER
            else:
                console_out_error("Error: {}".format(error))
                return MASTER_FAILURE
        elif response_data is None or 'auth_token' not in response_data:
            console_out_error("Error: Malformed response from server")
            return MASTER_FAILURE

        auth_token = response_data.get('auth_token')
        resources.user.write(TEMP_AUTH_TOKEN, auth_token)
        console_out_success("Login successfully")
        return SUCCESS


class Register(BaseCase):
    welcome = "Register with DeepCluster"

    def execute(self, FLAGS):
        email = prompt.query("Please enter your email address:")
        console_out_info(
            "Password must be 8 - 20 characters and can contain alphanumeric and @#$%^&+=")
        password = getpass.getpass("Please enter your password: ")
        password_re = re.compile('^[A-Za-z0-9@#$%^&+=]{8,20}$')
        if not password_re.match(password):
            console_out_error("Error: Password invalid")
            return USER_INPUT_ERROR

        re_password = getpass.getpass("Please re-enter your password: ")

        if password != re_password:
            console_out_error("Error: Passwords do not match")
            return USER_INPUT_ERROR

        data = {
            'email': email,
            'password': password
        }

        return self.register(data)

    def register(self, data):
        server_url = "{}/api/v1/user/register/".format(self.master_endpoint)
        result, response, _, error = request_server(server_url, "post", data=data)
        if not result:
            if not response:
                console_out_error("Error: {}".format(error))
                return MASTER_FAILURE
            else:
                console_out_error("Error: {}".format(error))
                return MASTER_FAILURE
        else:
            console_out_success("Registered successfully")
            log_in_case = Login(self.master_endpoint)
            log_in_case.login(data)
            return SUCCESS
