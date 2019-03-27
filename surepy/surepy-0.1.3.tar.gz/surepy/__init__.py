"""
surepy

MIT License
Copyright (c) 2018 Benjamin Lebherz <git@benleb.de>
"""

import asyncio
import logging
import random

import aiohttp
import async_timeout

ACCEPT = "Accept"
ACCEPT_ENCODING = "Accept-Encoding"
ACCEPT_LANGUAGE = "Accept-Language"
AUTHORIZATION = "Authorization"
CONNECTION = "Connection"
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_TEXT_PLAIN = "text/plain"
ETAG = "ETag"
HTTP_HEADER_X_REQUESTED_WITH = "X-Requested-With"
ORIGIN = "Origin"
REFERER = "Referer"
USER_AGENT = "User-Agent"


# get logger & configure basic log format
_LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s | [%(name)s] - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
_LOGGER.setLevel(logging.WARNING)


_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930F Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/64.0.3282.137 Mobile Safari/537.36"
_RESOURCE: str = "https://app.api.surehub.io/api"
_RESOURCES: dict = dict(
    auth=f"{_RESOURCE}/auth/login",
    device="{}{}".format(_RESOURCE, "/device/{flap_id}/status"),
    household="{}{}".format(_RESOURCE, "/household/{household_id}/device"),
    pet="{}{}".format(_RESOURCE, "/pet/{pet_id}/position"),
    timeline="{}{}".format(_RESOURCE, "/timeline/household/{household_id}"),
)


