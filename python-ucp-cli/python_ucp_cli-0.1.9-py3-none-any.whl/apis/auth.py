import requests
from collections import namedtuple

LoginResponse = namedtuple('LoginResponse', [
    'auth_token'
])


# Perform POST /auth/login to get auth_token
def login(
    base_url,
    username,
    password,
    timeout=5,
    verify_tls=False
):
    """Login and get auth_token
    
    base_url (string):
        Base URL to ucp server
    username (string):
        Login username
    password (string):
        Login password
    timeout(int):
        Timeout in seconds
    Returns:
        Auth token (string)
    """
    payload = {
        "username": username,
        "password": password,
    }

    try:

        response = requests.post(
            base_url + '/auth/login',
            json=payload,
            timeout=timeout,
            verify=verify_tls
        )
        response.raise_for_status()
        data = response.json()
        login_response = LoginResponse(
            auth_token=data['auth_token'] 
        )
        return login_response

    except (requests.ConnectionError, requests.Timeout) as e:
        raise errors.Unavailable() from e

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Invalid username and/or password.")



# Perform GET /api/clientbundle to get user bundle zip file.
def clientbundle(
    base_url, 
    auth_token,
    timeout=5,
    verify_tls=False
):
    """Download clientbundle

    base_url (string):
        Base URL to ucp server
    auth_token (string):
        Auth token
    timeout(int):
        Timeout in seconds

    Returns:
        User client bundle (zip file)
    """

    headers = {
        "Authorization": "Bearer " + auth_token,
    }
    
    response = requests.get(
        base_url + '/api/clientbundle',
        headers=headers,
        timeout=timeout,
        verify=verify_tls
    )
    response.raise_for_status()
    return response.content
