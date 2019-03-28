import click
import os
import pendulum
import string
import sys
from ._version import __version__

na = 'NaN'
sep = '\t'


def float_cast(v):
    if v == na:
        return v
    _ = float(v)
    return v


def int_cast(v):
    if v == na:
        return v
    _ = int(v)
    return v


def text_cast(v):
    return v


def time_cast(v):
    return pendulum.parse(v)


typelu = {
    'float': float_cast,
    'integer': int_cast,
    'text': text_cast,
    'time': time_cast
}


def parse_line(line, types):
    fields = line.rstrip().split(sep)
    valid = []
    if len(fields) != len(types):
        raise ValueError("field count doesn't match type count in header")
    for i, t in enumerate(types):
        valid.append(typelu[t](fields[i]))
    return [valid[0].isoformat()] + valid[1:]


def sanitize_column_name(colname):
    """
    Make column names safe to use as a SQL identifier.

    Only keep characters in [a-zA-z0-9$_]. If a name starts with a number
    prepend with an 'x'.
    """
    whitelist = string.ascii_uppercase + string.ascii_uppercase.lower() + '0123456789' + '_$'
    whitelist = set(list(whitelist))
    letters = set(list(string.ascii_uppercase + string.ascii_uppercase.lower()))
    c = ''.join([c for c in list(colname) if c in whitelist])
    if len(c) and c[0] not in letters:
        c = 'x' + c
    return c


@click.command()
@click.argument('infile', type=click.Path(exists=True), nargs=1)
@click.argument('outfile', type=click.Path(), nargs=1)
@click.version_option(version=__version__)
def cli(infile, outfile):
    with open(infile, mode='r', encoding='utf-8') as fin:
        with open(outfile, mode='w', encoding='utf-8') as fout:
            header_lines = []
            for i in range(7):
                line = fin.readline().rstrip()
                if line == '':
                    print("error in header of infile", file=sys.stderr)
                    sys.exit(1)
                header_lines.append(line)
            headers = header_lines[6].split(sep)
            sanitized_headers = [sanitize_column_name(h) for h in headers]
            fout.write(','.join(sanitized_headers) + '\n')
            
            types = header_lines[4].split(sep)

            linenum = 8
            for line in fin:
                try:
                    outputs = parse_line(line, types)
                except Exception as e:
                    print(os.linesep.join(["Error with line {}:".format(linenum), line.rstrip(), str(e), '']), file=sys.stderr)
                else:
                    if outputs:
                        fout.write(','.join(outputs) + '\n')
                linenum += 1
