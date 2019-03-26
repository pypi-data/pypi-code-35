# default co2logserver configuration
import os
import re
import math
import logging
from co2logserver.utils import *

# User Configuration

__doc__ = """
This module contains the default configuration values.
"""

CO2LOGSERVER_NAME = "co2logserver"
"""
the name of this server
"""

CO2LOGSERVER_DB = "co2.sqlite"
"""
the database file to use
"""

CO2LOGSERVER_LOGLEVEL = logging.WARNING
"""
loglevel for the application
"""

CO2LOGSERVER_SENSEMAPI_LOGLEVEL = logging.WARNING
"""
loglevel for the :mod:`sensemapi` backend
"""

CO2LOGSERVER_CHECKSUM_SALTS = []
"""
The possible salts to check the salted payload checksums against. By default,
no checksums are configured. If no salts are configured, the columns
:any:`CO2LOGSERVER_MATCHED_CHECKSUMS_COL` and
:any:`CO2LOGSERVER_FAILED_CHECKSUMS_COL` will both be empty.
"""

CO2LOGSERVER_UPLOAD_REQUIRES_AUTH = False
"""
Whether uploading requires a salt authentication. Defaults to ``False``.
"""

CO2LOGSERVER_DOWNLOAD_REQUIRES_AUTH = False
"""
Whether downloading requires a salt authentication. Defaults to ``False``.
"""

CO2LOGSERVER_UPLOAD_HELP = True
"""
Whether to show upload help. Defaults to ``True``.
"""


def CO2LOGSERVER_AUTH_CHECKER(x):
    """
    If authentication is required on a route, this function is called with a
    dictionary of checksum algorithm names mapped to matching salts as created
    in :any:`co2logserver.authentication.authentication` and returns a boolean
    value indicating whether authentication should be granted to this request.
    By default, at least one checksum should be given and all handed checksums
    should match.
    """
    return len(x) and all(x.values())


CO2LOGSERVER_DATA_TABLE_NAME = "data"
"""
This is the name for the data table
"""

CO2LOGSERVER_MATCHED_CHECKSUMS_COL = "matched_checksums"
"""
This is the header field name for the matched checksum algorithm names
"""

CO2LOGSERVER_FAILED_CHECKSUMS_COL = "failed_checksums"
"""
This is the header field name for the failed checksum algorithm names
"""

CO2LOGSERVER_UPLOAD_TIME_COL = "time_upload_utc"
"""
This is the header field name for the upload time
"""

CO2LOGSERVER_TIME_COLS = ["time"]
"""
These columns are converted with :any:`CO2LOGSERVER_TIME_CONVERTER`.
"""


def CO2LOGSERVER_TIME_CONVERTER(val, col):
    """
    Columns in :any:`CO2LOGSERVER_TIME_COLS` are converted with this function.
    The function is given the following arguments:

    val
        the column value
    col
        the column name

    The function returns a :class:`datetime.datetime` object. By default, all
    :any:`CO2LOGSERVER_TIME_COLS` are converted with
    :func:`utc_datetime_from_unix_timestamp`, which converts UNIX-timestamps
    (seconds since 1970-01-01) in UTC.
    """
    return utc_datetime_from_unix_timestamp(val)


CO2LOGSERVER_MAX_LIMIT_OF_ROWS = 1000
"""
This is the maximum number of rows returned from the `/download` method.
"""


def CO2LOGSERVER_ACCEPT_NEW_COLUMN(col):
    """
    This function is called with the name of a received nonexistant column name
    and should return a boolean value indicating whether this column should be
    created.  By default, all new columns are accepted.
    """
    return True


CO2LOGSERVER_ALLOW_EMPTY_ROWS = False
"""
Whether empty rows, i.e. rows that would only contain automatic data like
:any:`CO2LOGSERVER_MATCHED_CHECKSUMS_COL` and
:any:`CO2LOGSERVER_UPLOAD_TIME_COL` should be accepted. Defaults to ``False``.
"""

