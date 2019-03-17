from os.path import join, dirname, exists

from dccli.error_codes import SUCCESS
from dccli.job import Submit, Download, CheckProgress, StreamLog
from dccli.user import Register, Login
from test.test_common import test_config, clean_up_login_token, s3_client
from test.test_user import test_login_user

_master_endpoint = test_config["master_endpoint"]
_output_path = join(dirname(__file__))

register = Register(_master_endpoint)
user_data = {
    'email': test_config["email"],
    'password': test_config["password"]
}
register.register(user_data)

# start a new login
clean_up_login_token()
login = Login(_master_endpoint)
login.login(user_data)

_job_uuid = None
_test_maker = join(dirname(__file__), 'testmarker')


def test_end2end_submit():
    test_login_user()

    class DummyFlag:
        c = True

    submit_case = None
    try:
        submit_case = Submit(_master_endpoint)
        assert submit_case.execute(DummyFlag()) == SUCCESS
    finally:
        print(submit_case.job_uuid)
        _job_uuid = submit_case.job_uuid
        with open(_test_maker, 'w') as f:
            f.write(_job_uuid)

        if submit_case is not None and _job_uuid is not None:
            s3_client.s3_delete_by_key(bucket=test_config["s3_bucket_name"], s3_folder=_job_uuid, key=None)


def test_download_output():
    if not exists(_test_maker):
        test_end2end_submit()

    with open(_test_maker, 'r') as f:
        _job_uuid = f.read()

    class DummyFlag:
        job_uuid = _job_uuid
        dest = _output_path

    download_case = Download(_master_endpoint)
    print(DummyFlag.job_uuid)
    assert download_case.execute(DummyFlag) == SUCCESS


def test_check_progress():
    if not exists(_test_maker):
        test_end2end_submit()

    with open(_test_maker, 'r') as f:
        _job_uuid = f.read()

    class DummyFlag:
        job_uuid = _job_uuid

    progress_case = CheckProgress(_master_endpoint)
    assert progress_case.execute(DummyFlag) == SUCCESS


def test_stream_log():
    if not exists(_test_maker):
        test_end2end_submit()

    with open(_test_maker, 'r') as f:
        _job_uuid = f.read()

    class DummyFlag:
        job_uuid = _job_uuid

    log_case = StreamLog(_master_endpoint)
    assert log_case.execute(DummyFlag) == SUCCESS
