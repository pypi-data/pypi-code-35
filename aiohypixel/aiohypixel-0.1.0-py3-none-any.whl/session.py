#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# MIT License

# Copyright (c) 2018-2019 Tmpod

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This defines a connection to the Hypixel API. 
All requests will pass through here and this will handle everything for you
"""

__all__ = ("HypixelSession",)

import aiohttp
import asyncio
import logging
from typing import Set, Union
from random import choice
import re

from .asyncinit import AsyncInit
from .shared import *
from .player import *
from .guild import *
from .boosters import *
from .keys import *
from .friends import *
from .watchdogstats import *

#: This is the base URL for all the requests regarding the Hypixel API
BASE_API_URL = "https://api.hypixel.net/"

#: Max API keys set acceptable lenght if no 'force validation' option is passed
KEY_SET_LEN_NO_FORCE = 10

#: This is the message sent when you try to do a request with an invalid key
INVALID_KEY_MESSAGE = "Invalid API key!"

#: Mojang name lookup endpoint
MOJANG_API_URL = "https://api.mojang.com/users/profiles/minecraft/"

#: This is th length of a UUID. 32 hex digits + 4 dashes
UUID_LENGTH = (32, 36)

#: This is the boundaries of char lenghts for Minecraft usernames
MC_NAME_LENGTH = (3, 16)

#: Regex pattern to filter UUID strings
UUID_RE = re.compile(
    r"^[0-9a-f]{8}-?[0-9a-f]{4}-?[1-5][0-9a-f]{3}-?[89AB][0-9a-f]{3}-?[0-9a-f]{12}$", re.I
)

MONGO_ID_RE = re.compile(r"^[a-f\d]{24}$", re.I)


class HypixelSession(AsyncInit):
    """
	Represents a connection to the Hypixel API.
	"""

    def __init__(
        self,
        api_keys: Union[str, Set[str]],
        *,
        base_url: str = BASE_API_URL,
        force_validation: bool = False,
        ignore_validation_errors: bool = False,
    ) -> None:
        """
		Does some basic validation checks and setting some attributes. 
		A validation request will be done in :attr:`__ainit__`
		"""
        self._logger = logging.getLogger(__name__)
        self._logger.debug(
            "Starting a new session! Doing some base checks to the API key(s)"
        )

        if not isinstance(api_keys, (str, set)):
            self._logger.error("The keys provided are not valid! Raising ValueError")
            raise ValueError(
                "You can only pass a string (single key) or list or set with strings (multiple keys)."
            )
        elif isinstance(api_keys, str):
            self.api_keys = (api_keys.strip(),)
        else:
            self.api_keys = tuple(k.strip() for k in api_keys)

        self._logger.debug("Finished aggregating the key(s)!\nNow setting up some more stuff...")

        self._loop = asyncio.get_event_loop()
        self.aiohttp = aiohttp.ClientSession(loop=self._loop)
        self._base_url: str = base_url
        self._force_key_vald: bool = force_validation
        self._ignore_vald_err: bool = ignore_validation_errors

        self._logger.debug("Base init all done! Loop and aiohttp session acquired!")

    async def __ainit__(
        self,
        api_keys: Union[str, Set[str]],
        *,
        base_url: str = BASE_API_URL,
        force_validation: bool = False,
        ignore_validation_errors: bool = False,
    ) -> None:
        """
        This is where the keys are validated through abstract requests to the API, effectively 
        testing them. This uses the ``key`` endpoint which is also used in :attr:`get_key`
        """
        self._logger.debug(
            "Now proceeding with a request validation of the provided keys!"
        )
        if len(self.api_keys) > KEY_SET_LEN_NO_FORCE and not self._force_key_vald:
            self._logger.info(
                "The collection of keys is too long and you haven't specified "
                "'force_validation', so it will be skipped!"
            )
        else:
            invalid_keys = await self._check_keys(self.api_keys)
            self.api_keys = tuple(set(self.api_keys) - invalid_keys)
        self._logger.debug("Async init all done! The session is now fully ready!")

    async def _check_keys(self, keys: Union[str, Set[str]]) -> Union[None, Set[str]]:
        """This will do the actual checking of the keys via some requests"""
        rejected_keys = set()
        for k in keys:
            async with self.aiohttp.get(f"{BASE_API_URL}key/?key={k}", ssl=False) as resp:
                result = await resp.json()
                # Probably the second check isn't even really necessary
                if (
                    not result.get("success")
                    and result.get("cause") == INVALID_KEY_MESSAGE
                ):
                    if self._ignore_vald_err:
                        self._logger.info(
                            '"%s" isn\'t valid! It was rejected by the API! Removing it...',
                            k,
                        )
                        rejected_keys.add(k)
                    else:
                        self._logger.error(
                            '"%s" isn\'t valid! It was rejected by the API! Raising ValueError!',
                            k,
                        )
                        raise InvalidAPIKey(f"{k} isn't a valid API key!")
        self._logger.debug(
            "Finished checking the API keys. Encoutered %s error%s!",
            len(rejected_keys) or "no",
            "s" if rejected_keys else "",
        )
        return rejected_keys

    async def edit_keys(
        self, new_keys: Union[str, Set[str]], force_validation: bool = False
    ) -> None:
        """
        Allows you to edit your registered keys for this session. 
        Will verify the keys again, just like in :attr:`__ainit__`
        """
        if len(self.api_keys) > KEY_SET_LEN_NO_FORCE and not force_validation:
            self._logger.info(
                "The collection of keys is too long and you haven't specified "
                "'force_validation', so it will be skipped!"
            )
        else:
            invalid_keys = await self._check_keys(self.api_keys)
            self.api_keys = tuple(set(self.api_keys) - invalid_keys)
        self._logger.info(
            "Keys were changed! Check the logs to see if there was any error "
            "(applicable if you set it to ignore the errors"
        )

    async def name_to_uuid(self, query: str) -> str:
        """
        Gets the UUID for the player with the given name.
        Uses the Mojang API for that.
        """
        self._logger.debug("Fetching UUID from name: %s", query)
        async with self.aiohttp.get(f"{MOJANG_API_URL}{query}") as resp:
            resp.raise_for_status()
            return (await resp.json())["id"]

    async def uuid_to_name(self, query: str) -> str:
        """
        Gets the name for the player with the given UUID.
        Uses the Mojang API for that.
        """
        self._logger.debug("Fetching name from UUID: %s", query)
        async with self.aiohttp.get(f"{MOJANG_API_URL}{query}") as resp:
            resp.raise_for_status()
            return (await resp.json())["name"]

    async def _fetch_json(self, endpoint: str, params: dict = None):
        """
        Fetches the JSON from the passed endpoint with the given params.
        
        Note:
            ``key`` will always be a param.
        """
        self._logger.debug("Starting to fetch JSON from the **%s** endpoint with these params: %s", endpoint, params)

        self._logger.debug("Chosing key...")
        if params is None:
            params = {"key": choice(self.api_keys)}

        elif "key" not in params:
            params["key"] = choice(self.api_keys)
        self._logger.debug("Chose: `%s`\nNow doing the actual fetching...", params["key"])

        async with self.aiohttp.get(f"{BASE_API_URL}{endpoint}", params=params, ssl=False) as resp:
            resp.raise_for_status()
            result = await resp.json()

        try:
            if not result["success"]:
                self._logger.error("Request failed! Cause: %s", result["cause"])
                raise UnsuccesfulRequest(result["cause"])

            self._logger.debug("Request was successful! Returning result...")
            return result
        except KeyError:
            raise HypixelAPIError(
                "Something went wrong with the Hypixel API! Try again later."
            )

    @staticmethod
    def is_uuid(query: str) -> bool:
        return bool(UUID_RE.findall(query))

    async def get_player(self, query: str) -> Player:
        """
        Gets a full player object (general info + game stats) with the given query.
        The query can either be a UUID or a Minecraft IGN.
        """
        self._logger.debug("Checking if query is a UUID...")
        if self.is_uuid(query):
            query_type = "uuid"
        else:
            query_type = "name"

        result = await self._fetch_json("player", params={query_type: query})

        return process_raw_player(result["player"])

    async def get_player_stats(self, query: str) -> Tuple[ImmutableProxy]:
        """
        Gets a player's stats with the given query.
        The query can either be a UUID or a Minecraft IGN.
        """
        self._logger.debug("Checking if query is a UUID...")
        if self.is_uuid(query):
            query_type = "uuid"
        else:
            query_type = "name"

        result = await self._fetch_json("player", params={query_type: query})

        return process_raw_player_stats(result["player"])

    async def get_player_info(self, query: str) -> Player:
        """
        Gets a player object with just the network info that does not relate to any stats.
        The query can either be a UUID or a Minecraft IGN.
        """
        self._logger.debug("Checking if query is a UUID...")
        if self.is_uuid(query):
            query_type = "uuid"
        else:
            query_type = "name"

        result = await self._fetch_json("player", params={query_type: query})

        return process_raw_player(result["player"], partial=True)

    async def get_guild(self, query: str) -> Guild:
        """
        Gets a guild object from the given query.
        This query can be either an ID or a name
        """
        self._logger.debug("Checking if query is a UUID...")
        if MONGO_ID_RE.findall(query):
            query_type = "id"
        else:
            query_type = "name"

        result = await self._fetch_json("guild", params={query_type: query})

        return process_raw_guild(result["guild"])

    async def get_guild_by_player(self, query: str) -> Union[None, Guild]:
        """
        Gets a guild object to which the player with the given name/UUID belongs to.
        Can be ``None``, of course.
        """
        self._logger.debug("Checking if query is a UUID...")
        if self.is_uuid(query):
            uuid = query
        else:
            self._logger.debug("Need to get the UUID for this name!")
            uuid = self.name_to_uuid(query)
                        
        g_id = (await self._fetch_json("findGuild", params={"byUuid": uuid})).get("guild")

        if g_id is None:
            return

        result = await self._fetch_json("guild", params={"id": g_id})

        return process_raw_guild(result["guild"])

    async def get_key(self, query: str) -> Key:
        """Gets a Key object from the passed query."""
        if not self.is_uuid(query):
            raise InvalidAPIKey(
                f"{query} isn't a valid UUID and so it isn't a valid key!"
            )

        result = await self._fetch_json("key", params={"key": query})

        return process_raw_key(result["record"])

    async def get_friends(self, query: str) -> Tuple[Friend]:
        """Gets a tuple of Friend objects that the player with the given name/UUID has."""
        if not self.is_uuid(query):
            raise ValueError(f"{query} isn't a valid UUID!")

        result = await self._fetch_json(
            "friends", params={"uuid": query}
        )

        friends = (process_raw_friend(f) for f in result.get("records"))

        return tuple(friends)

    async def get_boosters(self) -> Tuple[Booster]:
        """Gets a tuple of Booster objects denoting the currently active boosters on the Hypixel Network"""
        result = await self._fetch_json("boosters")

        boosters = tuple(process_raw_booster(b) for b in result.get("boosters", ()))

        return {"boosters": boosters, "state": result.get("boosterState")}

    async def get_watchdogstats(self):
        """Gets the current WatchDog stats"""
        result = await self._fetch_json("watchdogstats")

        return process_raw_wds(result)
