# -*- coding: utf-8 -*-

import sys
import itertools
import functools
import collections

import werkzeug.datastructures

import cookieman.resources
import cookieman.exceptions
import cookieman.compat


class Browser(object):
    '''
    :attr name:
    :type name: str
    :attr platform:
    :type platform: str
    :attr version:
    :type version: Tuple[Union[int, str]]
    :attr maxcookies:
    :type maxcookies: int
    :attr maxsize:
    :type maxsize: int
    :attr maxtotal:
    :type maxtotal: int
    '''
    __slots__ = (
        'name', 'platform', 'version', 'maxcookies', 'maxsize',
        'maxtotal',
        )

    def __init__(self, name='', platform='', version=(), maxcookies=1,
                 maxsize=4096, maxtotal=None):
        '''
        :param name: browser name
        :type name: str
        :param platform: browser platform
        :type platform: str
        :param version: browser version
        :type version: Iterable[str]
        :param maxcookies: maximum number of cookies
        :type maxcookies: int
        :param maxsize: maximum number of bytes of every cookies
        :type maxsize: int
        :param maxtotal: maximum number of total bytes of all cookies
        :type maxtotal: Union[int, None]
        '''
        self.name = name
        self.platform = platform
        self.version = tuple(version)
        self.maxcookies = maxcookies
        self.maxsize = maxsize
        self.maxtotal = (
            min(maxtotal, maxcookies * maxsize)
            if maxcookies and maxtotal else
            maxtotal
            if maxtotal else
            maxcookies * maxsize
            )

    def __repr__(self):
        '''
        Return repr(self).

        :returns: string representation of object
        :rtype: str
        '''
        name = '%s.%s' % (
            self.__class__.__module__,
            self.__class__.__name__
            )
        props = {attr: getattr(self, attr) for attr in self.__slots__}
        return '<%s%r>' % (name, props)

    @classmethod
    def parse_version(cls, version):
        '''
        Convert version (str or tuple) to version tuple.

        :param version: version value (str or tuple)
        :type version: Union[str, Iterable[str]]
        :returns: version tuple
        :rtype: Tuple[Union[int, str], ...]
        '''
        stringlike = cookieman.compat.StringLike
        if version:
            if isinstance(version, stringlike):
                version = version.split('.')
            return tuple(
                int(i) if isinstance(i, stringlike) and i.isdigit() else i
                for i in version
                )
        return ()

    @classmethod
    def from_spec(cls, name, properties):
        '''
        Create browser object based on limits database data.

        :param name: browser identifier (name:platform:version)
        :type name: str
        :param properties:
        :type properties: Mapping[str, str]
        :returns: browser object
        :rtype: cookieman.limits.Browser
        '''
        name, platform, version = name.split(':')[:3]
        return cls(
            name,
            platform or '',
            cls.parse_version(version),
            int(properties['maxcookies']),
            int(properties['maxsize']),
            int(properties['maxtotal']),
            )


class Limits(object):
    '''
    Browser limits database
    '''
    browser_class = Browser
    mapping_class = werkzeug.datastructures.ImmutableDict
    dbparser_class = cookieman.compat.ConfigParser

    def __init__(self, browsers=()):
        '''
        :param browsers: iterable with all available browsers
        :type browsers: Iterable[cookieman.limits.Browser]
        '''
        self.browsers_by_key = self.mapping_class(
            (key, tuple(browsers)) for key, browsers in itertools.groupby(
                sorted(
                    browsers,
                    key=lambda browser: (browser.name, browser.platform,
                                         browser.version),
                    reverse=True,
                ),
                key=lambda browser: (browser.name, browser.platform)))
        self.default = self.browser_class()

    def get(self, name='', platform='', version=()):
        '''
        Get browser limits object based on given browser name, platform,
        and version.

        :param name: browser name
        :type name: str
        :param platform: browser platform name
        :type platform: str
        :param version: browser version tuple
        :type version: Union[str, tuple[str, ...]]
        :returns: browser limits object
        :rtype: cookieman.limits.Browser
        '''
        version = self.browser_class.parse_version(version)
        search_keys = (
            ((name, platform), version),
            ((name, platform), ()),
            ((name, ''), version),
            ((name, ''), ()),
            (('', ''), ()),  # database default
            )
        for (key, version) in search_keys:
            for browser in self.browsers_by_key.get(key, ()):
                if browser.version <= version:
                    return browser
        return self.default

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.browsers_by_key == other.browsers_by_key
            )

    @classmethod
    def load(cls, path=None):
        '''
        Load browser limits database file. If None or no path is given,
        it will load cookieman's builtin limits database.

        :param path: path or None
        :type path: Union[str, None]
        :returns: Limits object
        :rtype: cookieman.limits.Limits
        '''
        if path is None:
            data = cookieman.resources.read_text('limits.ini')
        else:
            with open(path, 'rb') as f:
                data = f.read().decode('utf-8')

        parser = cls.dbparser_class()
        parser.read_string(data)

        return cls(
            cls.browser_class.from_spec(name, parser[name])
            for name in parser.sections()
            )


