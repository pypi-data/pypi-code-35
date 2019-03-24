import os
import sys
import argparse
from cuisel import cuisel

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', help='show line numbers', action='store_true')
    parser.add_argument('-m', '--modeline', help='show modeline', action='store_true')
    args = parser.parse_args()

    istream = sys.stdin.read()
    if '\n' in istream:
        items = [line for line in istream.split('\n') if line]
    else:
        items = istream.split()

    # handles pipe I/O
    ftty = open('/dev/tty', 'r+')
    if not sys.stdin.isatty():
        sys.stdin.close()
        os.dup2(ftty.fileno(), 0)
    fout = None
    if not sys.stdout.isatty():
        fout = os.dup(sys.stdout.fileno())
        os.dup2(ftty.fileno(), sys.stdout.fileno())

    selected = cuisel(items, number=args.number,
            modeline=args.modeline)
    if '\n' in istream:
        result = '\n'.join([item for _, item in selected]) + '\n'
    else:
        result = ' '.join([item for _, item in selected])

    if fout is not None:
        with os.fdopen(fout, 'w') as f:
            f.write(result)
    else:
        ftty.write(result)


if __name__ == '__main__':
    main()
