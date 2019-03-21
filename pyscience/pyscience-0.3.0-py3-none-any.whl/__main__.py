'''
pyscience - python science programming
Copyright (c) 2019 Manuel Alcaraz Zambrano

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import sys
import traceback
import argparse
import pyscience
from pyscience.interpreter import PyscienceInterpreter

def main(args):
    if args.version:
        print(f'pyscience {pyscience.__version__}')
        return
    
    if args.debug:
        pyscience.DEBUG = True
    
    print(f'''pyscience {pyscience.__version__} Copyright (C) 2019  Manuel Alcaraz Zambrano
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions; type `license` for details.
''')
    
    interpreter = PyscienceInterpreter()
    
    if pyscience.DEBUG:
        print('Debug mode is on\n')
    
    while 1:
        cmd = interpreter.input()
        
        if cmd in ('q', 'quit', 'exit'):
            break
        elif cmd == 'license':
            print(__doc__)
            continue
        elif not cmd:
            continue
        
        interpreter.exec_function(cmd)

def run():
    parser = argparse.ArgumentParser(prog='pyscience', description='python science programming')
    
    parser.add_argument("-d", "--debug", help="show additional information for developers", action="store_true")
    parser.add_argument("-v", "--version", help="show version and exits", action="store_true")
    
    args = parser.parse_args()
    
    main(args)

if __name__ == '__main__':
    run()
