#! -*- coding:utf-8 -*-

"""
This is a trivial config library.

I tend to go round and round on the "best way to do config".
For now I am content with just passing in a location for an
.ini file, and getting back a dict.

No mess no fuss.

I amsure later on we can add default locations, envvars etc.

usage::

   from mikadolib.common import config
   confd = config.read_ini('/path/to/file.ini')
   x = confd['MYKEY'] 

"""
import configparser


def read_ini(inifilepath):
    """Read a given inifile 

    I am not messing about with combining default ini files or
    otherwise trying to be clever.  *Maybe* have /etc/ location for
    the default file but in general I find that just complicates what
    should be simple, and gets very complicated when dealing with
    diffenrnt envs 

    >>> import config
    >>> c = config.read_ini('/home/pbrian/.devstation/config.ini')
    >>> c
    {'default': {'foo': 'bar', 'balh': '2'}}


    """
    conf = configparser.ConfigParser()
    conf.read(inifilepath)
    return convert_conf_to_dict(conf)

def convert_conf_to_dict(confobj):
    """Convert configparser object to just plain dict """
    d = {}
    for section in confobj._sections:
        d[section] = {};
        d[section].update(confobj[section])
    return d

if __name__ == '__main__':
    import doctest
    doctest.testmod()
