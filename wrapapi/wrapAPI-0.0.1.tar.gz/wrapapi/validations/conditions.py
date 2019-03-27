

class Condition(object):

    def __init__(self, expected):
        self.expected = expected
        self._current = None

    def __str__(self) -> str:
        return f'{self.__class__.__name__} to {self.expected}'

    def _assignee(self, current) -> None:
        """
        :param any current: need for error message only
        """
        self._current = current

    def is_valid(self, current) -> bool:
        self._assignee(current)
        return self._match(current)

    def _match(self, current):
        """
        For example:
            >> return self.expected == current
        :param any: current:
        :rtype bool
        """
        raise NotImplementedError

    def message(self):
        """
        For example:
            >> return 'Not equal, expected: 12, current: 5'
        :rtype str
        """
        raise NotImplementedError


class Equal(Condition):

    def _match(self, current):
        return self.expected == current

    @property
    def message(self):
        return (
            f'Not equal: {self.expected} == {self._current}\n'
            f'\t -> expected: {self.expected}\n'
            f'\t -> current: {self._current}\n'
        )


class NotEqual(Condition):

    def _match(self, current):
        return self.expected != current

    @property
    def message(self):
        return (
            f'Equal: {self.expected} != {self._current}\n'
            f'\t -> expected: {self.expected}\n'
            f'\t -> current: {self._current}\n'
        )


class Less(Condition):

    def _match(self, current):
        return self.expected < len(current)

    @property
    def message(self):
        return (
            f'Not less: {self.expected} < {len(self._current)}\n'
            f'\t -> expected: {self.expected}\n'
            f'\t -> current: {self._current}\n'
        )


class LessOrEqual(Condition):

    def _match(self, current):
        return self.expected <= len(current)

    @property
    def message(self):
        return (
            f'Not less and not equal: {self.expected} <= {len(self._current)}\n'
            f'\t -> expected: {self.expected}\n'
            f'\t -> current: {self._current}\n'
        )


class Greater(Condition):

    def _match(self, current):
        return self.expected > len(current)

    @property
    def message(self):
        return (
            f'Not greater: {self.expected} > {len(self._current)}\n'
            f'\t -> expected: {self.expected}\n'
            f'\t -> current: {self._current}\n'
        )


class GreaterOrEqual(Condition):

    def _match(self, current):
        return self.expected >= len(current)

    @property
    def message(self):
        return (
            f'Not greater and not equal: {self.expected} >= {len(self._current)}\n'
            f'\t -> expected: {self.expected}\n'
            f'\t -> current: {self._current}\n'
        )


class Is(Condition):

    def _match(self, current):
        return self.expected is current

    @property
    def message(self):
        return (
            f'Not valid: {self.expected} is {self._current}\n'
            f'\t -> expected: {self.expected}\n'
            f'\t -> current: {self._current}\n'
        )


class IsNot(Condition):

    def _match(self, current):
        return self.expected is not current

    @property
    def message(self):
        return (
            f'Not valid: {self.expected} is not {self._current}\n'
            f'\t -> expected: {self.expected}\n'
            f'\t -> current: {self._current}\n'
        )


class IsInstance(Condition):

    def _match(self, current):
        return isinstance(current, self.expected)

    @property
    def message(self):
        return (
            f'Not valid: {self.expected} is {type(self._current)}\n'
            f'\t -> expected: {self.expected}\n'
            f'\t -> current: {self._current}\n'
        )


class IsNotInstance(Condition):

    def _match(self, current):
        return not isinstance(current, self.expected)

    @property
    def message(self):
        return (
            f'Not valid: {self.expected} is {type(self._current)}\n'
            f'\t -> expected: {self.expected}\n'
            f'\t -> current: {self._current}\n'
        )


class Be(object):

    def __init__(self, request, report):
        self.request = request
        self._json = request.json()
        self._report = report

    def _must(self, condition):
        if not condition.is_valid(self._json):
            self._report.add_error(self.request, condition.message)
        return self

    def equal(self, expected):
        return self._must(Equal(expected))

    def not_equal(self, expected):
        return self._must(NotEqual(expected))

    def less(self, expected):
        return self._must(Less(expected))

    def less_or_equal(self, expected):
        return self._must(LessOrEqual(expected))

    def greater(self, expected):
        return self._must(Greater(expected))

    def greater_or_equal(self, expected):
        return self._must(GreaterOrEqual(expected))

    def is_(self, expected):
        return self._must(Is(expected))

    def is_not(self, expected):
        return self._must(IsNot(expected))

    def is_none(self):
        return self._must(Is(None))

    def is_not_none(self):
        return self._must(IsNot(None))

    def is_instance(self, expected):
        return self._must(IsInstance(expected))

    def is_not_instance(self, expected):
        return self._must(IsNotInstance(expected))

    def schema(self):
        # TODO need implement json_checker
        pass


class Has(object):

    def __init__(self, request, report):
        self.request = request
        self._report = report

    def __call__(self, *args, **kwargs) -> bool:
        return self.empty()

    def empty(self) -> bool:
        return bool(self.request.json())

    def dict(self, **kwargs) -> bool:
        # TODO make
        errors = []
        # for k, v in kwargs:
        #     res = find_key(self.request, k)
        #     res == v
        return False

    def key(self, expected_key) -> bool:
        # TODO make
        # find_key()
        return False

    def value(self, expected_value) -> bool:
        # TODO make
        # find_value()
        return False


class Should(object):

    def __init__(self, request, report):
        self._request = request
        self._report = report
        self._be = None
        self._has = None

    @property
    def be(self) -> Be:
        if not self._be:
            self._be = Be(self._request, report=self._report)
        return self._be

    @property
    def has(self) -> Has:
        if not self._has:
            self._has = Has(self._request, report=self._report)
        return self._has
