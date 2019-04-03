from . import endpoints
from ...api import _request_executor

def challenger_leagues_by_queue (service_platform, 
                                 api_key,
                                 queue):
    """ Get the challenger league for given queue.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/game-constants.html
        https://developer.riotgames.com/api-methods/#league-v4/GET_getChallengerLeague

    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        queue (str): The queue for which to get the challenger league.
    Returns:
        dict: the details of the response to the issued http request. 
    """
    
    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["league"]["challengerleagues"]["by-queue"]["endpoint"].format(queue)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)

def grandmaster_leagues_by_queue (service_platform,  
                                  api_key,
                                  queue):
    """ Get the grandmaster league for given queue.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/game-constants.html
        https://developer.riotgames.com/api-methods/#league-v4/GET_getGrandmasterLeague

    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        queue (str): The queue for which to get the grandmaster league.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["league"]["grandmasterleagues"]["by-queue"]["endpoint"].format(queue)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)

def leagues (service_platform, 
             api_key,
             league_id):
    """ Get league with given ID, including inactive entries.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#league-v4/GET_getLeagueById

    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        league_id (str): The UUID of the league to get.
    Returns:
        dict: the details of the response to the issued http request. 
    """
    
    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["league"]["leagues"]["endpoint"].format(league_id)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)

def master_leagues (service_platform, 
                    api_key,
                    queue):
    """ Get the master league for given queue.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/game-constants.html
        https://developer.riotgames.com/api-methods/#league-v4/GET_getMasterLeague

    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        queue (str): The queue for which to get the master league.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["masterleagues"]["by-queue"]["endpoint"].format(queue)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)

def positional_rank_queues (service_platform, 
                            api_key):
    """ Get the queues that have positional ranks enabled.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#league-v4/GET_getQueuesWithPositionRanks

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
    path = endpoints.v4["positional-rank-queues"]["endpoint"]

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)

def positions_by_summoner (service_platform, 
                           api_key,
                           encrypted_summoner_id):
    """ Get league positions in all queues for a given summoner ID.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#league-v4/GET_getAllLeaguePositionsForSummoner

    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        encrypted_summoner_id (str): The id of the summoner for which to get the league positions in all queues.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["positions"]["by-summoner"]["endpoint"].format(encrypted_summoner_id)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)
