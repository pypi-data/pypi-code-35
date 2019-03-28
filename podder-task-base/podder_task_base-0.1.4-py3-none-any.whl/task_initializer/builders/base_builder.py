from typing import Any
import os


class BaseBuilder(object):
    def __init__(self) -> None:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(this_dir, "../templates")
        self.templates_dir = templates_dir

    def execute(self, target_dir: str, file: str, option: Any) -> None:
        raise NotImplementedError
