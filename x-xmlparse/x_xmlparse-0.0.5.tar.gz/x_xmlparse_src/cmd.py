import sys
import argparse
from lxml import html, etree
from .parse import  parse, show, tree_text, tree_text_draw, nearby
from .download import  add_url_to_download, exe, add_url, init_process, update
from termcolor import  cprint
from functools import  partial
import  concurrent

parser = argparse.ArgumentParser(usage="Manager project, can create git , sync , encrypt your repo")
parser.add_argument("parse", help="default to initialize a projet in current dir")
parser.add_argument('-j', "--json", default=False,action='store_true', help="display current json")
parser.add_argument('-t', "--text", default=False,action='store_true', help="display sub text")
parser.add_argument('-tr', "--tree", default=False,action='store_true', help="set tree to display all attris")
parser.add_argument("-C","--context", default=False,action='store_true', help="display ele's context")
parser.add_argument("-D","--download", default=False,action='store_true', help="download from href")
parser.add_argument("-G","--get", default=False,action='store_true', help="pre curl url from infile and parse")
parser.add_argument("-p","--proxy", default='socks5h://127.0.0.1:1080',type=str, help="set download proxy , like socks5h://127.0.0.1:1080")
parser.add_argument("-lc","--encoding", default='utf-8',type=str, help="set encoding for xml parse , default: utf-8")
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),default=sys.stdin)


def threadparser(res, par_str=''):
    return  parse(res, par_str)


def main():
    args = parser.parse_args()
    parse_str = args.parse
    if args.get:
        ls = args.infile.readlines()
        all_c = len(ls)
        init_process(all_c, 'from file to parse')

        
        thread_parser = partial(threadparser, par_str = parse_str)

        fus = []
        results = []
        for l in ls:
            u = l.strip()
            if not u:continue
            if args.json:
                shower = partial(show, tp='json', tree=args.tree, encoding=args.encoding, url=u, log=True)
            elif args.text:
                shower = partial(show, tp='text', tree=args.tree, encoding=args.encoding, url=u, log=True)
            else:
                shower = partial(show , tree=args.tree, encoding=args.encoding, url=u, log=True)
            fus.append(add_url(u, args.proxy, thread_parser, shower))

        for f in concurrent.futures.as_completed(fus):
            show_lins = f.result()
            update()
            results += show_lins
        for l in results:
            print(l)


        sys.exit(0)
    if args.infile:
        res = parse(args.infile.read(), parse_str)
        if args.context:
            res = [nearby(i) for i in res]

        


        if args.json:
            show(res, tp='json', tree=args.tree, encoding=args.encoding)
        elif args.text:
            show(res, tp='text', tree=args.tree, encoding=args.encoding)
        elif args.download:
            for q in res:
                attr = q.attrib
                if 'href' in attr and not attr['href'].startswith("javascript") and not attr['href'].endswith("#") :
                    u = attr['href']
                    if u.startswith("http"):
                        cprint("[+] : %s" % u)
                        add_url_to_download(u, args.proxy)
        else:
            show(res, encoding=args.encoding)

        if args.download:
            exe.shutdown()

        if args.get:
            exe.shutdown()            



if __name__ == "__main__":
    main()
