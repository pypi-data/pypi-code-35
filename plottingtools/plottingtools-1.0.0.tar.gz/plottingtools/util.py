# util.py
# Author: Joshua Beard
# Created: 2019-01-08
# NOTE: This code was pulled from youtill on 2019-03-22, because youtill is not
# on the PyPI yet

import collections
from numpy import prod
from warnings import warn

VERBOSITY = 0
DEBUG = False

operations = collections.OrderedDict()
operations['<='] = lambda x, y: x <= y
operations['>='] = lambda x, y: x >= y
operations['=='] = lambda x, y: x == y
operations['!='] = lambda x, y: x != y
operations['>'] = lambda x, y: x > y
operations['<'] = lambda x, y: x < y


def trycast(item, newtype):
    try:
        cast = newtype(item)
    except (ValueError):
        cast = item
    return cast


def isiterable(item):
    return isinstance(item, collections.Iterable)


def isnumeric(item):
    return str(item).isnumeric()


def isoperation(string):
    """ Determines if a string is a valid operation according to the operations
        dictionary
        Example:
            >>> assert(isoperation('<='))
            >>> assert(isoperation('>='))
            >>> assert(isoperation('=='))
            >>> assert(isoperation('!='))
            >>> assert(isoperation('>'))
            >>> assert(isoperation('<'))
    """
    return string in operations.keys()


def deprecated(f):
    """ Allows function decoration to raise a warning when called
        Raises a UserWarning instead of DeprecationWarning so that it's
        detectable in an IPython session.
        For use, see examples/deprecated.py
    """
    def deprec_warn():
        deprecation_msg = '{} is deprecated - consider replacing it'.format(f.__name__)  # NOQA
        warn(deprecation_msg)
        f()
    return deprec_warn


def check_constraints(param_value, param_name, constraints, check_all=True):
    """ function for checking if a parameter value is valid within constraints.
        Parameters:
            param_value: The value of the parameter to check
            param_name: The name of the parameter
            constraints: The dictionary containing all constraints on this
                parameter, including type or numerical constraints
        Returns:
            bool: whether the param_value is properly constrained
        Example:
            >>> v = dict(s=str,
            ...          n=('>=1', '<5'),
            ...          l=collections.Iterable,
            ...          na=(None),
            ...          e=(lambda x: True if x is None else isinstance(x, str)))
            >>> assert(check_constraints('a', 's', v))
            >>> assert(not check_constraints(1, 's', v))
            >>> assert(check_constraints(1, 'n', v))
            >>> assert(check_constraints(4, 'n', v))
            >>> assert(not check_constraints(5, 'n', v))
            >>> assert(check_constraints('anything', 'na', v))
            >>> assert(check_constraints('string', 'e', v))
            >>> assert(check_constraints(None, 'e', v))
            >>> assert(not check_constraints(1, 'e', v))
    """

    def _check_constraint(item, c, item_name=None):
        """ Helper to determine if item is correctly constrained by c
            Parameters:
                item: the value to check
                c: constraint to check against
        """

        def _isop(c, opstr):
            """ Helper to determine if a constraint is the same as an operation string
                Parameters:
                    c (str): constraint to check e.g. '<3', '>=0'
                    opstr (str): operation we're concerned with e.g. '<', '>='
                Returns:
                    (bool) True if constraint matches operation, False OTW
                Example:
                    >>> assert(_isop('<3', '<')
                    >>> assert(_isop('>=3', '>=')
                    >>> assert(_isop('==3', '==')
                    >>> assert(not _isop('==3', '!=')
                    >>> assert(not _isop('>=3', '>')
                    >>> assert(not _isop('<3', '<=')
            """
            return c.startswith(opstr) and not c.split(opstr)[1].startswith('=')  # NOQA

        def _getval(c, opstr):
            """ Helper to get the value on the RHS of the constraint - only
                called when (opstr in c) is True
                Parameters:
                    c (str): constraint containing operation e.g. '<3', '>=0'
                    opstr (str): operation we're pulling out e.g. '<', '>='
                Returns:
                    (float)
                Example:
                    >>> assert(_getval('<3', '<') == 3)
                    >>> assert(_getval('>=3', '>=') == 3)
                    >>> assert(_getval('==3', '==') == 3)
            """
            return float(c.split(opstr)[1])

        # No constraint
        if c is None:
            return True

        # Constrained by type
        elif type(c) == type or c == collections.Iterable:
            return isinstance(item, c)

        # Item should be a number and constrained by some operation
        elif isinstance(c, str):
            numeric = any([c.startswith(opstr) for opstr in operations.keys()])
            if numeric:
                try:
                    item = float(item)
                except (ValueError, TypeError):
                    return False
                else:
                    correct_or_dontcare = [op(item, _getval(c, opstr))        # NOQA Check operation
                                           if _isop(c, opstr)                 # NOQA Only if operation is constraint
                                           else True                          # NOQA OTW, don't care
                                           for opstr, op in operations.items()]  # NOQA For all operations given
                    return all(correct_or_dontcare)
            else:
                return item == c

        # If constraint is, for instance, a lambda function verifying that a
        # parameter is either None or satisfies some other constraint
        # e.g. (lambda x: x is None or isinstance(x, str))
        elif isinstance(c, type(lambda x: x)):
            if VERBOSITY > 0:
                print('param {}\n  {}({}) evaluates to {}'.format(
                    item_name,
                    c.__name__,
                    item,
                    c(item) if c is not None else 'N/A'))
            return c(item)

        else:
            raise NotImplementedError

    # First get the actual constraint(s)
    constraint = constraints.get(param_name)

    # If multiple constraints, check all (or any) of them
    if isiterable(constraint):
        if check_all:
            return all([_check_constraint(param_value, c, param_name) for c in constraint])  # NOQA
        else:
            return any([_check_constraint(param_value, c, param_name) for c in constraint])  # NOQA

    else:
        return _check_constraint(param_value, constraint, param_name)


