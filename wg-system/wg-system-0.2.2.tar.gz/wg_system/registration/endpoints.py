from starlette.requests import Request as StarletteRequest
from starlette.responses import PlainTextResponse, RedirectResponse
from .. utils import is_recaptcha_passed

async def register_v0(request: StarletteRequest) -> PlainTextResponse:
    # Use is_recaptcha_passed
    pass

async def confirm_v0(request: StarletteRequest, confirmation_code: str) -> RedirectResponse:
    pass
