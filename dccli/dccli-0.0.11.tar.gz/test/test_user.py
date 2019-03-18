import uuid
from os.path import join, dirname

from dccli.error_codes import SUCCESS
from dccli.user import Register, Login
from test.test_common import test_config
from clint import resources

master_endpoint = test_config["master_endpoint"]
job_uuid = test_config["job_uuid"]
output_path = join(dirname(__file__), "test_out")

resources.init('DeepCluster', 'dccli')


def test_register_user():
    register_case = Register(master_endpoint)

    rand_email = f"{str(uuid.uuid4())[0:8]}@uw.edu"
    user_data = {
        'email': rand_email,
        'password': test_config["password"]
    }

    assert register_case.register(user_data) == SUCCESS


def test_login_user():
    login = Login(master_endpoint)
    user_data = {
        'email': test_config["email"],
        'password': test_config["password"]
    }

    assert login.login(user_data) == SUCCESS
