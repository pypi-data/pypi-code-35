from . import endpoints
from ...api import _request_executor

def codes (service_platform,
           api_key,
           tournament_id,
           spectator_type,
           team_size,
           pick_type,
           map_type,
           allowed_summoner_ids=None,
           count=None,
           metadata=None):
    """ Create a mock tournament code for the given tournament.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#tournament-v4/POST_createTournamentCode

    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        tournament_code (str): The tournament code to update.
        api_key (str): The client's api key.
        spectator_type (str): The spectator type. Supported values include "NONE", "LOBBYONLY", and "ALL".
        pick_type (str): The pick type. Supported values include "BLIND_PICK", "DRAFT_MODE", "ALL_RANDOM", and "TOURNAMENT_DRAFT".
        map_type (str): The map type. Supported values include "SUMMONERS_RIFT", "TWISTED_TREELINE", and "HOWLING_ABYSS".
        allow_summoner_ids (str): A list of encrypted summonerIds eligible to join the lobby. (default [])
        count (int): The number of codes to create (maximum 1000).
        metadata (str): Used to denote any custom information about the game.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    query_parameters = {
        "count": count,
        "tournamentId": tournament_id
    }

    body_parameters = {
        "spectatorType": spectator_type,
        "teamSize": team_size,
        "pickType": pick_type,
        "allowedSummonerIds": allowed_summoner_ids,
        "mapType": map_type,
        "metadata": metadata
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["tournament-stub"]["codes"]["endpoint"]

    return _request_executor.post("".join([url, path]),
                                  header_parameters=header_parameters,
                                  query_parameters=query_parameters,
                                  body_parameters=body_parameters)

def providers (service_platform,
               api_key,
               region,
               url):
    """ Creates a mock tournament provider and returns its ID.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#tournament-v4/POST_registerProviderData

    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        region (str): The region in which the provider will be running tournaments. Supported values include "BR", "EUNE", "EUW", "JP", "LAN", "LAS", "NA", "OCE", "PBE", "RU", and "TR".
        url (str): 	The provider's callback URL to which tournament game results in this region should be posted.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    body_parameters = {
        "region": region,
        "url": url
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["tournament-stub"]["codes"]["endpoint"]

    return _request_executor.post("".join([url, path]),
                                  header_parameters=header_parameters,
                                  body_parameters=body_parameters)

def tournaments (service_platform,
                 api_key,
                 provider_id,
                 name=None):
    """ Creates a mock tournament and returns its ID.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#tournament-v4/POST_registerProviderData

    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        provider_id (int): 	The provider ID to specify the regional registered provider data to associate this tournament.
        name (str): The name of the tournament. (default None)
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    body_parameters = {
        "name": name,
        "provider_id": provider_id
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["tournament-stub"]["codes"]["endpoint"]

    return _request_executor.post("".join([url, path]),
                                  header_parameters=header_parameters,
                                  body_parameters=body_parameters)