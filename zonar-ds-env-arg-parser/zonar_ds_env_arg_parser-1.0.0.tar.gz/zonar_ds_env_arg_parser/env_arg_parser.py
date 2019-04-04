import os


class __EnvArgParser(object):
    """
    Works a lot like ArgParse but ONLY for environment variables.

    Based on this idea: https://pypi.python.org/pypi/ConfigArgParse
    but hand rolled because ConfigArgParse's documentation was sparse and we only need to read in Environment variables
    """

    def __init__(self):
        self.args = []
        self.OPTIONS = _Options()
        self.initialized = False

    def add_argument(self, **kwargs):
        """
        Each add argument call is in the form:
        add_argument(env_var='SOMEVARNAME', required=True, help='This variable does whatever', type=str, validation=lambda x: somethingsomething)

        :param env_var: The environment variable is fetched from the environment and placed into the
        resulting object as an instance WITH THAT SAME NAME.
        (i.e PROMETHEUS_CLIENT the environment variable will become OPTIONS.PROMETHEUS_CLIENT)

        :param required: can be true or false, if required=False a default must be provided

        :param default: The default value.  Must be set if required=False, cannot be set if required=True

        :param validation: Optional, a function should be provided that takes a single value,
        and should return True, False (or an Exception).  False or an exception will prevent the program from launching

        :param help: This message is displayed if an argument doesnt exist or fails validation.
        It should explain to the user what the argument is for to assist them in defining it.

        :param type: Optional, if the value needs to be something other than a string, specify what it should be converted to.
        """
        # Check to see if our required function arguments are defined
        if 'env_var' not in kwargs or 'required' not in kwargs or "help" not in kwargs:
            raise Exception("'env_var', 'required' and 'help' are mandatory for each add argument call")

        # If required is false but a default is not defined, that's a problem
        if not kwargs['required'] and 'default' not in kwargs:
            raise Exception("If 'required' is false then a 'default' must be provided")

        # Otherwise, if required is TRUE, then we cannot have a default
        elif kwargs['required'] and 'default' in kwargs:
            raise Exception("'Default' cannot be provided if required=True")

        self.args.append(kwargs)

    def parse_args(self):
        self.initialized = True
        for a in self.args:
            a = _Struct(**a)
            if a.env_var not in os.environ:
                # We don't have an environment value set
                if a.required:
                    self._log_and_throw(f"Environment variable {a.env_var} is required "
                                        f"but was not found on the system.  Help: {a.help}")
                else:
                    self.OPTIONS.set_attribute(a.env_var, self._convert_if_necessary(a, a.default))
            else:
                env_value = os.environ[a.env_var]
                # We do have an environment value set
                if hasattr(a, 'validation'):
                    # If we have a validation method defined for this argument, lets run it
                    try:
                        validated = a.validation(env_value)
                    except Exception:
                        validated = False

                    if not validated:
                        self._log_and_throw(f"Environment variable {a.env_var} did not pass validation. "
                                            f"Its value was set to {env_value}.  Help: {a.help}")

                # If we're still here, we either passed
                # validation or didn't have any to begin
                # with. Either way, set the option and move on.
                self.OPTIONS.set_attribute(a.env_var, self._convert_if_necessary(a, env_value))

    def get_options(self):
        if not self.initialized:
            self.parse_args()
        return self.OPTIONS

    def initialize(self):
        if not self.initialized:
            self.parse_args()

    def _convert_if_necessary(self, a, val):
        """
        Helper method to convert a given argument to a different type.

        :param a: argument
        :return: The converted val
        """
        if hasattr(a, 'type'):
            try:
                val = a.type(val)
            except Exception as e:
                self._log_and_throw(f"An exception occurred when converting {a.env_var}. "
                                    f"Tried to convert {val} to {a.type}. Exception: {e}")
        return val

    @staticmethod
    def _log_and_throw(message):
        """
        A little convenience method to log an error and raise is as an Exception
        """
        print(message)
        raise Exception(message)


class _Struct:
    """
    Silly hack to get dictionaries to behave like objects (where each entry is an attribute)

    Its silly there isn't a more "official" way to do this in python since its
    cleaner to read, if someone knows a better way please use it, I stole this from
    https://stackoverflow.com/questions/1305532/convert-python-dict-to-object
    """
    def __init__(self, **entries):
        self.__dict__.update(entries)


class _Options(object):
    """
    This object has attributes set on it depending on what options are passed in.
    """
    def __init__(self):
        pass

    def set_attribute(self, name, value):
        setattr(self, name, value)

    def __str__(self):
        option_strings = []
        for attr, value in self.__dict__.items():
            option_strings.append(str(attr) + " = " + str(value))
        return "\n".join(option_strings)


# This is what's meant to be imported so we only have a single instance of __EnvArgParser
env_arg_parser = __EnvArgParser()
