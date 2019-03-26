# system modules
import hashlib
import functools

# internal modules
from co2logserver import app
from co2logserver.utils import *
from co2logserver.exceptions import *
from co2logserver.config import config

# external modules
from flask import request


def header_checksum():
    """
    Generator yielding header fields containing valid and available checksums

    Yields:
        sequence: algorithm name and lowercase hex checksum
    """
    for key, value in request.headers.items():
        m = config("SALTED_CHECKSUM_HEADER_REGEX").fullmatch(key)
        if not m:
            continue
        algorithm = m.groupdict().get("algorithm", "").lower()
        app.logger.debug(
            "Header {} looks like a candidate to "
            "contain a salted payload {} hash".format(repr(key), algorithm)
        )
        if algorithm in hashlib.algorithms_guaranteed:
            hashfunc = hashlib.new(algorithm)
            hashlen = hashfunc.digest_size * 2  # 2 hex digits/byte
            if re.fullmatch(
                pattern="[a-f0-9]{{{}}}".format(hashlen),
                string=value,
                flags=re.IGNORECASE,
            ):
                yield (algorithm, value.lower())
            else:
                app.logger.warning(
                    "{} does not look like a valid "
                    "{} hexdigest".format(repr(value), algorithm)
                )
        else:
            app.logger.warning(
                "There is no such hash function {}".format(repr(algorithm))
            )
            continue


def matching_salt(payload, checksum, algorithm):
    """
    Generator yielding the next matching salt in
    :any:`CO2LOGSERVER_CHECKSUM_SALTS` given the payload, the checksum and the
    algorithm. Remember frequently matching salts and save them in a
    configuration variable ``CO2LOGSERVER_SALTS_COUNT``

    Args:
        payload (str or bytes): the payload
        checksum (str): the hex checksum
        algorithm (str): the algorithm name as available in :mod:`hashlib`

    Yields:
        str: the next matching salt
    """
    if not app.config.get("CO2LOGSERVER_SALTS_COUNT"):
        app.config["CO2LOGSERVER_SALTS_COUNT"] = collections.Counter()
    for salt in sorted(
        # sort the salts (actually does not make sense), but...
        config("CHECKSUM_SALTS"),
        # ... sort by the matching frequency, if yet matched
        key=lambda s: config("SALTS_COUNT").get(s, 0),
        # ... use frequently matched salts first
        reverse=True,
    ):
        app.logger.debug("Considering salt '{}'".format(salt))
        calc_checksum = salted_checksum(payload, salt, algorithm)
        app.logger.debug(
            "Salted with '{}', "
            "the received payload has a {} checksum '{}'".format(
                salt, algorithm, calc_checksum
            )
        )
        if checksum == calc_checksum:
            app.logger.debug(
                "{} checksum matches with salt {}!".format(
                    algorithm, repr(salt)
                )
            )
            # count up matching frequency for this salt
            config("SALTS_COUNT")[salt] += 1
            yield salt
        else:
            app.logger.debug(
                "{} Checksum doesn't match with salt {}!".format(
                    algorithm, repr(salt)
                )
            )
            continue


def authentication(required=False):
    """
    Decorator for routes that require the salt authentication being checked.
    Routes decorated with this decorator (this decoration has to be performed
    **before** decoration with :any:`flask.Flask.route`) get handed an argument
    ``matching_salts`` containing a dictionary of hash algorithm names mapped
    to the salt that let the checksum match.

    Args:
        required (bool or str, optional): Whether the authentication is
            required on this route. If authentication fails or is missing and
            ``required`` evaluates to ``False``, an exception is raised. Aside
            from boolean values, it is also possible to specify a configuration
            key string whose corresponding value is then evaluated at runtime
            to determine the value for ``required``.
    """

    def decorator(decorated_function):
        @functools.wraps(decorated_function)
        def wrapper(*args, **kwargs):
            # we can't overwrite the required variable directly because of
            # strangeness happening, thus we create another variable
            match_required = (
                app.config[required] if required in app.config else required
            )
            # determine payload to use
            if request.method in ("GET", "HEAD"):
                app.logger.debug(
                    "This is a {} request, thus we don't use the "
                    "body as payload but the path {}".format(
                        request.method, repr(request.full_path)
                    )
                )
                payload = request.full_path
            else:
                payload = request.get_data()
            app.logger.debug("The payload is: {}".format(payload))
            if not config("CHECKSUM_SALTS"):
                app.logger.debug(
                    "No salts are configured. " "Cannot verify matching_salts."
                )
            # find matching salts for all given checksums
            matching_salts = {
                # find the matching salt for this checksum
                alg: next(matching_salt(payload, cs, alg), None)
                # find all checksums in the header
                for alg, cs in header_checksum()
            }
            app.logger.debug("Matching salts:\n{}".format(matching_salts))
            if matching_salts:
                if all(matching_salts.values()):
                    app.logger.info("All checksum checks succeeded!")
                else:
                    app.logger.warning("Not all checksum checks succeeded!")
            else:
                app.logger.debug("No checksums were given")
                if match_required:
                    raise MissingAuthentication
            if match_required:
                auth_granted = config("AUTH_CHECKER")(matching_salts)
                if auth_granted:
                    app.logger.debug(
                        "CO2LOGSERVER_AUTH_CHECKER says the "
                        "provided checksums are enough"
                    )
                else:
                    app.logger.error(
                        "CO2LOGSERVER_AUTH_CHECKER says the "
                        "provided checksums are not enough to authenticate"
                    )
                    raise InvalidAuthentication
            else:
                app.logger.debug("Checksum matching is not required")
            # call the decorated function and hand the authentication
            kwargs.update(matching_salts=matching_salts)
            retval = decorated_function(*args, **kwargs)
            return retval

        return wrapper

    return decorator
