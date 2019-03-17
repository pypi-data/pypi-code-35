import sys

from pycmdparse.abstract_opt import AbstractOpt
from pycmdparse.cmdline import CmdLine
from pycmdparse.opt_acceptresult_enum import OptAcceptResultEnum
from pycmdparse.parseresult_enum import ParseResultEnum
from pycmdparse.positional_params import PositionalParams


class MyCmdLine(CmdLine):
    """
    An example of how a developer would use pycmdparse for a hypothetical
    'foo-utility'.

    The developer use case is:

    1) Subclass the 'CmdLine' class, and provide a yaml definition for the
       utility's command line and usage instructions, based on this example.
    2) Call the inherited parse method of the sub-class. This will first parse
       the yaml to build an internal set of data structures, then parse the
       command line using those data structures. The result will be a set of
       fields injected into the subclass, or, a collection of errors that the
       utility can display to the console.
    3) If the user specified '-h' or '--help', then the utility can use
       pycmdparse to display usage instructions as defined in the yaml.
       (Content is formatted to fit the console window width.)
    4) If the command line is successfully parsed, the utility can use the
       injected fields to obtain the values of the command line options
       provided by the user. The injected  field names are specified in the
       yaml. If desired, the values can be type-validated. The utility can also
       perform custom validation using a provided validation hook.

    The requirements for how to format the yaml are in the yaml below.
    """

    yaml_def = '''
    # The 'yaml_def' field is defined in the base class.
    #
    # Every top-level entry in the yaml is optional. The 'supported_options'
    # entry, and the 'positional_params' entry cause parsing of the command
    # line to occur. Other entries just define console content to display when
    # the user requests help via '-h' or '--help'. YAML is indent-sensitive.
    # This YAML document works. So if you preserve the indent - it should
    # continue to work.  

    # utility
    #
    # ------------
    # Users will run 'foo-utility' from the command line. In the usage
    # instructions, this utility name displays at the top of the usage
    # instructions, with a double underline. If you want to require options
    # and/or positional params, specify require_args: true. Then, if the user
    # just offers the utility name on the command line with no args, the parser
    # will return a parse result of SHOW_USAGE. If require_args is false in the
    # yaml or omitted, then if the user simply types the utility name on the
    # command line, this will not cause a parse error. This could be useful
    # in a situation where your utility has defaults for every single command
    # line option/param - or - doesn't support any command line options/params.
    
    utility:
        name: foo-utility
        require_args: true

    # summary
    # -------
    #
    # provide a top-line summary to help the user quickly understand the purpose
    # of the utility. This displays to the console under the program name.
    
    summary: >
        The foo-utility searches the internet for all available information
        about the etymology of 'foo'. (See
        https://en.wikipedia.org/wiki/Foobar). Various options and parameters
        can be provided as command line arguments to tailor the behavior of the
        utility. 
    
    # usage
    # -----
    #
    # 'usage' is a really brief synopsis of what the command line looks like to
    # invoke the utility. If there is no usage section, then usage is generated
    # to the console by pycmdparse from the defined options/parameters as well
    # as the positional_params. This example provides an explicit usage section.
    # The usage is intended to be an abbreviated usage scenario. There appear to
    # be many approaches to this among the universe of console utilities. So for
    # the explicit case, whatever is provided here is displayed verbatim. You
    # can comment this out to see the generated usage.

    usage: >
     foo-utility [options] PREVIOUSFOO

    # positional_params
    # -----------------
    #
    # The existence of the 'positional_params' entry causes positional param
    # parsing. Positional params are everything after "--" on the command line,
    # or, everything on the command line after all known options are parsed, or,
    # everything on the command line if there are no defined options.
    #
    # The 'positional_params' entry contains two sub-entries: 'params', and
    # 'text'. Both are used only to format usage to the console - and only if
    # the 'usage' entry above is not provided. In this case, the value of
    # 'params' is appended to the displayed supported options, and the 'text'
    # is appended to that, on a separate line. So the pycmdparse-generated
    # usage - including supported options and positional params - for the
    # foo-utility - would print to the console as follows, using the
    # 'positional_params' spec in this yaml:
    #
    #     Usage:
    #
    #     foo-utility [-v,--verbose] [-h,--help] [-d,--depth <n>]
    #                 [-e,--exclude <term1 ...>] PREVIOUSFOO
    #
    #     PREVIOUSFOO is an optional file spec. If the results of a prior foo
    #     analysis are available in the PREVIOUSFOO file, then the utility only
    #     displays the deltas between the current foo etymology, and the
    #     etymology saved in the specified file. This parameter can be an
    #     absolute - or relative - file specifier. 
    #
    # Note that the 'params' entry has no meaning to pycmdparse. It's only a
    # mnemonic for the user.
    
    positional_params:
      params: PREVIOUSFOO
      text: >
        PREVIOUSFOO is an optional file spec. If the results of a prior foo
        analysis are available in the PREVIOUSFOO file, then the utility only
        displays the deltas between the current foo etymology, and the etymology
        saved in the specified file. This parameter can be an absolute - or
        relative - file specifier. 

    # supported_options
    # -----------------
    #
    # The 'supported_options' entry defines the options and associated params
    # for the utility. If this entry exists, then option parsing occurs.
    # Otherwise, no option parsing occurs. All options provide a single-
    # character (short) form, and a long form. Example: '-t', and '--timeout'.
    # Options are case-sensitive. There are two types of options:
    #
    # An example of a 'bool' is: '--verbose'. It is False by default, and only
    # True if provided on the command line. It is always optional, since it
    # always has a value.
    #
    # A 'param' option is an option taking one or more params, like '--filelist
    # FILE1 FILE2 FILE3', or '--file FILE'. A param option's parameters are
    # terminated differently depending on the param type. More details are
    # provided below, and, in the docstring of the ParamOpt class
    #
    # Param options are either required, or not required. Required options that
    # are not provided on the command line cause a parse error. Non-required
    # options can have a default in the yaml. Non-required options that are not
    # provided on the command line and that don't have default specified have
    # a value of 'None' upon conclusion of arg parsing.
    #
    # All options must belong to a category. It's fine if there is only one
    # category. If the category entry has a value, then it is displayed to the
    # console when usage instructions are displayed. Otherwise the presence of
    # the category has no effect. The purpose is to support categorization
    # of options, which some complex utilities will want. The fact that it is
    # required in the yaml just simplifies the pycmdparse yaml handling.
    #
    # The example foo-utility supports the following options: '--verbose',
    # '--exclude', and '--depth'. '--verbose' is boolean, '--exclude' is param
    # accepting multiple values, and '--depth' is param accepting only a
    # single value.
        
    supported_options:

      # As stated, at least one category is required under 'supported_options' 

      - category: Common options  # 'Common options' could have been omitted,
                                  # then nothing would print here

        # The options element lists all the options in the category 

        options:
        
        # each option is an array of key/value entries. The supported keys are
        # listed for each option type. If a key is omitted, its value is None.
        # Each option requires either a short-form _or_ long-form option key.
        # Both are allowed. A 'name', and an option type - 'opt' - are 
        # also required.
        
        - name    : verbose  # the Python field name that pycmdparse will inject
                             # into the utility's CmdLine subclass
          short   : v        # matches '-v' on the command line
          long    : verbose  # matches '--verbose' on the command line
          opt     : bool     # this is a 'bool' option
          # Displays on the console in usage instructions:
          help: >
            Causes verbose output. Can result in significant volumes of
            information to be emanated to the console. Use with caution.
        - name    : help
          short   : h
          long    : help
          opt     : bool
          help: >
            Displays this help text.

      # multiple categories are supported, but not required

      - category: Less common options
        options:
        - name      : depth
          short     : d
          long      : depth
          hint      : n      # a hint for the user in usage instructions.
                             # Displays like: "-d,--depth <n>"
          required  : false  # omission from the command line will not cause a
                             # parse error
          datatype  : int    # If omitted from the yaml, param is a string.
                             # Types: int/float/date/bool. See 'AbstractOpt'
          opt       : param  # this is a 'param' option. 'multi_type' is
                             # omitted, so it accepts exactly one param
          default   : 1      # if the option is omitted from the command line,
                             # then the param gets this value
          help: >
            Specifies the recursion level of the search. If not specified on the
            command line, then a default value of one (1) is used. Increasing
            the recursion level can provide a better analysis result, but can
            significantly increase the processing time. The max value is 92.
        - name      : exclude
          short     : e
          long      : exclude
          hint      : term1 ...
          required  : false
          opt       : param       # another param option
          multi_type: no-limit    # from: 'exactly', 'at-most', 'no-limit'.
                                  # See: 'ParamOpt'
          count     :             # ignored for no-limit. Otherwise required
          help: >
            Specifies a list of terms that cause the utility to stop recursing
            at any given level. Multiple terms can be provided. There is no
            limit to the number of terms.

    # details
    # -------
    #
    # the details section is just a place to put more detail than seems
    # appropriate in the 'usage' section. Some utilities have really complex
    # options and parameters. For example, if a parameter value is itself a
    # lookup into a table, or if there are many many usage scenarios, and so
    # forth.Embedded newlines in the yaml are preserver (e.g. for tabular
    # formatting if needed.) Otherwise, content is fitted by pycmdparse to the
    # console window width.

    details: >
      The recursion algorithm uses a weighting scheme to determine the amount
      of detailed parsing to perform at any given level of the search hierarchy.
      The following search terms illustrate the weighting:

         weight  term
         ------  ------
         1       foo
         2       bar
         3       baz
         4       foobar

    # examples
    # --------
    #
    # The 'examples' entry contains a list of 'example' entries. Examples are
    # just that. They consist of an 'example' key, and an 'explanation' key.
    # They are displayed below the details section, pretty much as they appear
    # in the yaml.
    
    examples:
      - example: foo-utility --verbose --exclude fizzbin frobozz
        explanation: >
          Performs a full traversal, with detailed diagnostic information
          displaying to the console, but terminating recursion into any
          hierarchy containing the terms 'fizzbin', or 'frobozz'.

      - example: >
          foo-utility --verbose --exclude fizzbin frobozz --
          my-saved-search-file
        explanation: >
          Same as the example above, but in this case compares the results
          determined by the utility to the results previously generated in the
          file 'my-saved-search-file' in the current working directory. Only
          the deltas display to the console. (Note - the specified file must
          adhere to the foo-utility's stringent formatting requirements.)

      - example: foo-utility -d 42
        explanation: >
          Performs a search with no search term exclusions, and minimal
          (non-verbose) console output. But only recurses to a depth of 42.

    # addendum
    # --------
    #
    # For copyright, version, author, license, URL, anything else. Content
    # is displayed as is, fitted to the console window width.

    addendum: >
      Version 1.2.3, Copyright (C) The Author 2019\n

      In the Public Domain\n

      Github: https://github.com/theauthor/foo-utility
    '''

    @classmethod
    def validator(cls, to_validate):
        """
        Provides an optional custom validator. The validator is called by the
        parser to validate each arg (one at a time) as well as the list of
        positional params (all together) that were parsed from the command line.
        This callback occurs after all built-in parsing is complete and has
        passed: only if it is a class function, and only if the function is
        named 'validator'

        :param to_validate: an instance of 'PositionalParams', or an instance of
        a subclass of 'AbstractOpt'

        :return: a tuple. Element zero is OptAcceptResultEnum.ERROR if there was
        a validation error. In this case, element one is the corresponding error
        message to display to the user. When your validator returns ERROR to
        pycmdparse, that causes the 'CmdLine.parse()' function to return an
        error. Then your utility code calls 'CmdLine.display_info(...)' passing
        the value received from 'CmdLine.parse()'. Example code in main()
        illustrates this

        if the function returns None in tuple element zero, then pycmdparse
        interprets that as success: no validation error.
        """

        if isinstance(to_validate, PositionalParams):
            if len(to_validate.params) > 1:
                return OptAcceptResultEnum.ERROR, "Only one filename for " \
                                                  "delta comparison supported"
        elif isinstance(to_validate, AbstractOpt):
            if to_validate.opt_name == "depth":
                if to_validate.value > 92:
                    return OptAcceptResultEnum.ERROR, "{} exceeds max " \
                                                      "recursion level of 92".\
                        format(to_validate.value)
        return None,

    # Fields below are injected using the field names from the supported_options
    # yaml section. It's not necessary to define them. If not defined, they are
    # injected. If defined, their values are set from the command line. This
    # example sets them explicitly so the IDE doesn't emanate 'unresolved
    # attribute' warnings when referenced outside the class

    verbose = None
    exclude = None
    depth = None


