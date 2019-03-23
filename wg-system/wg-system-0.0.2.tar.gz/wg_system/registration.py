from os import getenv
from email.mime.text import MIMEText
from aiosmtplib import SMTP
from starlette.applications import Starlette
from starlette.requests import Request as StarletteRequest
from starlette.responses import PlainTextResponse, RedirectResponse

REGISTRATION = Starlette()

# Base URL of confirmation endpoint
CONFIRM_BASE_URL = getenv('CONFIRM_BASE_URL', 'https://wmgames.ee/confirm')
# Page that greets new participant, universal for everybody and without personal data
WELCOME_PAGE_URL = getenv('WELCOME_PAGE_URL', 'https://wmgames.ee/welcome')
NOT_FOUND_PAGE_URL = getenv('NOT_FOUND_PAGE_URL', 'https://wmgames.ee/404')

# SMTP related configuration
SMTP_HOST = getenv('SMTP_HOST', '172.17.0.1')
SMTP_PORT = int(getenv('SMTP_PORT', '25'))
SMTP_FROM = getenv('SMTP_FROM', 'Worldman Games <info@wmgames.ee>')

@REGISTRATION.route('/v0/register', methods=['POST'])
async def register_endpoint(request: StarletteRequest) -> PlainTextResponse:
    form = await request.form()
    
    # CHECK RECAPTCHA FIELD

    # CHECK OTHER FORM FIELDS FOR PROBLEMS
    email = form['email']
    name = form['name']
    surname = form['surname']

    # CHECK IF EMAIL EXISTS IN DATABASE

    # GENERATE CONFIRMATION CODE
    confirmation_code = 'generated_random_64_symbols'

    # ADD NEW PARTICIPANT TO DATABASE

    # SEND EMAIL TO NEW PARTICIPANT
    smtp = SMTP(hostname=SMTP_HOST, port=SMTP_PORT)
    message = MIMEText(f"""Your email ({email}) was just used in registration form at Worldman Games (https://wmgames.ee/).
Please confirm it to get Your start number by clicking the link below:

{CONFIRM_BASE_URL}/{confirmation_code}

If You did not registered - ignore this message.""")

    message['From'] = SMTP_FROM
    message['To'] = f'{name} {surname} <{email}>'
    message['Subject'] = 'Registration Confirmation'

    try:
        await smtp.connect()
        await smtp.send_message(message)
    except:
        # LOG EXCEPTION HERE (?)
        return PlainTextResponse('Mail Server Problem!')

    return PlainTextResponse('Check Your Email!')

@REGISTRATION.route('/v0/confirm/{confirmation_code}', methods=['GET'])
async def confirm_endpoint(request: StarletteRequest, confirmation_code: str) -> RedirectResponse:
    if not confirmation_code:
        return RedirectResponse(NOT_FOUND_PAGE_URL)

    # CHECK IF CODE IS VALID

    # MAKE CHANGES IN DATABASE FOR USER WITH THIS CODE

    # SEND EMAIL WITH START POSITION AND INFORMATION ABOUT EVENT

    return RedirectResponse(WELCOME_PAGE_URL)
