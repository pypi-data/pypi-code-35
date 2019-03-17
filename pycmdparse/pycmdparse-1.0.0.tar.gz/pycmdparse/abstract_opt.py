import datetime
import re
from abc import ABC, abstractmethod

from pycmdparse.cmdline_exception import CmdLineException
from pycmdparse.datatype_enum import DataTypeEnum
from pycmdparse.opt_acceptresult_enum import OptAcceptResultEnum


class AbstractOpt(ABC):
    """
    Provides the basic functionality to parse and store a value from the
    command line. Must be subclassed to provide specific functionality.
    """

    def __init__(self, opt_name, short_key, long_key, opt_hint, required,
                 is_internal, default_value, data_type, help_text):
        """
        Instance initializer for an option. Sets instance fields from passed
        values and performs some basic state initialization.

        :param opt_name: this is a valid Python identifier for the option. See
        'Determining the option name' further down.
        :param short_key: E.g. "v", for "-v"
        :param long_key: E.g. "verbose", for "--verbose"
        :param opt_hint: For options accepting params, this is a mnemonic for the user
        that is presented in the usage instructions. E.g. if the usage instructions for
        the option looks like this: "-f,--filenane <pathspec>" then "pathspec" is the
        hint.
        :param required: True if the option must be supplied on the command line, else
        False. Default is false.
        :param is_internal: If True, then this is an internal option and doesn't
        appear on the usage instructions. Default is false.
        :param default_value: A default value. Ignored if this is a mandatory option.
        (It wouldn't make sense to require the user to provide an option on the
        command line but then specify a default value for that option.)
        :param data_type: Supports rudimentary data type validation. Expects a
        DataTypeEnum object
        :param help_text: Help text for the option

        Determining the option name: after an option is parsed, its value is injected
        into the CmdLine subclass running the arg parser. The Python identifier that
        is used to hold the option value is the first non-null, in order, from:
        opt_name, long_key, short_key. So, to further abbreviate the yaml, if the
        option key is also a valid Python identifier, then the name element of the
        option in the yaml can be omitted. E.g. for option '--verbose', the injected
        field name would be 'verbose'. For option '--file-name', it would be
        'file_name' because dashes are converted to underlines by this process.
        The short-form is the lowest precedence. A field named 'v', for example,
        is legal, if not readable, but is supported. An invalid Python identifier
        raises an exception.

        """
        if not long_key and not short_key:
            raise CmdLineException("YAML must specify 'short' or 'long' "
                                   "option key")
        if short_key and len(short_key) != 1:
            raise CmdLineException("Invalid short key: '{}'".format(short_key))

        self._opt_name = next(e for e in [opt_name, long_key, short_key] if e)\
            .replace('-', '_')
        self._short_key = short_key
        self._long_key = long_key
        self._opt_hint = opt_hint
        self._required = required
        self._is_internal = is_internal
        self._default_value = default_value
        self._data_type = data_type
        self._help_text = help_text
        self._value = None
        if not required and default_value:
            # an optional param with a default is immediately considered initialized
            self._initialized = True
        else:
            # if required, ignore the default value because the option must be
            # provided on the command line or the arg parser will return a parse error
            self._initialized = False
        # the option actually encountered on the command line (e.g. "-f", or
        # "--filename"):
        self._supplied_key = None
        self._from_cmdline = False

    def __repr__(self):
        s = "opt_name: {} short_key: {}; long_key: {}; value: {}; required: {}; " \
            "hint: {}; is_internal: {}; initialized: {}; default value: {}; " \
            "data_type: {}; help_text: {}"
        return s.format(self._opt_name, self._short_key, self._long_key, self._value,
                        self._required, self._opt_hint, self._is_internal,
                        self._initialized, self._default_value, self._data_type,
                        self._help_text)

    @property
    def opt_name(self):
        return self._opt_name

    @property
    def short_key(self):
        return self._short_key

    @property
    def long_key(self):
        return self._long_key

    @property
    def keys_and_hint(self):
        """
        Returns the keys and the hint for an option, formatted for help. The hint is
        a token or mnemonic that briefly lets the user know what parameter is expected
        for an option.

        :return: E.g.: if short key is "f" and long key is "file-name", and hint is
        "pathspec", then returns: "-f,--file-name <pathspec>". If short key is "a"
        and long key is "action", and hint is is "upload|download", then returns:
        "-a,--action <upload|download>". If short key is "t" and long key is
        "timeout", and hint is is "n", then returns: "-t,--timeout <n>". Etc.
        """
        s = ""
        if self._short_key:
            s += "-" + self._short_key
        if self._long_key:
            s += "" if len(s) == 0 else ","
            s += "--" + self._long_key
        if self._opt_hint:
            s += " <" + self._opt_hint + ">"
        return s

    @property
    def initialized(self):
        """
        This property indicates whether an option has been assigned a value.

        For boolean options, return is always true because boolean options are
        initialized to have a value of False, and then the value is set to True if the
        option is specified on the command line. So either way, a boolean is
        initialized.

        Param options behave differently: A mandatory param option is initialized only
        if supplied on the command line. Otherwise it is not initialized.

        A non-mandatory option is initialized if a default was specified in the yaml,
        or, the option and parameter was provided on the command line. The setup for
        this is handled in the constructor, and in the accept and do_final_validate
        functions. This getter just returns the result of that adjudication.
        """
        return self._initialized

    @property
    def required(self):
        return self._required

    @property
    def opt_hint(self):
        return self._opt_hint

    @property
    def default_value(self):
        return self._default_value

    @property
    def data_type(self):
        return self._data_type

    @property
    def help_text(self):
        return self._help_text

    @property
    def is_internal(self):
        return self._is_internal

    @property
    def supplied_key(self):
        return self._supplied_key

    @property
    def from_cmdline(self):
        return self._from_cmdline

    @property
    @abstractmethod
    def value(self):
        pass

    @property
    def option_keys(self):
        """
        Returns the keys formatted for usage help.

        :return: E.g. if short key is "-f" and long key is "--filename" then returns
        "-f,--filename". If only one or the other of short or long key is defined,
        then returns only that part.
        """
        to_return = ""
        if self._short_key:
            to_return += "-" + self._short_key
        if self._long_key:
            to_return += "/" if len(to_return) > 0 else ""
            to_return += "--" + self._long_key
        return to_return

    def accept(self, stack):
        """
        If the token on the top of the stack matches the short or long key for the
        option, then processes the token from the stack, delegating processing to a
        sub-class. If the option is successfully processed, then the sub-class is
        expected to consume all its tokens, so the stack is positioned at the next
        token so parsing can continue.

        :param stack: the command line stack

        :return: a tuple: element zero is an OptAcceptResultEnum value, element
        one is an error message if element zero is OptAcceptResultEnum.ERROR
        """
        if stack.size() == 0:
            return OptAcceptResultEnum.IGNORED,
        if not re.compile("-{1,2}\\w").match(stack.peek()):
            # only match options starting with dash or double dash. (Triple-
            # dash is ignored)
            return OptAcceptResultEnum.IGNORED,
        if stack.peek().lstrip("-") in [self._short_key, self._long_key]:
            return self._do_accept(stack)
        return OptAcceptResultEnum.IGNORED,

    @abstractmethod
    def do_final_validate(self):
        """
        After all command line args parsed, give options a chance to do final
        validation. Supports scenario like "my-util -f VAL1 -f VAL2 -f VAL3. Now,
        the '-f' opt has three values. Is that ok? Can't do the check until the entire
        command line has been parsed

        :return: a tuple: element zero is an OptAcceptResultEnum value, element one is
        an error message if element zero is OptAcceptResultEnum.ERROR
        """
        pass

    def _validate_datatype(self, val):
        """
        The the option has a data type (which is not required) then validates that the
        option value matches the specified data type. Only very basic typing is
        supported: integers, floating point, and a rudimentary date. Anything beyond
        that would need to be handled by the utility via the validation callback.

        :param val: the option value to validate

        :return: the passed value, converted to the object data type, if a data type
        is defined. If a data type is not defined, then returns None. If a data type
        is defined and the value doesn't match the type, then returns None.
        """
        if self._data_type is DataTypeEnum.BOOL:
            if isinstance(val, bool):
                return val
            try:
                return bool(val)
            except ValueError:
                return None
        elif self._data_type is DataTypeEnum.INT:
            if isinstance(val, int):
                return val
            try:
                return int(val)
            except ValueError:
                return None
        elif self._data_type is DataTypeEnum.DECIMAL:
            if isinstance(val, float):
                return val
            try:
                return float(val)
            except ValueError:
                return None
        elif self._data_type is DataTypeEnum.DATE:
            if isinstance(val, datetime.date) or isinstance(val, datetime.datetime):
                if isinstance(val, datetime.datetime):
                    return val.date()
                else:
                    return val
            try:
                return AbstractOpt._parse_date(val)
            except ValueError:
                return None
        return None

    @staticmethod
    def _parse_date(value):
        """
        Provides a really rudimentary date parser. Accepts YYYY-MM-DD and MM-DD-YYYY
        with separators of dash, period, or forward slash.

        :param value: a string to convert to a date

        :return: a datetime.date object if the conversion could be performed,
        otherwise None
        """
        patterns = {
            "^[0-9]{2,4}([-/\\.])[0-9]{1,2}([-/\\.])[0-9]{1,2}$": "%Y1%m2%d",
            "^[0-9]{1,2}([-/\\.])[0-9]{1,2}([-/\\.])[0-9]{2,4}$": "%m1%d2%Y"
        }
        for pattern in patterns.keys():
            p = re.compile(pattern)
            g = p.match(value)
            if g and len(g.groups()) == 2:
                to_return = patterns[pattern].replace("1", g.groups()[0])\
                    .replace("2", g.groups()[1])
                return datetime.datetime.strptime(value, to_return).date()
        return None

    @abstractmethod
    def _do_accept(self, stack):
        """
        Subclass-specific option handling

        :param stack: the command line stack. Subclass is expected to leave the stack
        ready for the next option to parse - meaning all tokens on the stack that
        belong to the option have been popped.

        :return: a tuple: element zero is an OptAcceptResultEnum value, element
        one is an error message if element zero is OptAcceptResultEnum.ERROR
        """
        pass
