#!/usr/bin/env python3
import fileinput
import matplotlib
filename = matplotlib.matplotlib_fname()
print('In file: {}'.format(filename))
text_to_search = 'backend '
replacement_text = '#backend '
print('replace {} by {}'.format(text_to_search, replacement_text))
with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace(text_to_search, replacement_text), end='')
