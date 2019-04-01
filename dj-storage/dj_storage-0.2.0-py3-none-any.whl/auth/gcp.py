import google.auth
from google.auth.transport.requests import AuthorizedSession


def get_session(hostname):
	credentials, project = google.auth.default(scopes = [
		'https://www.googleapis.com/auth/devstorage.read_only',
		'https://www.googleapis.com/auth/devstorage.read_write',
	])
	return AuthorizedSession(credentials)
