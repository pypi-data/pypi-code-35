from urllib.parse import urlencode
from requests_async import post

async def is_recaptcha_passed(recaptcha_response_field: str, recaptcha_secret_key: str) -> bool:
    """Checks if ReCAPTCHA v2 response is from human via Google ReCAPTCHA API."""
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Worldman Games System'}

    params = urlencode({
        'secret': recaptcha_secret_key,
        'response': recaptcha_response_field
    }).encode('utf-8')

    # Getting response from Google ReCAPTCHA API
    response = await post('https://www.google.com/recaptcha/api/siteverify',
                          params=params, headers=headers, timeout=5)

    # Checking if user passed ReCAPTCHA check
    if not response.json()['success']:
        return False

    return True

