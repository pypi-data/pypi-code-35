#!/usr/bin/env python3
import argparse
import logging
import os

import outband.connectors.auto

_LOGGER = logging.getLogger("outband")
_PASSWORD_ENVIRONMENT_VARIABLE = "OUTBAND_PASSWORD"

def parse_arguments() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Connect to an out-of-band management KVM console from the command line.")
	parser.add_argument("host", help="The host to connect to.")
	parser.add_argument("--username", help="The username to use for logging in. If none is provided, the default for the appropriate type will be used.")
	parser.add_argument("--password", help="The password to use for logging in (can also be provided via the %s environment variable). If none is provided, the default for the appropriate type will be used." % _PASSWORD_ENVIRONMENT_VARIABLE)
	parser.add_argument("--type", type=lambda type_name: outband.connectors.auto.KVMType[type_name.upper()], choices=outband.connectors.auto.KVMType, default=outband.connectors.auto.KVMType.AUTO)
	parser.add_argument("--preserve-temp-files", action="store_true", help="Keep temporary files created when establishing the connection.")
	arguments = parser.parse_args()
	if arguments.password is None and _PASSWORD_ENVIRONMENT_VARIABLE in os.environ:
		arguments.password = os.environ[_PASSWORD_ENVIRONMENT_VARIABLE]
	return arguments

def main() -> None:
	logging.basicConfig()
	_LOGGER.setLevel(logging.INFO)

	arguments = parse_arguments()
	arguments.type.value.connect(arguments.host, username=arguments.username, password=arguments.password, preserve_temp_files=arguments.preserve_temp_files)

if __name__ == "__main__":
	main()