class ParameterRegister(collections.OrderedDict):
    def __init__(self, constraints=None, defaults=None, accept_none=False, match_all_constraints=True):
        super().__init__()
        self.constraints = constraints
        self.defaults = defaults
        self.accept_none = accept_none
        self.match_all_constraints = match_all_constraints

    def register(self, kwarg_name, constraints=None, default=None):
        self.constraints[kwarg_name] = constraints
        self.defaults[kwarg_name] = default

    def check_kwargs(self, **kwargs):
        if self.accept_none:
            valid = {k: check_constraints(v, k, self.constraints, check_all=self.match_all_constraints) or v is None for k, v in kwargs.items()}  # NOQA
        else:
            valid = {k: check_constraints(v, k, self.constraints, check_all=not self.self.match_all_constraints) for k, v in kwargs.items()}  # NOQA
        return valid

    def set_uninitialized_params(self, defaults=None):
        if defaults is not None:
            defaults_notset = {key: defaults[key]
                               for key in defaults
                               if self.get(key) is None}
        elif self.defaults is not None:
            defaults_notset = {key: self.defaults[key]
                               for key in self.defaults
                               if self.get(key) is None}
        else:
            print('No defaults dictionary given - cannot set')

        self.update(**defaults_notset)

    def _err_fmt(self, key, kwarg_dict):
        return '{} expects {} but got {}'.format(key, self.constraints[key], kwarg_dict[key])  # NOQA

    def set(self, **kwargs):
        no_check = kwargs.get('no_check')
        if not no_check:
            is_good = self.check_kwargs(**kwargs)
            if not all(is_good.values()):
                bad_kwargs = ', '.join([self._err_fmt(kwarg, kwargs) for kwarg, good in is_good.items() if not good])  # NOQA
                raise ValueError(bad_kwargs)

        for k, v in kwargs.items():
            self[k] = v

    @property
    def hashable_str(self):
        return ','.join(['{}:{}'.format(k, v) for k, v in self.items()])

    @property
    def _pretty(self):
        s = self.__class__.__name__
        for k, v in self.items():
            s += '\n  {}: {}'.format(k, v.__repr__())
        s += '\nConstraints'
        for k, v in self.constraints.items():
            s += '\n  {}: {}'.format(k, v)
        s += '\nDefaults'
        for k, v in self.defaults.items():
            s += '\n  {}: {}'.format(k, v.__repr__())
        s += '\n'
        return s

    def __repr__(self):
        return self._pretty


if __name__ == "__main__":
    import doctest
    doctest.testmod()
