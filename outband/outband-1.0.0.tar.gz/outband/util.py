import pathlib

import requests

_SYSTEM_CA_BUNDLES = [
	pathlib.Path("/etc/ssl/certs/ca-certificates.crt"),
]

_SESSION = requests.Session()
for bundle in _SYSTEM_CA_BUNDLES:
	if bundle.exists():
		_SESSION.verify = str(bundle)
		break

def get_session() -> requests.Session:
	return _SESSION
