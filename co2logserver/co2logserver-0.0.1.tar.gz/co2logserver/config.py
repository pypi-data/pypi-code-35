# system modules
import os
import itertools
import hashlib
import re
import logging

# internal modules
from co2logserver.database import DataBaseHandler
from co2logserver import app

# external modules
from flask import g

__doc__ = """
This module contains functions to extract or create more sophisticated objects
from the configuration.
"""


def config(key):
    """
    Shortcut function to access configuration variables prefixed with
    ``CO2LOGSERVER_``.

    Args:
        key (str): the configuration key without the ``CO2LOGSERVER_`` prefix

    Returns:
        object : the configuration value
    """
    return app.config["CO2LOGSERVER_{}".format(key)]


def database():
    """
    Returns the global :class:`co2logserver.database.DataBaseHandler` for this
    request, set it up if necessary.

    Returns:
        co2logserver.database.DataBaseHandler : the database handler
    """
    try:
        db = g._database
    except AttributeError:
        dbfile = config("DB")
        db = g._database = DataBaseHandler(dbfile)
    return db


def osem_account():
    """
    Returns the global :class:`sensemapi.account.SenseMapAccount` for this
    request, set it up if necessary.

    Returns:
        sensemapi.account.SenseMapAccount : the OpenSenseMap account
    """
    try:
        osem_account = g._osem_account
    except AttributeError:
        try:
            import sensemapi
        except ImportError as e:  # pragma: no cover
            raise type(e)(
                "For OpenSenseMap integration "
                "the 'sensemapi' package is needed."
            )
        if config("OSEM_AUTH_CACHE"):  # pragma: no cover
            account_auth_cache = sensemapi.cache.SQLiteAuthentiCache(
                directory=sensemapi.xdg.XDGPackageDirectory(
                    name="XDG_CACHE_HOME", packagename="co2logserver"
                ).path,
                name="{}-osem-auth".format(
                    re.sub("[^a-zA-Z0-9_-]", "-", config("NAME"))
                ).lower(),
            )
        else:
            account_auth_cache = None
        if config("OSEM_REQUEST_CACHE"):  # pragma: no cover
            from cachecontrol.caches.file_cache import FileCache

            filecachedir = os.path.join(
                sensemapi.xdg.XDGPackageDirectory(
                    name="XDG_CACHE_HOME", packagename="co2logserver"
                ).path,
                "{}-osem-requests".format(
                    re.sub("[^a-zA-Z0-9_-]", "-", config("NAME"))
                ).lower(),
            )
            account_request_cache = FileCache(filecachedir)
        else:
            account_request_cache = None
        # redirect logging from sensemapi and cachecontrol
        for name, logger in logging.getLogger().manager.loggerDict.items():
            if any(mod in name for mod in ("sensemapi", "cachecontrol")):
                if hasattr(logger, "setLevel"):
                    logger.setLevel(config("SENSEMAPI_LOGLEVEL"))
                    if hasattr(logger, "addHandler"):
                        for handler in app.logger.handlers:
                            if handler not in logger.handlers:
                                logger.addHandler(handler)
        osem_account = sensemapi.account.SenseMapAccount(
            api=config("OSEM_API"),
            email=config("OSEM_EMAIL"),
            username=config("OSEM_USERNAME"),
            password=config("OSEM_PASSWORD"),
            cache_password=config("OSEM_CACHE_PASSWORD"),
            auth_cache=account_auth_cache,
            request_cache=account_request_cache,
        )
    return osem_account


def hash_algorithm_combination(sortkey=None):
    """
    Generator yielding the next combination of :any:`hashlib`'s
    ``algorithms_guaranteed``.

    Yields:
        sequence of str : combination of algorithmn names
    """
    return itertools.chain.from_iterable(
        itertools.combinations(
            sorted(hashlib.algorithms_guaranteed, key=sortkey), n
        )
        for n in range(1, len(hashlib.algorithms_guaranteed) + 1)
    )


def needed_matching_hash_algorithmns(
    preferred=("md5", "sha1", "sha256", "sha512")
):
    """
    Generator yielding the next valid combination of matching hash algorithm
    names needed for :any:`CO2LOGSERVER_AUTH_CHECKER` to return ``True``.
    Prefers the standard algorithmns ``md5``, ``sha1``, ``sha256`` and
    ``sha512``.

    Args:
        preferred (sequence of str, optional): preferred algorithm names. Need
            to be present in :any:`hashlib`'s ``algorithms_guaranteed``.

    Yields:
        sequence of str : the next valid algorithmn combination
    """
    sortkey = (
        lambda alg: "0{}".format(alg)
        if any(h in alg for h in preferred)
        else alg
    )
    algorithms = hash_algorithm_combination(sortkey=sortkey)
    return map(
        tuple,
        filter(
            config("AUTH_CHECKER"),
            map(lambda x: {k: True for k in x}, algorithms),
        ),
    )
