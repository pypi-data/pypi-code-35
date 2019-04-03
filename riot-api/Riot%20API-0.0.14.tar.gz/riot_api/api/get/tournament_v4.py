from . import endpoints
from ...api import _request_executor

def codes (service_platform, 
           api_key,
           tournament_code):
    """ Returns the tournament code DTO associated with a tournament code string.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#tournament-v4/GET_getTournamentCode
        
    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        tournament_code (str): The code of the tournament whose tournament code DTO to get.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["tournament"]["codes"]["endpoint"].format(tournament_code)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)

def lobby_events_by_code (service_platform,
                          api_key,
                          tournament_code):
    """ Gets a list of lobby events by tournament code.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#tournament-v4/GET_getLobbyEventsByCode
        
    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        tournament_code (str): The code of the tournament whose list of lobby events to get.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["tournament"]["lobby-events"]["by-code"]["endpoint"].format(tournament_code)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)