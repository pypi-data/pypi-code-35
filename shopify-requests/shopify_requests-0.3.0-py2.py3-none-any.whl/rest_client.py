from time import sleep

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

RATE_LIMIT_CODES = (429, 430)


class RestClient():
    def __init__(
            self, myshopify_domain,
            access_token=None,
            username=None,
            password=None,
            connect_retries=None,
            backoff_factor=None,
            max_limit_retries=None,
            limit_backoff_factor=None,
    ):
        """Create a session client for this Shopify store.

        Note:
        - Only access_token or (username and password) are required
        - urllib3 documents backoff_factor as:
        {backoff factor} * (2 ** ({number of total retries} - 1))

        :param: myshopify_domain: foobar.myshopify.com
        :param: access_token: OAuth token from a pubilc app
        :param username: Username for private app
        :param password: Password for private app
        :param connect_retries: how many connection-related errors to retry on
                                default: 3
        :param backoff_factor: how quickly to backoff for safe retries
                               default: 0.5
        :param max_limit_retries: how many retries to do when rate limited
                                  default: 0
        :param limit_backoff_factor: same as backoff_factor but for rate limited
                                     default: 0.5
        """
        if connect_retries is None:
            connect_retries = 3
        if backoff_factor is None:
            backoff_factor = 0.5
        if max_limit_retries is None:
            max_limit_retries = 0
        if limit_backoff_factor is None:
            limit_backoff_factor = 0.5

        self.myshopify_domain = myshopify_domain
        if myshopify_domain is None:
            raise TypeError('myshopify_domain is required')

        self.session = requests.Session()
        if access_token:
            self.session.headers['X-Shopify-Access-Token'] = access_token
        elif username and password:
            self.session.auth = username, password
        else:
            msg = 'access_token or username and password are required'
            raise ValueError(msg)

        self.max_limit_retries = max_limit_retries
        self.limit_backoff_factor = limit_backoff_factor

        retry = Retry(
            total=None,  # fallback on other counts
            read=0,  # dont retry after data made it to the server
            connect=connect_retries,
            backoff_factor=backoff_factor,
            respect_retry_after_header=False,
            redirect=0,
        )
        adapter = HTTPAdapter(max_retries=retry)
        prefix = "https://{}/admin/".format(self.myshopify_domain)
        self.session.mount(prefix, adapter)

        self.session.headers['Accept'] = 'application/json'

    def _url(self, url):
        return "https://{}/admin/{}".format(self.myshopify_domain, url)

    def _within_limit(self, f):
        max_attempts = self.max_limit_retries + 1
        attempt = 0
        while attempt < max_attempts:
            resp = f()
            if resp.status_code not in RATE_LIMIT_CODES:
                break
            attempt += 1
            if attempt < max_attempts:
                tts = self.limit_backoff_factor * (2 ** (attempt - 1))
                sleep(tts)
        return resp

    def get(self, url, **kwargs):
        return self._within_limit(
            lambda: self.session.get(self._url(url), **kwargs)
        )

    def put(self, url, **kwargs):
        return self._within_limit(
            lambda: self.session.put(self._url(url), **kwargs)
        )

    def post(self, url, **kwargs):
        return self._within_limit(
            lambda: self.session.post(self._url(url), **kwargs)
        )

    def patch(self, url, **kwargs):
        return self._within_limit(
            lambda: self.session.patch(self._url(url), **kwargs)
        )

    def delete(self, url, **kwargs):
        return self._within_limit(
            lambda: self.session.delete(self._url(url), **kwargs)
        )

    def close(self):
        self.session.close()