CO2LOGSERVER_OSEM_UPLOAD = False
"""
Set this to True to upload received data to the `OpenSenseMap
<https://opensensemap.org>`_.
"""

CO2LOGSERVER_OSEM_API = os.environ.get("SENSEMAP_API")
"""
Url of the OpenSenseMap API. By default, the API url is taken
from the environment variable ``SENSEMAP_API``. If unset, the default
:any:`sensemapi.account.SenseMapAccount.api` is used.
"""

CO2LOGSERVER_OSEM_USERNAME = os.environ.get("SENSEMAP_USERNAME")
"""
Login username for the OpenSenseMap. By default, the username is taken
from the environment variable ``SENSEMAP_USERNAME``. Either
:any:`CO2LOGSERVER_OSEM_USERNAME` or :any:`CO2LOGSERVER_OSEM_EMAIL` need to be
set.
"""

CO2LOGSERVER_OSEM_EMAIL = os.environ.get("SENSEMAP_EMAIL")
"""
Login email for the OpenSenseMap. By default, the email is taken
from the environment variable ``SENSEMAP_EMAIL``. Either
:any:`CO2LOGSERVER_OSEM_USERNAME` or :any:`CO2LOGSERVER_OSEM_EMAIL` need to be
set.
"""

CO2LOGSERVER_OSEM_PASSWORD = os.environ.get("SENSEMAP_PASSWORD")
"""
Login password for the OpenSenseMap. By default, the password is taken
from the environment variable ``SENSEMAP_PASSWORD``.
"""

CO2LOGSERVER_OSEM_AUTH_CACHE = True
"""
Whether the OpenSenseMap authentication should be cached. Caching is highly
recommended as it speeds up the upload because signing in is then only
performed when necessary and on every upload. By default (``True``),
authentication caching is enabled. If enabled, the cache is located under
``$XDG_CACHE_HOME/co2logserver`` (which should default to
``$HOME/.cache/co2logserver``) in a file having the :any:`CO2LOGSERVER_NAME` in
its name.
"""

CO2LOGSERVER_OSEM_REQUEST_CACHE = True
"""
Whether specific OpenSenseMap requests should be cached (i.e. whether
:mod:`sensemapi.client.SenseMapClient.request_cache` should be used). Caching
is highly recommended as it speeds up things. By default (``True``),
request caching is enabled. If enabled, the request cache is located under
``$XDG_CACHE_HOME/co2logserver`` (which should default to
``$HOME/.cache/co2logserver``) in a directory structure having the
:any:`CO2LOGSERVER_NAME` in its top-level name.
"""

CO2LOGSERVER_OSEM_CACHE_PASSWORD = False
"""
The value for :any:`sensemapi.account.SenseMapAccount.cache_password`. By
default, the password is not cached.
"""


def CO2LOGSERVER_OSEM_COL_REDIRECT(col):
    """
    This function is called with the column name as argument to determine
    whether this column should be considered for OpenSenseMap upload. By
    default, this function returns ``True`` for any column, so any column will
    be redirected to the OpenSenseMap.
    """
    return True


def CO2LOGSERVER_OSEM_BOX_REDIRECT(box):
    """
    This function is called with the value of :any:`CO2LOGSERVER_OSEM_BOX_COL`
    as argument to determine whether this senseBox should be considered for
    OpenSenseMap upload. By default, this function returns ``True`` for any
    box, so any box will be redirected to the OpenSenseMap.
    """
    return True


def CO2LOGSERVER_OSEM_VALUE_FILTER(box, col, val):
    """
    This function is called with the following arguments to return the value
    uploaded to the OpenSenseMap:

    box
        the value of :any:`CO2LOGSERVER_OSEM_BOX_COL`
    col
        the column name
    val
        the value of the column

    By default, the value is rounded to 3 decimal places.
    """
    return round(val, 3)


