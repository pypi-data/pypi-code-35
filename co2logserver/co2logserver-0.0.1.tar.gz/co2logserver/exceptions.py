# system modules
import hashlib

# internal modules
from co2logserver import app

# external modules
from werkzeug.exceptions import *


class AuthenticationError(Forbidden):
    description = "Authentication Error"


class MissingAuthentication(AuthenticationError):
    description = (
        "No salted payload checksum given. "
        "Specify one or more header fields that match {} and "
        "contain a hexadecimal digest of the payload with the proper "
        "salt appended calculated with the specific algorithm. "
        "Available algorithmns are {}."
    ).format(
        repr(app.config["CO2LOGSERVER_SALTED_CHECKSUM_HEADER_REGEX"].pattern),
        ", ".join(sorted(hashlib.algorithms_guaranteed)),
    )


class InvalidAuthentication(AuthenticationError):
    description = (
        "Invalid or insufficient checksum authentication. "
        "Specify one or more header fields that match {} and "
        "contain a hexadecimal digest of the payload with the proper "
        "salt appended calculated with the specific algorithm. "
        "Available algorithmns are {}."
    ).format(
        repr(app.config["CO2LOGSERVER_SALTED_CHECKSUM_HEADER_REGEX"].pattern),
        ", ".join(sorted(hashlib.algorithms_guaranteed)),
    )
