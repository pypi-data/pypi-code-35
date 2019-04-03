from typing import get_type_hints

from .fields.field import field, Field


class TypeHintDescriptor:
    def __init__(self):
        self.type_hints = None

    def __get__(self, _, cls):
        if not self.type_hints:
            self.type_hints = get_type_hints(cls)

        return self.type_hints


class Section:
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls._type_hints = TypeHintDescriptor()

    def __init__(self, _=None, **kwargs):
        if _:
            self.__dirty = False
            return
        else:
            self.__dirty = True

        for field_name, type in self._type_hints.items():
            if field_name in kwargs:
                setattr(self, field_name, kwargs[field_name])
            else:
                setattr(self, field_name, self.__default(field_name, field(type)))

    def __str__(self):
        return self.serialize()

    def __repr__(self):
        def repr_(field):
            from .model import Model
            value = getattr(self, field)
            if isinstance(value, Model):
                return f'{type(value).__name__}(key={value.key!r}, version={value.version!r})'
            else:
                return repr(value)

        return f'{type(self).__name__}(' + \
            ', '.join(f'{field}={repr_(field)}' for field in self._type_hints) + \
            ')'

    def __eq__(self, other):
        if type(self) == type(other):
            return all(getattr(self, field) == getattr(other, field) for field in self._type_hints)
        else:
            return False

    def __setattr__(self, name, value):
        if name in self._type_hints:
            self.__dirty = True

        super().__setattr__(name, value)

    def __default(self, field_name, field):
        if hasattr(type(self), field_name):
            default = getattr(type(self), field_name)
        elif hasattr(field, 'default'):
            default = field.default
        else:
            raise ValueError(f'Missing value for {field_name}')

        return default() if callable(default) else default

    @property
    def dirty(self):
        from .model import Model
        return self.__dirty or \
               any(getattr(self, key).dirty
                   for key, field in self._type_hints.items()
                   if isinstance(field, type) and
                   issubclass(field, Section) and
                   not issubclass(field, Model))

    @dirty.setter
    def dirty(self, value):
        from .model import Model
        self.__dirty = value
        for key, field in self._type_hints.items():
            if isinstance(field, type) and \
               issubclass(field, Section) and \
               not issubclass(field, Model):
                setattr(getattr(self, key), 'dirty', value)

    def serialize(self, **kwargs):
        def map_to_value(field_name, field, value):
            if hasattr(type(self), field_name) and getattr(type(self), field_name) == value:
                return None
            else:
                try:
                    value = field.serialize(value)
                    return None if value in [[], {}] else value
                except ValueError:
                    raise ValueError(f'Missing value for {field_name}')

        data = {key: map_to_value(key, field(model, **kwargs), getattr(self, key))
                for key, model in self._type_hints.items()}
        data = {key: value for key, value in data.items() if value is not None}
        return data if data else None

    def deserialize(self, data, **kwargs):
        def map_to_model(field_name, field, value):
            try:
                return field.deserialize(value)
            except ValueError:
                return self.__default(field_name, field)

        for key, model in self._type_hints.items():
            value = map_to_model(key, field(model, **kwargs), data.get(key))
            setattr(self, key, value)


class SectionField(Field):
    type = Section

    def is_serialsized(self, value):
        return isinstance(value, dict)

    def is_deserialized(self, value):
        return isinstance(value, self.type)

    def _serialize(self, value):
        return value.serialize(**self.context)

    def _deserialize(self, value):
        instance = self.concrete_type(value)
        instance.deserialize(value, **self.context)
        return instance
