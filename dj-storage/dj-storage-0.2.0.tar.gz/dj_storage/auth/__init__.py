import requests

session_providers = {}

try:
	from dj_storage.auth import gcp
except ImportError:
	pass
else:
	session_providers['storage.googleapis.com'] = gcp.get_session


def get_session(hostname):
	try:
		return session_providers[hostname](hostname)
	except KeyError:
		return requests.Session()
