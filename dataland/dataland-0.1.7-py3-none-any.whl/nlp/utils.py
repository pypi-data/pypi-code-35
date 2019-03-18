import unicodedata

import regex
from zhon import hanzi, zhuyin

from ..utils import deprecated

ZH_PATTERNS = rf"[{hanzi.characters+zhuyin.characters}]"


def split_and_join(text: str, splitter: str = "", joiner: str = "") -> str:
    """Split string first, then join back to a new string by specified delimiter."""

    return joiner.join(text.split(splitter or None))


def halfwidth(text: str, form="NFKD") -> str:
    """Convert the string to halfwidth"""

    return unicodedata.normalize(form, text)


@deprecated(replaced_by=halfwidth)
def _halfwidth(text: str) -> str:
    """Convert the string to halfwidth.

    full-width characters' unicodes range from 65281 to 65374 (0xFF01 - 0xFF5E in hex)
    half-width characters' unicodes range from 33 to 126 (0x21 - 0x7E in hex)
    `space` in full-width: 12288(0x3000), in half-width: 32(0x20)
    since the unicode difference is fixed between
    full- and half-width forms of single character,
    convert the character to half-width by numeric shifting,
    and handle `space` as a special case
    """
    rstring = ""
    for char in text:
        code = ord(char)
        if code == 0x3000:
            code = 0x0020
        else:
            code -= 0xFEE0
        if code < 0x0020 or code > 0x7E:  # fallback check
            rstring += char
        else:
            rstring += chr(code)
    return rstring


def normalize(text: str, form="NFKD") -> str:
    """Get the normal form form for the Unicode string `unistr`."""

    return regex.sub(r"\p{M}", "", halfwidth(text, form))


def unigram(text: str) -> str:
    """Separate each [`Han` character](https://en.wikipedia.org/wiki/CJK_characters) with space character in sentences

    Args:
        text (str)

    Returns:
        str

    Examples:
        >>> unigram("abc一二三cde efg四五六")
        'abc 一 二 三 cde efg 四 五 六'
    """

    return split_and_join(
        regex.sub(r"({})".format(ZH_PATTERNS), r" \1 ", text), joiner=" "
    )
