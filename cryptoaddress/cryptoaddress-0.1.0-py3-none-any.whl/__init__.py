# -*- encoding: utf-8 -*-
from cryptoaddress.core import BitcoinAddress, CryptoAddress, LitecoinAddress

ADDRESS_CLASS_BY_SYMBOL = {addr_class.symbol: addr_class for addr_class in [BitcoinAddress, LitecoinAddress]}


def get_crypto_address(symbol: str, address: str, *args, **kwargs) -> CryptoAddress:
    cryptoaddress_class = ADDRESS_CLASS_BY_SYMBOL.get(symbol)
    if cryptoaddress_class is None:
        raise ValueError('Cryptoaddress not supported: "%s"' % symbol)
    return cryptoaddress_class(address, *args, **kwargs)


__all__ = [
    'CryptoAddress',
    'BitcoinAddress',
    'LitecoinAddress',
    'get_crypto_address',
]
