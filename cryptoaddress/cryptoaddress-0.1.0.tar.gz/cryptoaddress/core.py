from abc import ABC

from cryptoaddress.utils import validate_address


class CryptoAddress(ABC):
    """Base class for all crypto addresses."""
    symbol = None

    def __init__(self, address: str) -> None:
        """Creates a CryptoAddress. This is an abstract class and must not be instantiated but subclassed.

        Args:
            address: cryptoaddress as a string.

        Raises:
            NotImplementedError: if trying to instantiate a CryptoAddress object instead of a subclass.
            ValueError: if the CryptoAddress is invalid.
        """
        if type(self) is CryptoAddress:  # pylint: disable=unidiomatic-typecheck
            raise NotImplementedError('"%s" is an abstract class and should not be instantiated.' %
                                      self.__class__.__name__)
        self._address = address
        self._validate()

    def _validate(self) -> None:
        """Checks if a given crypto address is valid, raising an exception if it's not.

        Raises:
            ValueError: if the crypto address is not valid.
        """
        raise NotImplementedError('"%s" must be overridden by subclasses.')

    def __str__(self) -> str:
        return self._address

    def __repr__(self) -> str:
        return '<{} address={}>'.format(self.__class__.__name__, self._address)


class BitcoinLikeAddress(CryptoAddress):
    """This class represents the abstraction of a Bitcoin address."""
    symbol = None
    magicbytes_mainnet = tuple()
    magicbytes_testnet = tuple()

    def __init__(self, address: str, network_type: str = 'mainnet') -> None:
        """Creates a Bitcoin address.

        Args:
            address: Bitcoin-like address as a string.
            network_type: either 'mainnet' or 'testnet'.

        Raises:
            NotImplementedError: if trying to instantiate a BitcoinLikeAddress object instead of a subclass.
            ValueError: if 'network_type' is not a valid value, or the Bitcoin address is invalid.
        """
        if type(self) is BitcoinLikeAddress:  # pylint: disable=unidiomatic-typecheck
            raise NotImplementedError('"%s" is an abstract class and should not be instantiated.' %
                                      self.__class__.__name__)
        self._network_type = network_type
        super().__init__(address)

    def _validate(self) -> None:
        if self._network_type == 'mainnet':
            magicbytes = self.magicbytes_mainnet
        elif self._network_type == 'testnet':
            magicbytes = self.magicbytes_testnet
        else:
            raise ValueError('"network_type" has to be "mainnet" or "testnet".')
        if not validate_address(self._address, allowed_magicbytes=magicbytes):
            raise ValueError('"%s" is not a valid %s.' % (self._address, self.__class__.__name__))

    def __repr__(self) -> str:
        return '<{} address={} network_type={}>'.format(self.__class__.__name__, self._address, self._network_type)


class BitcoinAddress(BitcoinLikeAddress):  # pylint: disable=too-few-public-methods
    """This class represents a Bitcoin address.

        The Bitcoin address will be validated upon creation, raising an exception if it is not valid.
        For more information see about version, hashing algorithm and checksum see the following links:
        https://github.com/libbitcoin/libbitcoin/wiki/Altcoin-Version-Mappings
        https://github.com/bitcoin/bitcoin/blob/master/src/chainparams.cpp#L131

    """
    symbol = 'BTC'
    magicbytes_mainnet = (0x00, 0x05)
    magicbytes_testnet = (0x6f, 0xc4)


class LitecoinAddress(BitcoinLikeAddress):  # pylint: disable=too-few-public-methods
    """This class represents the abstraction of a Litecoin address.

        The Litecoin address will be validated upon creation, raising an exception if it is not valid.
        For more information see about version, hashing algorithm and checksum see the following links:
        https://github.com/libbitcoin/libbitcoin/wiki/Altcoin-Version-Mappings
        https://github.com/litecoin-project/litecoin/blob/master/src/chainparams.cpp#L135
    """
    symbol = 'LTC'
    magicbytes_mainnet = (0x30, 0x05, 0x32)
    magicbytes_testnet = (0x6f, 0xc4, 0x3a)
