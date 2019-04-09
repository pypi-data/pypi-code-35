from hashlib import sha256
from typing import Union, Tuple, Optional

# For more information regarding base58 see the following link:
# https://github.com/bitcoin/bitcoin/blob/78dae8caccd82cfbfd76557f1fb7d7557c7b5edb/src/base58.cpp#L14
DIGITS_58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def _decode_base58(address: str, length: int) -> bytes:
    """Decode a base58-encoded address.

    This form of base58 decoding is Bitcoin specific. Be careful outside of
    Bitcoin context.


    Args:
        address: base58-encoded address to decode.
        length: number of bytes that represent the given address.

    Returns:
        The decoded representation of the given base58-encoded address.

    Raises:
        ValueError: If the address cannot be converted to base58.
    """
    number = 0
    for char in address:
        try:
            number = number * 58 + DIGITS_58.index(char)
        except ValueError:
            msg = "Character not part of Bitcoin's base58: '%s'"
            raise ValueError(msg % (char,))
    return number.to_bytes(length, 'big')


def _encode_base58(bytestring: bytes) -> str:
    """Encode a bytestring to a base58 encoded string.

    Args:
        bytestring: bytes to encode in base58 format.

    Returns:
        The base58 string representation of the given bytes.
    """
    zeros = 0
    for byte in bytestring:
        if not byte:
            zeros += 1
        else:
            break
    number = int.from_bytes(bytestring, 'big')
    result = ''
    number, rest = divmod(number, 58)
    while number or rest:
        result += DIGITS_58[rest]
        (number, rest) = divmod(number, 58)
    return zeros * '1' + result[::-1]  # reverse string


def validate_address(address: str, allowed_magicbytes: Optional[Union[int, Tuple[int, ...]]] = 0) -> bool:
    """Check the integrity of a Bitcoin address.

    Args:
        address: Bitcoin address as a string.
        allowed_magicbytes: Tuple of integers representing the valid first byte of the address.

    Returns:
         True if the address is a valid Bitcoin address, and False otherwise.
    """
    if isinstance(allowed_magicbytes, int):
        allowed_magicbytes = (allowed_magicbytes,)
    try:
        bcbytes = _decode_base58(address, length=25)
    except ValueError:
        return False
    # Check magic byte
    if all(bcbytes[0] != magicbyte for magicbyte in allowed_magicbytes):
        return False

    # Compare checksum
    # For more information see https://en.bitcoin.it/wiki/Base58Check_encoding#Creating_a_Base58Check_string
    checksum = sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]
    if bcbytes[-4:] != checksum:
        return False
    # Encoded bytestring should be equal to the original address,
    # for example '14oLvT2' has a valid checksum, but is not a valid btc
    # address
    return address == _encode_base58(bcbytes)
