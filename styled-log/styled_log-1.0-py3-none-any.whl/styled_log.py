__title__ = "styled-log"
__version__ = "1.0"
__author__ = "Nicholas Lawrence"
__license__ = "MIT"
__copyright__ = "Copyright 2019-2020 Nicholas Lawrence"

import logging
import sys
from collections import OrderedDict
from types import MappingProxyType

import colorama.ansi as ca

_ANSI_MAP = {}
_STYLE_OFF = "\033[0m"


def construct_default_ansi_map():
    """
    Generates human-readable names -> ansi style code dictionary. Currently accounts for the design / separation of
    styles in Colorama library, which is main reason default values of ColoredFormatter read like '<color>_fore'"

    :return:  dict = human readable style names to ansi map
    """

    colorama_ansi_map = {'Fore' : ca.Fore,
                         'Back' : ca.Back,
                         'Style': ca.Style
                         }

    # unpack class design and assign ansi codes to names
    output_ansi_map = {}
    for class_name, ansi_class in colorama_ansi_map.items():
        for ansi_name, ansi_code in ansi_class.__dict__.items():
            breadcrumbed_name = f'{ansi_name}_{class_name}'.lower()  # i.e. 'red_fore', 'blue_back', 'bright_style'
            output_ansi_map[breadcrumbed_name] = ansi_code

    return MappingProxyType(output_ansi_map)


def load_ansi_map(ansi_map=None):
    """Insert supplied ansi_map to global variable."""
    global _ANSI_MAP
    _ANSI_MAP = ansi_map or construct_default_ansi_map()


def style(text, styles):
    """
    Reference global ansi map to apply ansi style codes.
    :param text: string
    :param styles: tuple of ansi codes

    :return: input string preceed by supplied ansi codes, and ending with the ansi-off code.
    """
    if styles:
        ansi_prefix = "".join([_ANSI_MAP[style] for style in styles])
        return f"{ansi_prefix}{text}{_STYLE_OFF}"

    else:
        return text


def show_ansi_map():
    """Convenience function to show the effect of the current ansi codes."""
    for k, v in _ANSI_MAP.items():
        print(f"{k} - {style('This is an example', (v,))}")


load_ansi_map()


class StyledFormatter(logging.Formatter):
    default_ansi_map = OrderedDict()
    default_ansi_map['%(levelname)s'] = {'DEBUG'   : ('blue_fore',),
                                         'INFO'    : ('blue_fore',),
                                         'WARNING' : ('red_fore', 'bright_style'),
                                         'ERROR'   : ('red_fore', 'bright_style'),
                                         'CRITICAL': ('red_fore', 'bright_style'),
                                         }

    default_ansi_map["%(asctime)s"] = ('blue_fore',)
    default_ansi_map['%(name)s'] = ('blue_fore',)
    default_ansi_map['%(message)s'] = ('normal_style',)

    def __init__(self, attribute_styles=None, attribute_delim=' ; ', attribute_delim_styles=tuple(), date_format=''):
        """
        logging.Formatter class that applies ansi codes as declared in the global ansi map, to the attributes of the log
        record.

        :param attribute_styles: Hashmap of logger attribute strings to either a tuple of ansi-styles, as seen in the global
        ansi map, or another hashmap of potential values to tuples of ansi-styles.
        :param attribute_delim: Character to seperate logger attributes.
        :param attribute_delim_styles: Tuple of ansi-styles to style the delimiter.
        :param date_format: Date format string as expected in the parent class. Determine datetime representation.
        """
        self.attribute_styles = attribute_styles or self.default_ansi_map
        self.attribute_delim = attribute_delim
        self.attribute_delim_styles = attribute_delim_styles
        self.date_format = date_format

        self._initialize_parent_with_styled_delimiter()

    def _initialize_parent_with_styled_delimiter(self):
        """
        Style the attribute delimiter and provide that string to the parent class __init__. Also, because we are string
        formatting, ensure all formats are expecting strings.
        """
        styled_delimiter = style(text=self.attribute_delim, styles=self.attribute_delim_styles)

        _fmt = styled_delimiter.join(self.attribute_styles.keys())
        _fmt = _fmt.replace(')d', ')s')
        _fmt = _fmt.replace(')f', ')s')

        super().__init__(_fmt, self.date_format)

    def formatMessage(self, record):
        """
        Iterate over provided attribute styling dict, and either style the value based on sequence of styles, or check
        to see if specific styling for the observed value was provided, and if so, apply that styling.

        :param record: logging record

        :return: logger output
        """

        styled_attributes = {}
        for attr, style_rules in self.attribute_styles.items():

            attr_name = attr[2:-2]  # i.e. %(module)s --> module (so we can lookup value in record)
            value = record.__dict__[attr_name]

            if isinstance(style_rules, (list, tuple)):
                styled_value = style(text=value, styles=style_rules)

            elif isinstance(style_rules, dict) and value in style_rules:
                    styled_value = style(text=value.rjust(8) if attr_name == 'levelname' else value,
                                         styles=style_rules[value])

            else:
                styled_value = value

            styled_attributes[attr_name] = styled_value

        return self._fmt % styled_attributes


def get_default_styled_logger(name, log_level_no=20):
    """
    It is assumed the user doesn't want to retain the default logger stderr writing (otherwise you'd receive duplicate
    logs for the same message). We import the logging library here again to prevent any previous calls to basicConfig
    from misconfiguring the formatter.

    :return: logger
    """
    import logging

    # don't call basicConfig

    logger = logging.getLogger(name)
    logger.setLevel(log_level_no)

    logger.handlers = []  # otherwise multiple calls to this function will produce multiple output for each log

    styled_formatter = StyledFormatter()

    writes_to_console = logging.StreamHandler(sys.stderr)
    writes_to_console.setFormatter(styled_formatter)

    logger.addHandler(writes_to_console)

    return logger
