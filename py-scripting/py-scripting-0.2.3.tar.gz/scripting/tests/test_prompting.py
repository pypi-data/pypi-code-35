from scripting import error, status, success


def test_utf8_encoding():
    status("hi")
    success("yay!")
    error("boo!")
