#!/usr/bin/python3
import logging
import logging.handlers
logging.basicConfig(
  handlers=[logging.handlers.SysLogHandler(address='/dev/log')],
  format="%(message)s",
  level=0,
)

import subprocess
import os
import sys
import pathlib
import configparser
import pwd
import shutil

logger = logging.getLogger()


def find_aps():
    cmd = shutil.which("autophonesync")
    if cmd is None:
        curfile = pathlib.Path(sys.argv[0]).resolve()
        maybe = curfile.parent / "autophonesync"
        if maybe.exists():
            cmd = str(maybe)
    if cmd is None:
        raise Exception("Cannot find autophonesync")
    return cmd


def run_backup(user, serial):
    logger.info("Starting backup of %s for %s", serial, user)
    # TODO: compatibility with non-systemd systems
    cmd = subprocess.run(
        [
            'systemd-run', '--uid=' + user, '--gid=plugdev', '--no-ask-password',
            find_aps(), 'run', serial,
        ],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
      )
    logger.debug("systemd-run (%i):\n%s", cmd.returncode, cmd.stdout.decode('ascii'))


def devices_for_user(home):
    config = configparser.ConfigParser(
        strict=True,
        interpolation=None,
    )
    config.read(home / '.config' / 'phonesync')
    return config.sections()


def iter_homes():
    for pw in pwd.getpwall():
        yield pw.pw_name, pathlib.Path(pw.pw_dir)


def main():
    serial = os.environ['ID_SERIAL_SHORT']

    for username, home in iter_homes():
        devs = set(devices_for_user(home))
        if serial in devs:
            logger.info("Starting backup for %s", username)
            run_backup(username, serial)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.exception("Exception raised: %r", e)
        raise
