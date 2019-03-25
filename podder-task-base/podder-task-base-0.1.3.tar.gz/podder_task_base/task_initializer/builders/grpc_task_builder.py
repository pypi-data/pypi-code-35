from typing import Any
import os
import shutil

from jinja2 import Environment, FileSystemLoader

from podder_task_base.task_initializer.builders.base_builder import BaseBuilder
from podder_task_base.utils import string_utils


class GrpcTaskBuilder(BaseBuilder):
    def execute(self, target_dir: str, file: str, option: Any) -> None:
        src_path = os.path.join(self.templates_dir, file)
        dst_path = os.path.join(target_dir, file)
        task_class = string_utils.to_camel_case(option)
        data = {"task_class": task_class}

        env = Environment(
            loader=FileSystemLoader(self.templates_dir), trim_blocks=True)
        content = env.get_template(file).render(data)
        with open(dst_path, "w") as file:
            file.write(content)