class ShrinkManager(object):
    '''
    Manager class for cookie shrinking functions
    '''
    _key_added_exc = type('KeyAdded', (Exception, ), {})

    def __init__(self):
        self.handlers = collections.defaultdict(set)

    def register(self, key_or_keys, shrink_fnc=None):
        '''
        Register session shrink function for specific session key or
        keys. Can be used as decorator.

        Usage:
        >>> @shrinker.register('my_session_key')
        ... def my_shrink_fnc(data):
        ...     del data['my_session_key']
        ...     return data

        :type shrink_fnc: Callable[[dict, bool], dict]

        :param key_or_keys: key or list of keys would be affected
        :type key_or_keys: Union[str, Iterable[str]]
        :param shrink_fnc: shrinking function (optional for decorator)
        :type shrink_fnc: shrink_fnc
        :returns: either original given shrink_fnc or decorator
        :rtype: Union[Callable[[shrink_fnc], shrink_fnc], shrink_fnc]
        '''
        if shrink_fnc is None:
            return functools.partial(self.register, key_or_keys)

        keys = (
            (key_or_keys,)
            if isinstance(key_or_keys, cookieman.compat.StringLike) else
            key_or_keys
            )
        for name in keys:
            self.handlers[name].add(shrink_fnc)
        return shrink_fnc

    @classmethod
    def _purge(cls, key, data):
        '''
        Default handler for unhandled keys. This just removes the key.

        :param key: data dict key to remove
        :type key: str
        :param data: data mapping
        :type data: collections.abc.MutableMapping
        :returns: updated mapping
        :rtype: collections.abc.MutableMapping
        '''
        del data[key]
        return data

    def _iter_handled(self, keys, last=False):
        '''
        :param keys:
        :type keys: Iterable[str]
        :param last:
        :type last: bool
        :returns: Generator of callables
        :rtype: Generator[
            Callable[[Mapping[Any, Any]], Mapping[Any, Any]],
            Tuple[Iterable[str], bool],
            None
            ]
        '''
        again = True
        handlers = self.handlers
        visited = set()
        while again:
            again = False
            for key in tuple(keys):
                if key in visited:
                    continue

                revisit = False
                for handler in handlers.get(key, ()):
                    if key not in keys:
                        revisit = False
                        break

                    keys, shrunk = (yield lambda data: handler(data, last))
                    revisit |= shrunk

                if revisit:
                    again = True
                else:
                    visited.add(key)

    def _iter_purge(self, keys, last=False):
        '''
        :param keys:
        :type keys: Iterable[str]
        :param last:
        :type last: bool
        :returns: Generator of callables
        :rtype: Generator[
            Callable[[Mapping[Any, Any]], Mapping[Any, Any]],
            Tuple[Iterable[str], bool],
            None
            ]
        '''
        handlers = self.handlers
        for key in tuple(keys):
            if last or key not in handlers:
                yield (lambda data: self._purge(key, data))

    def _iter_tasks(self, keys):
        '''
        Iterate through key handlers, receiving if it worked or not and,
        based on that, keeps returning other handled.

        :param keys: possible handler keys to iterate
        :type keys: Iterable[str]
        :returns: Generator of callables
        :rtype: Generator[
            Callable[[Mapping[Any, Any]], Mapping[Any, Any]],
            Tuple[Iterable[str], bool],
            None
            ]

        Iteration logic:
        1. Handler functions for keys on data.
        2. Functions to purge unhandled keys.
        3. Handler functions for keys on data (receiving last=True)
        4. Functions to purge every key.
        '''
        strategies = [
            lambda keys: self._iter_handled(keys),
            lambda keys: self._iter_purge(keys),
            lambda keys: self._iter_handled(keys, True),
            lambda keys: self._iter_purge(keys, True),
            ]
        for strategy in strategies:
            strategy_iter = strategy(keys)
            try:
                keys, changed = (yield next(strategy_iter))
                while True:
                    keys, changed = (yield strategy_iter.send((keys, changed)))
            except StopIteration:
                pass

    def shrink(self, data, browser, dump_fnc, serialize_fnc):
        '''
        Apply, iteratively, shrink functions to data until it fits into
        given browser limits. If it's not possible, raises error.

        :param data: mapping
        :type data: Mapping
        :param browser: browser limits object
        :type: Browser
        :param dump_fnc: callable which returns binary data payload
        :type dump_fnc: Callable[[Any], int]
        :param serialize_fnc: callable which returns cookies
        :type serialize_fnc: Callable[
            [bytes],
            Iterable[cookieman.cookie.Cookie]
            ]
        :returns: partitioned cookies
        :rtype: Iterable[cookieman.cookie.Cookie]
        :raises exceptions.CookieSizeException: if unable to get under limits
        '''
        handlers_iter = None
        old_size = sys.maxsize
        maxsize = browser.maxsize
        maxcookies = browser.maxcookies

        while True:
            payload = dump_fnc(data)
            cookies = list(serialize_fnc(payload))
            size = sum(map(len, cookies))

            if size <= maxsize and len(cookies) <= maxcookies:
                return cookies

            try:
                if handlers_iter:
                    shrunk = len(payload) < old_size
                    handler = handlers_iter.send((data, shrunk))
                else:
                    handlers_iter = iter(self._iter_tasks(data))
                    handler = next(handlers_iter)
            except StopIteration:
                break

            old_size = len(payload)
            data = handler(data)

        raise cookieman.exceptions.CookieSizeException(
            'Session cookies exceeded browser maxsize %d' % (
                browser.maxsize,
                )
            if len(cookies) > maxsize else
            'Session cookies exceeded browser maxcookies %d' % (
                browser.maxcookies
                )
            )
