import os
import sys
import subprocess

import click


def trim(docstring):
    """from https://www.python.org/dev/peps/pep-0257/"""
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = 1000
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < 1000:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    # indent everythin by two
    trimmed = ['  {}'.format(line) for line in trimmed]
    # Return a single string:
    return '\n'.join(trimmed)


def check_uid():
    """UID must be defined as environment variable.  Add the following
       line to your shell startup skript (e.g. ~/.bashrc)
         export UID"""
    return 'UID' in os.environ


def check_map_count():
    """max_map_count must be at least 262144. Temporarily increase limit:
       $ sysctl -w vm.max_map_count=262144

       To persist the limit you have to add the following line
       to your /etc/sysctl.d/99-sysctl.conf:
         vm.max_map_count=262144"""

    max_map_count = int(open('/proc/sys/vm/max_map_count').read())
    return max_map_count >= 262144


def check_docker():
    """"""
    cmd = ['docker', 'version']
    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        check_docker.__doc__ += 'docker executable not found'
        return False
    stdout_data, stderr_data = proc.communicate()
    if stderr_data != b'':
        check_docker.__doc__ += stderr_data.decode('utf-8')
        return False

    # TODO check minimum version of docker
    return True


def check_docker_compose():
    """"""
    cmd = ['docker-compose', 'version']
    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        check_docker.__doc__ += 'docker-compose executable not found'
        return False
    stdout_data, stderr_data = proc.communicate()
    if stderr_data != b'':
        check_docker.__doc__ += stderr_data.decode('utf-8')
        return False

    # TODO check minimum version of docker compose
    return True


def main():
    checks = [check_uid, check_map_count, check_docker, check_docker_compose]
    ok = True
    for check in checks:
        name = check.__name__
        if check():
            msg = '✔ {}'.format(name)
            click.echo(click.style(msg, fg='green'))
        else:
            msg = '✖ {}'.format(name)
            click.echo(click.style(msg, fg='red'))
            click.echo(trim(check.__doc__))
            ok = False

    if not ok:
        sys.exit(1)


if __name__ == '__main__':
    main()
