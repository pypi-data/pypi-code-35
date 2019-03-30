import re
import unicodedata
from enum import Enum
from functools import reduce
from itertools import accumulate
from typing import Iterator, Tuple


class Kind(Enum):
    COMMENT = 1
    CODE = 2
    ESCAPE = 3


COMMENT_HEADER = re.compile(r"^#\s*")
ESCAPE_HEADER = re.compile(r"^#\s*(~{3,}|`{3,})")


def _new_line(source):
    """Returns the new line code according to the current source."""
    return "\r\n" if "\r\n" in source else "\n"


def format_text(source: str, max_line_length: int = 79) -> str:
    nl = _new_line(source)
    return nl.join(wrapper(source, max_line_length))


def wrapper(source: str, max_line_length: int) -> Iterator[str]:
    for kind, line in joiner(source):
        if kind == Kind.COMMENT:
            yield from wrap(line, max_line_length)
        else:
            yield line


def wrap(line: str, max_line_length: int, pre: str = "# ") -> Iterator[str]:
    max_line_length -= len(pre)
    is_wides = [is_wide(x) for x in line]
    position = list(accumulate(2 if x else 1 for x in is_wides))
    splitterable = [False] + [
        x == " " or (is_wides[k] and is_wides[k + 1]) for k, x in enumerate(line[1:])
    ]

    begin = end = head = 0
    while True:
        if splitterable[head]:
            end = head
        head += 1
        if head >= len(line):
            yield pre + line[begin:].strip()
            break
        elif position[head] - position[begin] - 1 >= max_line_length and begin != end:
            yield pre + line[begin : end + 1].strip()
            begin = end = end + 1


def is_wide(character: str) -> bool:
    return unicodedata.east_asian_width(character) in ["F", "W"]


def is_splittable(line, head) -> bool:
    return line[head] == " " or is_wide(head - 1) or is_wide(head)


def joiner(source: str) -> Iterator[Tuple[Kind, str]]:
    def joint(tail: str, head: str) -> str:
        if is_wide(tail) and is_wide(head):
            return ""
        else:
            return " "

    def join(first: str, second: str) -> str:
        return joint(first[-1], second[0]).join([first, second])

    iterator = splitter(source)
    for kind, line in iterator:
        if kind == Kind.COMMENT:
            lines = []
            for kind, line_ in iterator:
                if kind == Kind.COMMENT:
                    lines.append(line_)
                else:
                    yield Kind.COMMENT, reduce(join, lines, line)
                    yield kind, line_
                    break
            else:
                yield Kind.COMMENT, reduce(join, lines, line)
        else:
            yield kind, line


def splitter(source: str) -> Iterator[Tuple[Kind, str]]:
    nl = _new_line(source)
    iterator = iter(source.split(nl))
    for line in iterator:
        if line.startswith("# #"):
            yield Kind.ESCAPE, line
        elif line.startswith("#"):
            match = re.match(ESCAPE_HEADER, line)
            if match:
                # yield Kind.ESCAPE, re.sub(COMMENT_HEADER, "", line)
                yield Kind.ESCAPE, line
                escape_pattern = match.group()
                while True:
                    try:
                        line = next(iterator)
                    except StopIteration:
                        break
                    # yield Kind.ESCAPE, re.sub(COMMENT_HEADER, "", line)
                    yield Kind.ESCAPE, line
                    if line.startswith(escape_pattern):
                        break
            else:
                line = re.sub(COMMENT_HEADER, "", line)
                if line:  # Drop comment line without any text.
                    yield Kind.COMMENT, line
        else:
            yield Kind.CODE, line
