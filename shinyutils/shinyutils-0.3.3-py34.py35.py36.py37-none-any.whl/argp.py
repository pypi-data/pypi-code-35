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

from shinyutils.subcls import get_subclass_from_name


class LazyHelpFormatter(
    ArgumentDefaultsHelpFormatter, MetavarTypeHelpFormatter
):

    # pylint: disable=no-member
    DEF_PAT = re.compile(r"(\(default: (.*?)\))")
    DEF_CSTR = str(crayons.magenta("default"))

    def _format_action(self, action):
        if action.dest == "help":
            return ""

        helpstr = action.help
        action.help = "\b"

        if action.nargs == 0:
            # hack to fix length of option strings
            action.option_strings = [
                s + str(crayons.normal("", bold=True))
                for s in action.option_strings
            ]
        astr = super()._format_action(action)

        m = re.search(self.DEF_PAT, astr)
        if m:
            mstr, dstr = m.groups()
            astr = astr.replace(
                mstr, f"({self.DEF_CSTR}: {crayons.magenta(dstr, bold=True)})"
            )

        if helpstr:
            astr += f"\t{helpstr}\n"

        return astr

    def _get_default_metavar_for_optional(self, action):
        if action.type:
            try:
                return action.type.__name__
            except AttributeError:
                return type(action.type).__name__
        return None

    def _get_default_metavar_for_positional(self, action):
        if action.type:
            try:
                return action.type.__name__
            except AttributeError:
                return type(action.type).__name__
        return None

    def _metavar_formatter(self, action, default_metavar):
        base_formatter = super()._metavar_formatter(action, default_metavar)

        def color_wrapper(tuple_size):
            f = base_formatter(tuple_size)
            return tuple(str(crayons.red(s, bold=True)) for s in f)

        return color_wrapper

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


class ClassType:
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, string):
        try:
            return get_subclass_from_name(self.cls, string)
        except Exception as e:
            raise ArgumentTypeError(e)
