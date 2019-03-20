from __future__ import absolute_import

import sys
import kmd


def main(args=None):
    return kmd.Kmd().run(args)


if __name__ == '__main__':
    sys.exit(main())

