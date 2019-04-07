import subprocess
from lib_pipeline.docker import Docker
from lib_pipeline.singleton import Singleton
from lib_pipeline.helpers import execute, remove_files


class Terraform(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.docker = Docker()

    def exec(self, command, options='', cwd=None, env_args=''):
        options = " ".join(options)
        return execute(
            f"""terraform {command} {env_args} {options}""",
            cwd,
        )

    def init(self, bucket, region, environment, backend_config='', cwd=None, env_args=''):
        self.exec("init", options=backend_config, cwd=cwd, env_args=env_args)

    def plan(self, region, environment, options, cwd=None, env_args=''):
        vars = [
            f"""--var-file="{environment}/{region}.tfvars" """,
            f"""--var="profile={environment}" {options} """,
        ]
        self.exec("plan", options=vars, cwd=cwd, env_args=env_args)

    def apply(self, region, environment, options, cwd=None, env_args=''):
        vars = [
            f"""--var-file="{environment}/{region}.tfvars" """,
            f"""--var="profile={environment}" {options} """,
            "--auto-approve",
        ]
        self.exec("apply", options=vars, cwd=cwd, env_args=env_args)

    def taint(self, bucket, region, environment, *args, backend_config='', cwd=None, env_args=''):
        options = " ".join(args)
        self.init(bucket, region, environment, options, backend_config=backend_config, cwd=cwd, env_args=env_args)
        self.plan(region, environment, options, cwd=cwd, env_args=env_args)
        self.exec("taint", options=options, cwd=cwd, env_args=env_args)

    def deploy(self, bucket, region, environment, *args, backend_config='', cwd=None, env_args=''):
        options = " ".join(args)
        remove_files(".terraform", cwd=cwd)
        self.init(bucket, region, environment, backend_config=backend_config, cwd=cwd, env_args=env_args)
        self.plan(region, environment, options, cwd=cwd, env_args=env_args)
        self.apply(region, environment, options, cwd=cwd, env_args=env_args)