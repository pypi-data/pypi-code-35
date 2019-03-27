from __future__ import unicode_literals

import pytest

from pip_reqs.parser import RequirementsParser


SETUP_PY = """
from setuptools import setup, find_packages

setup(
    name = 'Test Package',
    version = '1.0.0',
    url = 'https://github.com/test.git',
    author = 'Author Name',
    author_email = 'author@gmail.com',
    description = 'Description of test package',
    packages = find_packages(),
    install_requires = {requirements!r},
)
"""


@pytest.mark.parametrize(
    "reqs,expected_ext,expected_local",
    [
        ("", [], []),
        ("django", [b"django"], []),
        ("django==2.0", [b"django==2.0"], []),
        (
            "https://github.com/django/django/master.zip",
            [b"https://github.com/django/django/master.zip"],
            [],
        ),
    ],
)
def test_requirements_parser_parse(
    reqs, expected_ext, expected_local, tmp_path
):
    reqs_in = tmp_path / "requirements.in"
    reqs_in.write_text(reqs)

    parser = RequirementsParser()
    ext_reqs, local_reqs = parser.parse(str(reqs_in))

    assert ext_reqs == expected_ext
    assert local_reqs == expected_local


@pytest.mark.parametrize(
    "local_reqs,expected_ext,expected_local",
    [(["django"], [b"django"], ["-e file://{tmpdir}/local"])],
)
def test_requirements_parser_parse_local(
    local_reqs, expected_ext, expected_local, tmp_path
):
    expected_local = [
        e.format(tmpdir=tmp_path).encode("utf-8") for e in expected_local
    ]

    pkg = tmp_path / "local"
    pkg.mkdir()
    (pkg / "setup.py").write_text(SETUP_PY.format(requirements=local_reqs))

    reqs_in = tmp_path / "requirements.in"
    reqs_in.write_text("-e {}".format(pkg))

    parser = RequirementsParser()
    ext_reqs, local_reqs = parser.parse(str(reqs_in))

    assert ext_reqs == expected_ext
    assert local_reqs == expected_local


@pytest.mark.parametrize("reqs", [
    "-e git+https://github.com/project.git#egg=test",
])
def test_requirements_parser_parse_error(reqs, tmp_path):
    reqs_in = tmp_path / "requirements.in"
    reqs_in.write_text(reqs)

    parser = RequirementsParser()
    with pytest.raises(NotImplementedError):
        parser.parse(str(reqs_in))
