"""
Utilities for inspecting and checking data.

Functions
–––––––––
check_if_method
    Checks to see if a named argument corresponds to a method of a given class.
"""
import inspect
import types

def check_if_method(instance, name):
    """Check if a given name corresponds to a method of a class instance."""
    attribute = inspect.getattr_static(instance, name, None)
    if type(attribute) is types.FunctionType:
        flag = True
    else:
        flag = False
    return flag

