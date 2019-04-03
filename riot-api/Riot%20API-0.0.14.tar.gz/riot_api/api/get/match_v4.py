from . import endpoints
from ...api import _request_executor

def matches (service_platform, 
             api_key,
             match_id):
    """ Get a match by its match ID.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#match-v4/GET_getMatch
        
    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        match_id (str): The id of the match to get.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["match"]["matches"]["endpoint"].format(match_id)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)

def matchlists_by_account (service_platform,
                           api_key,
                           encrypted_account_id, 
                           champion=None,
                           queue=None,
                           season=None,
                           begin_time=None,
                           end_time=None,
                           begin_index=None,
                           end_index=None):
    """ Get the matchlist for a given account.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#match-v4/GET_getMatchlist

    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        encrypted_account_id (str): The id of the account whose matchlist to get.
        champion (set[int]): Champion idss to include in the matchlist.
        queue (set[int]): The queue ids of matches to be included in the matchlist.
        season (set[int]): The season ids of matches to be included in the matchlist. 
        begin_time (int): The minimum begin time of matches to be included in the matchlist. Specified as epoch milliseconds.
        end_time (int): The maximum end time of matches to be included in the matchlist. Specified as epoch milliseconds.
        begin_index (int): The begin index of matches to be included in the matchlist.
        end_index (int): The end index of matches to be included in the matchlist.
    Returns:
        dict: the details of the response to the issued http request. 
    """
    
    header_parameters = {
        "X-Riot-Token": api_key
    }

    query_parameters = {
        "champion": champion,
        "queue": queue,
        "season": season,
        "beginTime": begin_time,
        "endTime": end_time,
        "beginIndex": begin_index,
        "endIndex": end_index
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["match"]["matchlists"]["by-account"]["endpoint"].format(encrypted_account_id)
    
    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters,
                                 query_parameters=query_parameters)

def timelines_by_match (service_platform, 
                        api_key, 
                        match_id):
    """ Get match timeline by match ID.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#match-v4/GET_getMatchTimeline
        
    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        match_id (str): The id of the match whose timeline to get.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["match"]["timelines"]["by-match"]["endpoint"].format(match_id)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)

def matches_by_tournament_code_ids (service_platform, 
                                    api_key, 
                                    tournament_code):
    """ Get match IDs by tournament code.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#match-v4/GET_getMatchIdsByTournamentCode
        
    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        tournament_code (str): The code of the tournament whose matches to get.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["match"]["matches"]["by-tournament-code"]["endpoint"].format(tournament_code)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)

def matches_by_tournament_code (service_platform, 
                                api_key,
                                match_id,
                                tournament_code):
    """ Get match by match ID and tournament code.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#match-v4/GET_getMatchByTournamentCode
        
    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        match_id (int): The id of the match to get.
        tournament_code (str): The code of the tournament from which to get the match.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["match"]["matches"]["{}"]["by-tournament-code"]["endpoint"].format(tournament_code)
    
    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)