from dataclass_structor import structure, unstructure
from ._fixtures import AnimalEnum as Animal, SoundsEnum as Sounds


def test_unstructure__animal():
    assert unstructure(Animal.ANT) == "ANT"


def test_structure__animal():
    assert structure("BEE", Animal) == Animal.BEE


def test_unstructure__sounds():
    assert unstructure(Sounds.CAT) == "CAT"


def test_structure__sounds():
    assert structure("DOG", Sounds) == Sounds.DOG
