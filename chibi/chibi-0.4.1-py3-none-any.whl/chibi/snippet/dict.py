import re

from . import regex as chibi_regex
from .string import camel_to_snake
from chibi.snippet.is_type import is_like_list


def keys_to_snake_case( d ):
    result = {}
    for k, v in d.items():
        if isinstance( k, str ):
            k = camel_to_snake( k )
        if isinstance( v, ( dict, list, tuple ) ):
            v = _inner_keys_to_snake_case( v )
        result[k] = v
    return result


def _inner_keys_to_snake_case( d ):
    if isinstance( d, dict ):
        return keys_to_snake_case( d )
    elif isinstance( d, list ):
        return [ _inner_keys_to_snake_case( a ) for a in d ]
    elif isinstance( d, tuple ):
        return tuple( _inner_keys_to_snake_case( a ) for a in d )
    return d


def replace_keys( d, dr ):
    """
    replace the the keys of a dictionary using another dictioanry for guide

    Parameters
    ----------
    d: dict
        dict is going to have replace his keys
    dr: dict
        dict is going to use for remplace his keys

    Example
    =======
    >>>replace_keys( { 'a': 'a' }, { 'a': 'b' } )
    {'b':'a'}
    """
    if is_like_list( d ):
        for v in d:
            replace_keys( v, dr )
    elif isinstance( d, dict ):
        for k, value in d.items():
            try:
                new_key = dr[k]
                del d[k]
                d[ new_key ] = value
            except KeyError as e:
                pass
            replace_keys( value, dr )


def rename_keys( d, func ):
    """
    rename the keys in a dict using a function

    Parameters
    ----------
    d: dict
        target dict
    func: callable
        function is going to rename rename the keys
    """
    if not callable( func ):
        raise NotImplementedError
    result = {}
    for k, v in d.items():
        result[ func( k ) ] = v
        if isinstance( v, dict ):
            rename_keys( v, func )
    return result


def lower_keys( d ):
    """
    lower all the keys in the dict

    Parameters
    ----------
    d: dict
        target dict
    """
    return rename_keys( d, func=lambda x: x.lower() )


def pop_regex( d, regex ):
    """
    do pop to the keys match with the regex and form a new dict with
    those keys and values

    parameters
    ----------
    d: dict
        target dict
    regex: str or regex
        string to compile the regex or a regex object
    """
    if isinstance( regex, str ):
        regex = re.compile( regex )
    keys = [ k for k in d.keys() ]
    result = {}
    for k in keys:
        if chibi_regex.test( regex, k ):
            result[ k ] = d.pop( k )
    return result


def get_regex( d, regex ):
    """
    hace get a las llaves del dicionario que concuerden con el regex
    y forma un nuevo dicionario con ese

    parameters
    ----------
    d: dict
        dicionarrio que se le haran los gets
    regex: str or regex
        string que se compilara para ser regex
    """
    if isinstance( regex, str ):
        regex = re.compile( regex )
    keys = [ k for k in d.keys() ]
    result = {}
    for k in keys:
        if chibi_regex.test( regex, k ):
            result[ k ] = d.get( k )
    return result
