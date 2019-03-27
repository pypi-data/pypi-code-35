import enum
import dataclasses
import typing


class AnimalEnum(enum.Enum):
    """An enum to test int enums"""

    ANT = 1
    BEE = 2
    CAT = 3
    DOG = 4


class SoundsEnum(enum.Enum):
    """An enum to test string enums"""

    CAT = "meow"
    DOG = "dog"


@dataclasses.dataclass
class DataClassGuest:
    first_name: typing.Optional[str] = None


class SlottedGuest:
    __slots__ = ("first_name",)

    def __init__(self, first_name: typing.Optional[str] = None):
        self.first_name = first_name

    def __repr__(self):
        return f"Guest(first_name={repr(self.first_name)})"

    def __eq__(self, other):
        return self.first_name == other.first_name
