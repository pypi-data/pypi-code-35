# -*- coding:utf-8 -*-
import os

MEMO = os.path.expanduser('~/.global_memo_v0_0_1')

def _help():
    message = ['usage: gmemo [option | text]',
               'Options and arguments:',
               '-a     : Display all lines.',
               '-h N   : Display N lines from the begining.',
               '-t N   : Display N lines from the end.',
    ]
    _print_lines(message)

def _all(memo):
    if os.path.exists(memo):
        lines = _read_lines(memo)
        _print_lines(lines)

def _head(memo, n):
    try:
        int(n)
    except:
        _print_lines(['Error : Must input number after "-h".'])
        return

    if os.path.exists(memo):
        lines = _read_lines(memo)
        _print_lines(lines[:int(n)])

def _tail(memo, n):
    try:
        int(n)
    except:
        _print_lines(['Error : Must input number after "-t".'])
        return

    if os.path.exists(memo):
        lines = _read_lines(memo)
        _print_lines(lines[-int(n):])

def _read_lines(memo):
    lines = []
    with open(memo, 'r') as f:
        for line in f:
            lines.append(line.strip())
    return lines

def _add_line(memo, line):
    with open(memo, 'a') as f:
        f.write(line + '\n')

def _print_lines(lines):
    print(os.linesep.join(lines))

def main(argv=None):
    if argv:
        option = argv[1]
        if option == '--help':
            _help()
        elif option == '-a':
            _all(MEMO)
        elif option == '-h':
            if len(argv) >= 3:
                _head(MEMO, argv[2])
            else:
                _head(MEMO, '1')
        elif option == '-t':
            if len(argv) >= 3:
                _tail(MEMO, argv[2])
            else:
                _tail(MEMO, '1')
        else:
            line = ' '.join(argv[1:])
            _add_line(MEMO, line)

if __name__ == '__main__':
    import sys
    main(argv=sys.argv)