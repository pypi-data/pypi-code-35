from typing import Callable, Union


class DimensionProperty:
    """Property of an entity dimension comparison, e.g. duck (entity),
    beaks (dimension), are_rounded (property)"""

    def __init__(
            self, description: str = None,
            resolver: Union[Callable, str] = None):
        """
        :param description: description of the property
        :param resolver: name of the class method implementing the logic that
        computes the value of the property. If no resolver defined, the name is
        resolve_<property_field_name>
        """
        self.description = description
        self.resolver = resolver
