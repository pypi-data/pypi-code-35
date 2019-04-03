from . import endpoints
from ...api import _request_executor

def champion_masteries_by_summoner (service_platform, 
                                    api_key,
                                    encrypted_summoner_id):
    """ Get all champion mastery entries sorted by number of champion points descending,

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#champion-mastery-v4/GET_getAllChampionMasteries

    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        encrypted_summoner_id (str): the id of the summoner whose champion masteries to get.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["champion-mastery"]["champion_masteries"]["by-summoner"]["endpoint"].format(encrypted_summoner_id)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)

def champion_masteries_by_summoner_by_champion (service_platform, 
                                                api_key,
                                                encrypted_summoner_id, 
                                                champion_id):
    """ Get a champion mastery by player ID and champion ID.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#champion-mastery-v4/GET_getChampionMastery

    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        encrypted_summoner_id (str): the id of the summoner whose champion mastery to get.
        champion_id (int): the id of the champion whose champion mastery to get.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["champion-mastery"]["champion_masteries"]["by-summoner"]["by-champion"]["endpoint"].format(encrypted_summoner_id, champion_id)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)

def scores_by_summoner (service_platform, 
                        api_key,
                        encrypted_summoner_id):
    """ Get a player's total champion mastery score, which is the sum of individual champion mastery levels

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#champion-mastery-v4/GET_getChampionMasteryScore

    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        encrypted_summoner_id (str): the id of the summoner whose champion mastery score to get.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["champion-mastery"]["scores"]["by-summoner"]["endpoint"].format(encrypted_summoner_id)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)