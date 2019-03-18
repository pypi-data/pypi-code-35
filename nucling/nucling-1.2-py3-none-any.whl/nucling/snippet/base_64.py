import base64
import os


def base64_encode( s ):
    """
    encode a kind of string in base64

    Parameters
    ----------
    s: string
        a kind of string wanted encode in base64

    Returns
    -------
    string
        a string of base64 in utf-8

    Notes
    -----
    the chars set used for the encode of base64
    are the set of urlsafe

    Examples
    --------
    >>>  base64_encode( 'asdf' )
    'YXNkZg=='
    """
    if isinstance( s, str ):
        s = s.encode( 'utf-8' )
    return base64.urlsafe_b64encode( s ).decode( 'utf-8' )


def base64_decode( s ):
    """
    dencode a string of base64

    Parameters
    ----------
    s: string
        a string of base64

    Returns
    -------
    string
        the decode string in utf-8

    Examples
    --------
    >>>  base64_decode( 'YXNkZg==' )
    'asdf'
    """
    return base64.urlsafe_b64decode( s ).decode( 'utf-8' )


def random_b64( number_of_bytes=3 ):
    """
    Generate a random string of base64

    Parameters
    ----------
    number_of_bytes: int, optional
        number of bytes used for generated the string of base64
        ( the default is 3 )

    Returns
    -------
    string
        a string of base64

    Examples
    --------
    >>> random_b64()
    'nuff'
    >>> random_b64( 1 )
    'VA=='
    >>> random_b64( 4 )
    '9Vag-Q=='
    """
    return base64_encode( os.urandom( number_of_bytes ))


def base64_decode_optional_padding( data ):
    """
    Decode base64, padding being optional.

    Parameters
    ----------
    data: string
        Base64 data as an ASCII byte string
    """
    if isinstance( data, bytes ):
        data = data.decode()
    else:
        data = data.encode( 'utf-8' )
    missing_padding = len( data ) % 4
    if missing_padding != 0:
        data += b'=' * ( 4 - missing_padding )
    return base64_decode( data )
