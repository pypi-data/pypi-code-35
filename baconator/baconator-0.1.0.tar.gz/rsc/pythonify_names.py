#!/usr/bin/env python3
"""Generates the names.py file from the list of names."""
import pathlib


def load_names():
    names_file = pathlib.Path(__file__).parent / 'names'
    with open(names_file, 'r') as fp:
        return [name.rstrip().split() for name in fp if name[0] != '#']


def write_names(fp, var, first_last, index):
    names = sorted(set([name[index] for name in first_last]))
    fp.write(f'{var} = [\n')
    for name in names[:-1]:
        fp.write(f"    '{name}',\n")
    fp.write(f"    '{names[-1]}'\n")  # no trailing comma
    fp.write(']\n')


if __name__ == '__main__':
    names = load_names()
    names_py = pathlib.Path(__file__).parents[1] / 'baconator' / 'names.py'
    with open(names_py, 'w') as fp:
        fp.write('# This file was automatically generated.\n')
        fp.write(f'# See {__file__}.\n\n')
        write_names(fp, 'FIRST_NAMES', names, 0)
        fp.write('\n')
        write_names(fp, 'LAST_NAMES', names, -1)
