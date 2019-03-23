import inspect
import os
import re


def append_ex_doc(function, create_doc, output_doc_path="examples/README.md"):
    """
        It extracts docs and some info from function and then passes it to `create_doc` function
        that is supposed to be responsible for building a documentation.
        Then the result is appended to `output_doc_path`.

        The reason to handle it in this way is to avoid lies in example / documentation.
        The documentation is build out of test or example function's outcome.
        If test/example breaks, doc creation breaks as well.

        Doctest tools I know are way too primitive. I want it other way around. First python code - then doc.
    """

    example_fcn_name = function.__name__
    py_source_code = get_clean_function_source(function)
    doc_text = inspect.getdoc(function) or "# {}\n".format(example_fcn_name)

    def make_rel_path(path_):
        """Function to create links relative to output doc file."""
        return os.path.relpath(path_, os.path.dirname(output_doc_path))

    py_source_file = inspect.getsourcefile(function)
    examples_dir = os.path.dirname(py_source_file)
    py_relative_path = make_rel_path(py_source_file)

    content = create_doc(example_fcn_name, examples_dir, doc_text, py_relative_path, py_source_code, make_rel_path)

    with open(output_doc_path, 'at') as f:
        f.write(content)


def get_clean_function_source(function):
    """
        'clean' means without a decorator and without function docstring.

        `inspect.getsource` returns the function body with decorator and with it's doc-string.
        We would rather to get just source code.
        This one uses a parametrized regex to substitute decorator, docstring and everything
        starting from a terminator `# example ends here`
    """
    fcn_name = function.__name__
    find_pattern = r".*def {}(.+?)\n\s*(?:'''.*?'''|\"\"\".*?\"\"\"|)\s*(\n.*)".format(fcn_name)
    sub_pattern = r"def {}\1\2".format(fcn_name)
    terminator_pattern = r"(?:\s*#\s*example ends here.*)"
    whole_body = inspect.getsource(function)
    without_docstring = re.sub(find_pattern, sub_pattern, whole_body, 0, re.MULTILINE | re.DOTALL)
    return re.sub(terminator_pattern, "\n", without_docstring, 1, re.MULTILINE | re.DOTALL) + "\n"
