import os
import sys
import hashlib
import click


def get_algorithms_available():
    if hasattr(hashlib, "algorithms_available"):
        methods = list(hashlib.algorithms_available)
        methods.sort()
        return methods
    else:
        return ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]


def get_hash_method(script):
    script = os.path.realpath(script)
    _, filename = os.path.split(script)
    name, _ = os.path.splitext(filename)
    return name


def get_file_hash(hash_method_name, file):
    buffer_size = 1024 * 64
    close_file_flag = False
    if file == "-":
        fileobj = sys.stdin.buffer
    else:
        fileobj = open(file, "rb")
        close_file_flag = True
    try:
        gen = hashlib.new(hash_method_name)
        while True:
            buffer = fileobj.read(buffer_size)
            if not buffer:
                break
            gen.update(buffer)
        return gen.hexdigest()
    finally:
        if close_file_flag:
            fileobj.close()


def print_hash_code(code, file, verbose):
    if not verbose:
        click.echo(code)
    else:
        click.echo("{code} {file}".format(code=code, file=file))


def do_hash(hash_method_name, verbose, files):
    if not files:
        files = ["-"]
    for file in files:
        code = get_file_hash(hash_method_name, file)
        print_hash_code(code, file, verbose)


@click.command()
@click.option("-m", "--method", help="Hash method. All available methods are: {0}".format(", ".join(get_algorithms_available())))
@click.option("-v", "--verbose", is_flag=True)
@click.argument("files", nargs=-1)
@click.pass_context
def do_hash_with_context(context, method, verbose, files):
    if not method:
        method = context.obj["method"]
    if not method in get_algorithms_available():
        print("Hash method: {0} is NOT available.".format(method))
        print("All available methods are: {0}".format(", ".join(get_algorithms_available())))
    else:
        do_hash(method, verbose, files)


def main():
    method = get_hash_method(sys.argv[0])
    do_hash_with_context(obj={"method": method})


if __name__ == "__main__":
    main()
