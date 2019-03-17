from pycmdparse.bool_opt import BoolOpt
from pycmdparse.cmdline_exception import CmdLineException
from pycmdparse.datatype_enum import DataTypeEnum
from pycmdparse.multitype_enum import MultiTypeEnum
from pycmdparse.param_opt import ParamOpt


class OptFactory:
    """
    Provides functionality to create the appropriate option type from the passed
    dictionary - representing an option from the yaml - provided by the yaml parser.
    """

    OPT_KEY = "opt"
    """yaml for an option can include this entry, specifying the option type"""

    BOOL_OPT = "bool"
    """A boolean option - an option that doesn't take a parameter"""

    PARAM_OPT = "param"
    """An option that takes one or more parameters"""

    KNOWN_OPTION_TYPES = [BOOL_OPT, PARAM_OPT]
    """
    The valid values that can be specified in the 'opt' dictionary entry
    in the yaml spec
    """

    @staticmethod
    def create_option(opt_dict):
        """
        Creates a specific sub-class of 'AbstractOpt' based on the "opt" dictionary
        value in the passed dictionary

        :param opt_dict: A dictionary provided by the yaml parser, representing the
        spec for an option

        :return: a subclass of 'AbstractOpt' based on the passed dictionary "opt" entry
        value. If the dictionary doesn't contain an opt entry, then a PARAM type is
        created. This is done as a convenience to eliminate the need to specify the
        option type in the yaml.

        :raises: CmdLineException if the passed dictionary contains an "opt" entry
        value that is not a known option type. (See OptFactory.KNOWN_OPTION_TYPES)
        """

        option_type = opt_dict.get(OptFactory.OPT_KEY)
        if not option_type:
            option_type = OptFactory.PARAM_OPT
        if option_type in OptFactory.KNOWN_OPTION_TYPES:
            return OptFactory._new_option(option_type, opt_dict)
        else:
            raise CmdLineException("Unknown option type: {}".format(
                option_type))

    @staticmethod
    def _new_option(opt_type, opt_dict):
        """
        Actually creates an 'AbstractOpt' subclass object

        :param opt_type: expected to be in OptFactory.KNOWN_OPTION_TYPES. The function
        doesn't validate that, since this is an internal function and the validation
        is performed by the caller. :param opt_dict: a dictionary from the yaml parser,
        built from the yaml defining an option. Missing entries are passed to the
        subclass constructor as None.

        :return: the created object
        """

        opt_name = opt_dict.get("name")
        short_key = opt_dict.get("short")
        long_key = opt_dict.get("long")
        opt_hint = opt_dict.get("hint")
        required = opt_dict.get("required")
        is_internal = opt_dict.get("internal")
        default = opt_dict.get("default")
        data_type = DataTypeEnum.fromstr(opt_dict.get("datatype"))
        help_text = opt_dict.get("help")

        if opt_type == OptFactory.BOOL_OPT:
            return BoolOpt(opt_name, short_key, long_key, opt_hint, required,
                           is_internal, help_text)
        else:  # param
            multi_type = MultiTypeEnum.fromstr(opt_dict.get("multi_type"))
            if not multi_type:
                multi_type = MultiTypeEnum.EXACTLY
            count = opt_dict.get("count")
            if not count and multi_type in [MultiTypeEnum.EXACTLY,
                                            MultiTypeEnum.AT_MOST]:
                count = 1
            return ParamOpt(opt_name, short_key, long_key, opt_hint, required,
                            is_internal, default, multi_type, count, data_type,
                            help_text)
