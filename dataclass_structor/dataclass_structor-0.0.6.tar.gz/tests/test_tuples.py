from typing import Tuple
from dataclass_structor import structure, unstructure


def test_unstructure__tuple():
    assert unstructure(tuple([])) == tuple([])
    assert unstructure(tuple(["x"])) == tuple(["x"])
    assert unstructure(tuple([1])) == tuple([1])


def test_structure__tuple__size_zero():
    assert structure([], Tuple) == tuple([])


def test_structure__tuple__size_one():
    assert structure([1], Tuple[int]) == tuple([1])
    assert structure(["x"], Tuple[str]) == tuple(["x"])
    assert structure(["1"], Tuple[int]) == tuple([1])


def test_structure__tuple__size_two_or_more():
    assert structure(["1", "x", 2], Tuple[int, str, int]) == tuple([1, "x", 2])
