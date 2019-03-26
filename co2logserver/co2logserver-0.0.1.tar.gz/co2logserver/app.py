# system modules
import os
import sys
import logging

# external modules
from flask import Flask

app = application = Flask(__name__)

app.config.from_object("co2logserver.config_default")
if os.environ.get("CO2LOGSERVER_CONFIG"):
    app.config.from_envvar("CO2LOGSERVER_CONFIG")

# configuration checks
if app.config["CO2LOGSERVER_OSEM_UPLOAD"]:
    for x in ("type", "quantity", "unit"):
        assert x in app.config["CO2LOGSERVER_OSEM_COL_REGEX"].groupindex, (
            "The CO2LOGSERVER_OSEM_COL_REGEX does not have a "
            "captured group named '{}'"
        ).format(x)

app.logger.setLevel(app.config["CO2LOGSERVER_LOGLEVEL"])
