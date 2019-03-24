import sys
import argparse
from .xlsx import  parse
from .download import  add_url_to_download, exe
from termcolor import  cprint
from functools import  partial
import  io
STDIN =  io.open("/dev/stdin")

parser = argparse.ArgumentParser(usage="Manager project, can create git , sync , encrypt your repo")
parser.add_argument('-p',"--parse", default='', help="default to initialize a projet in current dir")
parser.add_argument('-j', "--json", default=False,action='store_true', help="display current json, default csv")
parser.add_argument('-n', "--name", nargs='*', help="names sheet to display.")
parser.add_argument('-l', "--list", default=False,action='store_true', help="display only sheet name and first row")
parser.add_argument("-C","--context", default=False,action='store_true', help="display ele's context")
parser.add_argument("-e","--encoding", default='utf-8',type=str, help="set encoding for xml parse , default: utf-8")
parser.add_argument('infile', nargs='?', type=argparse.FileType('rb'), default=STDIN)


def main():
    args = parser.parse_args()
    if args.infile:
        cc = args.infile.read()
        parser_func = partial(parse,cc, args.parse, context=args.context)
        
        if args.json:
            parser_func = partial(parser_func, tp='json')
        elif args.list:
            parser_func = partial(parser_func, tp='info')
        
        if args.name:
            for name in args.name:
                parser_func(name=name)
        else:
            parser_func()




if __name__ == "__main__":
    main()