CO2LOGSERVER_OSEM_BOX_COL = "box"
"""
This column is used as a senseBox identifier Data rows with the same value in
this column are assigned to the same senseBox. If a data row does not contain
this column, a default :any:`CO2LOGSERVER_OSEM_BOX_COL` of
:any:`CO2LOGSERVER_OSEM_BOX_COL_DEFAULT`.
"""

CO2LOGSERVER_OSEM_BOX_COL_DEFAULT = "generic"
"""
Default value for datasets containing no :any:`CO2LOGSERVER_OSEM_BOX_COL`.
"""

CO2LOGSERVER_OSEM_LAT_COL = "lat"
"""
This column is used for the latitude of the senseBox.
"""

CO2LOGSERVER_OSEM_LON_COL = "lon"
"""
This column is used for the longitude of the senseBox.
"""

CO2LOGSERVER_OSEM_HEIGHT_COL = "height"
"""
This column is used for the height of the senseBox.
"""


def CO2LOGSERVER_DEFAULT_LAT(box):
    """
    This function is called with the following arguments to determine the
    latitude of a senseBox if the data does not contain the information:

    box:
        the value of the :any:`CO2LOGSERVER_OSEM_BOX_COL`

    By default, ``None`` is returned which means that the latitude could not be
    determined.
    """
    return None


def CO2LOGSERVER_DEFAULT_LON(box):
    """
    This function is called with the following arguments to determine the
    longitude of a senseBox if the data does not contain the information:

    box:
        the value of the :any:`CO2LOGSERVER_OSEM_BOX_COL`

    By default, ``None`` is returned which means that the longitude could not
    be determined.
    """
    return None


CO2LOGSERVER_OSEM_TIME_COL = next(iter(CO2LOGSERVER_TIME_COLS), "time")
"""
This column is used for the measurement time. By default, the first value in
:any:`CO2LOGSERVER_TIME_COLS` is used.
"""

CO2LOGSERVER_OSEM_MIN_SECONDS_BETWEEN_UPLOADS = 0
"""
The minimum amount of seconds to leave between uploads of sensor measurements,
i.e. if the :any:`sensemapi.sensor.senseBoxSensor.last_time` is less than
:any:`CO2LOGSERVER_OSEM_MIN_SECONDS_BETWEEN_UPLOADS` seconds in the past, the
upload is skipped.
"""


def CO2LOGSERVER_OSEM_EXPOSURE_DETERMINER(box):
    """
    This function is called to determine the
    :any:`sensemapi.senseBox.senseBox.exposure`. It is called with the
    following arguments:

    box:
        the value of the :any:`CO2LOGSERVER_OSEM_BOX_COL`

    By default, the first value out of ``indoor``, ``outdoor`` and ``mobile``
    which is contained in the value of :any:`CO2LOGSERVER_OSEM_BOX_COL` is
    used, defaulting to ``mobile``.
    """
    return next(
        (x for x in ("indoor", "outdoor", "mobile") if box in x), "mobile"
    )


CO2LOGSERVER_OSEM_DEFAULT_WEBLINK = (
    "https://gitlab.com/tue-umphy/co2mofetten/python3-co2logserver"
)
"""
This is the default ``weblink`` value for any senseBox.
"""

CO2LOGSERVER_OSEM_DEFAULT_DESCRIPTION = (
    "This senseBox was automatically created by an instance of co2logserver, "
    "a simple Python HTTP data logging server, named '{servername}'."
)
"""
This is the default :any:`sensemapi.senseBox.senseBox.description`. This string
is formatted with the arguments:

servername
    the :any:`CO2LOGSERVER_NAME`
"""

