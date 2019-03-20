from __future__ import absolute_import

import sys
import cmd


def main():
    try:
        cmd.Cmd().cmdloop()
    except KeyboardInterrupt:
        sys.stdout.write('\n')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())

