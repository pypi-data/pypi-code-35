from typing import Set
from dataclass_structor import structure, unstructure


def test_unstructure__set():
    assert unstructure(set([])) == set([])
    assert unstructure(set(["x"])) == set(["x"])
    assert unstructure(set([1])) == set([1])
    assert unstructure(set([2, "y"])) == set([2, "y"])


def test_structure__homogeneous_set():
    assert structure([], Set[int]) == set([])
    assert structure(["1"], Set[int]) == set([1])
    assert structure(["1"], Set[str]) == set(["1"])


def test_structure__hetrogeneous_set():
    assert structure(["1", 2], Set[int]) == set([1, 2])
    assert structure(["1", 2], Set[str]) == set(["1", "2"])
    assert structure(["1", 2], Set[str]) == set(["1", "2"])
