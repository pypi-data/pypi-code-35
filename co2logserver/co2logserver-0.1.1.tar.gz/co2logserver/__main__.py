# system modules
import argparse
import logging
import sys
import os

# internal modules
from co2logserver import app


def absolute_path(x):
    if os.path.isabs(x):
        return x
    else:
        return os.path.abspath(x)


parser = argparse.ArgumentParser(description="CO2 log server")
parser.add_argument("-b", "--bind", help="server bind address", default="")
parser.add_argument(
    "-p", "--port", type=int, help="HTTP server port", default=8080
)
parser.add_argument(
    "-f", "--dbfile", type=absolute_path, help="path to SQLite3 database file"
)
parser.add_argument(
    "-c", "--config", type=absolute_path, help="path to configuration file"
)
parser.add_argument(
    "-v", "--verbose", help="verbose logger", action="store_true"
)
parser.add_argument(
    "-d", "--debug", help="debug mode", action="store_true", default=False
)
parser.add_argument(
    "-t", "--threaded", help="", action="store_true", default=False
)
parser.add_argument(
    "-n", "--processes", help="number of processes to use", type=int, default=1
)
args = parser.parse_args()

clilogger = logging.getLogger("cli")

loglevel = logging.DEBUG if args.verbose else logging.INFO

app.config["CO2LOGSERVER_LOGLEVEL"] = loglevel
app.logger.setLevel(loglevel)

if args.config:
    app.config.from_pyfile(args.config)

if args.dbfile:
    app.config.update(CO2LOGSERVER_DB=args.dbfile)

app.run(
    host=args.bind,
    port=args.port,
    debug=args.debug,
    threaded=args.threaded,
    processes=args.processes,
)
