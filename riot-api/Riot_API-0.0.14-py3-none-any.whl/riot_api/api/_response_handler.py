_DEFAULT_DELAY_FOR_STATUS_CODE_404 = 0
_DEFAULT_DELAY_FOR_STATUS_CODE_500 = 0
_DEFAULT_DELAY_FOR_STATUS_CODE_502 = 0
_DEFAULT_DELAY_FOR_STATUS_CODE_503 = 0
_DEFAULT_DELAY_FOR_STATUS_CODE_504 = 0

def handle (response):

    status_code = response.status_code

    if status_code == 200:

        return {   
            "successful": True,
            "body": response.json()
        }

    elif status_code == 400:

        return {
            "successful": False,
            "error": {
                "status_code": 400,
                "reason": "Bad Request"
            },
            "retry": False
        }

    elif status_code == 401:

        return {
            "successful": False,
            "error": {
                "status_code": 401,
                "reason": "Unauthorized"
            },
            "retry": False
        }

    elif status_code == 403:

        return {
            "successful": False,
            "error": { 
                "status_code": 403,
                "reason": "Forbidden"
            },
            "retry": False
        }

    elif status_code == 404:

        return {
            "successful": False,
            "error": {
                "status_code": 404,
                "reason": "Not Found"
            },
            "retry": True,
            "delay": _DEFAULT_DELAY_FOR_STATUS_CODE_404
        }
 
    elif status_code == 415:

        return {
            "successful": False,
            "error": {
                "status_code": 403,
                "reason": "Unsupported Media Type"
            },
            "retry": False
        }

    elif status_code == 429:

        return {
            "successful": False,
            "error": {
                "status_code": 429,
                "reason": "Rate Limit Exceeded"
            },
            "retry": True,
            "delay": float(response.headers["Retry-After"])
        }

    elif status_code == 500:

        return {
            "successful": False,
            "error": {
                "status_code": 500,
                "reason": "Internal Server Error"
            },
            "retry": True,
            "delay": _DEFAULT_DELAY_FOR_STATUS_CODE_500
        }

    elif status_code == 502:

        return {
            "successful": False,
            "error": {
                "status_code": 502,
                "reason": "Bad Gateway"
            },
            "retry": True,
            "delay": _DEFAULT_DELAY_FOR_STATUS_CODE_502
        }

    elif status_code == 503:

        return {
            "successful": False,
            "error": {
                "status_code": 503,
                "reason": "Service Unavailable"
            },
            "retry": True,
            "delay": _DEFAULT_DELAY_FOR_STATUS_CODE_503
        }

    elif status_code == 504:

        return {
            "successful": False,
            "error": {
                "status_code": 504,
                "reason": "Gateway Timeout"
            },
            "retry": True,
            "delay": _DEFAULT_DELAY_FOR_STATUS_CODE_504
        }

    else:

        return None