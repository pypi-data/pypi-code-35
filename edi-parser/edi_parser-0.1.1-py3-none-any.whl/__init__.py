from edi_parser.utils.loaders import *
from edi_parser.processor import *
from typing import Union, List, TextIO

name = "edi_parser"


def main(template_name: Union[str, None], file: Union[TextIO, None], data: List[List[Union[str, int]]]) -> list:
    template = None
    if template_name is not None:
        template = load_template(template_name)
    elif file is not None:
        template = load_file(file)

    type_rules = template['rules']['types']
    order_rules = template['rules']['file_format']['order_rules']

    return parse(template, type_rules, order_rules, data)
