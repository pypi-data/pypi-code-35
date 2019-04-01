from .field import field, Field


class VectorField(Field):
    types = set, frozenset, tuple, list

    def __init__(self, field):
        super().__init__(field)

        if len(field.__args__) != 1:
            raise TypeError('Vector fields must specify element type')

    @property
    def default(self):
        return self.type

    def _serialize(self, value):
        field_ = field(self.concrete_type.__args__[0], **self.context)
        return [field_.serialize(value) for value in value]

    def _deserialize(self, value):
        field_ = field(self.concrete_type.__args__[0], **self.context)
        return self.type(field_.deserialize(value) for value in value)


class MapField(Field):
    type = dict
    default = dict

    def __init__(self, field):
        super().__init__(field)

        if len(field.__args__) != 2:
            raise TypeError('Map fields must specify key and element type')

    def _serialize(self, value):
        key_field = field(self.concrete_type.__args__[0], **self.context)
        value_field = field(self.concrete_type.__args__[1], **self.context)
        return {key_field.deserialize(key): value_field.serialize(value) for key, value in value.items()}

    def _deserialize(self, value):
        key_field = field(self.concrete_type.__args__[0], **self.context)
        value_field = field(self.concrete_type.__args__[1], **self.context)
        return {key_field.deserialize(key): value_field.deserialize(value) for key, value in value.items()}
