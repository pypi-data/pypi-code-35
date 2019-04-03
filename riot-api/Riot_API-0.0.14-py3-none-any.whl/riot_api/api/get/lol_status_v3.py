from . import endpoints
from ...api import _request_executor

def shard_data (service_platform, 
                api_key):
    """ Get League of Legends status for the given shard.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#lol-status-v3/GET_getShardData

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
    path = endpoints.v3["status"]["shard-data"]["endpoint"]
    
    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)