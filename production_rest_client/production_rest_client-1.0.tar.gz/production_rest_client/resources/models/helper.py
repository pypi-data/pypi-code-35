# coding=utf-8


class RestError(Exception):
    def __init__(self, value):
        super(RestError, self).__init__()
        self.value = value

    def __str__(self):
        return repr(self.value)

def rest_get_call(full_url, session, timeout):
    """**REST Get Call**
    Makes a REST call using GET

    :param full_url: url of the rest call
    :type full_url: str
    :param session: requests session
    :type session: Session
    :param timeout: timeout in seconds of the call
    :type timeout: int
    :returns: returns results result
    :rtype: requests.Response

    """
    try:
        result = session.get(full_url, timeout=timeout)
        if result.status_code == 200:
            return result
        raise RestError(result.text)
    except Exception:
        raise

def rest_post_json_call(full_url, session, key_value_set, timeout):
    """**REST Post Map Call**
    Makes a REST call using POST with a JSON Key value set

    :param full_url: url of the rest call
    :type full_url: str
    :param session: requests session
    :type session: Session
    :param key_value_set: KeyBuilder.get_json
    :type key_value_set: json
    :param timeout: timeout in seconds of the call
    :type timeout: int
    :param key_value_set:
    :returns: returns results result
    :rtype: requests.Response

    """
    header = {'content-type': 'application/json'}
    try:
        result = session.post(full_url, data=key_value_set, headers=header, timeout=timeout)
        if result.status_code == 200:
            return result
        raise RestError(result.text)
    except Exception:
        raise


def rest_delete_call(full_url, session, timeout):
    """**REST Get Call**
    Makes a REST call using GET

    :param full_url: url of the rest call
    :type full_url: str
    :param session: requests session
    :type session: Session
    :param timeout: timeout in seconds of the call
    :type timeout: int
    :returns: returns results result
    :rtype: requests.Response

    """
    try:
        result = session.delete(full_url, timeout=timeout)
        if result.status_code == 200:
            return result
        raise RestError(result.text)
    except Exception:
        raise
