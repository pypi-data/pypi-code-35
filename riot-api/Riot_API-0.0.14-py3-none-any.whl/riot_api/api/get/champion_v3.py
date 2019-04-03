from . import endpoints
from ...api import _request_executor

def champion_rotations (service_platform, 
                        api_key):
    """ Returns champion rotations, including free-to-play and low-level free-to-play rotations .

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#champion-v3/GET_getChampionInfo

    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v3["host"]["endpoint"].format(service_platform)
    path = endpoints.v3["platform"]["champion-rotations"]["endpoint"]

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)