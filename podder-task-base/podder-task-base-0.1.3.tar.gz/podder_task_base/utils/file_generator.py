import os

from jinja2 import Environment, FileSystemLoader
from podder.utils import string_utils

from ..build import templates


class FileGenerator(object):
    def execute(self,
                data: dict,
                template_file: str,
                dest_path: str,
                template_dir: dict = None) -> None:
        if template_dir is None:
            template_dir = os.path.dirname(os.path.abspath(templates.__file__))
        env = Environment(
            loader=FileSystemLoader(template_dir), trim_blocks=True)

        # Add custom method to jinja2 filters
        env.filters['to_snake_case'] = string_utils.to_snake_case
        env.filters['to_camel_case'] = string_utils.to_camel_case
        env.filters['to_kebab_case'] = string_utils.to_kebab_case
        env.filters['to_env_var_case'] = string_utils.to_env_var_case

        content = env.get_template(template_file).render(data)
        self.make_dest_dir(dest_path)

        with open(dest_path, "w") as file:
            file.write(content)

    def make_dest_dir(self, dest_path: str):
        dir_path = os.path.dirname(dest_path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
