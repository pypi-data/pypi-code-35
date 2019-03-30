from pyls import hookimpl

from pheasant.renderers.script.script import Script

script = Script()


@hookimpl(hookwrapper=True)
def pyls_format_document(document):
    outcome = yield
    format_document(document, outcome)


@hookimpl(hookwrapper=True)
def pyls_format_range(document, range):
    outcome = yield
    format_document(document, outcome, range)


def format_document(document, outcome, range=None):
    if not document.source.startswith("# "):
        return

    if range is None:
        range = {
            "start": {"line": 0, "character": 0},
            "end": {"line": len(document.lines), "character": 0},
        }
        text = document.source
    else:
        range["start"]["character"] = 0
        range["end"]["character"] = 0
        # range["end"]["line"] += 1  # For cursor staying.
        start = range["start"]["line"]
        end = range["end"]["line"]
        text = "".join(document.lines[start:end])

    result = outcome.get_result()
    if result:
        text = result[0]["newText"]

    max_line_length = get_max_line_length(document.path) or 79

    formatted_text = script.convert(text, max_line_length)

    if formatted_text == text:
        return

    result = [{"range": range, "newText": formatted_text}]
    outcome.force_result(result)


def get_max_line_length(filename: str) -> int:
    try:
        import pycodestyle
    except ImportError:
        return 0

    try:
        style_guide = pycodestyle.StyleGuide(parse_argv=True)
        return style_guide.options.max_line_length
    except Exception:
        return 0
