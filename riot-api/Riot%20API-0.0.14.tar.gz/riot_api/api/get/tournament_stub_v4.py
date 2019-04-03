from . import endpoints
from ...api import _request_executor

def lobby_events_by_code (service_platform,
                          api_key,
                          tournament_code):
    """ Gets a mock list of lobby events by tournament code.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#tournament-stub-v4/GET_getLobbyEventsByCode
        
    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        tournament_code (str): The code of the tournament whose mock list of lobby events to get.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["tournament-stub"]["lobby-events"]["by-code"]["endpoint"].format(tournament_code)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)