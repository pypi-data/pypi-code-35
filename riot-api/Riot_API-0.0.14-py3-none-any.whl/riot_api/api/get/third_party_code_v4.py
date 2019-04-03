from . import endpoints
from ...api import _request_executor

def third_party_code_by_summoner (service_platform, 
                                  api_key,
                                  encrypted_summoner_id):
    """ Get third party code for a given summoner ID.

    References:
        https://developer.riotgames.com/regional-endpoints.html
        https://developer.riotgames.com/api-methods/#third-party-code-v4/GET_getThirdPartyCodeBySummonerId
        
    Arguments:
        service_platform (str): The service platform that the request should be issued to.
        api_key (str): The client's api key.
        encrypted_summoner_id (str): The id of the summoner whose third party code to get.
    Returns:
        dict: the details of the response to the issued http request. 
    """

    header_parameters = {
        "X-Riot-Token": api_key
    }

    url = endpoints.v4["host"]["endpoint"].format(service_platform)
    path = endpoints.v4["platform"]["third-party-code"]["by-summoner"]["endpoint"].format(encrypted_summoner_id)

    return _request_executor.get("".join([url, path]),
                                 header_parameters=header_parameters)