if __name__ == "__main__":
    """
    This function shows how to use pycmdparse:
    
    1) Subclass CmdLine as above
    2) Initialize the subclass with: a) yaml, b) validator, and c) class
       fields 1:1 to options
    3) Call 'parse', passing sys.argv
    4) If not SUCCESS, let the subclass handle it. (Show errors, or show help)
    5) Otherwise use the injected/initialized subclass fields to access command
       line options/params
    
    After installing the package, or, creating a pipenv try the following
    from the command lines:
    
    python example/example.py --exclude X Y Z -vd 34 /home/me/my-file

    python example/example.py --help

    python example/example.py -d 500

    python example/example.py -d nan

    python example/example.py my-file-1 my-file-2
    """
    # un-comment to run independently of the command line
    # sys.argv = "example/example.py --exclude X Y Z -vd 34 /home/me/my-file"
    parse_result = MyCmdLine.parse(sys.argv)
    if parse_result.value != ParseResultEnum.SUCCESS.value:
        MyCmdLine.display_info(parse_result)
        exit(1)
    print("verbose = {}".format(MyCmdLine.verbose))
    print("exclude = {}".format(MyCmdLine.exclude))
    print("depth = {}".format(MyCmdLine.depth))
    print("positional params = {}".format(MyCmdLine.positional_params))
    exit(0)
