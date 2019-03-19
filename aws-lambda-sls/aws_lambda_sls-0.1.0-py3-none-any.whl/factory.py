import warnings
import importlib
from aws_lambda_sls.package import *
from aws_lambda_sls.deploy import *
from aws_lambda_sls.utils import UI, OSUtils
from aws_lambda_sls.awsclient import AWSClient
from aws_lambda_sls.local import LocalDevServer
from aws_lambda_sls.constants import *
from boto3.session import Session


def create_aws_session(aws_params=None, profile=None):
    return Session(profile_name=profile, **aws_params or {})


class CLIFactory(object):
    def __init__(self, project_dir, os_utils=None, debug=False, profile=None, environ=None):
        self.project_dir = project_dir
        self.debug = debug
        self.profile = profile
        if environ is None:
            environ = dict(os.environ)
        self._environ = environ
        self._os_utils = os_utils
        if not self._os_utils:
            self._os_utils = OSUtils()

    def create_app_packager(self, stage="dev", force_download=False):
        ui, os_utils, app = UI(), OSUtils(), self.load_app()
        pip_runner = PipRunner(
            pip=SubprocessPip(os_utils=os_utils),
            osutils=os_utils
        )
        dependency_builder = PipDependencyBuilder(
            osutils=os_utils, ui=ui,
            pip_runner=pip_runner,
            force_download=force_download
        )
        return AppPackager(
            app, os_utils, ui, stage, SAMTemplateGenerator(),
            LambdaDeploymentPackager(app, os_utils, dependency_builder, ui)
        )

    def create_app_deployer(self, stage="dev", profile=None):
        return AppDeployer(
            self.load_app(),
            OSUtils(),
            UI(),
            stage,
            AWSClient(create_aws_session(profile=profile))
        )

    def create_local_server(self, app_obj, host, port, stage):
        return LocalDevServer(app_obj, host, port, stage)

    def create_deploy_file(self, project_dir):
        return self._os_utils.joinpath(
            project_dir,
            DEFAULT_PACKAGE_DIST,
            DEFAULT_PACKAGE_FILE
        )

    def create_deploy_directory(self, project_dir, out, recreate=True):
        directory = self._os_utils.joinpath(project_dir, out)
        if recreate:
            self._os_utils.recreate_dir(directory)
        return directory

    def generate_requirement_file(self):
        SubprocessRequire(os_utils=self._os_utils).main()

    def load_app(self, project_dir=None):
        if not project_dir:
            project_dir = self.project_dir
        if project_dir not in sys.path:
            sys.path.insert(0, project_dir)
        vendor_dir = os.path.join(project_dir, 'vendor')
        if os.path.isdir(vendor_dir) and vendor_dir not in sys.path:
            sys.path.append(vendor_dir)
        try:
            app_module = importlib.import_module('app')
            app = getattr(app_module, 'app')
            app.root_path = project_dir
        except SyntaxError as e:
            message = (
                          'Unable to import your app.py file:\n\n'
                          'File "%s", line %s\n'
                          '  %s\n'
                          'SyntaxError: %s'
                      ) % (getattr(e, 'filename'), e.lineno, e.text, e.msg)
            raise RuntimeError(message)
        return app


def validate_python_version(actual_py_version=None):
    lambda_version = REQUIRE_PYTHON_VERSION
    if actual_py_version is None:
        actual_py_version = 'python%s.%s' % sys.version_info[:2]
    if actual_py_version != lambda_version:
        warnings.warn("You are currently running %s, but the closest "
                      "supported version on AWS Lambda is %s\n"
                      "Please use %s, otherwise you may run into "
                      "deployment issues. " %
                      (actual_py_version, lambda_version, lambda_version),
                      stacklevel=2)
