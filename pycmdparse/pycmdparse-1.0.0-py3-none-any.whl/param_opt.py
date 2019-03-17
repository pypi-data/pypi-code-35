from pycmdparse.abstract_opt import AbstractOpt
from pycmdparse.cmdline_exception import CmdLineException
from pycmdparse.multitype_enum import MultiTypeEnum
from pycmdparse.opt_acceptresult_enum import OptAcceptResultEnum


class ParamOpt(AbstractOpt):
    """
    Implements a parameterized option taking one or more parameters. E.g. "-f file",
    "-f file1 file2'. Supports multiple parameter values as indicated by the
    'multi_type' and 'count' fields. There are three multi option types, as indicated
    by the multi_type constructor arg, which is a MultiTypeEnum enum.

    MultiTypeEnum values:

    EXACTLY
    For this kind, as soon as the specified count of params is pulled from the cmd line
    stream, initialization of the option completes. The param values are not inspected
    and so - can look like options. E.g., if count is 2 and the command line is:

    "my-utility --files foo --bar p1 p2"

    Then this would result in the 'files' option having parameters: ['foo', '--bar']
    and - assuming no other defined options - the positional params would be
    ['p1', 'p2']. Note that for this type - if the command line doesn't contain the
    required number of params, then it is a parse error. E.g., this is a parse error,
    if the param is defined as EXACTLY 3:

    "my-utility --files foo bar"

    AT_MOST
    For this kind, the parser attempts to pull up to the specified count of parameters
    and the presence of an option terminates consumption of tokens from the command
    line. E.g.: if count is 4, and the command line is:

    "my-utility --multi-files foo --bar p1 p2"

    Then this would result in the multi-files option having parameters ['foo']. Then
    parsing would continue with --bar. If there's a --bar option defined then good,
    else it's a parse error.

    NO_LIMIT
    This pulls parameters from the command line until the next option is encountered
    (a token starting with dash) or the positional param option ("--") is encountered.
    If at the end of the command line stream, this can consume the positional params
    too. I.e., given this command line:

    "my-utility --multi-files foo bar p1 p2"

    The result would be the multi-files option having parameters ['foo', 'bar',
    'p1', 'p2'] and the positional parameters being empty. If the utility requires
    positional params, none would be available. To prevent that, the command line
    would need to look like:

    "my-utility --multi-files foo bar -- p1 p2"

    If the multi-type is not specified in the yaml, then it defaults to EXACTLY 1.
    If the type is EXACTLY 1 - either by fallback as described or by explicit
    initialization, then the param value is provided as a scalar. In all other cases,
    the param value is provided as a list - which could be empty, but will never be
    'None'.

    For options of this type, the following command line forms produce the same
    parse result:

    "-f A B C", and "-f A -f B -f C" both result in the "-f" option having params
    value: ['A','B','C']
    """

    @property
    def multi_type(self):
        return self._multi_type

    @property
    def count(self):
        return self._count

    def __init__(self, opt_name, short_key, long_key, opt_hint, required, is_internal,
                 default_value, multi_type, count, data_type, help_text):
        # enforce the default value to be stored internally as a list
        if default_value and not isinstance(default_value, list):
            default_value = [default_value]
        super().__init__(opt_name, short_key, long_key, opt_hint, required,
                         is_internal, default_value, data_type, help_text)
        self._multi_type = multi_type if multi_type else MultiTypeEnum.EXACTLY
        self._count = 1 if not multi_type or not count else count
        self._value = []
        # validate defaults against instance data type
        if not self._ensure_data_type(self._default_value):
            raise CmdLineException("Data type does not match specification: {}"
                                   .format(self._default_value))
        if self._default_value and \
            self._multi_type in [MultiTypeEnum.AT_MOST, MultiTypeEnum.EXACTLY] \
            and len(self._default_value) > self._count:
            raise CmdLineException("Invalid defaults supplied: {}"
                                   .format(self._default_value))

    @property
    def value(self):
        """
        :return: If the type is EXACTLY, and the specified count is one, then return
        the value as a scalar. (It's more natural to get the value from a single-param
        option as a scalar than to constantly have to access it as my_field[0].) If
        the type is not multi, or the count is not zero, then return a list of
        values - which could be empty.
        """
        to_return = self._value if self._initialized and self._from_cmdline \
            else self._default_value
        if self._multi_type is MultiTypeEnum.EXACTLY and self._count == 1:
            return to_return[0] if to_return and len(to_return) == 1 else None
        return [] if not to_return else to_return

    def _do_accept(self, stack):
        """
        Based on the multi-type, pull tokens from the command line to initialize
        the options.

        :param stack: the command line. Expection is the stack is positioned at the
        command line arg matching this option

        :return: A tuple. Element zero is OptAcceptResultEnum.ACCEPTED if no parse
        errors, else OptAcceptResultEnum.ERROR. Element one is an error message if
        element zero is ERROR
        """
        if stack.size() < 2:
            return OptAcceptResultEnum.ERROR, "{}: requires a value, which "\
                                              "was not supplied"\
                .format(self._opt_name)
        self._supplied_key = stack.pop()
        while stack.size() > 0:
            if stack.peek().startswith("-")\
                    and self._multi_type is not MultiTypeEnum.EXACTLY:
                # next option terminates param collection unless it's an
                # exact count param
                break
            if self._multi_type in [MultiTypeEnum.AT_MOST,
                                    MultiTypeEnum.EXACTLY] and \
                    len(self._value) == self._count:
                break
            self._value.append(stack.pop())
        return OptAcceptResultEnum.ACCEPTED,

    def _ensure_data_type(self, values):
        """
        Ensures that the values in the passed list conform to the object's data
        type

        :param values: a list of values to inspect. If the list is non-empty, values
        in the list might be modified. E.g. if the class is INT and list is
        ['123', '456'] then it will be modified to contain [123, 456]

        :return: True if a) the object has a defined data type, and the object values
        are in conformance - or b) the object has no defined type, or c) there are
        no values to validate. Returns False if the object has a defined type and
        the passed values list contains something to validate, and something in the
        list is not in conformance with the data type.
        """
        if self._data_type and values:
            for i, v in enumerate(values):
                tmp = self._validate_datatype(v)
                if not tmp:
                    return False
                values[i] = tmp
        return True

    def do_final_validate(self):
        """
        Handle data type conversion, and param count verification since options can be
        provided multiple times on the command line. E.g. "-f A -f B -f C" is the
        same as "-f A B C"

        :return: a tuple: element zero is an OptAcceptResultEnum value, element
        one is an error message if element zero is OptAcceptResultEnum.ERROR
        """

        if len(self._value) == 0:
            # nothing from the command line - caller must handle
            return OptAcceptResultEnum.IGNORED,

        if self._multi_type is MultiTypeEnum.EXACTLY \
                and len(self._value) != self._count:
            return OptAcceptResultEnum.ERROR,\
                   "{}: expected {} parameter(s) but found {}".format(
                       self._supplied_key, self._count, len(self._value))

        if not self._ensure_data_type(self._value):
            return OptAcceptResultEnum.ERROR,\
                   "{}: {} has incorrect data type. Expected {}".format(
                       self._supplied_key, self._value, self._data_type.tostr())

        self._initialized = True
        self._from_cmdline = True
        return OptAcceptResultEnum.ACCEPTED,
