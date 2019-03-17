#!/usr/bin/env python
# -*- coding: utf8 -*-
import logging
import os
import sys
import click
import sentry_sdk
# DON'T PUT HERE ANY MISSINGLINK import directly, use local imports


def _setup_logger(log_level):
    if not log_level:
        return

    log_level = log_level.upper()

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    handler = logging.StreamHandler(stream=sys.stderr)
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    logging_method = getattr(root_logger, log_level.lower())
    logging_method('log level set to %s (this is a test message)', log_level)


def main():
    os.environ['MISSINGLINKAI_DISABLE_EXCEPTION_HOOK'] = '1'
    os.environ['MISSINGLINKAI_DISABLE_LOGGING_HOOK'] = '1'

    from missinglink.commands import add_commands, cli
    from missinglink.commands.global_cli import self_update, set_pre_call_hook
    from missinglink.commands.mali_version import MissinglinkVersion
    from missinglink.core.exceptions import MissingLinkException
    from missinglink.legit.gcp_services import GooglePackagesMissing, GoogleAuthError

    def setup_pre_call(ctx):
        if ctx.obj.log_level is not None:
            _setup_logger(ctx.obj.log_level)

        with sentry_sdk.configure_scope() as cli_scope:
            token_data = ctx.obj.config.token_data

            cli_scope.set_tag('command', ctx.invoked_subcommand)
            cli_scope.user = {'id': token_data.get('uid'), 'email': token_data.get('email'), 'username': token_data.get('name')}

    def setup_sentry_sdk():
        cli_version = MissinglinkVersion.get_missinglink_cli_version()

        is_dev_version = cli_version is None or cli_version.startswith('0')
        if is_dev_version:
            return

        sentry_sdk.init(
            'https://604d5416743e430b814cd8ac79103201@sentry.io/1289799',
            release=cli_version)

        with sentry_sdk.configure_scope() as scope:
            scope.set_tag('source', 'ml-cli')

    setup_sentry_sdk()
    set_pre_call_hook(setup_pre_call)

    if sys.argv[0].endswith('/mali') and not os.environ.get('ML_DISABLE_DEPRECATED_WARNINGS'):
        click.echo('instead of mali use ml (same tool with a different name)', err=True)

    if os.environ.get('MISSINGLINKAI_ENABLE_SELF_UPDATE'):
        self_update()

    add_commands()
    try:
        cli()
    except GooglePackagesMissing:
        click.echo('you to run "pip install missinglink[gcp]" in order to run this command', err=True)
    except GoogleAuthError:
        click.echo('Google default auth credentials not found, run gcloud auth application-default login', err=True)
    except MissingLinkException as ex:
        click.echo(ex, err=True)


if __name__ == "__main__":
    main()
