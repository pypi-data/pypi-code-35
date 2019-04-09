import os

from scripting import cp


def test_cp(tmpdir):
    p = tmpdir.mkdir("src").join("hello.txt")
    p.write("hello!")

    src = os.path.join("src", "hello.txt")
    dest = os.path.join("dest", "hi.txt")
    with tmpdir.as_cwd():
        cp(src, dest, create_dirs=True)
        with open(dest, "r") as fp:
            contents = fp.read()

    assert contents == "hello!"


def test_cp_to_dot(tmpdir):
    p = tmpdir.mkdir("src").join("hello.txt")
    p.write("hello!")

    src = os.path.join("src", "hello.txt")
    dest = os.path.join(".", "hi.txt")
    with tmpdir.as_cwd():
        cp(src, dest, create_dirs=True)
        with open(dest, "r") as fp:
            contents = fp.read()

    assert contents == "hello!"


def test_cp_from_dot(tmpdir):
    p = tmpdir.join("hello.txt")
    p.write("hello!")

    src = os.path.join(".", "hello.txt")
    dest = os.path.join("dest", "hi.txt")
    with tmpdir.as_cwd():
        cp(src, dest, create_dirs=True)
        with open(dest, "r") as fp:
            contents = fp.read()

    assert contents == "hello!"


def test_cp_to_cwd(tmpdir):
    p = tmpdir.mkdir("src").join("hello.txt")
    p.write("hello!")

    src = os.path.join("src", "hello.txt")
    dest = "hi.txt"
    with tmpdir.as_cwd():
        cp(src, dest, create_dirs=True)
        with open(dest, "r") as fp:
            contents = fp.read()

    assert contents == "hello!"


def test_cp_from_cwd(tmpdir):
    p = tmpdir.join("hello.txt")
    p.write("hello!")

    src = "hello.txt"
    dest = os.path.join("dest", "hi.txt")
    with tmpdir.as_cwd():
        cp(src, dest, create_dirs=True)
        with open(dest, "r") as fp:
            contents = fp.read()

    assert contents == "hello!"


def test_cp_from_abspath(tmpdir):
    p = tmpdir.join("hello.txt")
    p.write("hello!")

    with tmpdir.as_cwd():
        src = os.path.abspath("hello.txt")
        dest = os.path.join("dest", "hi.txt")
        cp(src, dest, create_dirs=True)
        with open(dest, "r") as fp:
            contents = fp.read()

    assert contents == "hello!"


def test_cp_to_abspath(tmpdir):
    p = tmpdir.join("hello.txt")
    p.write("hello!")

    with tmpdir.as_cwd():
        src = "hello.txt"
        dest = os.path.abspath(os.path.join("dest", "hi.txt"))
        cp(src, dest, create_dirs=True)
        with open(dest, "r") as fp:
            contents = fp.read()

    assert contents == "hello!"


def test_cp_with_folders(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("hello!")

    src = os.path.join("sub", "hello.txt")
    dest = os.path.join("dest", "sub", "hi.txt")
    with tmpdir.as_cwd():
        cp(src, dest, create_dirs=True)
        with open(dest, "r") as fp:
            contents = fp.read()

    assert contents == "hello!"
