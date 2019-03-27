from attr import attrs, attrib


@attrs(repr=False, slots=True, hash=True)
class list_items_are_instances_of(object):
    """
    Checks if items of a list are the right value ...
    """
    type = attrib()

    def __call__(self, inst, attr, value):
        """
        We use a callable class to be able to change the ``__repr__``.
        """
        for item in value:
            self.check_if_item_is_instance(attr, item)

    def check_if_item_is_instance(self, attr, value):
        if not isinstance(value, self.type):
            raise TypeError(
                "All instances of '{name}' must be {type!r} (got {value!r} that is a "
                "{actual!r}).".format(
                    name=attr.name,
                    type=self.type,
                    actual=value.__class__,
                    value=value,
                ),
                attr,
                self.type,
                value,
            )

    def __repr__(self):
        return "<instance_of validator for type {type!r}>".format(
            type=self.type
        )
