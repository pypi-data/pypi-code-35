import requests
from collections import namedtuple

def get_version(
    base_url, 
    auth_token,
    timeout=5,
    verify_tls=False
):
    """Get version information from UCP
    
    base_url (string):
        Base URL to ucp server
    auth_token (string):
        Auth token
    timeout(int):
        Timeout in seconds

    Returns:
        Version information
    """

    headers = {
        "Authorization": "Bearer " + auth_token,
    }
    
    response = requests.get(
        base_url + '/version',
        headers=headers,
        timeout=timeout,
        verify=verify_tls
    )
    response.raise_for_status()
    return response.content
