import shutil

from pycmdparse.util import Util


class ShowInfo:
    """
    Displays errors and usage instructions to the console.
    """
    @staticmethod
    def show_errors(parse_errors, utility_name):
        """
        Displays all passed errors to the console.

        :param parse_errors: a List of strings, each of which is ostensibly an
        error message
        :param utility_name: the name of the program utilizing the pycmdparse package
        """
        print("\nError{}:\n".format("(s)" if len(parse_errors) > 1 else ""))
        for parse_error in parse_errors:
            print(parse_error)
        if utility_name:
            print("\nFor usage instructions, try: {0} -h (or {0} --help)\n"
                  .format(utility_name))

    @staticmethod
    def show_usage(utility_name, summary, usage, supported_options, details,
                   examples, positional_params, addendum):
        """
        Displays comprehensive usage instructions, as defined by the function
        arguments. Only those components that are provided as non-empty are
        displayed. Others are ignored.

        :param utility_name: the program name
        :param summary: a summary description of what the program does
        :param usage: Abbreviated 'quick-start' usage guidance
        :param supported_options: a list of OptCategory objects defining the
        valid command-line options
        :param details: a section to present more detailed information
        :param examples: a list of UsageExample objects
        :param positional_params: defines the supported positional parameters.
        Instance of PositionalParams class
        :param addendum: A free-form string of supplemental information the
        utility author would like to convey
        """
        max_len, ignore = shutil.get_terminal_size()

        if utility_name:
            print("\n" + utility_name + "\n" + "=" * len(utility_name))

        if summary:
            for line in Util.split_string(summary, max_len):
                print(line)

        # if not explicitly defined in the yaml, then auto-generated here
        if usage:
            print("Usage:\n")
            for line in Util.split_string(usage, max_len):
                print(line)
        else:
            ShowInfo._generate_usage(utility_name, supported_options,
                                     positional_params, max_len)

        if positional_params and positional_params.help_text:
            for line in Util.split_string(positional_params.help_text, max_len):
                print(line)

        if supported_options:
            print("Options and parameters:")
            left_len = ShowInfo._calc_left_len(supported_options)
            for category in supported_options:
                if category.category and len(category.category.strip()) > 0:
                    print("\n{}:\n".format(category.category))
                for line in ShowInfo._get_option_help(category.options, max_len,
                                                      left_len):
                    print(line)

        if details:
            print("Additional detail:\n")
            for line in Util.split_string(details, max_len):
                print(line)

        if examples:
            print("Examples:\n")
            for example in examples:
                print(example.example + "\n")
                for line in Util.split_string(example.explanation, max_len):
                    print(line)

        if addendum:
            print("Supplemental:\n")
            for line in Util.split_string(addendum, max_len):
                print(line)

    @staticmethod
    def _generate_usage(utility_name, supported_options, positional_params,
                        max_len):
        """
        Generates abbreviated usage by listing all the options, then the positional
        params 'text' field.

        :param utility_name: the utility name using pycmdparse
        :param supported_options: the defined options and parameters from the yaml
        :param positional_params: " positional params
        :param max_len: max console width
        """
        if not utility_name and not supported_options \
                and not positional_params:
            return

        print("Usage:\n")
        utility_name = utility_name + " " if utility_name else ""
        line = utility_name

        if supported_options:
            for category in supported_options:
                for option in category.options:
                    k = "[" + option.keys_and_hint + "]"
                    if len(line) + len(k) > max_len:
                        print(line)
                        line = ShowInfo._fixed(" ", len(utility_name))
                    line += k + " "

        if positional_params:
            param_text = positional_params.param_text
            for word in param_text.split():
                if len(line) + len(word) > max_len:
                    print(line)
                    line = ShowInfo._fixed(" ", len(utility_name))
                line += word + " "
        if len(line.strip()) > 0:
            print(line)
        print()

    @staticmethod
    def _calc_left_len(supported_options):
        """
        Calculates the max length of the keys and hint for all options, to support
        vertically aligning the option help. The keys and hint for an option are
        like "-f,--filename <filename-spec>"

        :param supported_options: the defined options and parameters from the yaml

        :return: the max length
        """
        left_len = 0
        for category in supported_options:
            for option in category.options:
                left_len = len(option.keys_and_hint) \
                    if len(option.keys_and_hint) > left_len else left_len
        return left_len

    @staticmethod
    def _get_option_help(supported_options, max_len, left_len):
        """
        Gets the help text for an option, and breaks it into lines to format it for
        display to the console. E.g.:

        -d,--depth<n>  This is the help text
                       for the depth option.

        :param supported_options: the defined options and parameters from the yaml
        :param max_len: max console window width. The help is chunked to not exceed
        :param left_len: the max length of the keys and hints

        :return: the help text, ready to be printed. In the example above, returns:
        an array with two elements: ["-d,--depth<n>  This is the help text",
        "               for the depth option."]
        """
        to_return = []
        if max_len <= left_len:
            # safety - make width big enough so the math works
            max_len = left_len + 10
        for opt in supported_options:
            if opt.is_internal:
                continue
            help_text = ShowInfo._prepend_required(opt.help_text, opt.required)
            opt_helps = Util.split_string(help_text, max_len - left_len - 1)
            help_lines = len(opt_helps)
            cur_line = 0
            is_new = True
            for opt_help in opt_helps:
                cur_line += 1
                if is_new:
                    to_return.append(ShowInfo._fixed(opt.keys_and_hint,
                                                     left_len) + " " + opt_help)
                    is_new = False
                else:
                    if cur_line == help_lines and len(opt_help) == 0:
                        continue
                    to_return.append(ShowInfo._fixed(" ", left_len) + " " + opt_help)
        return to_return

    @staticmethod
    def _prepend_required(help_text, required):
        """
        Returns the passed help text prepended with "Optional. " or "Mandatory. ",
        based on the value of the passed 'required' param. If the passed help text
        is 'None' or blank, then returns the help text as is.

        :param help_text: Text to perhaps prepend
        :param required:  True if the option is required, else False - the
        option is not required to be provided on the command line

        :return: The value of 'help_text', potentially prepended as described.
        """
        if not help_text or len(help_text.strip()) == 0:
            return help_text
        else:
            return ("Mandatory. " if required else "Optional. ") + help_text

    @staticmethod
    def _fixed(val, width):
        """
        Returns the passed value string right-padded with 'width'

        :param val:   The string to pad
        :param width: The desired width

        :return: The right-padded string. E.g. fixed("XYZ", 10)
        returns: "XYZ       "
        """
        return (val + (" " * width))[0:width]
