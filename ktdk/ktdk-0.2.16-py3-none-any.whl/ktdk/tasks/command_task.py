import logging

from ktdk.asserts import matchers
from ktdk.core.tasks import Task
from ktdk.tasks.command import Command, CommandResult

log = logging.getLogger(__name__)


class CommandTask(Task):
    def __init__(self, command=None, args=None, executor=Command,
                 command_config=None, output_name=None, **kwargs):
        super().__init__(**kwargs)
        self.add_tags('command')
        self.name = self.name or command
        self.executor = executor or Command
        self._cmd = command
        self._command_config = command_config or {}
        self.args = args or []
        self._output_name = output_name

    def build_args(self, *args):
        arr = []
        arr.extend(args)
        arr.extend(self.args)
        return arr

    @property
    def command_path(self) -> str:
        """Name of the command, if not provided, it will try to use the <task_name>_command
        form the config
        Returns(str): name or path to the command
        """
        return self._cmd or self.context.config.get(self.name + '_command')

    @property
    def command_config(self) -> dict:
        cfg = self._command_config
        cfg['timeout'] = cfg.get('timeout') or self.context.config.get(self.name + '_timeout') or \
                         self.context.config.get('timeout')
        return cfg

    def command(self):
        """Creates the command instance based on the executor
            Executor can be the Command or ValgrindCommand
        Returns:

        """
        path = str(self.command_path)
        args = self.build_args()
        return self.executor(path, args=args, output_name=self._output_name, **self.command_config)

    def execute(self, **kwargs) -> CommandResult:
        return self.command().set_task(self).invoke(**kwargs)

    def _run(self, *args, **kwargs):
        result = self.execute()
        if result.nok:
            log.warning(f"[CMD] Command failed {self.namespace}: {result}")
        self.asserts.check(result, matchers.CommandOK())
        self.context.config.set_test('command_result', result)
