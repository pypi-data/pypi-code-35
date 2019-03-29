# -*- coding: utf-8 -*-

import abc
import json
import typing as T
from functools import partial
from inspect import signature

from .registry import decoders
from .registry import encoders
from .registry import import_object


class DictConvertible(abc.ABC):
    """
    This abstract class implements the :meth:`to_dict` and :meth:`from_dict`.
    Every class implementing those two methods will be a subclass of
    :class:`DictConvertible`. It is not necessary to inherit from this class.

    """
    @abc.abstractmethod
    def to_dict(self):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, data_dict: dict):
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, other_cls: type):
        is_dict_convertible = (hasattr(other_cls, 'to_dict') and
                               hasattr(other_cls, 'from_dict'))
        return is_dict_convertible


class StrConvertible(abc.ABC):
    """
    This abstract class implements the :meth:`to_str` and :meth:`from_str`.
    Every class implementing those two methods will be a subclass of
    :class:`StrConvertible`. It is not necessary to inherit from this class.

    """
    @abc.abstractmethod
    def to_str(self):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_str(cls, json_str: str):
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, other_cls: type):
        is_str_convertible = (hasattr(other_cls, 'to_str') and
                              hasattr(other_cls, 'from_str'))
        return is_str_convertible


class JsonerSerializable(abc.ABC):
    """
    The :class:`JsonerSerializable` serves as an abstract class
    which indicated if an instance can be serialized by *Jsoner*.
    Therefore it implements the :meth:`__subclasshook__` method.

    An object is serializable by *Jsoner* if it is registered
    in the encoding-, decoding-registry or if it is convertible to a dict or
    to a string.
    """
    @classmethod
    def __subclasshook__(cls, other_cls: type):
        try:
            is_serializable = other_cls in decoders and other_cls in encoders
        except TypeError:
            return False

        if not is_serializable:
            is_serializable |= (issubclass(other_cls, StrConvertible) or
                                issubclass(other_cls, DictConvertible))

        return is_serializable


def _is_instance_of_type(obj_or_type: T.Union[object, type]) -> bool:
    """
    If the argument of this function is an instance of :class:`type`,
    the function returns true.

    .. note::
        If the argument is a class which is defined in a local
        namespace, the function return false as well.
    :param obj_or_type:
    :return:
    """
    is_a_cls = isinstance(obj_or_type, type)
    is_a_cls &= '<locals>' not in obj_spec(obj_or_type)

    return is_a_cls


def obj_spec(obj_or_type: T.Union[object, type]) -> str:
    """
    This function returns the path of the argument class.

    If the argument is an instance of :class:`type`, it returns the
    path of the argument itself.

    Usage::
        >>> from jsoner.serialization import obj_spec
        >>> class A:
        ...     pass

        >>> obj_spec(A)  # doctest: +ELLIPSIS
        '...A'

        >>> a = A()
        >>> obj_spec(a)  # doctest: +ELLIPSIS
        '...A'

    :param obj_or_type:
    :return:
    """
    if isinstance(obj_or_type, type):
        path = obj_or_type.__module__ + '.' + obj_or_type.__qualname__
    else:
        path = obj_or_type.__class__.__module__ + '.' + obj_or_type.__class__.__qualname__
    return path


class JsonEncoder(json.JSONEncoder):
    """
    JsonEncoder will decode all objects, which implement either `to_dict`
    and `from_dict` or `to_str` and `from_str`.

    .. note::
        :meth:`from_str` and :meth:`from_dict` must be a
        ``classmethod``. It is enough to implement either
        :meth:`from_str` and :meth:`to_str` or
        :meth:`from_dict` and :meth:`to_dict`. If both are implemented, then
        :meth:`from_dict` and :meth:`to_dict` are preferred.

    If you do not want to implement methods in your class, or you might have
    no access to the class definition, you can use
    :func:`jsoner.registry.encoders` and :func:`jsoner.registry.decoders`.

    """
    def default(self, obj, *args, **kwargs):

        if isinstance(obj, JsonerSerializable):
            obj_dict = {
                '__obj_cls__': obj_spec(obj),
                '__json_data__': None
            }
            if isinstance(obj, DictConvertible):
                obj_data = obj.to_dict()
            elif isinstance(obj, StrConvertible):
                obj_data = obj.to_str()
            else:
                encoder = encoders.get(obj)
                if isinstance(encoder, T.Callable):
                    obj_data = encoder(obj)
                else:
                    obj_data = encoder
            obj_dict['__json_data__'] = obj_data
            return obj_dict

        elif _is_instance_of_type(obj):
            return {'__cls__': obj_spec(obj)}

        else:
            return super().default(obj)


def json_hook(primitive: T.Any) -> T.Any:
    """
    This hook will try to recreate an object from the data it receives. It
    it fails to do so, it will just return the original data.

    :param primitive:
    :return:
    """
    if not isinstance(primitive, T.Dict):
        return primitive
    else:
        return maybe_convert_to_obj(primitive)


def maybe_convert_to_obj(data: dict) -> T.Any:
    """
    This function will try to create an object from the data dictionary.

    :param data:
    :return:
    """
    if '__cls__' in data:
        _cls = data.get('__cls__', '')

        try:
            return import_object(_cls)
        except ImportError:
            return data

    elif '__obj_cls__' in data:
        _cls = data.get('__obj_cls__', '')
        try:
            cls = import_object(_cls)
        except ImportError:
            return data

        obj_data = data.get('__json_data__')

        if issubclass(cls, DictConvertible):
            return cls.from_dict(obj_data)
        elif issubclass(cls, StrConvertible):
            return cls.from_str(obj_data)
        else:
            decoder = decoders.get(cls)
            if decoder is None:
                return data
            if callable(decoder):
                sig = signature(decoder)
                if len(sig.parameters) == 1:
                    return decoder(obj_data)
                else:
                    return decoder(obj_data, cls)
            else:
                return decoder or data
    else:
        return data


dump = partial(json.dump, cls=JsonEncoder)
dumps = partial(json.dumps, cls=JsonEncoder)
load = partial(json.load, object_hook=json_hook)
loads = partial(json.loads, object_hook=json_hook)
