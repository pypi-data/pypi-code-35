import yaml

from pycmdparse.class_property import classproperty, classproperty_support
from pycmdparse.cmdline_exception import CmdLineException
from pycmdparse.opt_acceptresult_enum import OptAcceptResultEnum
from pycmdparse.opt_category import OptCategory
from pycmdparse.opt_factory import OptFactory
from pycmdparse.parseresult_enum import ParseResultEnum
from pycmdparse.positional_params import PositionalParams
from pycmdparse.showinfo import ShowInfo
from pycmdparse.splitter import Splitter
from pycmdparse.usage_example import UsageExample


@classproperty_support
class CmdLine:
    """
    Provides the top-level functionality for the package. Usage:
    1) Import the package
    2) Sub-class this class
    3) Initialize the 'yaml_def' field in the subclass with a
       yaml definition of option/param/usage requirements
    4) Call the 'parse()' function to parse the command line. If successful, the
       function injects fields into the subclass - one for each option defined in
       the yaml spec.
    5) Access the fields injected into the subclass to get the values provided by
       the user on the command line
    6) If there is an error parsing the command line, use the class to display the
       errors, or, display usage instructions as defined in the yaml
    """

    yaml_def = None
    """A yaml string that defines the parsing rqts. and usage instructions"""

    _utility_name = None
    """The name of the program or utility that is importing the module"""

    _require_args = None
    """True if the utility requires at least one command line arg"""

    _summary = None
    """A very short summary that captures the key purpose of the utility"""

    _usage = None
    """
    If None, then usage will be generated by the module from options and positional
    params. Otherwise specifies a abbreviated 'quick start' usage guidance
    """

    _positional_params = None
    """
    After all options and option parameters are parsed, or, after '--' is encountered,
    everything else is a positional param. Stored in a PositionalParams object
    """

    _supported_options = None
    """
    A collection of supported options. The structure is a list of OptCategory objects,
    each of which contains a list of AbstractOpt-subclassed objects. Each AbstractOpt
    object defines the behavior of a command-line option/parameter. The parser uses
    the "name" field from each AbstractOpt object to inject a field - with that name
    - into the subclass of this class. The utility code can then reference the command
    line option value using this injected field.

    E.g., say an option was -'f' for 'file name'. Specifying 'filename' as the option
    name would result in a field named 'filename' being added to the class. Say the
    user - when running the enclosing program - specified 'f=/my-file.tar' on the
    command line. After successful command-line parsing, the enclosing utility code
    would be able to rely on the existence of a field named 'filename' in this class
    having value '/my-file.tar'.
    """

    _details = None
    """
    A section to provide additional, perhaps more technical, content below the usage
    and options sections
    """

    _examples = None
    """
    A List of UsageExample objects, providing useful examples on how to run the
    enclosing program with common sets of options to solve common problems.
    """

    _addendum = None
    """
    Free-form text after the examples. Used for copyright, licensing, bug report URLs,
    author information, Github URL, website URLs, etc.
    """

    _parse_errors = None
    """
    Initialized by the parser with any errors encountered during
    command-line parsing
    """

    # noinspection PyMethodParameters
    @classproperty
    def parse_errors(cls):
        """
        :return:  the parse errors as a list. Could be empty. Never None
        """
        return cls._parse_errors

    # noinspection PyMethodParameters
    @classproperty
    def positional_params(cls):
        """
        :return:  the positional params as a list. Could be empty. Never None
        """
        return cls._positional_params.params if cls._positional_params else []

    @classmethod
    def reset(cls):
        """
        Supports testing. Nulls the class object's fields
        """
        cls._positional_params = None
        cls._supported_options = None
        cls._details = None
        cls._addendum = None
        cls._examples = None
        cls._usage = None
        cls._summary = None
        cls._utility_name = None
        cls._require_args = None
        cls._parse_errors = None
        # don't reset the yaml def - it might be being reused for a test

    @classmethod
    def get_option(cls, option_name):
        """
        Gets an option using the name defined in the yaml path:
        category.options[n].name. Provided in case there is a need to access
        option metadata.

        :param option_name: As specified in the option's "name" field in the yaml

        :return: the option object if one exists by the passed name, else None
        """
        flattened_options = CmdLine._flatten(cls._supported_options)
        for opt in flattened_options:
            if opt.opt_name == option_name:
                return opt
        return None

    @classmethod
    def display_info(cls, parse_result):
        """
        Shows usage, or shows errors, based on the passed parse_result arg. If the
        passed value indicates a parse error, then displays the errors in the internal
        class errors collection. If the passed value indicates to show usage
        instructions (e.g. if -h was provided on the command line) then shows the
        usage instructions defined in the yaml that was used to initialize the class.

        :param parse_result: the result of a prior command line parse operation
        """
        if parse_result in [ParseResultEnum.PARSE_ERROR,
                            ParseResultEnum.MISSING_MANDATORY_ARG]:
            if cls._parse_errors and len(cls._parse_errors) > 0:
                ShowInfo.show_errors(cls._parse_errors, cls._utility_name)
        elif parse_result is ParseResultEnum.SHOW_USAGE:
            cls.show_usage()

    @classmethod
    def show_usage(cls):
        """
        Shows full usage instructions (mainly to support test)
        """
        ShowInfo.show_usage(cls._utility_name, cls._summary, cls._usage,
                            cls._supported_options, cls._details, cls._examples,
                            cls._positional_params, cls._addendum)

    @classmethod
    def parse(cls, cmd_line):
        """
        Entry point for the class. Parses the yaml in the 'yaml_def' class field to
        initialize associated class fields, then parses the passed command line
        against the options defined by the yaml. If all is successful then adds one
        field to the class for each defined option, and initializes that field with
        the parameter specified on the command line for the option. (Or, for boolean
        options that don't take parameters, sets those values to True or False.)

        :param cmd_line: Can be a single string, which the function tokenizes and
        processes, or, can be a list, like the Python interpreter provides in
        sys.argv. The first element is expected to be the invoking utility name.
        This element is ignored by the parser.

        :return: a ParseResultEnum, indicating the results of the command-line parse.
        """
        cls._init_from_yaml()
        has_options = True if cls._supported_options else False
        if type(cmd_line) is str:
            cmdline_stack = Splitter.split_str(cmd_line, has_options)
        elif type(cmd_line) is list:
            cmdline_stack = Splitter.split_list(cmd_line, has_options)
        else:
            raise CmdLineException("Can only parse a string or a list")
        if cmdline_stack.size() == 1 and cls._require_args:
            # if there are no command line args, but the class wants them, then
            # return SHOW PARSE_ERROR
            cls._append_error("At least one option or param is required")
            return ParseResultEnum.PARSE_ERROR
        cmdline_stack.pop()  # discard - arg 0 is utility name
        return cls._parse(cmdline_stack)

    @classmethod
    def _parse(cls, cmdline_stack):
        """
        Actually does the command line parsing.

        :param cmdline_stack: as built from the command line. Left at top, right
        at bottom

        :return: a ParseResultEnum object indicating the result of the parse
        """
        flattened_options = CmdLine._flatten(cls._supported_options)
        if len(flattened_options) > 0:
            # if empty, then no options, so all command-line args are
            # positional params
            while cmdline_stack.size() > 0:
                if cmdline_stack.peek().lower() in ["-h", "--help"]:
                    return ParseResultEnum.SHOW_USAGE
                if cmdline_stack.peek() == "--":
                    cmdline_stack.pop()
                    cls._handle_positional_params(cmdline_stack)
                    break
                accept_result = OptAcceptResultEnum.IGNORED,
                for supported_option in flattened_options:
                    accept_result = supported_option.accept(cmdline_stack)
                    if accept_result[0] is not OptAcceptResultEnum.IGNORED:
                        break
                if accept_result[0] is OptAcceptResultEnum.IGNORED:
                    if not cmdline_stack.peek().startswith("-"):
                        if not cmdline_stack.has_options():
                            cls._handle_positional_params(cmdline_stack)
                            break
                        else:
                            cls._append_error("Unsupported option: '{0}'".
                                              format(cmdline_stack.peek()))
                            return ParseResultEnum.PARSE_ERROR
                    else:
                        cls._append_error("Unsupported option: '{0}'".
                                          format(cmdline_stack.peek()))
                        return ParseResultEnum.PARSE_ERROR
                elif accept_result[0] is OptAcceptResultEnum.ERROR:
                    cls._append_error(accept_result[1])
                    return ParseResultEnum.PARSE_ERROR

        if cmdline_stack.size() > 0:
            cls._handle_positional_params(cmdline_stack)

        if cmdline_stack.size() > 0:
            cls._append_error("Arg parse error at: {0}".format(
                cmdline_stack.pop_all()))
            return ParseResultEnum.PARSE_ERROR

        for supported_option in flattened_options:
            accept_result = supported_option.do_final_validate()
            if accept_result[0] is OptAcceptResultEnum.ERROR:
                cls._append_error(accept_result[1])
                return ParseResultEnum.PARSE_ERROR

        missing = [opt for opt in flattened_options if opt.required
                   and not opt.initialized]

        if len(missing) != 0:
            cls._append_error("Mandatory option(s) not provided: {0}".format(
                [opt.option_keys for opt in missing]))
            return ParseResultEnum.MISSING_MANDATORY_ARG

        # A callback can be defined in the subclass to perform customized validation
        # of positional params - and - individual options on the command line. The
        # function must return a tuple: element zero is an # OptAcceptResultEnum
        # value, and element one is an error message to display to the user if
        # element zero is 'ERROR'

        if hasattr(cls, 'validator') and callable(cls.validator):
            for supported_option in flattened_options:
                accept_result = cls.validator(supported_option)
                if accept_result[0] is OptAcceptResultEnum.ERROR:
                    cls._append_error(accept_result[1])
                    return ParseResultEnum.PARSE_ERROR

            accept_result = cls.validator(cls._positional_params)
            if accept_result[0] is OptAcceptResultEnum.ERROR:
                cls._append_error(accept_result[1])
                return ParseResultEnum.PARSE_ERROR

        # all is good: inject fields into the subclass - one for each option - and
        # set their values as parsed from the command line
        cls._add_fields()
        return ParseResultEnum.SUCCESS

    @staticmethod
    def _flatten(supported_opts):
        """
        Supported options are stored as lists, within categories. This reads all the
        option objects from the categories, and returns them as a single list, to
        avoid needing to constantly traverse the categories to get to the options.

        :param supported_opts: the class field that contains a list of categories,
        each of which contains a list of options

        :return: a list of only options
        """
        to_return = []
        if supported_opts:
            for category in supported_opts:
                to_return.extend(category.options)
        return to_return

    @classmethod
    def _handle_positional_params(cls, cmdline_stack):
        """
        If the yaml defines positional parameters, then pops all the remaining tokens
        off the stack and stores them as positional parameters. Caller will have
        already made the determination that the remaining command line tokens are
        in fact positional parameters. (This function doesn't check.). If the
        yaml doesn't define positional parameters, then does nothing.

        :param cmdline_stack: the remaining tokens on the command line
        """
        if cls._positional_params:
            cls._positional_params.params = cmdline_stack.pop_all()

    @classmethod
    def _append_error(cls, err_message):
        """
        Appends the passed error message to the class error list

        :param err_message: the error message to append
        """
        if not cls._parse_errors:
            cls._parse_errors = []
        cls._parse_errors.append(err_message)

    @classmethod
    def _add_fields(cls):
        """
        For each supported option, adds a field to the class having the same name as
        the options's name in the supported options collection, and set the value
        the class field to the value from the option object (i.e. the option's
        parameter.) The outer project code can then get the parameter directly from
        this class field rather than having to navigate the supported options
        collection, and then having to access the AbstractOpt subclass's interface.

        It's a little more intuitive way to access the option values. If the field is
        already present in the class, then this just sets the value, otherwise it
        creates the field and sets the value.
        """
        for opt in CmdLine._flatten(cls._supported_options):
            if not opt.opt_name.isidentifier():
                raise CmdLineException("Specified option name '{}' must be "
                                       "a valid Python identifier".
                                       format(opt.opt_name))
            if opt.opt_name in dir(CmdLine):
                raise CmdLineException("Specified option name '{}' clashes".
                                       format(opt.opt_name))
            setattr(cls, opt.opt_name, opt.value)

    @classmethod
    def _init_from_yaml(cls):
        """
        Parses the yaml string in the class 'yaml_def' field, and initializes the
        following class fields from the yaml: utility, summary, usage,
        positional_params, supported_options, details, examples, and addendum. If the
        yaml is missing an entry, then the corresponding class field is set to None.
        """
        if not cls.yaml_def:
            # nothing to do
            return

        try:
            parsed = yaml.load(cls.yaml_def, Loader=yaml.FullLoader)
            utility = parsed.get("utility")
            if utility:
                cls._utility_name = utility.get("name")
                cls._require_args = utility.get("require_args")
                if not isinstance(cls._require_args, bool):
                    cls._require_args = False
            cls._summary = parsed.get("summary")
            cls._usage = parsed.get("usage")
            if parsed.get("positional_params"):
                cls._positional_params = PositionalParams(
                    parsed.get("positional_params"))
            if parsed.get("supported_options"):
                for category in parsed.get("supported_options"):
                    opt_cat = OptCategory(category.get("category"))
                    for opt in category.get("options"):
                        opt_cat.options.append(OptFactory.create_option(opt))
                    if not cls._supported_options:
                        cls._supported_options = []
                    cls._supported_options.append(opt_cat)
            cls._details = parsed.get("details")
            if parsed.get("examples"):
                for example in parsed.get("examples"):
                    if not cls._examples:
                        cls._examples = []
                    cls._examples.append(UsageExample(example))
            cls._addendum = parsed.get("addendum")
        except CmdLineException as e:
            raise e
        except Exception as e:
            raise CmdLineException("Error parsing the yaml: " + e.args[0])
