import logging
from pathlib import Path
from typing import Collection, List, Set

from ktdk import Task, Test
from ktdk.asserts import checks, matchers
from ktdk.scenarios import FullScenario, Scenario
from ktdk.scenarios.simple import InOutFileScenario
from ktdk.tasks import cpp, fs
from ktdk.tasks.cpp import ValgrindCommand

log = logging.getLogger(__name__)


class CMiniSingleTaskScenario(FullScenario):
    """Execute just single CMiniTask scenario
    """

    def __init__(self, task_name: str, points=0.1, executor=ValgrindCommand, **kwargs):
        super().__init__(**kwargs)
        self.task_name = task_name
        self.points = points
        self.executor = executor

    def checkout_teacher_files(self):
        log.info(f"[CHECKOUT] All teacher files for task {self.task_name}")
        self.ft.test_files() \
            .add_task(fs.CopyFiles(f"{self.task_name}/**/*.*", output_subdir=self.task_name))

    def checkout_student_files(self):
        self.ft.submission().require_that(fs.ExistFiles(f"{self.task_name}/source.c"))
        self.ft.submission() \
            .add_task(fs.CopyFiles(f"{self.task_name}/source.c", output_subdir=self.task_name))

    def file_tasks(self):
        self.checkout_teacher_files()
        self.checkout_student_files()  # Needs to be in this order

    def compile_tasks(self):
        c_compile = cpp.CCompilerTask(executable=self.task_name,
                                      files=f'{self.task_name}/source.c',
                                      use_default_options=True)
        c_compile.require_that(checks.TaskResultCheck(matcher=matchers.ResultPassed()))
        c_compile.require_that(checks.ExecutableExists(executable=self.task_name))
        self.root_test.add_task(c_compile)
        return c_compile

    def run_tasks(self):
        subtests = _RunSubTestForTask(self.task_name, points=self.points)
        self.root_test.add_task(subtests)


class _RunSubTestForTask(Task):
    def __init__(self, task_name, points=0.1, **kwargs):
        super().__init__(**kwargs)
        self.task_name = task_name
        self.points = points

    @property
    def base(self) -> Path:
        return self.context.paths.workspace / self.task_name

    def __build_paths(self, ext: str) -> List['Path']:
        return list(self.base.glob(f'*.{ext}'))

    @property
    def out_paths(self) -> List['Path']:
        return self.__build_paths('out')

    @property
    def in_paths(self) -> List['Path']:
        return self.__build_paths('in')

    @property
    def args_paths(self) -> List['Path']:
        return self.__build_paths('args')

    @property
    def err_paths(self) -> List['Path']:
        return self.__build_paths('err')

    def _run(self, *args, **kwargs):
        names = dict(
            outs=_resolve_names(self.out_paths),
            ins=_resolve_names(self.in_paths),
            errs=_resolve_names(self.err_paths),
            args=_resolve_names(self.args_paths)
        )

        all_names = set().union(*names.values())
        log.info(f"[MINI] All subtests: {all_names}")
        all_tests = _build_tests(all_names, names)
        self._run_all(all_tests)

    def _in_out_test(self, name, points=0.0, stdin=None, stdout=None,
                     args=None, status_code=0, stderr=None, executor=ValgrindCommand):
        """Create instance of the in/out test
        Args:
            name(str): Test name
            points(float): Number of points for the test
            stdin(Path): File with stdin
            stdout(Path): Stdout file
            args(List['str']): List of arguments
            status_code(int): Status code
            stderr(Path): Stdout path
            executor: Executor instance

        Returns:

        """
        test = Test(name=name, desc=f'Subtest name: {name}', points=points)
        in_out_scenario = InOutFileScenario(
            executable=self.task_name, args=args, stdin=stdin, executor=executor,
            stdout=stdout, stderr=stderr, status_code=status_code)
        test.add_task(in_out_scenario)
        return test

    def _run_one(self, test: dict, num=0):
        def get_path(val): return self.base / val if val else None

        params = {key: get_path(value) for key, value in test.items() if key != 'name'}
        points = self.points / num
        params['args'] = self._extract_args(params['args']) if params['args'] else None
        test = self._in_out_test(test['name'], points=points, **params)
        self.test.add_test(test)

    def _extract_args(self, args):
        args = _read_args(args).split('\n')
        args = [arg for arg in args if arg]
        return args

    def _run_all(self, all_tests):
        num = len(all_tests)
        for test in all_tests:
            self._run_one(test, num=num)


class CMiniAllTasksScenario(Scenario):
    def __init__(self, points=1, **kwargs):
        super().__init__(**kwargs)
        self.points = points

    def list_teacher_directories(self) -> Set[str]:
        import os
        test_files = self.context.paths.test_files
        return {dI for dI in os.listdir(str(test_files)) if test_files.joinpath(dI).is_dir()}

    def list_of_student_impl(self) -> Set['str']:
        student_f = self.context.paths.submission
        sources = {p.parent.name for p in student_f.glob("*/source.c")}
        return sources

    def _create_test_for_task(self, task_name, points=0):
        main_test = Test(name=task_name, desc=f"Test for task: {task_name}")
        task_scenario = CMiniSingleTaskScenario(task_name=task_name, points=points)
        main_test.add_task(task_scenario)
        return main_test

    def _run(self, *args, **kwargs):
        teacher: set = self.list_teacher_directories()
        student: set = self.list_of_student_impl()
        intersection = student.intersection(teacher)
        num_tasks = len(teacher)
        ratio = self.points / float(num_tasks) if num_tasks else 0
        for task in intersection:
            test = self._create_test_for_task(task, points=ratio)
            self.root_test.add_test(test)


def _resolve_names(collection: Collection['Path']) -> Set['str']:
    return {p.resolve().stem for p in collection}


def _intersect_names(first: Set['str'], *sets) -> Set['str']:
    result = first
    for name_set in sets:
        result = result.intersection(name_set)
    return result


def _build_test(name, names):
    test = dict(
        stdout=f"{name}.out" if name in names['outs'] else None,
        stdin=f"{name}.in" if name in names['ins'] else None,
        stderr=f'{name}.err' if name in names['errs'] else None,
        args=f'{name}.args' if name in names['args'] else None,
        name=name,
    )
    return test


def _build_tests(all_names: Collection, names: Collection) -> Collection:
    return [_build_test(name, names) for name in all_names]


def _read_args(path: Path) -> str:
    return path.read_text(encoding='utf-8')
