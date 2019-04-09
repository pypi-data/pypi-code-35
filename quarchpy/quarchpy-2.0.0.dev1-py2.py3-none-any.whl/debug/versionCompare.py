import pkg_resources
from pkg_resources import parse_version, get_distribution
import re

def getQuarchPyVersion ():
    return pkg_resources.get_distribution("quarchpy").version

def requiredQuarchpyVersion (requiredVersion):    
    if (parse_version(getQuarchPyVersion ()) < parse_version(requiredVersion)):
        raise ValueError ("Current quarchpy version is not high enough, upgrade now!")
    else:
        return True