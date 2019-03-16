# Test just the hello function

from enhancesa import hello
from enhancesa.command_line import main

# Test the hello functions
def test_hello():
    s = hello()
    assert isinstance(s, str)

# Test the command line script
def test_console():
    # returns type(None) because a cmd script
    assert main() is None

