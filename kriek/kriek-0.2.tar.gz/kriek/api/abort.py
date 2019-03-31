from .exceptions import AbortException
from .response import Response
from .constants import HTTP_CODE_MEANING

def abort(code):
    raise AbortException(
        Response({"message": HTTP_CODE_MEANING[code]}, status_code=code)
    )
