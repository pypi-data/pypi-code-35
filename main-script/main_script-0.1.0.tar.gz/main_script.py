import inspect


__all__ = ["main_script"]


def main_script(f):
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    if mod.__name__ == "__main__":
        f()
    return f 
