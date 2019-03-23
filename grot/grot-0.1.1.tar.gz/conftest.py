import os
import shutil

import pytest

from examples.example2doc import append_ex_doc
from grot import string_types

THIS_DIR = os.path.dirname(__file__)
EXAMPLES_DIR = os.path.join(THIS_DIR, 'examples')
OUTPUT_README = os.path.join(EXAMPLES_DIR, "README.md")
VERBOSE_INFO = True


def info(text):
    if VERBOSE_INFO:
        print(text)


MARKDOWN_TEMPLATE = """\
{fdoc}
```python
{src}
```
Source of this example is in [{py_path}]({py_path}).

It generates raw dot-syntax text file in: [{dot_path}]({dot_path}).
And the final graph file is in: [{img_path}]({img_path}):

[![Rendered example image to be shown in gitlab)]({img_path}?raw=true "{fname}")]({img_path})

"""


def create_doc(example_fcn_name, examples_dir, fcn_docstring, py_relative_path, py_source_code, make_rel_path):
    base_out_file = os.path.join(examples_dir, 'out', example_fcn_name)
    dot_extension = ".gv"
    img_extension = ".png"
    graph_dot_path = base_out_file + dot_extension
    graph_image_path = base_out_file + dot_extension + img_extension
    output_graph = make_rel_path(graph_image_path)
    output_dot_path = make_rel_path(graph_dot_path)
    content = MARKDOWN_TEMPLATE.format(fname=example_fcn_name, fdoc=fcn_docstring,
                                       src=py_source_code,
                                       py_path=py_relative_path, img_path=output_graph, dot_path=output_dot_path)
    return content


def pytest_runtest_teardown(item, nextitem):
    assert isinstance(item, pytest.Function), "Unexpected things happened."
    if item.name.startswith("example"):
        print(item.config)
        append_ex_doc(item.function, create_doc, "examples/README.md")


@pytest.hookspec(firstresult=True)
def pytest_collect_directory(path, parent):
    if os.path.relpath(str(path), EXAMPLES_DIR) == '.':
        output_directory = os.path.join(EXAMPLES_DIR, 'out')

        to_remove = [p for p in (OUTPUT_README, output_directory) if os.path.exists(p)]
        if to_remove:
            info("\nRemoving example2doc outcomes:")
            for p in to_remove:
                info(" - {}".format(p))
                if os.path.isdir(p):
                    shutil.rmtree(p)
                else:
                    os.remove(p)
            info("")


def pytest_assertrepr_compare(op, left, right):
    if op == "==" and isinstance(left, string_types) and isinstance(right, string_types):
        if len(left) > 10 or len(right) > 10:
            compare_strings(left, right)


def side_by_side_diff(left, right):
    return """
--- (left):
{left}---
does not match currently defined reference:
--- (right):
{right}---

""".format(left=left, right=right)


def compare_strings(left, right):
    if left != right:
        print(side_by_side_diff(left, right))
    else:
        return True
