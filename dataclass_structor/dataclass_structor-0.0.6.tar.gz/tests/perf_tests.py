import datetime
import decimal
import typing

import perf  # pylint: disable=import-error

from dataclass_structor import structure, unstructure
from ._fixtures import AnimalEnum, DataClassGuest, SoundsEnum


def unstructure_assorted_primatives():
    unstructure("Potato")
    unstructure(1)
    unstructure(1.0)
    unstructure(True)


def structure_assorted_primatives():
    structure("Tomato", str)
    structure(1, int)
    structure(1.0, float)


def unstructure_assorted_simple_types():
    unstructure(decimal.Decimal(1.0))
    unstructure(datetime.datetime(2018, 2, 1, 2, 2, 2))
    unstructure(datetime.date(2018, 8, 28))


def structure_assorted_simple_types():
    structure("Tomato", str)
    structure(1, int)
    structure(1.0, float)


def unstructure_enums():
    unstructure(AnimalEnum.ANT)
    unstructure(SoundsEnum.CAT)


def structure_enums():
    structure("BEE", AnimalEnum)
    structure("DOG", SoundsEnum)


def structure_unions():
    structure("Potato", typing.Union[int, str])
    structure(1, typing.Union[int, str])
    structure(None, typing.Optional[str])
    structure("Potato", typing.Optional[str])


def unstructure_dataclass():
    unstructure(DataClassGuest(first_name="Bobby Jim"))


def structure_dataclass():
    structure({"first_name": "Bobby Jim"}, DataClassGuest)


RUNNER = perf.Runner(processes=5)
BENCHMARK_FNS = [
    unstructure_assorted_primatives,
    structure_assorted_primatives,
    unstructure_assorted_simple_types,
    structure_assorted_simple_types,
    unstructure_enums,
    structure_enums,
    structure_unions,
    unstructure_dataclass,
    structure_dataclass,
]

for fn in BENCHMARK_FNS:
    RUNNER.bench_func(fn.__name__, fn)
