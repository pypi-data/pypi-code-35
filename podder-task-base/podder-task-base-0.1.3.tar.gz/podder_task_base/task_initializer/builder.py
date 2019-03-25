import click
from stat import S_IRWXU, S_IRGRP, S_IXGRP, S_IROTH, S_IXOTH

from podder_task_base.task_initializer.builders import FilecopyBuilder
from podder_task_base.task_initializer.builders import MkdirBuilder
from podder_task_base.task_initializer.builders import GrpcTaskBuilder


class Builder(object):
    CHMOD755 = S_IRWXU | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH

    def __init__(self, target_dir: str, task_name: str) -> None:
        self.target_dir = target_dir
        self.task_name = task_name

    def init_task(self) -> None:
        builders = [
            [MkdirBuilder   , 'config'                             , None],
            [MkdirBuilder   , 'input'                              , None],
            [MkdirBuilder   , 'output'                             , None],
            [MkdirBuilder   , 'tmp'                                , None],
            [MkdirBuilder   , 'error'                              , None],
            [FilecopyBuilder, 'requirements.default.txt'           , None],
            [FilecopyBuilder, 'pytest.ini'                         , None],
            [FilecopyBuilder, 'run_codegen.py'                     , self.CHMOD755],
            [MkdirBuilder   , 'scripts'                            , None],
            [FilecopyBuilder, 'scripts/entrypoint.sh'              , self.CHMOD755],
            [FilecopyBuilder, 'scripts/pre-commit.sh'              , self.CHMOD755],
            [FilecopyBuilder, 'scripts/restart_grpc_server.sh'     , self.CHMOD755],
            [MkdirBuilder   , 'api'                                , None],
            [FilecopyBuilder, 'api/__init__.py'                    , None],
            [GrpcTaskBuilder, 'api/task_api.py'                    , self.task_name],
            [GrpcTaskBuilder, 'api/grpc_server.py'                 , self.task_name],
            [MkdirBuilder   , 'api/protos'                         , None],
            [FilecopyBuilder, 'api/protos/__init__.py'             , None],
            [GrpcTaskBuilder, 'api/protos/pipeline_framework.proto', self.task_name],
        ]
        self._build(
            builders=builders)

    def _build(self, builders: list) -> None:
        for builder, file, option in builders:
            builder().execute(self.target_dir, file, option)
        click.secho("{} : Completed successfully!".format(file), fg='green')
