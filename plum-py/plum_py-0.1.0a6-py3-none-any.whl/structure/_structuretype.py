# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Structure type metaclass."""

import operator

from .._plum import Plum
from .._plumtype import PlumType
from ._member import Member

try:
    import plum_c._fastsequence as fastsequence
except ImportError:
    fastsequence = None


class MemberInfo:

    def __init__(self, namespace):

        self.nbytes = 0
        self.names = []
        self.types = []
        self.defaults = []
        self.ignores = []
        self.touchups = []
        self.members = {}

        for name, cls in namespace.get('__annotations__', {}).items():
            try:
                self.nbytes += cls._nbytes
            except TypeError:
                # one or the other is None, set overall size as "varies"
                self.nbytes = None
            except AttributeError:
                raise TypeError(f'Structure member {name!r} must be a Plum subclass')

            try:
                # retrieve default or member definition after the type annotation
                member = namespace[name]
            except KeyError:
                # no default and no member definition present, create a member definition
                # and place it within the new class namespace to facilitate attribute
                # get/set capability
                member = Member()
                namespace[name] = member
            else:
                # if it's a default value, create a member definition with it and
                # overwrite the default in the new class namespace with the
                # member definition to facilitate attribute get/set capability
                if not isinstance(member, Member):
                    member = Member(default=member)
                    namespace[name] = member

            member.finalize(name, cls, self.members)

            self.members[name] = member
            self.names.append(name)
            self.types.append(member.cls)
            self.defaults.append(member.default)
            self.ignores.append(member.ignore)
            self.touchups.append(hasattr(member.cls, '__touchup__'))

        self.nbytes = self.nbytes if self.nbytes else None
        self.nitems = len(self.types)

    @property
    def parameters(self):
        parameters = []

        force_default = False

        for name, default, has_touchup in zip(self.names, self.defaults, self.touchups):
            if force_default or has_touchup or default is not None:
                force_default = True
                parameters.append(f'{name}=None')
            else:
                parameters.append(name)

        return ', '.join(parameters)

    def make_init(self):
        lines = [
            f'def __init__(self, {self.parameters}):',
            f'self.extend(({", ".join(self.names)}))'
            ]

        if True in self.touchups:
            lines.append('types = self.__plum_internals__[1]')

            for i, touchup_present in enumerate(self.touchups):
                if touchup_present:
                    lines.append(f'self[{i}] = types[{i}].__touchup__(self[{i}], self)')

        default_present = False

        for i, (name, default, cls) in enumerate(zip(self.names, self.defaults, self.types)):

            if default_present or (default is not None):
                default_present = True

                if default is None:
                    if not hasattr(cls, '__touchup__'):
                        lines.extend([
                            f'if {name} is None:',
                            f'    raise TypeError("__init__() missing required argument {name!r}")',
                            '',
                        ])
                else:
                    lines.extend([
                        f'if {name} is None:',
                        f'    self[{i}] = {default!r}',  # TODO - support defaults where repr isn't equiv
                        '',
                    ])

        return '\n    '.join(lines)

    def make_compare(self, name):
        indices = [i for i, ignore in enumerate(self.ignores) if not ignore]

        compare = EXAMPLE_COMPARE.replace('__eq__', name)

        unpack_expression = ', '.join(
            f's{i}' if i in indices else '_' for i in range(self.nitems))

        compare = compare.replace('s0, _, s2, _', unpack_expression)
        compare = compare.replace('o0, _, o2, _', unpack_expression.replace('s', 'o'))

        if name == '__eq__':
            return_logic = ' and '.join(f'(s{i} == o{i})' for i in indices)
        else:
            return_logic = ' or '.join(f'(s{i} != o{i})' for i in indices)

        return compare.replace('(s0 == o0) and (s2 == o2)', return_logic)


# example for 4 items where 2nd and last items are ignored
EXAMPLE_COMPARE = """
def __eq__(self, other):
    if type(other) is type(self):
        s0, _, s2, _ = self
        o0, _, o2, _ = other
        return (s0 == o0) and (s2 == o2)
    else:    
        return list.__eq__(self, other)
    """.strip()


def asdict_defined(self):
    names, _types, _has_touchups = self.__plum_internals__
    return {k: v for k, v in zip(names, self)}


def asdict_anonymous(self):
    names = self.__plum_names__
    return {k: v for k, v in zip(names, self) if k is not None}


def __pack_defined__(cls, memory, offset, item, dump):
    names, types, has_touchups = cls.__plum_internals__

    if isinstance(item, (list, tuple)):
        if (has_touchups and type(item) is not cls) or (len(item) != len(types)):
            # need actions performed during __init__ when __touchup__ present,
            # raise an exception via __init__ when len mismatch
            item = cls(*item)
    elif isinstance(item, dict):
        item = cls(**item)
    else:
        raise TypeError(f'{cls.__name__} must be a list, tuple, or dict')

    if dump:
        dump.cls = cls

        for i, (name, value_cls, value) in enumerate(zip(names, types, item)):
            subdump = dump.add_level(access=f'[{i}] (.{name})')
            offset = value_cls.__pack__(memory, offset, value, subdump)
    else:
        for value_cls, value in zip(types, item):
            offset = value_cls.__pack__(memory, offset, value, None)


