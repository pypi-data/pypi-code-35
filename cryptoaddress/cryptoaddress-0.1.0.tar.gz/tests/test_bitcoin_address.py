import pytest

from cryptoaddress.core import BitcoinAddress


@pytest.mark.parametrize(('address', 'network_type'), (
    ('1BoatSLRHtKNngkdXEeobR76b53LETtpyT', 'mainnet'),
    ('18vPrXytWtRhSrNDmuJMKREY9mS9kUsqLk', 'mainnet'),
    ('1Ed9LSctAZXC5F96z7ZdfB7xrWFzHkbvA8', 'mainnet'),
    ('1PZCUVS9CQTREbYZ9uq1xRog7V8x9GG2yt', 'mainnet'),
    ('1NdvXKxxfM4up6MzynD9FiTFY5iVo6JaVR', 'mainnet'),
    ('1MYK3794SdheTxmTATZ2svyMSqh6HZxzLQ', 'mainnet'),
    ('3E6eTHhZr5KT5XnyLFmyK8fM1vR2UBtqoi', 'mainnet'),
    ('3HPm5xXjHxFF6CbK7MasD1NbPodjp7mBG4', 'mainnet'),
    ('3Hb8jZY2GBVVqnwYBfQmMDu8FH2NWmVAD9', 'mainnet'),
    ('3Dyhp23A8gzp1gmf4pDmNJTRoqMXkfJTaZ', 'mainnet'),
    ('3D29zUU5cW1bPm4XwYQXphtmQAqtVG511z', 'mainnet'),
    ('3A7RgyQMesCyiyXobneBnncSDSwFKTJUSw', 'mainnet'),
    ('3PWSXz2fePM3Qk8kETGpbkbGhvNBwVrEbo', 'mainnet'),
    ('35jFdr2BhoW3K3GwxU5ESD5AJhZzKBHKHK', 'mainnet'),
    ('3JjcLvyxr4gx9ReMPSPaWVvgayooz1VMwf', 'mainnet'),
    ('mtQFox84Lx8RLQCXtVzVn1VfXP6bqbMFC1', 'testnet'),
    ('mvj52MCP4TXHPLMMNLioTh8VJxZL3U3ZVE', 'testnet'),
    ('n2qSd1ekdANkdn8unNLX7mEVgMcEe1yT6K', 'testnet'),
    ('mkLNyXiaN2A53UErSUdew7STiKqgX93LF2', 'testnet'),
    ('n2qSd1ekdANkdn8unNLX7mEVgMcEe1yT6K', 'testnet'),
    ('n3nv1QBd7ZHBN2gAobQF5LTiT8F59fSNo8', 'testnet'),
    ('miXhAwz1SgCqpcCP5LMVxrkKPhUCuDJw7f', 'testnet'),
    ('minDoXCGSx44KH9DBxGBC2wANhpE1hoGwi', 'testnet'),
    ('mn3XByTZwymcqiHiNm1XrTfw5e4LJ8QUsp', 'testnet'),
))
def test_valid_values(address: str, network_type: str) -> None:
    """Verify that valid Bitcoin addresses are successfully created."""
    bitcoin_address = BitcoinAddress(address, network_type=network_type)
    assert str(bitcoin_address) == address


@pytest.mark.parametrize(('address', 'network_type'), (
    ('', 'mainnet'),
    ('1', 'mainnet'),
    ('3', 'mainnet'),
    ('mvj52MCP4TXHPLMMNLioTh8VJxZL3U3ZVE', 'mainnet'),
    ('n3nv1QBd7ZHBN2gAobQF5LTiT8F59fSNo8', 'mainnet'),
    ('1NdvXKxxfM4up6MzynD9F', 'mainnet'),
    ('', 'testnet'),
    ('1PZCUVS9CQTREbYZ9uq1xRog7V8x9GG2yt', 'testnet'),
    ('1MYK3794SdheTxmTAT', 'testnet'),
    ('m', 'testnet'),
    ('n', 'testnet'),
))
def test_invalid_values(address: str, network_type: str) -> None:
    """Verify that invalid Bitcoin addresses are detected."""
    with pytest.raises(ValueError):
        BitcoinAddress(address, network_type=network_type)