class SurePetcare:
    """Communication with the Sure Petcare API."""

    def __init__(
        self, email, password, household_id, loop, session, auth_token=None, debug=False
    ):
        """Initialize the connection to the Sure Petcare API."""
        self._loop = loop
        self._session = session

        self.email = email
        self.password = password
        self.household_id = household_id

        self._device_id = self._generate_device_id()
        self._auth_token = auth_token

        self.sure_data = dict()
        self.flap_data = dict()
        self.pet_data = dict()
        self.household_data = dict()

        if debug:
            _LOGGER.setLevel(logging.DEBUG)
            _LOGGER.debug(f"initialization completed | vars(): {vars()}")

    @property
    def auth_token(self):
        """Return authentication token."""
        return self._auth_token

    async def _refresh_token(self) -> str:
        """Get or refresh the authentication token."""
        authentication_data = dict(
            email_address=self.email, password=self.password, device_id=self._device_id
        )

        try:
            with async_timeout.timeout(5, loop=self._loop):
                response: aiohttp.ClientResponse = await self._session.post(
                    _RESOURCES["auth"],
                    data=authentication_data,
                    headers=self._generate_headers(),
                )

            if response.status == 200:

                response = await response.json()

                if "data" in response and "token" in response["data"]:
                    self._auth_token = response["data"]["token"]

            elif response.status == 304:
                # Etag header matched, no new data avaiable
                pass

            elif response.status == 401:
                self._auth_token = None
                raise SurePetcareAuthenticationError()

            else:
                _LOGGER.debug(f"Response from {_RESOURCES['auth']}: {response}")
                self._auth_token = None

            return self._auth_token

        except (asyncio.TimeoutError, aiohttp.ClientError, AttributeError) as error:
            _LOGGER.debug("Failed to fetch %s: %s", _RESOURCES["auth"], error)

    async def get_flap_data(self, sure_id, second_try=False) -> dict:
        return await self.get_data(
            sure_id,
            resource=_RESOURCES["device"].format(flap_id=sure_id),
            second_try=False,
        )

    async def get_pet_data(self, sure_id, second_try=False) -> dict:
        return await self.get_data(
            sure_id, resource=_RESOURCES["pet"].format(pet_id=sure_id), second_try=False
        )

    async def get_data(self, sure_id, resource=None, second_try=False) -> dict:
        """Retrieve the flap data/state."""
        if sure_id not in self.sure_data:
            self.sure_data[sure_id] = dict()

        if not self._auth_token:
            await self._refresh_token()

        if not self.household_data:
            await self.get_household_data(self.household_id)

        try:
            with async_timeout.timeout(5, loop=self._loop):
                headers = self._generate_headers()

                if ETAG in self.sure_data[sure_id]:
                    headers[ETAG] = self.sure_data[sure_id][ETAG]
                    _LOGGER.debug(f"using available {ETAG}: {headers}")

                response: aiohttp.ClientResponse = await self._session.get(
                    resource, headers=headers
                )

            if response.status == 200:

                # self.sure_data[sure_id] = await response.json()
                response_json = await response.json()

                if "data" in response_json and "version" in response_json["data"]:
                    self.sure_data[sure_id]["components"] = response_json["data"].pop("version")
                    self.sure_data[sure_id].update(response_json.pop("data"))
                    self.sure_data[sure_id].update(response_json)
                else:
                    self.sure_data[sure_id] = response_json["data"]

                if ETAG in response.headers:
                    self.sure_data[sure_id][ETAG] = response.headers[ETAG].strip('"')

            elif response.status == 304:
                # Etag header matched, no new data avaiable
                pass

            elif response.status == 401:
                _LOGGER.debug(f"AuthenticationError! Retry: {second_try}: {response}")
                self._auth_token = None
                if not second_try:
                    token_refreshed = await self._refresh_token()
                    if token_refreshed:
                        await self.get_flap_data(sure_id, second_try=True)

                raise SurePetcareAuthenticationError()

            else:
                _LOGGER.debug(f"Response from {resource}: {response}")
                self.sure_data[sure_id] = None

            thing_ids = dict()
            for thing in self.household_data[self.household_id]["data"]:
                thing_ids[thing["id"]] = thing

            if sure_id in thing_ids:
                self.sure_data[sure_id].update(thing_ids[sure_id])

            return self.sure_data[sure_id]

        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error(f"Can not load data from {resource}")
            raise SurePetcareConnectionError()

    async def get_household_data(self, household_id, second_try=False) -> dict:
        """Retrieve the flap data/state."""
        device_resource = _RESOURCES["household"].format(household_id=household_id)

        if household_id not in self.household_data:
            self.household_data[household_id] = dict()

        if not self._auth_token:
            await self._refresh_token()

        try:
            with async_timeout.timeout(5, loop=self._loop):
                headers = self._generate_headers()
                if ETAG in self.household_data[household_id]:
                    headers[ETAG] = self.household_data[household_id][ETAG]
                    _LOGGER.debug(f"using available {ETAG} in headers: {headers}")

                response: aiohttp.ClientResponse = await self._session.get(
                    device_resource, headers=headers
                )

            if response.status == 200:

                self.household_data[household_id] = await response.json()

                if ETAG in response.headers:
                    self.household_data[household_id][ETAG] = response.headers[
                        ETAG
                    ].strip('"')

                for device in self.household_data[household_id]["data"]:
                    if device["id"] in self.flap_data:
                        self.flap_data[device["id"]].update(device)

            elif response.status == 304:
                # Etag header matched, no new data avaiable
                pass

            elif response.status == 401:
                _LOGGER.debug(f"AuthenticationError! Retry: {second_try}: {response}")
                self._auth_token = None
                if not second_try:
                    token_refreshed = await self._refresh_token()
                    if token_refreshed:
                        await self.get_household_data(household_id, second_try=True)

                raise SurePetcareAuthenticationError()

            else:
                _LOGGER.debug(f"Response from {device_resource}: {response}")
                self.household_data[household_id] = None

            return self.household_data[household_id]

        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error(f"Can not load data from {device_resource}")
            raise SurePetcareConnectionError()

    def _generate_headers(self):
        return {
            CONNECTION: "keep-alive",
            ACCEPT: f"{CONTENT_TYPE_JSON}, {CONTENT_TYPE_TEXT_PLAIN}, */*",
            ORIGIN: "https://surepetcare.io",
            USER_AGENT: _USER_AGENT,
            REFERER: "https://surepetcare.io/",
            ACCEPT_ENCODING: "gzip, deflate",
            ACCEPT_LANGUAGE: "en-US,en-GB;q=0.9",
            HTTP_HEADER_X_REQUESTED_WITH: "com.sureflap.surepetcare",
            AUTHORIZATION: f"Bearer {self._auth_token}",
        }

    @staticmethod
    def _generate_device_id():
        """Generate a "unique" client device ID based on MAC address."""
        random_bytes = ":".join(
            ("%12x" % random.randint(0, 0xFFFFFFFFFFFF))[i: i + 2]
            for i in range(0, 12, 2)
        )

        mac_dec = int(random_bytes.replace(":", "").replace("-", ""), 16)
        # Use low order bits because upper two octets are low entropy
        return str(mac_dec)[-10:]


class SurePetcareError(Exception):
    """General Sure Petcare Error exception occurred."""


class SurePetcareConnectionError(SurePetcareError):
    """When a connection error is encountered."""


class SurePetcareAuthenticationError(SurePetcareError):
    """When a authentication error is encountered."""