def __pack_anonymous__(cls, memory, offset, item, dump):
    if dump:
        dump.cls = cls

        if type(item) is cls:
            try:
                names = item.__plum_names__
            except AttributeError:
                names = tuple()
        elif isinstance(item, dict):
            names = item.keys()
            item = item.values()
        elif isinstance(item, (list, tuple)):
            names = [None] * len(item)
        else:
            raise TypeError(f'{cls.__name__} must be a list, tuple, or dict')

        for i, (name, value) in enumerate(zip(names, item)):
            if name:
                subdump = dump.add_level(access=f'[{i}] (.{name})')
            else:
                subdump = dump.add_level(access=f'[{i}]')

            value_cls = type(value)
            if not issubclass(value_cls, Plum):
                desc = f' ({name})' if name else ''
                raise TypeError(
                    f'item {i}{desc} in anonymous structure not a plum type '
                    f'instance: {value!r}')

            offset = value_cls.__pack__(memory, offset, value, subdump)
    else:
        if isinstance(item, dict):
            item = item.values()
        elif not isinstance(item, (list, tuple)):
            raise TypeError(f'{cls.__name__} must be a list, tuple, or dict')

        for value in item:
            value_cls = type(value)
            if not issubclass(value_cls, Plum):
                raise TypeError('item in anonymous structure not a plum type instance')

            offset = value_cls.__pack__(memory, offset, value, None)


def __getattr_anonymous__(self, name):
    # only for anonymous structures
    try:
        index = object.__getattribute__(self, '__plum_names__').index(name)
    except (AttributeError, ValueError):
        # AttributeError -> structure instantiated without names
        # ValueError -> name not one used during structure instantiation

        # for consistent error message, let standard mechanism raise the exception
        object.__getattribute__(self, name)
        raise RuntimeError('should never reach this line')
    else:
        return self[index]


def __setattr_anonymous__(self, name, value):
    try:
        index = self.__plum_names__.index(name)
    except ValueError:
        # AttributeError -> unpacking Structure and never instantiated
        # ValueError -> name not one used during structure instantiation
        raise AttributeError(
            f"{type(self).__name__!r} object has no attribute {name!r}")
    else:
        self[index] = value


def __setattr_defined__(self, name, value):
    # get the attribute to raise an exception if invalid name
    getattr(self, name)
    object.__setattr__(self, name, value)


class StructureType(PlumType):

    """Structure type metaclass.

    Create custom |Structure| subclass. For example:

        >>> from plum.structure import Structure
        >>> from plum.int.little import UInt16, UInt8
        >>> class MyStruct(Structure):
        ...     m0: UInt16
        ...     m1: UInt8
        ...
        >>>

    """

    def __new__(mcs, name, bases, namespace):
        member_info = MemberInfo(namespace)

        nbytes = member_info.nbytes

        names = tuple(member_info.names)  # convert to tuple
        types = tuple(member_info.types)  # convert to tuple
        has_touchups = True in member_info.touchups

        if member_info.members:
            # create custom __init__ within class namespace
            exec(member_info.make_init(), globals(), namespace)

            if True in member_info.ignores:
                # create custom __eq__ and __ne__ within class namespace
                exec(member_info.make_compare('__eq__'), globals(), namespace)
                exec(member_info.make_compare('__ne__'), globals(), namespace)

            # create member accessors
            for i, member_name in enumerate(member_info.names):
                def setitem(self, value, i=i):
                    self[i] = value
                namespace[member_name] = property(operator.itemgetter(i)).setter(setitem)

            namespace.update({
                'asdict': asdict_defined,
                '__pack__': classmethod(__pack_defined__),
                '__plum_names__': names,
                '__setattr__': __setattr_defined__,
            })
        else:
            namespace.update({
                'asdict': asdict_anonymous,
                '__getattr__': __getattr_anonymous__,
                '__pack__': classmethod(__pack_anonymous__),
                '__setattr__': __setattr_anonymous__,
            })

        namespace.update({
            '_nbytes': nbytes,
            '__plum_internals__': (names, types, has_touchups),
        })

        cls = super().__new__(mcs, name, bases, namespace)

        if fastsequence and types:
            # attach binary string containing plum-c accelerator "C" structure
            # (so structure memory de-allocated when class deleted)
            cls.__plum_c_internals__ = fastsequence.add_c_acceleration(
                cls,  -1 if nbytes is None else nbytes, len(types), types)

        return cls
