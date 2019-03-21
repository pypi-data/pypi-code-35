import argparse
import os
from .core import py_init, init, L
from .data import  search, Con, Proj, DB

parser = argparse.ArgumentParser(usage="Manager project, can create git , sync , encrypt your repo")
parser.add_argument("key", nargs='*', help="search in db and return path")
parser.add_argument("-i","--init", help="default to initialize a projet in current dir")
parser.add_argument("-d","--dependences", nargs="*", help="set dependences ")
parser.add_argument("-u", "--usage", help="usage to desscription")
parser.add_argument("-l", "--list", default=False,action='store_true',help="list all repo")
parser.add_argument("-r", "--rm", help="rm repo")
parser.add_argument("-c", "--cmd", default='',help="set cmd name")



def main():
    args = parser.parse_args()
    if args.init:
        if '/' in args.init:
            n = os.path.basename(args.init)
        elif ' ' in args.init:
            n = args.init.replace(' ', '_')
        elif '-' in args.init:
            n = args.init.replace('-', '_')
        else:
            n = args.init
        init(n)
        p = os.path.join(os.getcwd(), n)
        if not args.dependences:
            ss = []
        else:
            ss = args.dependences
        py_init(p, n, *ss, desc=args.usage, cmd=args.cmd)
    
    if args.key:
        v = search(' '.join(args.key))
        print(v[0].path, end='')
    
    if args.rm:
        c = Con(DB)
        r = c.query_one(Proj, name=args.rm)
        if r:
            c.delete(r)
                
            L("remove dir in path : %s "% r.path, color='blue')

    if args.list:
        c = Con(DB)
        rs = c.query(Proj)
        for r in rs:
            L("%s: %s" % (r.name, r.path), color='magenta')


if __name__ == "__main__":
    main()
