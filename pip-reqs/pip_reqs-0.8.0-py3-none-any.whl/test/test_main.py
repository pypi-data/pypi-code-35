from __future__ import unicode_literals

import pytest

from pip_reqs.__main__ import main, resolve


def test_main_no_args():
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 2


def test_resolve(tmp_path):
    reqs_in, reqs_out = tmp_path / "infile", tmp_path / "outfile"

    class DummyArgs:
        infile = str(reqs_in)
        outfile = str(reqs_out)

    class DummyClient:
        def resolve(self, text):
            assert text == b"dummy text"
            return b"dummy return"

    reqs_in.write_text("dummy text")

    resolve(DummyClient(), DummyArgs())

    assert reqs_out.read_text() == "dummy return"
