import argparse
from os import environ
from os.path import basename, dirname
import subprocess

from jinja2 import Environment, FileSystemLoader


__version__ = "0.1.0"


def defined_env(key):
    return key in environ


def get_env(key):
    return environ.get(key)


def run(cmd, cwd="."):
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        print(f"subprocess '{cmd}' exited with non-zero status, stderr: {proc.stderr}")
    return proc.stdout


def render_file(src, dest):
    j2 = Environment(loader=FileSystemLoader(dirname(src)))
    j2.filters['env'] = get_env
    j2.filters['run'] = run
    j2.tests['defined_env'] = defined_env
    template = j2.get_template(basename(src))
    rendered = template.render()
    with open(dest, mode="w") as fh:
        fh.write(rendered)


def main():
    parser = argparse.ArgumentParser(description='Render Jinja2 template to file.')
    parser.add_argument('src', help='The path to the Jinja2 template.')
    parser.add_argument('-d', '--dest', help='The path to write to.')
    args = parser.parse_args()
    if not args.dest:
        if args.src.endswith(".jinja"):
            args.dest = args.src.rstrip(".jinja")
        else:
            print("error: dest is required if src does not end with .jinja")
            exit(1)
    render_file(args.src, args.dest)


if __name__ == "__main__":
    main()
