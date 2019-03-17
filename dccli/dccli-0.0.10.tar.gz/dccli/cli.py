from clint import resources

from dccli.git_helper import get_repo_toplevel_dir
from dccli.job import Submit, CheckProgress, Download, StreamLog, Stop
from dccli.user import Login, Register
from dccli.utils import *


def main():
    if get_repo_toplevel_dir() is None:
        console_out_error("Error: Not in a git repository")
        exit(-1)

    support_functions = {
        "register": Register(),
        "login": Login(),
        "submit": Submit(),
        "progress": CheckProgress(),
        "stream": StreamLog(),
        "download": Download(),
        "stop": Stop()
    }

    function_lists = [k for k in support_functions.keys()]

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "function_name",
        type=str,
        help="function name you want to invoke",
        choices=function_lists)

    FLAGS, _ = parser.parse_known_args()
    function_name = FLAGS.function_name
    resources.init('DeepCluster', 'dccli')
    try:
        support_functions[function_name].parse_and_execute()
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        console_out_error("Error: Unexpected error {}".format(str(e)))
        if DEBUG:
            traceback.print_exc()
            exit(-1)


if __name__ == "__main__":
    main()
