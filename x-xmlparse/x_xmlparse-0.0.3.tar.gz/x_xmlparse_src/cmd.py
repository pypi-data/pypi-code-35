import sys
import argparse
from lxml import html, etree
from .parse import  parse, show, tree_text, tree_text_draw, nearby
from .download import  add_url_to_download, exe
from termcolor import  cprint

parser = argparse.ArgumentParser(usage="Manager project, can create git , sync , encrypt your repo")
parser.add_argument("parse", help="default to initialize a projet in current dir")
parser.add_argument('-j', "--json", default=False,action='store_true', help="display current json")
parser.add_argument('-t', "--text", default=False,action='store_true', help="display sub text")
parser.add_argument('-tr', "--tree", default=False,action='store_true', help="set tree to display all attris")
parser.add_argument("-C","--context", default=False,action='store_true', help="display ele's context")
parser.add_argument("-D","--download", default=False,action='store_true', help="download from href")
parser.add_argument("-p","--proxy", default=None,type=str, help="set download proxy , like socks5h://127.0.0.1:1080")
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),default=sys.stdin)


def main():
    args = parser.parse_args()
    if args.infile:
        res = parse(args.infile.read(), args.parse)
        if args.context:
            res = [nearby(i) for i in res]

        


        if args.json:
            show(res, tp='json', tree=args.tree)
        elif args.text:
            show(res, tp='text', tree=args.tree)
        elif args.download:
            for q in res:
                attr = q.attrib
                if 'href' in attr and not attr['href'].startswith("javascript") and not attr['href'].endswith("#") :
                    u = attr['href']
                    if u.startswith("http"):
                        cprint("[+] : %s" % u)
                        add_url_to_download(u, args.proxy)
        else:
            show(res)

        if args.download:
            exe.shutdown()



if __name__ == "__main__":
    main()
