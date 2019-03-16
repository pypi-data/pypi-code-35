import re
import io


def string_limit_visual_length(text, maxlen=None):
    """Limit a string to a *visual* length.

    Will cut string to a specified maximum length, ignoring ANSI
    escape codes in determining the length.

    This allows trimming coloured strings to terminal width.
    """

    stream = io.StringIO()

    TOKEN_RE = re.compile(
        r'(?P<ansi>\033\[((?:\d|;)*)([a-zA-Z]))|(?P<text>.)')

    textlen = 0
    has_ansi = False  # Needs RESET code

    for mo in re.finditer(TOKEN_RE, text):

        if textlen >= maxlen:
            break

        kind = mo.lastgroup
        value = mo.group()

        stream.write(value)

        if kind == 'text':
            textlen += len(value)

        if kind == 'ansi':
            has_ansi = True

    if has_ansi:
        # Add ANSI reset sequence
        stream.write('\x1b[0m')

    return stream.getvalue()
