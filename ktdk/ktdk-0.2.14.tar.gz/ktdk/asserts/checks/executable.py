import logging
import re

from ktdk.asserts import matchers
from ktdk.asserts.checks.general import AbstractExecResultMatchesTask

log = logging.getLogger(__name__)


class ExecutableExists(AbstractExecResultMatchesTask):
    def __init__(self, executable: str, **kwargs):
        super().__init__(**kwargs)
        self._executable = executable

    def _run(self, *args, **kwargs):
        self.asserts.require(self.context, matcher=matchers.DictHasKey('exec'))
        executables = self.context['exec']
        self.asserts.require(executables, matcher=matchers.DictHasKey(self._executable))
        exec_path = executables[self._executable]
        self.asserts.require(exec_path, matcher=matchers.FileExists())


class ReturnCodeMatchesCheck(AbstractExecResultMatchesTask):
    def _run(self, *args, **kwargs):
        self.asserts.check(self.exec_result.return_code, self.matcher)


class StdOutMatchesCheck(AbstractExecResultMatchesTask):
    def _run(self, *args, **kwargs):
        self.asserts.check(self.exec_result.stdout.content, self.matcher)


class StdErrMatchesCheck(AbstractExecResultMatchesTask):
    def _run(self, *args, **kwargs):
        self.asserts.check(self.exec_result.stderr.content, self.matcher)


class ValgrindPassedCheck(AbstractExecResultMatchesTask):
    REGEX = re.compile(r'ERROR SUMMARY: (\d+) errors')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def points_multiplier(self):
        if self._points_multiplier:
            return self._points_multiplier

        return self.context.config['valgrind_penalization'] or 0

    @property
    def valgrind_log(self) -> str:
        return self.context.config['valgrind_log']

    def __read_log_content(self):
        valgrind_log = self.valgrind_log
        if valgrind_log is None:
            return None
        valgrind_log = self.context.paths.results / valgrind_log
        return valgrind_log.read_text(encoding='utf-8')

    def _run(self, *args, **kwargs):
        self.asserts.check(self._asserted_zero_errors(), self.matcher)

    def _asserted_zero_errors(self):
        content = self.__read_log_content()
        if content is None:
            log.warning(f"[VALGRIND] Valgrind content is not set for {self.namespace}")
            return False
        passed = True
        errors = None
        for line in content.splitlines():
            match = ValgrindPassedCheck.REGEX.search(line)
            if match:
                errors = match.group(1)
                passed = int(errors) == 0
        if not passed:
            log.warning(f"[VALGRIND] Log {self.namespace}:\n{content}")
            log.warning(f"[VALGRIND] Found errors in Valgrind: {errors}")
        else:
            log.debug(f'[VALGRIND] Log {self.namespace}:\n{content}')
        return passed
