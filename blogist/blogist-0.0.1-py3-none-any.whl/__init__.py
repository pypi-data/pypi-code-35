import argparse

from blogist.gist import Gist


def main():
    parser = argparse.ArgumentParser(description='Generate blog posts from GitHub Gist')
    parser.add_argument('--name', '-n', type=str, required=True, help='your GitHub login name')
    parser.add_argument('--prefix', '-p', type=str, default='[blog]', help='the prefix of gist title that belongs to blog posts')
    parser.add_argument('--format', '-f', type=str, default='md', help='post format')
    parser.add_argument('--dir', '-d', type=str, default='_post/', help='where should posts store')

    args = parser.parse_args()
    gist = Gist(args.name, args.prefix, args.format)
    gist.fetch_all_posts()
    gist.store(args.dir)
