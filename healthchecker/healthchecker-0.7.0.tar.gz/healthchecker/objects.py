"""Helper objects definition."""

# -----------------------------------------------------------------------------
# Copyright (C) 2019 HacKan (https://hackan.net)
#
# This file is part of HealthChecker.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

import json
from hashlib import md5
from typing import Optional, List


class ServiceStatus(object):
    """Container for the result of a health check.

    Attributes:
        url:    The requested URL.
        alive:  True for a correct response, False otherwise.
        ok:     If additional checks over the response were requested, this
                value will be True if the checks passed, False otherwise. It's
                always False if alive is False. If no additional checks were
                requested, then it's equal to alive.
    """

    def __init__(self, url: Optional[str] = None,
                 alive: bool = False, ok: bool = False):
        """Container for the result of a health check."""
        self.url: str = url if url else ''
        self.alive: bool = alive
        self.ok: bool = ok

    def __bool__(self):
        """Return the value of the ok attribute."""
        return self.ok

    def __repr__(self) -> str:
        """Return the string representation of the object."""
        return 'ServiceStatus(id={}, url={}, alive={}, ok={})'.format(
            self.id,
            self.url,
            self.alive,
            self.ok
        )

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return repr(self)

    @property
    def id(self) -> str:
        """Return the first 8 hex digits of the md5's URL hash."""
        return md5(self.url.encode('utf-8')).hexdigest()[:8]

    @property
    def dict(self) -> dict:
        """Return a dict representing the object."""
        return {
            'id': self.id,
            'url': self.url,
            'alive': self.alive,
            'ok': self.ok,
        }

    def json(self, *, pretty: bool = False) -> str:
        """JSON string representation of the object.

        Set pretty to True to get a pretty-print string indented by 2 spaces.
        """
        indent = 2 if pretty else None
        return json.dumps(self.dict, indent=indent)


class ServiceStatusList(object):
    """List of ServiceStatus objects."""

    def __init__(self):
        """List of ServiceStatus objects."""
        self._statuses: List[ServiceStatus] = []

    def insert(self, index, value):
        """Insert a ServiceStatus element in the given position."""
        self._statuses.insert(index, value)

    def append(self, value: ServiceStatus):
        """Append a ServiceStatus element at the end."""
        self._statuses.append(value)

    def pop(self) -> ServiceStatus:
        """Get the last ServiceStatus element stored, removing it."""
        return self._statuses.pop()

    def __getitem__(self, index: int) -> ServiceStatus:
        """Get the ServiceStatus element from the given position."""
        return self._statuses.__getitem__(index)

    def __iter__(self):
        """Iterate over ServiceStatus elements."""
        return self._statuses.__iter__()

    def __len__(self):
        """Get the amount of ServiceStatus elements stored."""
        return len(self._statuses)

    def __delitem__(self, index: int):
        """Remove the ServiceStatus at the given position."""
        self._statuses.__delitem__(index)

    def __setitem__(self, index: int, value: ServiceStatus):
        """Set a position with a given ServiceStatus element."""
        self._statuses.__setitem__(index, value)

    def __repr__(self) -> str:
        """Return the string representation of the object."""
        return 'ServiceStatusList([{}])'.format(', '.join([repr(status)
                                                           for status in self._statuses]))

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return repr(self)

    def __bool__(self) -> bool:
        """Return True if every ServiceStatus element is True, else False."""
        return all(self) if len(self) else False

    def json(self, *, pretty: bool = False) -> str:
        """JSON string representation of the object.

        Set pretty to True to get a pretty-print string indented by 2 spaces.
        """
        indent = 2 if pretty else None
        return json.dumps([status.dict for status in self._statuses],
                          indent=indent)
