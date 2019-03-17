import sys

from pycmdparse.abstract_opt import AbstractOpt
from pycmdparse.cmdline import CmdLine
from pycmdparse.opt_acceptresult_enum import OptAcceptResultEnum
from pycmdparse.parseresult_enum import ParseResultEnum
from pycmdparse.positional_params import PositionalParams


class MyCmdLine(CmdLine):
    """
    Provides a template to clone into a new utility
    """

    yaml_def = '''
    utility:
      name:
      require_args: true # false

    summary: >
      TBD

    #usage: >
    # TBD

    positional_params:
      params: TBD
      text: >
        TBD

    supported_options:
      - category:
        options:
        - name    : tbd1
          short   : t
          long    : tbd-1
          hint    : tbd1
          required: false
          datatype:
          opt     :
          count   :
          default :
          help: >
            TBD
        - short   : z
          long    : tbd-2
          help: >
            This shows the minimum requirement to define a parseable option.
            The injected name is derived from the long key if available, else
            the short key. The key is converted to a Python identifier by
            replacing dashes with underscores. If a valid identifier, it is
            used, otherwise an error is thrown. Since the option type ('opt')
            is omitted, pycmdparse defines it as a param option taking exactly
            one parameter. As defined above, the command line arg would be:
            '--tbd-2 xyz', or -z xyz'. And the injected field name would be
            'tbd_2'.

    details: >
      TBD

    examples:
      - example: TBD
        explanation: >
          TBD

      - example: TBD
        explanation: >
          TBD

    addendum: >
      TBD
    '''

    @classmethod
    def validator(cls, to_validate):
        some_error_condition = False
        if isinstance(to_validate, PositionalParams):
            if some_error_condition:
                return OptAcceptResultEnum.ERROR, "TODO error message"
        elif isinstance(to_validate, AbstractOpt):
            if to_validate.opt_name == "your_field":
                if some_error_condition:
                    return OptAcceptResultEnum.ERROR, "TODO error message"
        return None,

    # these fields will be injected if not defined. If defined, their values
    # will be set by the parser

    tbd1 = None   # name defined explicitly in the yaml
    tbd_2 = None  # no name, so derived from the long key by pycmdparse


# To run this from the command line, 'pipenv shell' from the main directory
# Then: 'python example/clone_me.py --tbd-2 Y --tbd-1 X'
# Prints:
# tbd1 = X
# tbd_2 = Y

if __name__ == "__main__":
    parse_result = MyCmdLine.parse(sys.argv)
    if parse_result.value != ParseResultEnum.SUCCESS.value:
        MyCmdLine.display_info(parse_result)
        exit(1)
    print("tbd1 = {}".format(MyCmdLine.tbd1))
    print("tbd_2 = {}".format(MyCmdLine.tbd_2))
    exit(0)
