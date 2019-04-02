import click
import shutil
from pathlib import Path
from stat import S_IRWXU, S_IRGRP, S_IXGRP, S_IROTH, S_IXOTH

from podder_task_base.task_initializer.builders import FilecopyBuilder
from podder_task_base.task_initializer.builders import MkdirBuilder
from podder_task_base.task_initializer.builders import TaskNameBuilder


class Builder(object):
    CHMOD755 = S_IRWXU | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH

    def __init__(self, task_name: str, target_dir: str) -> None:
        this_dir = Path(__file__).resolve().parent
        self.templates_dir = str(this_dir.joinpath("templates").resolve())
        self.target_dir = target_dir
        self.task_name = task_name
        if Path(target_dir).exists():
            shutil.rmtree(target_dir)

    def init_task(self) -> None:
        shutil.copytree(self.templates_dir, self.target_dir,
            ignore=shutil.ignore_patterns('__pycache__'))

        for path in Path(self.target_dir + "/scripts").glob("*.sh"):
            path.chmod(self.CHMOD755)

        builders = [
            [TaskNameBuilder, 'task_name.ini'                      , self.task_name],
            [TaskNameBuilder, 'api/task_api.py'                    , self.task_name],
            [TaskNameBuilder, 'api/grpc_server.py'                 , self.task_name],
            [TaskNameBuilder, 'api/protos/pipeline_framework.proto', self.task_name],
        ]
        self._build(
            builders=builders)

    def _build(self, builders: list) -> None:
        for builder, file, option in builders:
            builder(self.templates_dir).execute(self.target_dir, file, option)
        click.secho("{} : Completed successfully!".format(file), fg='green')
