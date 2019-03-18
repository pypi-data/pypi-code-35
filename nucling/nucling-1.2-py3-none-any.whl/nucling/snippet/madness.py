"""
function for get random things
"""
import base64
import random
import string

from nucling.snippet import base_64


def generate_string( length=10, letters=string.ascii_letters ):
    """
    Generate a random string

    Arguments
    ---------
    length: int, optional, default 10

    Returns
    -------
    string
        random string
    """
    return u''.join(
        random.choice(  letters ) for x in range( length )
    )


def generate_email( domain=None, extention=None ):
    """
    Generate random email

    Arguments
    ---------
    domain: string, optional
        Name of domain of email, if no sen is generate randomly
    extention: string, optional
        extencion of the email, if no send is generate randomly

    Returns
    -------
    string
        random string formatted randomly
    """
    if not domain:
        domain = generate_string( 10 )
    if not extention:
        extention = generate_string( 10 )
    return "{name}@{domain}.{extention}".format(**{
        'name': generate_string( 10 ),
        'domain': domain,
        'extention': extention,
    })


def generate_password(
        length=20,
        letters=(
            string.ascii_letters + string.digits + string.punctuation ) ):
    """
    generate a random password

    Arguments
    ---------
    length: int
        length of the new password
    letters: string
        list of all character what to be used
    """
    return generate_string( length, letters )


def generate_token( length=20 ):
    """
    generate tokens

    Arguments
    ---------
    length: int
        number of bytes want to used
    """
    return base_64.random_b64( length )


def generate_b64_unsecure( length=24 ):
    """
    generate a base 64 string without using urandom

    Arguments
    ---------
    length: int
        number of bytes want to be used
    """
    bites = bytearray( random.getrandbits( 8 ) for _ in range( length ) )
    return base64.urlsafe_b64encode( bites ).decode( 'utf-8' )
