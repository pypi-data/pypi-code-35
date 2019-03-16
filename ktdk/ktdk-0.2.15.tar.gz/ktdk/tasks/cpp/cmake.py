import logging
import re

from ktdk.asserts import matchers
from ktdk.asserts.matchers import IsNotEmpty
from ktdk.core.tasks import Task
from ktdk.tasks.build_task import BuildTask

log = logging.getLogger(__name__)


class MakeResultParser(BuildTask):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subdir = ''
        self.build_regex = re.compile(r"Built target ([\w\-_\.]+)")

    def _run(self, *args, **kwargs):
        names = self.__parse_b_names()
        log.info(f"[PROC] Binaries by make \"{self.namespace}\": {names}")
        self.asserts.check(names, IsNotEmpty("Binaries have not been found."))
        executables = {}
        for name in names:
            path = self.target / self.subdir / name
            executables[name] = path
        self.context.config.set_test('exec', executables)

    def __parse_b_names(self):
        names = []
        result = self.context.config['make_result']
        for line in result.stdout.content.splitlines():
            name = self.__parse_b_name(line)
            if name:
                names.append(name)
        return names

    def __parse_b_name(self, line):
        match = self.build_regex.search(line)
        return match.group(1) if match else None


class MakeTask(BuildTask):
    """Default make task, to execute the make command
    """

    def __init__(self, **kwargs):
        super().__init__(command=None, **kwargs)
        self.name = self.name or 'make'
        self.add_tags('make')

    @property
    def command_path(self) -> str:
        return super().command_path or 'make'

    def process_make(self, result):
        self.asserts.check(result, matchers.CommandOK())
        self.context.config.set_task('make_result', result)
        return result

    def run_make(self):
        result = self.execute()
        return self.process_make(result)

    def _run(self, *args, **kwargs):
        log.info(f'[BLD] Make {self.namespace}')
        old_dir = self.move_to_dir(self.target)  # TODO: Check and change the dir
        make_args = self.context.config.get('make_args') or []
        self.args.extend(make_args)
        self.run_make()
        self.move_to_dir(old_dir)


class CMakeTask(BuildTask):
    def __init__(self, **kwargs):
        super().__init__(command=None, **kwargs)
        self.name = self.name or 'cmake'
        self.add_tags('cmake', 'compile')

    @property
    def command_path(self) -> str:
        return super().command_path or 'cmake'

    def run_cmake(self):
        self.args.extend(self.context.config.get('cmake_args') or [])
        self.args.append(str(self.source))
        log.info(f"[CMAKE] Cmake {self.args}")
        result = self.execute()
        self.asserts.check(result, matchers.CommandOK())
        return result

    def _run(self, *args, **kwargs):
        log.info(f'[BLD] CMake {self.namespace}')
        old_dir = self.move_to_dir(self.target)
        result = self.run_cmake()
        self.move_to_dir(old_dir)
        return result


class CMakeBuildTask(Task):
    def __init__(self, target='', source='', cwd=None, cmake_location=None, **kwargs):
        super().__init__(**kwargs)
        self.target = target
        self.source = source
        self.cmake_location = cmake_location
        self.name = 'cmake_build'
        self.cmake = CMakeTask(target_dir=target, source_dir=source, cwd=cwd)
        self.make = MakeTask(target_dir=target, source_dir=source, cwd=cwd)
        self.make.add_task(MakeResultParser(target_dir=target, source_dir=source))
        self.add_task(self.cmake)
        self.add_task(self.make)
        self._cwd = cwd