CO2LOGSERVER_OSEM_COL_REGEX = re.compile(
    r"^"
    r"(?P<type>[^_]+)"
    r"_"
    r"(?P<quantity>[^_]+)"
    r"_"
    r"(?P<unit>.*)"
    r"$"
)
"""
This regular expression created with :func:`re.compile` is used to extract
information from the column title Columns matching this regular expression are
used to upload data to the OpenSenseMap. This regular expression MUST have the
named captured groups "type" (the sensor type), "unit" (the measurement unit)
and "quantity" (the measurement quantity). By default, columns are assumed to
be named like this: ``SENSORTYPE_QUANTITY_UNIT``.
"""

CO2LOGSERVER_OSEM_BOX_NAME_GENERATOR = "{servername} senseBox {box}".format
"""
This function is called with the following keyword arguments to return
the :any:`sensemapi.senseBox.senseBox.name`:

servername
    :any:`CO2LOGSERVER_NAME`
box
    the value of the column :any:`CO2LOGSERVER_OSEM_BOX_COL`

By default, it just joins the ``servername`` and the ``box`` with the word
``senseBox``.
"""

CO2LOGSERVER_OSEM_SENSOR_TITLE_GENERATOR = "{quantity}".format
"""
This function is called to return the :any:`sensemapi.senseBox.senseBox.name`.
It is called with keyword arguments corresponding to the :meth:`groupdict` of
:any:`CO2LOGSERVER_OSEM_COL_REGEX` as well as:

column
    the column name as received

By default, it just joins the ``type``, ``quantity`` and ``unit``.
"""


def CO2LOGSERVER_OSEM_UNIT_COVERTER(x):
    """
    This function is called with the :any:`CO2LOGSERVER_OSEM_COL_REGEX`'s
    ``unit`` and returns the string used for the
    :any:`sensemapi.sensor.senseBoxSensor.unit`.
    """
    return {"c": "°C", "percent": "%", "perc": "%"}.get(x.lower(), x)


CO2LOGSERVER_OSEM_ICONS = [
    "osem-moisture",
    "osem-temperature-celsius",
    "osem-temperature-fahrenheit",
    "osem-thermometer",
    "osem-windspeed",
    "osem-sprinkles",
    "osem-brightness",
    "osem-barometer",
    "osem-humidity",
    "osem-not-available",
    "osem-gauge",
    "osem-umbrella",
    "osem-clock",
    "osem-shock",
    "osem-fire",
    "osem-volume-up",
    "osem-cloud",
    "osem-dashboard",
    "osem-particulate-matter",
    "osem-signal",
    "osem-microphone",
    "osem-wifi",
    "osem-battery",
    "osem-radioactive",
]
"""
The available OpenSenseMap icons
"""


def CO2LOGSERVER_OSEM_ICON_DETERMINER(d):
    """
    This function is called to return the proper :any:`CO2LOGSERVER_OSEM_ICONS`
    for a sensor.  It is called with a single dict arguments corresponding to
    the :meth:`groupdict` of :any:`CO2LOGSERVER_OSEM_COL_REGEX` also
    containing:

    column
        the column name as received

    By default, it uses the first icon whose name contains the ``quantity``,
    defaulting to ``osem-not-available``.
    """
    return next(
        filter(lambda x: d["quantity"] in x, CO2LOGSERVER_OSEM_ICONS),
        "osem-not-available",
    )


CO2LOGSERVER_OSEM_MAX_POSITION_CHANGE = float("inf")
"""
The maximum allowed change in lat/lon-degrees. Detected changes higher than
this will prevent the upload of changed GPS coordinates as this is likely a
measurement error. By default, no restrictions are made.
"""

# static configuration

# You should NOT edit the following!

CO2LOGSERVER_SALTED_CHECKSUM_HEADER_REGEX = re.compile(
    r"Content-(?P<algorithm>\w+)-Salted", re.IGNORECASE
)
"""
This regular expression is :meth:`re.fullmatch` ed to determine header fields
containing salted payload hashes. It should have the following named captured
groups:

algorithmn
    the hashing algorithm name
"""
