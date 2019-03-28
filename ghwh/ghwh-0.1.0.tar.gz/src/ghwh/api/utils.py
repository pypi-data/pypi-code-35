from hmac import compare_digest
from hmac import new as hmac_new


def get_hexdigest(key, data, digest):
    return hmac_new(key, data, digest).hexdigest()


def signatures_match(data: bytes, key: bytes, digest: str, signature: str):
    """Test if the signature of data match"""
    return compare_digest(get_hexdigest(key, data, digest), signature)
