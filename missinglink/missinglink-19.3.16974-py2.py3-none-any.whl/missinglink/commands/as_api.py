# -*- coding: utf8 -*-
import json
import click
import six


class ApiException(Exception):
    pass


class InvalidJsonOutput(Exception):
    pass


class _ApiCall:
    def __init__(self, cli, command_cli, *commands, **kwargs):
        self._cli = cli
        self._commands = commands
        config_file = kwargs.pop('config_file', None)
        self._config_file = config_file
        self._command_cli = command_cli

    def __call__(self, *args, **kwargs):
        return self._run(*args, **kwargs)

    def _get_param(self, key):
        for param in self._command_cli.params:
            name = '--' + key if isinstance(param, click.Option) else key
            if name in param.opts or name in param.secondary_opts:
                return param

    @classmethod
    def __make_arg_list(cls, key, val, param):
        if isinstance(val, (list, tuple)):
            if len(val) > 1 and not param.multiple:
                raise AttributeError('parameter %s does not support multiple' % (key,))

            return val

        return [val]

    def __validate_param(self, key):
        param = self._get_param(key)

        if param is None:
            raise AttributeError('api %s() does not have "%s" kwarg' % ('.'.join(self._commands), key))

        return param

    @classmethod
    def __process_bool_param(cls, val, key, param):
        flag = key
        if isinstance(param, click.Option) and param.is_bool_flag and not val:
            if param.secondary_opts:
                flag = param.secondary_opts[0]
                val = True
            else:
                val = None

        if isinstance(param, click.Option) and not flag.startswith('--'):
            flag = '--' + key

        return val, flag

    @classmethod
    def __make_list_if_needed(cls, val):
        return val if isinstance(val, (list, tuple)) else [val]

    def __convert_to_arg(self, cmd_args, key, val):
        key = key.replace('_', '-')

        param = self.__validate_param(key)

        val, flag = self.__process_bool_param(val, key, param)

        val = self.__make_arg_list(key, val, param)

        for single_val in val:
            if single_val is None:
                continue

            if isinstance(param, click.Option):
                cmd_args.append(flag)

                if param.is_bool_flag:
                    continue

            cmd_args.extend([str(single_val_item) for single_val_item in self.__make_list_if_needed(single_val)])

    def _convert_to_args(self, *args, **kwargs):
        cmd_args = ['--output-format', 'json', '--skip-version-check', '--disable-interactive']

        if self._config_file is not None:
            cmd_args.extend(['--config-file', self._config_file])

        for cmd in self._commands:
            cmd_args.append(str(cmd))

        for val in args:
            cmd_args.append(str(val))

        for key, val in kwargs.items():
            self.__convert_to_arg(cmd_args, key, val)

        return cmd_args

    @classmethod
    def __handle_error_result(cls, result):
        try:
            exception_text = result.stderr.strip()
        except ValueError:
            exception_text = None

        if result.exc_info and not isinstance(result.exc_info[1], SystemExit):
            six.reraise(*result.exc_info)

        raise ApiException(exception_text)

    @classmethod
    def __return_json(cls, result):
        if not result.stdout:
            return

        try:
            return json.loads(result.stdout)
        except ValueError:
            msg = 'command output is not json format:\n"%s"' % result.stdout
            raise InvalidJsonOutput(msg)

    def _run(self, *args, **kwargs):
        from click.testing import CliRunner

        cmd_args = self._convert_to_args(*args, **kwargs)
        runner = CliRunner(mix_stderr=False)
        try:
            result = runner.invoke(self._cli, cmd_args, catch_exceptions=False, standalone_mode=False)
        except click.exceptions.MissingParameter as ex:
            type_param = 'arg' if isinstance(ex.param, click.Argument) else 'kwarg'
            six.raise_from(ValueError('required %s %s is missing' % (type_param, ex.param.human_readable_name.lower())), None)

        if result.exit_code != 0:
            self.__handle_error_result(result)

        return self.__return_json(result)


class _ApiProxy:
    def __init__(self, cli, *commands, **kwargs):
        self._cli = cli
        self._commands = list(commands) or []
        config_ctx = kwargs.pop('config_ctx', None)
        self._config_ctx = config_ctx or {}

    def _append_command(self, name):
        commands = self._commands[:]
        name = name.replace('_', '-')
        commands.append(name)

        return commands

    def _find_cli(self, name):
        current_cli = self._cli

        for current_cmd in self._append_command(name):
            if current_cmd in current_cli.commands:
                current_cli = current_cli.commands[current_cmd]
                continue

            raise AttributeError('command %s not found' % name)

        return current_cli

    def __getattr__(self, name):
        cli = self._find_cli(name)

        commands = self._append_command(name)
        proxy = _ApiProxy(self._cli, *commands, config_ctx=self._config_ctx)
        if isinstance(cli, click.Group):
            return proxy

        return _ApiCall(self._cli, cli, *commands, **self._config_ctx)


__as_api = None


def as_api(config_file=None):
    global __as_api

    if __as_api is not None:
        return __as_api

    from missinglink.commands import cli, add_commands

    add_commands()

    config_ctx = {
        'config_file': config_file
    }

    __as_api = _ApiProxy(cli, config_ctx=config_ctx)

    return __as_api


if __name__ == '__main__':
    as_api().data.query(volume_id=2, silent=True)
