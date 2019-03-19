# -*- coding: utf-8 -*-
from aws_lambda_sls.package import AppBuilder


class AppDeployer(AppBuilder):
    def __init__(self, app, os_utils, ui, stage, client):
        super(AppDeployer, self).__init__(app, os_utils, ui, stage)
        self._client = client

    def validate(self, **params):
        if not params.get("role_arn"):
            raise ValueError("Aws role must be define!")

    def deploy_app(self, deploy_file=None, s3_key=None):
        if s3_key:
            self._ui.write("Direct deploy from s3 key: %s\n" % s3_key)
        else:
            s3_key = self.gen_s3_key_from_deploy_file(deploy_file)
            self._client.put_object(
                self.s3_bucket, s3_key,
                self._os_utils.get_file_contents(deploy_file, binary=True)
            )
            self._ui.write("Upload deploy file to s3 key: %s\n" % s3_key)
        lf = self.create_lambda_function()
        params = {
            'function_name': lf.function_name,
            'role_arn': lf.role,
            's3_code': {
                "S3Bucket": self.s3_bucket,
                "S3Key": s3_key
            },
            'runtime': lf.runtime,
            'handler': lf.handler,
            'environment_variables': lf.environment,
            'tags': lf.tags,
            'timeout': lf.timeout,
            'memory_size': lf.memory_size,
            'security_group_ids': lf.security_group_ids,
            'subnet_ids': lf.subnet_ids,
        }
        self.validate(**params)
        self._ui.write("Waiting for stack create/update to complete\n")
        if self._client.lambda_function_exists(lf.function_name):
            execute_func = self._client.update_function
            del params["handler"]
        else:
            execute_func = self._client.create_function
        execute_func(**params)
        self._ui.write("Successfully created/updated function: %s\n" % lf.function_name)


__all__ = [
    "AppDeployer",
]
