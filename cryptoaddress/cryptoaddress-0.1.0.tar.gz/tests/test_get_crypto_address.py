import pytest

from cryptoaddress import get_crypto_address


@pytest.mark.parametrize(('address', 'network_type', 'symbol'), (
    ('1BoatSLRHtKNngkdXEeobR76b53LETtpyT', 'mainnet', 'BTC'),
    ('mtQFox84Lx8RLQCXtVzVn1VfXP6bqbMFC1', 'testnet', 'BTC'),
    ('3QfXkWcNsUH5rRJNurn5whbKJpniVmxmV5', 'mainnet', 'LTC'),
    ('mgYdmeWGZTBoZ9wyxuAFkregSoWga585Mu', 'testnet', 'LTC'),
))
def test_valid_values(address: str, network_type: str, symbol: str) -> None:
    """Verify that valid Bitcoin addresses are successfully created."""
    cryptoaddress = get_crypto_address(symbol, address, network_type=network_type)
    assert str(cryptoaddress) == address
