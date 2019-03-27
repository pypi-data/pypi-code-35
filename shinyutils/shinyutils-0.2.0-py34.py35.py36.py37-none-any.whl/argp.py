"""argp.py: utilities for argparse."""

from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentTypeError,
    MetavarTypeHelpFormatter,
    FileType,
)
import logging
import os
import re

import crayons


class LazyHelpFormatter(
    ArgumentDefaultsHelpFormatter, MetavarTypeHelpFormatter
):

    # pylint: disable=no-member
    DEF_PAT = re.compile(r"(\(default: (.*?)\))")
    TYPE_PAT = re.compile(r"(?<![\w-])int|str|float(?![\w-])")
    DEF_CSTR = str(crayons.magenta("default"))

    def _format_action(self, action):
        if not action.help:
            action.help = "\b"
        astr = super()._format_action(action)

        m = re.search(self.DEF_PAT, astr)
        if m:
            mstr, dstr = m.groups()
            astr = astr.replace(
                mstr, f"({self.DEF_CSTR}: {crayons.magenta(dstr, bold=True)})"
            )

        return re.sub(
            self.TYPE_PAT,
            lambda s: str(crayons.red(s.group(), bold=True)),
            astr,
        )

    def _get_default_metavar_for_optional(self, action):
        if action.type:
            return action.type.__name__

    def _get_default_metavar_for_positional(self, action):
        if action.type:
            return action.type.__name__

    def __init__(self, *args, **kwargs):
        if "max_help_position" not in kwargs:
            kwargs["max_help_position"] = float("inf")
        if "width" not in kwargs:
            kwargs["width"] = float("inf")
        super().__init__(*args, **kwargs)


def comma_separated_ints(string):
    try:
        return list(map(int, string.split(",")))
    except:
        raise ArgumentTypeError(
            f"`{string}` is not a comma separated list of ints"
        )


class OutputFileType(FileType):
    def __init__(self, *args, **kwargs):
        super().__init__("w", *args, **kwargs)

    def __call__(self, string):
        file_dir = os.path.dirname(string)
        if not os.path.exists(file_dir):
            logging.warning(f"no directory for {string}: trying to create")
            try:
                os.makedirs(file_dir)
            except Exception as e:
                raise ArgumentTypeError(f"could not create {file_dir}: {e}")
            logging.info(f"created {file_dir}")
        return super().__call__(string)


class OutputDirectoryType:
    def __call__(self, string):
        if not os.path.exists(string):
            logging.warning(f"{string} not found: trying to create")
            try:
                os.makedirs(string)
            except Exception as e:
                raise ArgumentTypeError(f"cound not create {string}: {e}")
            logging.info(f"created {string}")
        return string
