#! -*- coding:utf-8 -*-

"""
This is a trivial config library.

I tend to go round and round on the "best way to do config".
For now I am content with just passing in a location for an
.ini file, and getting back a dict.

No mess no fuss.

I am sure later on we can add default locations, envvars etc.

Because its an ini file it must have _sections_ - including the 
'default'.  This is awkward, as I dont like the API being
confd['default']['name'] and prefer confd['name']
However if I add a section myself, I clearly want it namespaced
as in confd['volumes']['data']


usage::

   from mikadolib.common import config
   confd = config.read_ini('/path/to/file.ini')
   x = confd['MYKEY'] 

"""
import configparser
import copy

def read_ini(inifilepath):
    """Read a given inifile 

    I am not messing about with combining default ini files or
    otherwise trying to be clever.  *Maybe* have /etc/ location for
    the default file but in general I find that just complicates what
    should be simple, and gets very complicated when dealing with
    diffenrnt envs
 
    >>> testd = {'hello':'sailor', 'section1': {'foo':'bar'}, 'bill':'ben'}
    >>> import config
    >>> loc = '/tmp/foo.ini' 
    >>> config.write_ini(testd, loc)
    >>> confd = config.read_ini(loc)
    >>> confd == testd # Test dict equalty and ensure round trip
    True

    """
    conf = configparser.ConfigParser()
    conf.read(inifilepath)
    return convert_conf_to_dict(conf)

def write_ini(confd, inifilepath):
    """Write a given dict `confd` to inifile format at `inifilepath`.

    confd must be a dict. Any dict items in confd will be treated as
    *sections* in the ini file, and their key/items will be written
    under the section name.  However anything else in confd not a dict
    will be assumed to be in 'default' section.

    default section is stored in ini file but reading will remove
    default and promote those keys to top level.

    We perfomr deepcopy, because else we will pop / transform the 
    dict passed in (ie changing something at outer level). THis is 
    unexpected so we avoid.

    """
    incomingd = copy.deepcopy(confd)
    conf = configparser.ConfigParser()
    removekeys = []
    for k,i in incomingd.items():
        if isinstance(i, dict):
            conf[k] = i
            removekeys.append(k)
    #remove all dict items from incoming confd. (canot change size of
    #dict whilst iterating over it)
    for k in removekeys:
        incomingd.pop(k)
    #all remaining items into default
    conf['default'] = incomingd
    with open(inifilepath, 'w') as fo:
        conf.write(fo)
    


def convert_conf_to_dict(confobj):
    """Convert configparser object to just plain dict """
    d = {}
    for section in confobj._sections:
        if section == 'default':
            d.update(confobj[section])
        else:
            d[section] = {};
            d[section].update(confobj[section])
    return d

if __name__ == '__main__':
    import doctest
    doctest.testmod()
