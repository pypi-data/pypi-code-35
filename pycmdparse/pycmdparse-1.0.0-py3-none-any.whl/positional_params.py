class PositionalParams:
    """
    Provides a container to hold positional parameter values and associated
    help text. No parsing of positional parameter values is performed. So, for
    example, if the command line is like:

    "my-utility -v -- foo bar --baz=frobozz"

    then the positional params list will be:

    ["foo", "bar", "--baz=frobozz"]

    Note: in order for positional param parsing to occur, the yaml must define
    a positional params dictionary entry.
    """
    def __init__(self, params_dict):
        """
        Initializes the instance from a positional params spec in the yaml. A
        positional params spec is expected to look like:

        positional_params:
          params: Free-form text
          text: >
            Free-form text

        The "params" and "text" entries are displayed in usage instructions, and have
        no other effect. In other words - its just documentation. When the command
        line is parsed, positional param values are placed into an instance of this
        class in the 'params' property. If a validator is defined, then this object
        is provided to the validator so the utility can validate the parameter
        values. (See the CmdLine class for more info on validation.)

        :param params_dict: a yaml-sourced dictionary representing the positional
        params spec
        """

        self._params = []
        """
        Initialized by the command line parser with all positional parameters
        supplied on the command line
        """

        if not params_dict:
            return
        self._param_text = params_dict.get("params")
        self._help_text = params_dict.get("text")

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        self._params = params

    @property
    def param_text(self):
        return self._param_text

    @property
    def help_text(self):
        return self._help_text
