from .base_64 import base64_decode_optional_padding
from .json import try_to_parse_json


def unsafe_decode_jwt( jwt_token ):
    """
    method for decode one jwt token without checking the caducity and
    the secret key

    Parameters
    ----------
    jwt_token: string

    Returns
    -------
    tuple
        contain the header and the payload of the token
    """
    jwt_parts = jwt_token.split( '.' )
    header = base64_decode_optional_padding( jwt_parts[0])
    payload = base64_decode_optional_padding( jwt_parts[1])
    return try_to_parse_json( header ), try_to_parse_json( payload )
