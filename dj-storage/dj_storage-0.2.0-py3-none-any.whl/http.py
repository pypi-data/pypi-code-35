from mimetypes import guess_type
from urllib.parse import urljoin, urlsplit

from dj_storage.auth import get_session

from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import Storage


class HTTPStorage(Storage):
	def __init__(self, base_url = None):
		self.base_url = base_url or settings.MEDIA_URL
		self._session = get_session(urlsplit(self.base_url).hostname)

	def _url(self, name):
		url = urljoin(self.base_url, name.lstrip("/"))
		assert (url.startswith(self.base_url))
		return url

	def url(self, name):
		return self._url(name)

	def delete(self, name):
		resp = self._session.delete(self._url(name))
		resp.raise_for_status()

	def exists(self, name):
		resp = self._session.head(self._url(name))
		if resp.status_code >= 200 and resp.status_code < 300:
			return True
		if resp.status_code == 404:
			return False
		resp.raise_for_status()

	def _save(self, name, content):
		headers = {}

		content_type = guess_type(name)
		if content_type[0]:
			headers['content-type'] = content_type[0]
		if content_type[1]:
			headers['content-encoding'] = content_type[1]

		resp = self._session.put(self._url(name), data = content, headers = headers)
		resp.raise_for_status()
		return name

	def _open(self, name, mode = 'rb'):
		assert mode == 'rb'

		resp = self._session.get(self._url(name), stream = True)
		resp.raise_for_status()

		resp.raw.decode_content = True
		return File(resp.raw)


Storage = HTTPStorage
