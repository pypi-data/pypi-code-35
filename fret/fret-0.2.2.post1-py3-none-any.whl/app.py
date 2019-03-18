import abc
import argparse
import collections
import functools
import importlib
import inspect as ins
import logging
import os
import pathlib
import shutil
import sys
from collections import namedtuple

import toml

from .exceptions import NotConfiguredError
from .common import Module, Workspace
from .util import classproperty, Configuration, colored


class App:
    """Application object. In charge of locating suitable app, importing
    modules, and run commands."""

    __slots__ = ['_root', '_config', '_commands', '_modules', '_cwd', '_imp']

    def __init__(self, path=None):
        self._cwd = None
        if path is None:
            p = pathlib.Path().absolute()
            if p.joinpath('fret.toml').exists():
                path = str(p)
            else:
                while p != pathlib.Path(p.root):
                    if p.joinpath('fret.toml').exists():
                        path = str(p)
                        self._cwd = os.getcwd()
                        os.chdir(path)
                        break
                    p = p.parent
                else:
                    path = pathlib.Path().absolute()

        sys.path.insert(0, str(path))
        self._root = pathlib.Path(path)
        self._imp = None

        self._config = None
        self._commands = {}
        self._modules = {}

        if self._root.joinpath('fret.toml').exists():
            cfg = toml.load(self._root.joinpath('fret.toml').open())
        else:
            cfg = {}
        self._config = Configuration(cfg)

    def import_modules(self, appname=None):
        appname = appname or os.environ.get('FRETAPP')
        if appname is not None:
            self._imp = importlib.import_module(appname)
        elif 'appname' in self._config:
            self._imp = importlib.import_module(self._config.appname)
        else:
            for appname in ['main', 'app']:
                try:
                    self._imp = importlib.import_module(appname)
                    break
                except ImportError:
                    pass
            else:
                logging.warning('no app found')
        return self._imp

    def register_module(self, cls, name=None):
        if name is None:
            name = cls.__name__
        self._modules[name] = cls

    def register_command(self, cls, name=None):
        if name is None:
            name = cls.__name__
        self._commands[name] = cls

    def load_module(self, name):
        if self._config is None:
            self.load()
        return self._modules[name]

    @property
    def config(self):
        if self._config is None:
            self.load()
        return self._config

    def workspace(self, path=None):
        if path is None:
            path = pathlib.Path(self._cwd).relative_to(self._root) if \
                self._cwd is not None else 'ws/_default'
        return Workspace(self, path)

    def __getattr__(self, key):
        return getattr(self.config, key)

    def main(self, args=None):
        self.register_command(config)
        self.register_command(clean)

        main_parser = _ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog='fret')

        main_parser.add_argument('-w', '--workspace', help='workspace dir')
        main_parser.add_argument('-q', action='store_true', help='quiet')
        main_parser.add_argument('-v', action='store_true', help='verbose')
        main_parser.add_argument('--app', help='app name')

        _subparsers = main_parser.add_subparsers(title='supported commands',
                                                 dest='command')
        _subparsers.required = True

        subparsers = {}
        for _cmd, _cls in self._commands.items():
            _sub = _subparsers.add_parser(
                _cmd, help=_cls.help,
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            subparsers[_cmd] = _sub
            _sub.set_defaults(func=_cls(self, _sub)._run)

        args = main_parser.parse_args() if args is None \
            else main_parser.parse_args(args)

        self.import_modules(args.app)

        # configure logger
        _logger = logging.getLogger()
        if args.q:
            _logger.setLevel(logging.WARNING)
        elif args.v:
            _logger.setLevel(logging.DEBUG)
        else:
            _logger.setLevel(logging.INFO)

        # remove logging related options
        del args.q
        del args.v
        del args.app

        logger = logging.getLogger(args.command)
        try:
            return args.func(args)
        except KeyboardInterrupt:  # pragma: no cover
            # print traceback info to screen only
            import traceback
            sys.stderr.write(traceback.format_exc())
            logger.warning('cancelled by user')
        except NotConfiguredError as e:  # pragma: no cover
            print('error:', e)
            subparsers['config'].print_usage()
            sys.exit(1)
        except Exception as e:  # pragma: no cover
            # print traceback info to screen only
            import traceback
            sys.stderr.write(traceback.format_exc())
            logger.error('exception occurred: %s', e)

    def configurable(self, wraps=None, submodules=None, states=None,
                     initialize_subs=False):
        def wrapper(cls):
            orig_init = cls.__init__
            positional, opt, varkw = _get_args(orig_init)
            if submodules is not None:
                setattr(cls, 'submodules', submodules)

            orig_state_dict = getattr(cls, 'state_dict', lambda _: {})
            orig_load_state_dict = getattr(cls, 'load_state_dict',
                                           lambda *_: None)

            def state_dict(sf):
                if states:
                    d = {k: getattr(sf, s) for s in states}
                else:
                    d = {}
                d.update(orig_state_dict(sf))
                return d

            def load_state_dict(sf, state):
                if states:
                    for s in states:
                        setattr(sf, s, state[s])
                        del state[s]
                orig_load_state_dict(sf, state)

            @classmethod
            def add_arguments(_, parser):
                with ParserBuilder(parser) as builder:
                    for name, spec in opt:
                        builder.add_opt(name, spec)

            def new_init(sf, *args, **kwargs):
                # get config from signature
                allowed_args = set(positional[1:]) | set(x[0] for x in opt)
                cfg = ins.getcallargs(orig_init, sf, *args,
                                      **{_k: _v for _k, _v in kwargs.items()
                                         if _k in allowed_args})
                del cfg['self']

                defaults = {_k: _v for _k, _v in opt}
                for name in defaults:
                    value = cfg[name]
                    if value != defaults[name]._params:
                        continue
                    cfg[name] = defaults[name].default()

                if not hasattr(sf, 'config'):
                    _cfg = cfg.copy()
                    _cfg.update(kwargs)
                    if varkw is not None:
                        del _cfg[varkw]
                    Module.__init__(sf, **_cfg)

                if varkw is None:
                    orig_init(sf, **cfg)
                else:
                    cfg.update(kwargs)
                    orig_init(sf, **cfg)

            # inherit Module methods
            for k, v in Module.__dict__.items():
                if k != '__dict__' and k not in cls.__dict__:
                    setattr(cls, k, v)
            setattr(cls, '__init__', new_init)
            setattr(cls, 'add_arguments', add_arguments)
            setattr(cls, 'state_dict', state_dict)
            setattr(cls, 'load_state_dict', load_state_dict)
            setattr(cls, '_init_subs', initialize_subs)

            if not cls.__name__.startswith('_'):
                self.register_module(cls)
            return cls

        if wraps is None:
            return wrapper
        else:
            return wrapper(wraps)

    def command(self, f):
        positional, opt, _ = _get_args(f)

        @functools.wraps(f)
        def new_f(*args, **kwargs):
            cfg = {k: v.default() for k, v in opt}
            cfg.update(kwargs)
            f_args = {k: v for k, v in zip(positional[1:], args[1:])}
            f_args.update(cfg)
            new_f.args = Configuration(**f_args)
            return f(*args, **cfg)

        class Cmd(Command):
            def __init__(self, _app, parser):
                for arg in positional[1:]:
                    parser.add_argument('-' + arg)
                with ParserBuilder(parser) as builder:
                    for k, v in opt:
                        builder.add_opt(k, v)

            def run(self, ws, args):
                return new_f(ws, **args._asdict())

        Cmd.__name__ = f.__name__
        self.register_command(Cmd)

        return new_f


def _get_args(f):
    spec = ins.getfullargspec(f)
    n_config = len(spec.defaults) if spec.defaults else 0
    args = spec.args if n_config == 0 else spec.args[:-n_config]
    defaults = [v if isinstance(v, argspec) else argspec.from_param(v)
                for v in spec.defaults] if spec.defaults else []
    kwargs = [] if n_config == 0 else \
        [(k, v) for k, v in zip(spec.args[-n_config:], defaults)]
    return args, kwargs, spec.varkw


class argspec:
    """In control of the behavior of commands. Represents arguments for
    :meth:`argparse.ArgumentParser.add_argument`."""

    __slots__ = ['_args', '_kwargs', '_params']

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._params = None

    @classmethod
    def from_param(cls, param):
        kwargs = dict()

        if isinstance(param, tuple):
            assert len(param) == 2 or len(param) == 3, \
                'should be default, help[, choices]'
            kwargs['default'] = param[0]
            kwargs['help'] = param[1]
            if len(param) == 3:
                kwargs['choices'] = param[2]
        elif param is not None:
            kwargs['default'] = param

        if isinstance(kwargs['default'], list):
            if kwargs['default']:
                kwargs['nargs'] = '+'
                kwargs['type'] = type(kwargs['default'][0])
            else:
                kwargs['nargs'] = '*'
        elif isinstance(kwargs['default'], bool):
            if kwargs['default']:
                kwargs['action'] = 'store_false'
            else:
                kwargs['action'] = 'store_true'
        elif kwargs['default'] is not None:
            kwargs['type'] = type(kwargs['default'])

        obj = cls(**kwargs)
        obj._params = param
        return obj

    def default(self):
        return self._kwargs.get('default') or None

    def spec(self):
        return self._args, self._kwargs


class ParserBuilder:
    def __init__(self, parser, style='java'):
        self._parser = parser
        self._style = style
        self._names = []
        self._spec = []

    def add_opt(self, name, spec):
        if spec.default() is True:
            # change name for better bool support
            spec._kwargs['dest'] = name
            name = 'no_' + name
        self._names.append(name)
        self._spec.append(spec)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        prefix = '-' if self._style == 'java' else '--'
        seen = set(self._names)
        for name, spec in zip(self._names, self._spec):
            args, kwargs = spec.spec()
            if not args:
                args = [prefix + name]
                short = ''.join(seg[0] for seg in name.split('_'))
                if short not in seen:
                    args.append('-' + short)
                    seen.add(short)
            else:
                kwargs['dest'] = name
            if 'help' not in kwargs:
                kwargs['help'] = 'parameter ' + name
            self._parser.add_argument(*args, **kwargs)


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        # customize error message
        self.print_usage(sys.stderr)
        err = colored('error:', 'r', style='b')
        self.exit(2, '%s %s\n' % (err, message))


class Command(abc.ABC):
    """Command interface."""
    __slots__ = []

    @classproperty
    def help(cls):
        return 'command ' + cls.__name__.lower()

    def _run(self, args):
        ws = get_app().workspace(args.workspace)
        cmd = args.command
        del args.command, args.func, args.workspace
        args = {name: value for (name, value) in args._get_kwargs()}
        args = namedtuple(cmd, args.keys())(*args.values())
        return self.run(ws, args)

    @abc.abstractmethod
    def run(self, ws, args):
        raise NotImplementedError


class config(Command):
    """Command ``config``,

    Configure a module and its parameters for a workspace.

    Example:
        .. code-block:: bash

            $ python app.run -w ws/test config Simple -foo=5
            In [ws/test]: configured Simple with Config(foo='5')
    """

    help = 'configure module for workspace'

    def __init__(self, app, parser):
        parser.add_argument('name', default='main', nargs='?',
                            help='module name')
        if sys.version_info < (3, 7):
            subs = parser.add_subparsers(title='modules available',
                                         dest='module')
        else:
            subs = parser.add_subparsers(title='modules available',
                                         dest='module', required=False)
        group_options = collections.defaultdict(set)
        try:
            _modules = app._modules
        except ImportError:
            _modules = {}

        for module, module_cls in _modules.items():
            _parser_formatter = argparse.ArgumentDefaultsHelpFormatter
            sub = subs.add_parser(module, help=module_cls.help,
                                  formatter_class=_parser_formatter)
            group = sub.add_argument_group('config')
            module_cls._add_arguments(group)
            for action in group._group_actions:
                group_options[module].add(action.dest)

            def save(args):
                with get_app().workspace(args.workspace) as ws:
                    m = args.module
                    cfg = [(name, value)
                           for (name, value) in args._get_kwargs()
                           if name in group_options[m]]
                    cfg = Configuration(cfg)
                    msg = '[%s] configured "%s" as "%s"' % \
                        (ws, args.name, m)
                    if cfg._config:
                        msg += ' with: ' + str(cfg)
                    print(msg, file=sys.stderr)
                    ws.register(args.name, get_app().load_module(m),
                                **cfg._dict())

            sub.set_defaults(func=save)

    def run(self, ws, args):
        cfg = ws.config_path
        if cfg.exists():
            cfg = cfg.open().read().strip()
            print(cfg)
            return cfg
        else:
            raise NotConfiguredError('no configuration in this workspace')


class clean(Command):
    """Command ``clean``.

    Remove all checkpoints in specific workspace. If ``--all`` is specified,
    clean the entire workspace
    """

    help = 'clean workspace'

    def __init__(self, _, parser):
        parser.add_argument('--all', action='store_true',
                            help='clean the entire workspace')
        parser.add_argument('-c', dest='config', action='store_true',
                            help='remove workspace configuration')
        parser.add_argument('-l', dest='log', action='store_true',
                            help='clear workspace logs')
        parser.add_argument('-s', dest='snapshot', action='store_true',
                            help='clear snapshots')

    def run(self, ws, args):
        if args.all:
            shutil.rmtree(str(ws))
        else:
            if (not args.config and not args.log) or args.snapshot:
                shutil.rmtree(str(ws.snapshot()))
            if args.snapshot:
                shutil.rmtree(str(ws.snapshot()))
            if args.config:
                try:
                    (ws.path / 'config.toml').unlink()
                except FileNotFoundError:
                    pass
            if args.log:
                shutil.rmtree(str(ws.log()))


_app = App()


def get_app():
    """Get current global app."""
    return _app


def set_global_app(app):
    """Set current global app."""
    global _app
    _app = app


def workspace(*args, **kwargs):
    """Build workspace within current app."""
    return get_app().workspace(*args, **kwargs)


def configurable(*args, **kwargs):
    return get_app().configurable(*args, **kwargs)


def command(*args, **kwargs):
    return get_app().command(*args, **kwargs)


__all__ = ['get_app', 'set_global_app', 'argspec', 'App',
           'workspace', 'configurable', 'command']
