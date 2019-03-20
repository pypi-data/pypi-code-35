import io
import contextlib
from typing import Optional
import logging
import traceback
import sys
import yattag
import uuid

LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s: %(message)s'


def capture_output(
    target: object,
    args: Optional[tuple] = None,
        kwargs: Optional[dict] = None) -> str:
    """Redirect stdout and stderr into string buffer and capture it.

    target object is executed with optional args, kwargs and all stdout/
    stderr that is captured, returned in string form.

    Args:
        target: object to execute, usually a function.
        args: target positional arguments (default: {None})
        kwargs: target keyword arguments (default: {None})
    """
    if not args:
        args = ()
    if not kwargs:
        kwargs = {}

    with io.StringIO() as sio:
        with contextlib.redirect_stdout(sio), contextlib.redirect_stderr(sio):
            target(*args, **kwargs)
            output = sio.getvalue()
            return output


def setup_logger(
        log_level: str = logging.WARNING, fmt: str = LOG_FORMAT) -> None:
    """Set up basic logging configuration."""
    logging.basicConfig(
        format=LOG_FORMAT,
        level=log_level)


def format_list_to_html(
        line_height=1, collapse_cfg: Optional[dict] = None) -> str:
    """Format list of strings into HTML string.

    Lines are converted into HTML paragraphs. line-height attribute is
    set for all paragraphs. This is default format.

    Optionally can specify collapse_cfg to make part of text
    "togglable" (aka read more/read less). Two ways are supported:
        - bootrstrap collapse (default).
        - attr_toggle on div that is "togglable".

    In both cases max_lines key is required.

    First case is used if max_lines is specified (maximum lines to
    show initially), but not attr_toggle. Optionally collapse_id can be
    passed to use it as anchor for bootsrap collapse toggle. Otherwise
    str(uuid.uuid4()) value is used.

    Second case is used if attr_toggle is used. This way only specified
    custom attribute is added on div that wraps paragraphs that should
    be hidden initially. Paragraphs toggle implementation must be done
    externally in this case.

    Args:
        line_height: paragraph height (default: {1})
        collapse_cfg: toggle show/hide part of text config
            (default: {None}) Used keys:
              - max_lines (int): number of paragraphs to show initially.
              - collapse_id (str): anchor for collapse div
                identification. If not set, will use randomly generated
                ID. Bootstrap implementation only.
              - attr_toggle (tuple): attribute used to toggle show/hide
                part of text. Custom implementation only.

    Returns:
        HTML string
    """
    def build_lines(lines):
        for line in lines:
            # Assuming that line is one paragraph, so `\n` is not needed.
            line = line.replace('\n', '')
            with tag('p'):
                text(line)

    def build_bootstrap_collapse(lines_to_hide):
        # Default to random ID if none was specified. It has
        # very low chance to run in collision, so there should
        # be no problem.
        collapse_id = (
            collapse_cfg.get('collapse_id') or str(uuid.uuid4()))
        with tag('div', id=collapse_id, klass='collapse'):
            build_lines(lines_to_hide)
        # Add button to toggle hidden lines.
        with tag(
            'a',
            ('data-toggle', 'collapse'),
            ('data-target', '#%s' % collapse_id),
                klass='btn btn-link'):
            text('Toggle More')

    def format_html(lines):
        with tag('div'):
            doc.attr(style='line-height: %s' % line_height)
            max_lines = collapse_cfg['max_lines']
            if max_lines == -1:  # Everything is showed.
                build_lines(lines)
            else:
                # Split into lines to show and to hide.
                # Lines to hide.
                lines_to_show = lines[0:max_lines]
                lines_to_hide = lines[max_lines:]
                # Build lines that will be visible all the time.
                build_lines(lines_to_show)
                # Build lines that will be hidden initially.
                if collapse_cfg.get('attr_toggle'):
                    # Using custom specified attribute that should be
                    # used to handle toggling of lines_to_hide (
                    # implementation must be done externally from this
                    # method).
                    with tag('div', collapse_cfg['attr_toggle']):
                        build_lines(lines_to_hide)
                else:
                    # Default to bootstrap implementation.
                    build_bootstrap_collapse(lines_to_hide)
        return doc.getvalue()

    if not collapse_cfg:
        collapse_cfg = {'max_lines': -1}
    doc, tag, text = yattag.Doc().tagtext()
    return format_html


def _format_exception() -> list:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return traceback.format_exception(exc_type, exc_value, exc_traceback)


def _get_formatted_exception(
        exc_lines: list, formatter=None) -> str:
    if not formatter:
        return ''.join(exc_lines)
    return formatter(exc_lines)


def get_formatted_exception(formatter=None) -> str:
    """Convert exception lines into formatter string.

    How string is formatted, depends on formatter function passed.
    Formatter acts as constructor, so it needs to be executed where its
    closure function can take specified arguments (if there are any) and
    do actual formatting.

    Args:
        formatter: logic how to format (default: {None}). If not
        specified will default to ''.join(exc_lines).

    Returns:
        formatted exception lines string
    """
    exc_lines = _format_exception()
    return _get_formatted_exception(exc_lines, formatter=formatter)
