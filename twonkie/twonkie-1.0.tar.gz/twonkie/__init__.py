from __future__ import print_function


from collections import deque


class _NoValue:
    pass


class Twonkie:

    def __init__(self, items, _path=None):
        self._items = iter(items)
        self._path = _path or (("Twonkie", type(items).__name__),)

    def __iter__(self):
        return iter(self._items)

    def __next__(self):
        return next(self._items)

    def __repr__(self):
        return '.'.join("{}({})".format(pair[0], ', '.join(map(str, pair[1:]))) for pair in self._path)

    def __str__(self):
        return '\n  |> '.join("{}({})".format(pair[0], ', '.join(map(str, pair[1:]))) for pair in self._path)

    def map(self, fn):
        return Twonkie(
            (fn(item) for item in self._items),
            self._path + (("map", fn.__name__),)
        )

    def smap(self, fn):
        """
        Map the splat of the items.
        """
        return Twonkie(
            (fn(*item) for item in self._items),
            self._path + (("smap", fn.__name__),)
        )

    def filter(self, key):
        return Twonkie(
            (item for item in self._items if key(item)),
            self._path + (("filter", key.__name__),)
        )

    def sfilter(self, key):
        """
        Filter the items, uses the splat operator on the key function, just like smap.
        """
        return Twonkie(
            (item for item in self._items if key(*item)),
            self._path + (("sfilter", key.__name__),)
        )

    def then(self, fn):
        return Twonkie(
            fn(self),
            self._path + (("then", fn.__name__),)
        )

    def flatten(self):
        def _inner():
            for subgroup in self._items:
                for item in subgroup:
                    yield item

        return Twonkie(
            _inner(),
            self._path + (("flatten",),)
        )

    def skip(self, n):
        def _inner():
            try:
                for _ in xrange(n):
                    next(self._items)

            except StopIteration:
                pass

            return self._items

        return Twonkie(
            _inner(),
            self._path + (("skip", n),)
        )

    def take(self, n):
        def _inner():
            try:
                for _ in xrange(n):
                    yield next(self._items)
            except StopIteration:
                pass

        return Twonkie(
            _inner(),
            self._path + (("take", n),)
        )

    def partition(self, n):

        def _take():
            try:
                for _ in xrange(n):
                    yield next(self._items)
            except StopIteration:
                pass

        def _inner():
            try:
                i = 0
                while True:
                    items = list(_take())

                    if not items:
                        break

                    yield Twonkie(
                        items,
                        self._path + (
                            ("partition", n),
                            ("skip", i),
                            ("first",),
                        )
                    )

                    i += 1

            except StopIteration:
                pass

        return Twonkie(
            _inner(),
            self._path + (("partition", n),)
        )

    def between(self, a, b, key=None):
        """
        Returns items between a and b. (Inclusive).
        """
        if key:
            return Twonkie(
                (item for item in self._items if a <= key(item) <= b),
                self._path + (("between", a, b, 'key={}'.format(key.__name__)),)
            )

        return Twonkie(
            (item for item in self._items if a <= item <= b),
            self._path + (("between", a, b),)
        )

    def exclude(self, excluded, key=None):
        """
        Excludes all items based on either their identity, or a key function.
        """
        if key:
            return Twonkie(
                (item for item in self._items if key(item) not in excluded),
                self._path + (("exclude", excluded, 'key={}'.format(key.__name__)),)
            )

        return Twonkie(
            (item for item in self._items if item not in excluded),
            self._path + (("exclude", excluded),)
        )

    def extend(self, items):
        """
        Yields all the items from this._items, followed by the items supplied to this function.
        """

        def _inner():
            for item in self:
                yield item

            for item in iter(items):
                yield item

        return Twonkie(
            _inner(),
            self._path + (("extend", items),)
        )

    def sort(self, key=None, reverse=False):
        """
        Sorts the items by key.
        """
        return Twonkie(
            sorted(self._items, key=key, reverse=reverse),
            self._path + (("sort", key.__name__, 'reverse={}'.format(reverse)),)
        )

    def unique(self, key=None):
        """
        Filter out items that aren't considered unique.
        You can optionally supply a key function to determine the identity.
        """

        def _inner():
            seen = set()

            if key:
                for item in self._items:
                    _item = key(item)
                    if key(item) not in seen:
                        seen.add(_item)
                        yield item
                return

            for item in self._items:
                if item not in seen:
                    seen.add(item)
                    yield item

        return Twonkie(
            _inner(),
            self._path + (("unique", key.__name__),)
        )

    def sweep(self, width, step=1):
        """
        Similar to itertools' pairwise, this will hand out _width_ number of items at a time, with an offset of _step_.
        Twonkie(range(11)).sweep(2) yields the same result as itertools.pairwise, while .sweep(3) would give you
        (0, 1, 2), (1, 2, 3), ... (8, 9, 10).
        The last item may be None-padded if there were not _step_ items left in the Twonkie.
        """

        def _inner():
            items = self.take(width)
            current = deque(items, maxlen=width)
            while items:
                yield tuple(current)
                items = self.take(step).tuple()
                current.extend(items)
                if items and len(items) < step:
                    current.extend([None] * (step - len(items)))

        return Twonkie(
            _inner(),
            self._path + (("sweep", width, step),)
        )

    def consume(self, n=None):
        """
        Consume n items. If n is None, consume everything.
        """
        self._path += (("consume",),)

        try:
            for _ in range(n) if n else self._items:
                next(self._items)

        except StopIteration:
            pass

        return self

    def tee(self, display=None):
        """
        Every item that falls through the tee function will be displayed using the display function.
        If none is supplied, print is used.
        """
        display = display or print

        def _inner():
            for item in self._items:
                display(item)
                yield item

        return Twonkie(
            _inner(),
            self._path + (("unique", display.__name__),)
        )

    # region Functions not resulting in a Twonkie.

    def any(self, key=None):
        if key is None:
            return any(self)

        return any((key(it) for it in self))

    def all(self, key=None):
        if key is None:
            return all(self)

        return all((key(it) for it in self))

    def first(self, key=None, default=_NoValue):
        try:
            if key is None:
                return next(self._items)

            return next(item for item in self._items if key(item))

        except StopIteration:
            if default is _NoValue:
                raise
            return default

    def reduce(self, fn, initial_value=_NoValue):
        result = initial_value

        if result is _NoValue:
            result = next(self._items)

        for item in self._items:
            result = fn(result, item)

        return result

    def len(self):
        """
        Consumes all items to produce a count.
        """
        return sum(1 for _ in self._items)

    def set(self):
        return set(self._items)

    def list(self):
        return list(self._items)

    def tuple(self):
        return list(self._items)

    def dict(self, key, transform=None):
        """
        Returns a dict of all items.
        """

        if transform is None:
            return {key(it): it for it in self._items}

        return {key(it): transform(it) for it in self._items}

    # endregion