import sys
from io import StringIO
from pygments import highlight, lexers, formatters


NEW_LINE = '\n'
CONTAINERS_TYPE = (list, tuple, set, frozenset, dict)


def pprint(value, stream=sys.stdout, indent: int = 4, width: int = 79, depth: int = None, sort_dict_keys: bool = False) -> None:
    """Pretty print a Python value to stream,
    which defaults to ``sys.stdout``. The output will not be colored.

    :param stream: the output stream, defaults to ``sys.stdout``
    :param indent: number of spaces to add for each level of nesting.
    :param width: maximum allowed number of columns in the output.
    :param depth: maximum depth to print nested structures.
    :param sort_dict_keys: dict keys should be sorted, Defaults to False.
    """
    doc = _repr(value, indent, width, depth, 0, sort_dict_keys)
    stream.write(doc)
    stream.write(NEW_LINE)


def cpprint(value, stream=sys.stdout, indent: int = 4, width: int = 79, depth: int = None, sort_dict_keys: bool = False) -> None:
    """Pretty print a Python value to stream,
    which defaults to sys.stdout. The output will be colored and
    syntax highlighted.

    :param stream: the output stream, defaults to ``sys.stdout``
    :param indent: number of spaces to add for each level of nesting.
    :param width: maximum allowed number of columns in the output.
    :param depth: maximum depth to print nested structures.
    :param sort_dict_keys: dict keys should be sorted, Defaults to False.
    """
    doc = _repr(value, indent, width, depth, 0, sort_dict_keys)
    colorful_doc = get_syntax_highlight(doc)
    stream.write(colorful_doc)
    stream.write(NEW_LINE)


def pformat(value, indent: int = 4, width: int = 79, depth: int = None, sort_dict_keys: bool = False) -> str:
    """Return a pretty printed representation of the value as a ``str``.
    The output is not colored.

    :param indent: number of spaces to add for each level of nesting.
    :param width: maximum allowed number of columns in the output.
    :param depth: maximum depth to print nested structures.
    :param sort_dict_keys: dict keys should be sorted, Defaults to False.
    """
    stream = StringIO()
    pprint(value, stream, indent, width, depth, sort_dict_keys)
    return stream.getvalue()


def _repr(value, indent: int, width: int, depth: int = None, level: int = 0, sort_dict_keys: bool = False) -> str:
    """ Parse the value to the pretty printer, use it to replace the
    ``repr()`` function
    """
    if depth is None:
        depth = float('inf')
    if level >= depth:
        return mapping_hidden_value(value)
    if sort_dict_keys and isinstance(value, dict):
        value = dict(sorted(value.items()))

    current_indent = generate_intent(indent, level)
    limit = width + 2 if isinstance(value, str) else width
    repr_value = repr(value)
    if len(repr_value) <= limit:
        return repr_value

    if isinstance(value, str):
        cuted_string = cut_string(value, width)
        return _repr(cuted_string, indent, width, depth, level, sort_dict_keys)
    elif isinstance(value, CONTAINERS_TYPE):
        components = list()
        child_indent = generate_intent(indent, level + 1)
        if isinstance(value, dict):
            # When format dict object, separate the key and the value,
            # send them to ``_repr()``, the key don't need to hidden value,
            # set the depth is ``inf``.
            for (k, v) in value.items():
                k_repr = _repr(k, indent, width, float('inf'), level + 1, sort_dict_keys)
                v_repr = _repr(v, indent, width, depth, level + 1, sort_dict_keys)
                components.append(f'{child_indent}{k_repr}: {v_repr}')
        else:
            for item in value:
                item_repr = _repr(item, indent, width, depth, level + 1, sort_dict_keys)
                components.append(f'{child_indent}{item_repr}')

        components_word = f',{NEW_LINE}'.join(components)
        format_value = f'{NEW_LINE}{components_word}{NEW_LINE}{current_indent}'

        if isinstance(value, list):
            return f'[{format_value}]'
        elif isinstance(value, tuple):
            return f'({format_value})'
        elif isinstance(value, frozenset):
            return f'frozenset([{format_value}])'
        else:
            return f'{{{format_value}}}'
    else:
        return repr_value


def mapping_hidden_value(value) -> str:
    """Return the hidden string use type map.
    """
    if isinstance(value, str):
        return 'str(...)'
    elif isinstance(value, float):
        return 'float(...)'
    elif isinstance(value, int):
        return 'int(...)'
    elif isinstance(value, complex):
        return 'complex(...)'
    if isinstance(value, list):
        return '[...]'
    elif isinstance(value, tuple):
        return '(...)'
    elif isinstance(value, frozenset):
        return 'frozenset(...)'
    elif isinstance(value, set):
        return 'set(...)'
    elif isinstance(value, dict):
        return '{...}'
    else:
        return repr(value)


def cut_string(word: str, width: int) -> tuple:
    """ Cut the string by space and width, return the tuple of string.
    """
    components = list()
    words = word.split(' ')
    for index, item in enumerate(words):
        suffix = '' if index == len(words) - 1 else ' '
        if components:
            concat_item = f'{components[-1]}{item}'
            # Concat two words,
            # if the concated word’s length is less than width,
            # add the concated word to components.
            if len(concat_item) <= width:
                components.pop()
                item = concat_item

        # When the item's length is more than width,
        # cut the item by width, and send the remained string to the loop.
        while len(item) >= width:
            components.append(item[:width])
            item = item[width:]
        else:
            components.append(f'{item}{suffix}')

    return tuple(components)


def generate_intent(indent: int, level: int) -> str:
    """Return the intent string by indent and level.
    """
    return indent * level * ' '


def get_syntax_highlight(word: str) -> str:
    """Return a syntax highlighted word of the input string.
    """
    return highlight(word,
                     lexers.Python3Lexer(),
                     formatters.Terminal256Formatter(style='native'))
