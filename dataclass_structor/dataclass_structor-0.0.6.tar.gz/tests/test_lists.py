from typing import List
from dataclass_structor import structure, unstructure


def test_unstructure__list():
    assert unstructure([]) == []
    assert unstructure(["x"]) == ["x"]
    assert unstructure([1]) == [1]
    assert unstructure([2, "y"]) == [2, "y"]


def test_structure__homogeneous_list():
    assert structure([], List[int]) == []
    assert structure(["1"], List[int]) == [1]
    assert structure(["1"], List[str]) == ["1"]


def test_structure__hetrogeneous_list():
    assert structure(["1", 2], List[int]) == [1, 2]
    assert structure(["1", 2], List[str]) == ["1", "2"]
    assert structure(["1", 2], List[str]) == ["1", "2"]
