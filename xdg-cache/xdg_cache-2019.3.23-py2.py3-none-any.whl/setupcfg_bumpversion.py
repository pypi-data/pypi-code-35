#!/usr/bin/env python
"""bump `setup.cfg` `[metadata]` `version`"""
try:
    from configparser import ConfigParser  # python 3+
except ImportError:
    from ConfigParser import ConfigParser  # python 2.x
import public
import os
import sys


@public.add
def bumpversion(path="setup.cfg"):
    """bump `setup.cfg` `[metadata]` `version`"""
    config = ConfigParser()
    config.read(path)
    cfg = open(path, 'w')
    new_version = "0.0.0"
    if config.has_option('metadata', 'version'):
        old_version = config.get('metadata', 'version')
        major, minor, patch = old_version.split(".")
        new_version = "%s.%s.%s" % (major, minor, int(patch) + 1)
    if not config.has_section('metadata'):
        config.add_section('metadata')
    config.set('metadata', 'version', new_version)
    config.write(cfg)
    cfg.close()
    return new_version


MODULE_NAME = os.path.splitext(os.path.basename(__file__))[0]
USAGE = 'usage: python -m %s' % MODULE_NAME


def _cli():
    if not os.path.exists("setup.cfg"):
        raise OSError("setup.cfg NOT EXISTS")
    version = bumpversion("setup.cfg")
    if version:
        print(version)


if __name__ == "__main__":
    if sys.argv[-1] == "--help":
        print(USAGE)
        sys.exit(0)
    _cli()
