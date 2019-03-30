from typing import List, Tuple

from tdameritrade_client.client import TDClient


def get_positions(client: TDClient) -> Tuple[str, List[List[str]]]:
    """
    Retrieve all positions for the authenticated account.

    Args:
        client: An authorized TDClient object.

    Returns:
        liq_value (str): The current liquidation value of the account.
        extracted_data (List[List[str]]): A list of positions where each position is
                                          [position_id, position_type, position_value].

    """

    acct_info = client.get_positions()
    positions = acct_info['securitiesAccount']['positions']
    liq_value = acct_info['securitiesAccount']['currentBalances']['liquidationValue']
    extracted_data = [
        [pos['instrument']['symbol'],
         pos['instrument']['assetType'],
         pos['marketValue']] for pos in positions]
    return liq_value, extracted_data
