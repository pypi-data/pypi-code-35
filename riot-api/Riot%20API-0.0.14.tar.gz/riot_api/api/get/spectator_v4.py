from . import endpoints
from ...api import _request_executor

def active_games_by_summoner (service_platform, 
                              api_key,
                              encrypted_summoner_id):
    """ Get current game information for the given summoner ID.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#spectator-v4/GET_getCurrentGameInfoBySummoner
        
    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        encrypted_summoner_id (str): The id of the summoner whose current game information to get.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["spectator"]["active-games"]["by-summoner"]["endpoint"].format(encrypted_summoner_id)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)

def feature_games (service_platform, 
                   api_key):
    """ Get list of featured games.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#spectator-v4/GET_getFeaturedGames
        
    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["spectator"]["featured-games"]["endpoint"]

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)