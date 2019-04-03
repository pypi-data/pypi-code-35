from . import endpoints
from ...api import _request_executor

def codes (service_platform,
           tournament_code,
           api_key,
           spectator_type,
           pick_type,
           map_type,
           allow_summoner_ids=[]):
    """ Update the pick type, map, spectator type, or allowed summoners for a code.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#tournament-v4/PUT_updateCode

    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        tournament_code (str): The tournament code to update.
        api_key (str): The client's api key.
        spectator_type (str): The spectator type. Supported values include "NONE", "LOBBYONLY", and "ALL".
        pick_type (str): The pick type. Supported values include "BLIND_PICK", "DRAFT_MODE", "ALL_RANDOM", and "TOURNAMENT_DRAFT".
        map_type (str): The map type. Supported values include "SUMMONERS_RIFT", "TWISTED_TREELINE", and "HOWLING_ABYSS".
        allow_summoner_ids (str): A list of encrypted summonerIds eligible to join the lobby. (default [])

    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    body_parameters = {
        "spectatorType": spectator_type,
        "pickType": pick_type,
        "allowSummonerIds": allow_summoner_ids,
        "mapType": map_type
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["tournament"]["codes"]["endpoint"].format(tournament_code)

    return _request_executor.put("".join([url, path]),
                                 header_parameters=header_parameters,
                                 body_parameters=body_parameters)

    