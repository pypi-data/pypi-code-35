from __future__ import print_function

import sys

if sys.version_info < (3, 6):
    print("# ", file=sys.stderr)
    print("# peachrecorder requires Python 3.6 or higher!", file=sys.stderr)
    print("#", file=sys.stderr)
    print("# Please upgrade your Python intepreter", file=sys.stderr)
    print("# If your operating system does not include the", file=sys.stderr)
    print("# required Python version, you can try using pyenv or similar tools.", file=sys.stderr)
    print("#", file=sys.stderr)
    sys.exit(1)

from .proj import run

run()
