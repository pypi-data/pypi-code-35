import requests

# Util methods used in multiple commands.


def req_get(auth_key, url):
    headers = {}
    if auth_key:
        headers['Authorization'] = 'Bearer {}'.format(auth_key)
    return requests.get(url, headers=headers, stream=True)


def req_post(auth_key, url, data):
    headers = {'Content-Type': 'application/json'}
    if auth_key:
        headers['Authorization'] = 'Bearer {}'.format(auth_key)
    return requests.post(url, data=data, headers=headers)
