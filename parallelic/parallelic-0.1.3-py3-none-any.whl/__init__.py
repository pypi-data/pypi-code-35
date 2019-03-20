__version__ = "0.1.3"

def main(**kwargs):
    from sys import argv
    from parallelic.util.utils import args_to_kv
    kwargs.update(args_to_kv(*argv))
    if kwargs["execMode"] == "manager":
        from parallelic.manager import main
    if kwargs["execMode"] == "runner":
        from parallelic.runner import main
    if kwargs["execMode"] == "frontend":
        from parallelic.frontend import main
    return main(**kwargs)
