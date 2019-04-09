import pytest

from cryptoaddress.core import LitecoinAddress


@pytest.mark.parametrize(('address', 'network_type'), (
    ('3QfXkWcNsUH5rRJNurn5whbKJpniVmxmV5', 'mainnet'),
    ('3PmniR1a9Pj8EMvpua4jodJxLoLSECAVpm', 'mainnet'),
    ('37R8Au1VJ9ms9wEh1vvM2fdiwWfJr36bUU', 'mainnet'),
    ('LXgVjKUg7ofyGujnZfNivcLb3VvLitKebS', 'mainnet'),
    ('3PmniR1a9Pj8EMvpua4jodJxLoLSECAVpm', 'mainnet'),
    ('LeRLhx2wcgQ3izsU67Z2TJjm6B4tfbR2r3', 'mainnet'),
    ('LWVs5kSw9Hc2JzJ1AUzEF6TXeEbghLcn75', 'mainnet'),
    ('3CaFsgN2frBGk9dyJPDEvgjxHdwNAPKUQ8', 'mainnet'),
    ('3KvzXb2Kak6ohRaERXFF2zZRpFQG7hm4ds', 'mainnet'),
    ('LeKAQfgTPwaexaDPtygmdBRhmhvezsVA9Z', 'mainnet'),
    ('LSt5cRxBKmBSrgz1P3cNpdLg4jybzywwKN', 'mainnet'),
    ('LXyw13JguXsHRCCm9JSYTztzrgKyASrb85', 'mainnet'),
    ('LeRRNnQ1nYJcMDTx4JiHUQEnXSvBihYdEr', 'mainnet'),
    ('LTF2uqxyLaQMTC6vd7hDHtJeDyzL3mCcuz', 'mainnet'),
    ('mgYdmeWGZTBoZ9wyxuAFkregSoWga585Mu', 'testnet'),
    ('mpoR7DHuydbEtaRziv13gfFcS16XYSi8oc', 'testnet'),
    ('n4rDEvfVYwDfRj5NBkcF9Y4EaJk7WXnfgZ', 'testnet'),
    ('n1osQrvM14tdZqSVLZvMNHKaPnuhcsVdQa', 'testnet'),
    ('n3nv1QBd7ZHBN2gAobQF5LTiT8F59fSNo8', 'testnet'),
    ('n2h9idbD43Vz5BT5zZYss2D1VthHT32hSt', 'testnet'),
    ('mpPR1S1m6jJGJSDyTt8RVbKE6dCgyAayNs', 'testnet'),
    ('mxRQ6qDR4ipHzwtAF18x5oo2nt9izXbDRD', 'testnet'),
))
def test_valid_values(address: str, network_type: str) -> None:
    """Verify that valid Litecoin addresses are successfully created."""
    bitcoin_address = LitecoinAddress(address, network_type=network_type)
    assert str(bitcoin_address) == address


@pytest.mark.parametrize(('address', 'network_type'), (
    ('', 'mainnet'),
    ('1', 'mainnet'),
    ('3', 'mainnet'),
    ('mvj52MCP4TXHPLMMNLioTh8VJxZL3U3ZVE', 'mainnet'),
    ('n3nv1QBd7ZHBN2gAobQF5LTiT8F59fSNo8', 'mainnet'),
    ('1NdvXKxxfM4up6MzynD9F', 'mainnet'),
    ('', 'testnet'),
    ('1PZCUVS9CQTREbYZ9uq1xROg7V8x9GG2yt', 'testnet'),
    ('1MYK3794SdheTxmTAT', 'testnet'),
    ('m', 'testnet'),
    ('n', 'testnet'),
))
def test_invalid_values(address: str, network_type: str) -> None:
    """Verify that invalid Litecoin addresses are detected."""
    with pytest.raises(ValueError):
        LitecoinAddress(address, network_type=network_type)
