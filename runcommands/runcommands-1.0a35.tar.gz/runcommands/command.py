import argparse
import inspect
import signal
import sys
import time
from collections import OrderedDict
from typing import Mapping

from .args import (
    DISABLE, Arg, ArgConfig, HelpArg, BoolOrAction, DictAddAction, ListAppendAction,
    TupleAppendAction)
from .exc import CommandError, RunCommandsError
from .util import cached_property, camel_to_underscore, get_hr, printer


__all__ = ['command', 'Command']


class Command:

    """Wraps a callable and provides a command line argument parser.

    Args:
        implementation (callable): A callable that implements the
            command's functionality. The command's console script will
            be generated by inspecting this callable.
        name (str): Name of command as it will be called from the
            command line. Defaults to ``implementation.__name__`` (with
            underscores replaced with dashes).
        description (str): Description of command shown in command
            help. Defaults to ``implementation.__doc__``.
        timed (bool): Whether the command should be timed. Will print an
            info message showing how long the command took to complete
            when ``True``. Defaults to ``False``.
        arg_config (dict): For commands defined as classes, this can be
            used to configure common base args instead of repeating the
            configuration for each subclass. Note that its keys should
            be actual parameter names and not normalized arg names.
        debug (bool): When this is set, additional debugging info will
            be shown.

    This is typically used via the :func:`command` decorator::

        from runcommands import command

        @command
        def my_command():
            ...

    Decorating a function with :func:`command` will create an instance
    of :class:`Command` with the wrapped function as its implementation.

    Args can be passed to :func:`command`, which will be passed through
    to the :class:`Command` constructor::

        @command(name='better-name')
        def my_command():
            ...

    It's also possible to use a class directly as a command::

        @command
        class MyCommand(Command):

            def implementation(self):
                ...

    Using the :func:`command` decorator on a class will create an
    instance of the class in the namespace where the class is defined.

    Command Names:

    A command's name is derived from the normalized name of its
    implementation function by default::

        @command
        def some_command():
            ...

        # Command name: some-command

    A name can be set explicitly instead, in which case it *won't* be
    normalized::

        @command(name='do_stuff')
        def some_command():
            ...

        # Command name: do_stuff

    If the command is defined as a class, its name will be derived from
    its class name by default (split into words then normalized)::

        class SomeCommand(Command):
            ...

        # Command name: some-command

    The `command` decorator or a class-level attribute can be used to
    set the command's name explicitly::

        @command(name='do_stuff')
        class SomeCommand(Command):
            ...

        class SomeCommand(Command):
            name = 'do_stuff'

        # Command name in both cases: do_stuff

    """

    def __init__(self, implementation=None, name=None, description=None, timed=False,
                 arg_config=None, default_args=None, debug=False):
        if implementation is None:
            if not hasattr(self, 'implementation'):
                raise CommandError(
                    'Missing implementation; it must be passed in as a function or defined as a '
                    'method on the command class')
            default_name = self.__class__.name
        else:
            self.implementation = implementation
            default_name = implementation.__name__

        self.name = (
            name or
            getattr(self.__class__, 'name', None) or
            self.normalize_name(default_name))

        self.description = description or self.get_description_from_docstring(self.implementation)
        self.timed = timed
        self.arg_config = arg_config or {}
        self.debug = debug
        self.default_args = default_args or {}

    @classmethod
    def command(cls, name=None, description=None, timed=False):
        args = dict(description=description, timed=timed)

        if isinstance(name, type):
            # Bare class decorator
            name.implementation.__name__ = camel_to_underscore(name.__name__)
            return name(**args)

        if callable(name):
            # Bare function decorator
            return cls(implementation=name, **args)

        def wrapper(wrapped):
            if isinstance(wrapped, type):
                wrapped.implementation.__name__ = camel_to_underscore(wrapped.__name__)
                return wrapped(name=name, **args)
            return cls(implementation=wrapped, name=name, **args)

        return wrapper

    def get_description_from_docstring(self, implementation):
        description = implementation.__doc__
        if description is not None:
            description = description.strip() or None
        if description is not None:
            lines = description.splitlines()
            title = lines[0]
            if title.endswith('.'):
                title = title[:-1]
            lines = [title] + [line[4:] for line in lines[1:]]
            description = '\n'.join(lines)
        return description

    def run(self, argv=None, **kwargs):
        argv = sys.argv[1:] if argv is None else argv

        if self.timed:
            start_time = time.monotonic()

        args = self.parse_args(argv)
        args.update(kwargs)
        result = self(**args)

        if self.timed:
            self.print_elapsed_time(time.monotonic() - start_time)

        return result

    def console_script(self, argv=None, **kwargs):
        argv = sys.argv[1:] if argv is None else argv
        if hasattr(self, 'sigint_handler'):
            signal.signal(signal.SIGINT, self.sigint_handler)
        try:
            result = self.run(argv, **kwargs)
        except RunCommandsError as result:
            if getattr(self, 'raise_on_error', False):
                raise
            return_code = result.return_code if hasattr(result, 'return_code') else 1
            result_str = str(result)
            if result_str:
                if return_code:
                    printer.error(result_str, file=sys.stderr)
                else:
                    printer.print(result_str)
        else:
            return_code = result.return_code if hasattr(result, 'return_code') else 0
        return return_code

    def __call__(self, *args, **kwargs):
        passed = set(tuple(self.parameters)[:len(args)])
        passed.update(kwargs)

        defaults = {}
        for name, value in self.default_args.items():
            if name not in passed:
                defaults[name] = value

        if self.debug:
            printer.debug('Command called:', self.name)
            printer.debug('    Received positional args:', args)
            printer.debug('    Received keyword args:', kwargs)
            if defaults:
                printer.debug('    Added default args:', ', '.join(defaults))

        if defaults:
            kwargs.update(defaults)

        if self.debug:
            printer.debug('Running command:', self.name)
            printer.debug('    Final positional args:', repr(args))
            printer.debug('    Final keyword args:', repr(kwargs))

        return self.implementation(*args, **kwargs)

    def parse_args(self, argv):
        temp_argv = []

        for arg in argv:
            # Look for grouped short options like `-abc` and convert to
            # `-a, -b, -c`.
            #
            # This is necessary because we set `allow_abbrev=False` on
            # the `ArgumentParser` in `self.arg_parser`. The argparse
            # docs say `allow_abbrev` applies only to long options, but
            # it also affects whether short options grouped behind a
            # single dash will be parsed into multiple short options.
            is_multi_short_option = (
                (len(arg) > 2) and   # Minimum length is 3, e.g. `-ab`
                (arg[0] == '-') and  # Is it a short option?
                (arg[1] != '-')      # No, it's a long option
            )
            if is_multi_short_option:
                temp_argv.extend('-{a}'.format(a=a) for a in arg[1:])
            else:
                temp_argv.append(arg)

        argv = temp_argv

        if self.debug:
            printer.debug('Parsing args for command `{self.name}`: {argv}'.format_map(locals()))
        parsed_args = self.arg_parser.parse_args(argv)
        parsed_args = vars(parsed_args)
        for k, v in parsed_args.items():
            if v == '':
                parsed_args[k] = None
        return parsed_args

    def normalize_name(self, name):
        name = camel_to_underscore(name)
        # Chomp a single trailing underscore *if* the name ends with
        # just one trailing underscore. This accommodates the convention
        # of adding a trailing underscore to reserved/built-in names.
        if name.endswith('_'):
            if name[-2] != '_':
                name = name[:-1]
        name = name.replace('_', '-')
        name = name.lower()
        return name

    def find_arg(self, name):
        """Find arg by normalized arg name or parameter name."""
        name = self.normalize_name(name)
        return self.args.get(name)

    def find_parameter(self, name):
        """Find parameter by name or normalized arg name."""
        name = self.normalize_name(name)
        arg = self.args.get(name)
        return None if arg is None else arg.parameter

    def get_arg_config(self, param):
        annotation = param.annotation
        if annotation is param.empty:
            annotation = self.arg_config.get(param.name) or ArgConfig()
        elif isinstance(annotation, type):
            annotation = ArgConfig(type=annotation)
        elif isinstance(annotation, str):
            annotation = ArgConfig(help=annotation)
        elif isinstance(annotation, Mapping):
            annotation = ArgConfig(**annotation)
        return annotation

    def get_short_option_for_arg(self, name, names, used):
        first_char = name[0]
        first_char_upper = first_char.upper()

        if name == 'help':
            candidates = (first_char,)
        elif name.startswith('h'):
            candidates = (first_char_upper,)
        else:
            candidates = (first_char, first_char_upper)

        for char in candidates:
            short_option = '-{char}'.format_map(locals())
            if short_option not in used:
                return short_option

    def get_long_option_for_arg(self, name):
        return '--{name}'.format_map(locals())

    def get_inverse_option_for_arg(self, long_option):
        if long_option == '--yes':
            return '--no'
        if long_option == '--no':
            return '--yes'
        if long_option.startswith('--no-'):
            return long_option.replace('--no-', '--', 1)
        return long_option.replace('--', '--no-', 1)

    def print_elapsed_time(self, elapsed_time):
        m, s = divmod(elapsed_time, 60)
        m = int(m)
        hr = get_hr()
        msg = '{hr}\nElapsed time for {self.name} command: {m:d}m {s:.3f}s\n{hr}'
        msg = msg.format_map(locals())
        printer.info(msg)

    @cached_property
    def parameters(self):
        implementation = self.implementation
        signature = inspect.signature(implementation)
        params = tuple(signature.parameters.items())
        params = OrderedDict(params)
        return params

    @cached_property
    def has_kwargs(self):
        return any(p.kind is p.VAR_KEYWORD for p in self.parameters.values())

    @cached_property
    def args(self):
        """Create args from function parameters."""
        params = self.parameters
        args = OrderedDict()

        # This will be overridden if the command explicitly defines an
        # arg named help.
        args['help'] = HelpArg(command=self)

        normalize_name = self.normalize_name
        get_arg_config = self.get_arg_config
        get_short_option = self.get_short_option_for_arg
        get_long_option = self.get_long_option_for_arg
        get_inverse_option = self.get_inverse_option_for_arg

        names = {normalize_name(name) for name in params}

        used_short_options = set()
        for param in params.values():
            annotation = get_arg_config(param)
            short_option = annotation.short_option
            if short_option:
                used_short_options.add(short_option)

        for name, param in params.items():
            if param.kind is param.VAR_KEYWORD:
                continue

            name = normalize_name(name)

            if name.startswith('_') or param.kind is param.KEYWORD_ONLY:
                continue

            annotation = get_arg_config(param)
            type = annotation.type
            choices = annotation.choices
            help = annotation.help
            inverse_help = annotation.inverse_help
            short_option = annotation.short_option
            long_option = annotation.long_option
            inverse_option = annotation.inverse_option
            action = annotation.action

            if param.default is param.empty:  # Positional
                short_option = None
                long_option = None
                inverse_option = None
            else:
                if not short_option:
                    short_option = get_short_option(name, names, used_short_options)
                    used_short_options.add(short_option)
                if not long_option:
                    long_option = get_long_option(name)
                if not inverse_option:
                    # NOTE: The DISABLE marker evaluates as True
                    inverse_option = get_inverse_option(long_option)

            args[name] = Arg(
                command=self,
                parameter=param,
                name=name,
                type=type,
                default=param.default,
                choices=choices,
                help=help,
                inverse_help=inverse_help,
                short_option=short_option,
                long_option=long_option,
                inverse_option=inverse_option,
                action=action,
            )

        option_map = OrderedDict()
        for arg in args.values():
            for option in arg.options:
                option_map.setdefault(option, [])
                option_map[option].append(arg)

        for option, option_args in option_map.items():
            if len(option_args) > 1:
                names = ', '.join(a.parameter.name for a in option_args)
                message = (
                    'Option {option} of command {self.name} maps to multiple parameters: {names}')
                message = message.format_map(locals())
                raise CommandError(message)

        return args

    @cached_property
    def positionals(self):
        args = self.args.items()
        return OrderedDict((name, arg) for (name, arg) in args if arg.is_positional)

    @cached_property
    def optionals(self):
        args = self.args.items()
        return OrderedDict((name, arg) for (name, arg) in args if arg.is_optional)

    @cached_property
    def option_map(self):
        """Map command-line options to args."""
        option_map = OrderedDict()
        for arg in self.args.values():
            for option in arg.options:
                option_map[option] = arg
        return option_map

    @cached_property
    def arg_parser(self):
        use_default_help = isinstance(self.args['help'], HelpArg)

        parser = argparse.ArgumentParser(
            prog=self.name,
            description=self.description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            argument_default=argparse.SUPPRESS,
            add_help=use_default_help,
            allow_abbrev=False,  # See note in `self.parse_args()`
        )

        default_args = self.default_args

        for name, arg in self.args.items():
            if name == 'help' and use_default_help:
                continue

            param = arg.parameter

            kwargs = {
                'help': arg.help,
            }

            metavar = name.upper().replace('-', '_')
            if (arg.is_dict or arg.is_list) and len(name) > 1 and name.endswith('s'):
                metavar = metavar[:-1]

            if arg.is_positional:
                # NOTE: Positionals are made optional if a default value
                # is specified via config.
                has_default = param.name in default_args

                if arg.is_dict:
                    kwargs['action'] = arg.action or DictAddAction
                    kwargs['nargs'] = '*' if has_default else '+'
                elif arg.is_list:
                    kwargs['action'] = arg.action or ListAppendAction
                    kwargs['nargs'] = '*' if has_default else '+'
                elif arg.is_tuple:
                    kwargs['action'] = arg.action or TupleAppendAction
                    kwargs['nargs'] = '*' if has_default else '+'
                else:
                    kwargs['type'] = arg.type
                    kwargs['action'] = arg.action or None
                    if has_default:
                        kwargs['nargs'] = '?'
                    if arg.choices is not None:
                        kwargs['choices'] = arg.choices

                kwargs['metavar'] = metavar
                parser.add_argument(param.name, **kwargs)
            else:
                options = arg.options
                kwargs['dest'] = param.name

                if arg.is_bool or arg.is_bool_or:
                    if arg.inverse_help:
                        inverse_help = arg.inverse_help
                    elif arg.help:
                        first_letter = kwargs['help'][0].lower()
                        the_rest = kwargs['help'][1:]
                        inverse_help = 'Don\'t {first_letter}{the_rest}'.format_map(locals())
                    else:
                        inverse_help = arg.help

                if arg.is_bool_or:
                    # Allow --xyz or --xyz=<value>
                    other_type = arg.type.type
                    true_or_value_kwargs = kwargs.copy()
                    true_or_value_kwargs['type'] = other_type
                    if arg.choices is not None:
                        true_or_value_kwargs['choices'] = arg.choices
                    true_or_value_kwargs['action'] = BoolOrAction
                    true_or_value_kwargs['nargs'] = '?'
                    true_or_value_kwargs['metavar'] = metavar

                    if arg.inverse_option is DISABLE:
                        true_or_value_arg_names = options
                    else:
                        true_or_value_arg_names = options[:-1]

                    parser.add_argument(*true_or_value_arg_names, **true_or_value_kwargs)

                    if arg.inverse_option is not DISABLE:
                        # Allow --no-xyz
                        false_kwargs = kwargs.copy()
                        false_kwargs['help'] = inverse_help
                        parser.add_argument(options[-1], action='store_false', **false_kwargs)
                elif arg.is_bool:
                    if arg.inverse_option is DISABLE:
                        true_arg_names = options
                    else:
                        true_arg_names = options[:-1]

                    parser.add_argument(*true_arg_names, action='store_true', **kwargs)

                    if arg.inverse_option is not DISABLE:
                        false_kwargs = kwargs.copy()
                        false_kwargs['help'] = inverse_help
                        parser.add_argument(options[-1], action='store_false', **false_kwargs)
                elif arg.is_dict:
                    kwargs['action'] = arg.action or DictAddAction
                    kwargs['metavar'] = metavar
                    parser.add_argument(*options, **kwargs)
                elif arg.is_list:
                    kwargs['action'] = arg.action or ListAppendAction
                    kwargs['metavar'] = metavar
                    parser.add_argument(*options, **kwargs)
                elif arg.is_tuple:
                    kwargs['action'] = arg.action or TupleAppendAction
                    kwargs['metavar'] = metavar
                    parser.add_argument(*options, **kwargs)
                else:
                    kwargs['type'] = arg.type
                    kwargs['action'] = arg.action
                    if arg.choices is not None:
                        kwargs['choices'] = arg.choices
                    kwargs['metavar'] = metavar
                    parser.add_argument(*options, **kwargs)

        return parser

    @property
    def help(self):
        help_ = self.arg_parser.format_help()
        help_ = help_.split(': ', 1)[1]
        help_ = help_.strip()
        return help_

    @property
    def usage(self):
        usage = self.arg_parser.format_usage()
        usage = usage.split(': ', 1)[1]
        usage = usage.strip()
        return usage

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.usage

    def __repr__(self):
        return 'Command(name={self.name})'.format(self=self)


command = Command.command
