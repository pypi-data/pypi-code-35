import re

import six

PY_IDENTIFIER_VALIDATOR = re.compile(r"^[^\d\W]\w*\Z", re.UNICODE)

PY_FILE_HEADER = """\
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been created with renew.
# A py-pickling tool: https://pypi.org/project/renew/

"""


def build_py_file_content(*objects):
    dependencies_list = []
    validate_objects(objects)
    snippets = []
    for reference_name, single_object in objects:
        snippet = "".join(dispatch_repr(single_object, True, dependencies_list))
        snippets.append("{} = {}\n".format(reference_name, snippet))

    imports = build_imports(dependencies_list)
    return PY_FILE_HEADER + imports + "\n".join(snippets)


def dispatch_repr(object_, top_level=False, dep_list=None):
    if hasattr(object_, "make_py_reference"):
        for element in object_.dispatch_repr(top_level, dep_list):
            yield element

    elif isinstance(object_, list):
        items_reprs = [(None, list(dispatch_repr(item, top_level, dep_list))) for item in object_]
        for element in make_a_markup("[", items_reprs, "]"):
            yield element
    elif isinstance(object_, tuple):
        items_reprs = [(None, list(dispatch_repr(item, top_level, dep_list))) for item in object_]
        for element in make_a_markup("(", items_reprs, ")"):
            yield element
    elif isinstance(object_, set):
        items_reprs = [(None, list(dispatch_repr(item, top_level, dep_list))) for item in sorted(object_)]
        for element in make_a_markup("{", items_reprs, "}"):
            yield element
    elif isinstance(object_, dict):
        items_reprs = [(kw, list(dispatch_repr(value, top_level, dep_list)))
                       for kw, value in sorted(object_.items(), key=lambda x: str(x[0]))]
        for element in make_a_markup("{", items_reprs, "}", as_dict=True):
            yield element
    elif isinstance(object_, six.string_types) and len(object_) > 80:
        if top_level:
            yield "(\n"
            indent = "    "
        else:
            indent = ""
        for line in _split_long_string(object_):
            yield indent + repr(line) + "\n"
        if top_level:
            yield ")"

    else:
        try:
            yield repr(object_)
        except Exception:
            yield object.__repr__(object_)


def build_imports(iterable):
    sorted_ = sorted(iterable, key=lambda x: x[0] or x[1])
    return "".join(make_import_statement(*d) for d in sorted_) + "\n"


def make_import_statement(src, namespace):
    if src:
        return "from {} import {}\n".format(src, namespace)
    else:
        return "import {}\n".format(namespace)


def make_a_markup(begin, items_reprs, end, item_delimiter=",", as_dict=False):
    single_line_body = ", ".join(_form_single_line(items_reprs, as_dict))
    single_line_reproduction = begin + single_line_body + end
    if len(single_line_reproduction) <= 100 or not items_reprs:
        yield single_line_reproduction
    else:
        yield begin + "\n"
        for element in _form_multi_line(items_reprs, item_delimiter, as_dict):
            yield element
        yield end


def _form_single_line(items_representations, as_dict):
    kw_delimiter = ": " if as_dict else "="
    for keyword, value_reps in items_representations:
        if keyword:
            if as_dict:
                keyword = repr(keyword)
            preamble = keyword + kw_delimiter
        else:
            preamble = ""
        yield preamble + "".join(value_reps)


def _form_multi_line(items_reprs, item_delimiter, as_dict):
    kw_delimiter = ": " if as_dict else "="
    indent = "    "
    for keyword, value_reps in items_reprs:
        is_first = True
        for argument_reproduction in value_reps:
            if is_first and keyword is not None:
                if as_dict:
                    keyword = repr(keyword)
                preamble = keyword + kw_delimiter
            else:
                preamble = ""
            optional_break = (item_delimiter + "\n") if not argument_reproduction.endswith("\n") else ""
            is_first = False
            yield indent + preamble + argument_reproduction + optional_break


def _split_long_string(long_string, max_line_width=80):
    lines = long_string.split("\n")
    if not any(len(line) > max_line_width for line in lines):
        for not_last, line in enumerate(lines, 1 - len(lines)):
            yield line + ("\n" if not_last else "")
    else:
        words = long_string.split(" ")
        if not any(len(word) > max_line_width for word in words):
            line, pos = "", 0
            for not_last, word in enumerate(words, 1 - len(words)):
                word += " " if not_last else ""
                line += word
                pos += len(word)
                if pos >= 80:
                    yield line
                    line, pos = "", 0
            if line:
                yield line
        else:
            pos = 0
            while pos < len(long_string):
                yield long_string[pos:pos + max_line_width]
                pos += max_line_width


def validate_objects(objects):
    for i, item in enumerate(objects):
        if not isinstance(item, tuple):
            msg = "Expecting item number {} to be tuple, got {}."
            raise TypeError(msg.format(i, type(item).__name__))
        if len(item) != 2:
            raise TypeError("Expecting tuples with two items, got {} at item number {}".format(len(item), i))
        name, obj = item
        if not isinstance(name, six.string_types):
            msg = "Expecting first item in tuple to be a string, got {} at item number {}"
            raise TypeError(msg.format(type(name).__name__, i))
        if not PY_IDENTIFIER_VALIDATOR.match(name):
            raise ValueError("{} is not a valid python identifier - given at item number {}".format(name, i))
