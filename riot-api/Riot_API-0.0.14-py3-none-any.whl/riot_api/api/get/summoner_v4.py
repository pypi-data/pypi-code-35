from . import endpoints
from ...api import _request_executor

def summoners_by_account (service_platform, 
                          api_key,
                          encrypted_account_id):
    """ Get a summoner by account ID.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#summoner-v4/GET_getByAccountId
        
    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        encrypted_account_id (str): The id of the account from which to get the summoner.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"]
    path = endpoints.v4["summoner"]["summoners"]["by-account"]["endpoint"].format(encrypted_account_id)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)

def summoners_by_name (service_platform, 
                       api_key,
                       summoner_name):
    """ Get a summoner by summoner name.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#summoner-v4/GET_getBySummonerName
        
    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        summoner_name (str): The name of the summoner to get.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"]
    path = endpoints.v4["summoner"]["summoners"]["by-name"]["endpoint"].format(summoner_name)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)

def summoners_by_puuid (service_platform, 
                        api_key,
                        encrypted_puuid):
    """ Get a summoner by PUUID.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#summoner-v4/GET_getByPUUID
        
    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        encrypted_puuid (str): The puuid of the summoner to get.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"]
    path = endpoints.v4["summoner"]["summoners"]["by-puuid"]["endpoint"].format(encrypted_puuid)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)

def summoners (service_platform, 
               api_key,
               encrypted_summoner_id):
    """ Get a summoner by summoner ID.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#summoner-v4/GET_getBySummonerId
        
    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        encrypted_summoner_id (str): The id of the summoner to get.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"]
    path = endpoints.v4["summoner"]["summoners"]["endpoint"].format(encrypted_summoner_id)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)