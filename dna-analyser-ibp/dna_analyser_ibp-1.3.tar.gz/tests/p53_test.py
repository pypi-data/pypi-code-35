import time

import pandas as pd
import pytest

from DNA_analyser_IBP.callers.sequence_caller import SequenceModel
from DNA_analyser_IBP.callers.user_caller import User
from DNA_analyser_IBP.callers.p53_caller import (
    P53Analyse as P53,
    P53AnalyseFactory,
    p53_delete_analyse,
    p53_load_by_id,
    p53_load_all,
)

from . import vcr_instance


@pytest.fixture(scope="module")
@vcr_instance.use_cassette
def user():
    return User(
        email="user@mendelu.cz", password="user", server="http://localhost:8080/api"
    )


@pytest.fixture(scope="module")
def sequence():
    return SequenceModel(
        id="987acc67-5714-47b1-b56f-1dc56ded7c87",
        name="n",
        created="c",
        type="t",
        circular="cr",
        length=100,
        ncbi="NCB",
        tags=["ss"],
        fastaComment=None,
        nucleicCounts=None,
    )


@pytest.fixture(scope="module")
def p53():
    return P53(
        id="some_id",
        created="start_date",
        tags=["tag1", "tag2"],
        finished="end_date",
        title="some_title",
        sequenceId="some_sequence_id",
        resultCount=128,
        threshold=1.5,
    )


@vcr_instance.use_cassette
def test_p53_creation_and_retrieving_data_frame(p53):
    """It should create p53 object + test pandas dataframe creation."""

    assert isinstance(p53, P53)
    data_frame = p53.get_dataframe()

    assert isinstance(data_frame, pd.DataFrame)
    assert data_frame["id"][0] is "some_id"
    assert data_frame["sequence_id"][0] is "some_sequence_id"


"""
@vcr_instance.use_cassette
def test_p53_creation_and_deleting(user, sequence):
    #It should create p53 analyse + deletes it.

    factory = P53AnalyseFactory(
        user=user, id=sequence.id, tags=["test", "sequence"], threshold=20
    )

    analyse = factory.analyse
    assert isinstance(analyse, P53)
    assert analyse.title == "Escherichia coli str. K-12 substr. MG1655"

    time.sleep(2)

    res = p53_delete_analyse(user=user, id=analyse.id)
    assert res is True
"""


@vcr_instance.use_cassette
def test_p53_fail_delete(user, p53):
    """It should test deleting non existing analyse."""

    res = p53_delete_analyse(user=user, id=p53.id)
    assert res is False


"""
@vcr_instance.use_cassette
def test_load_all_and_load_by_id_p53s(user, sequence):
    #It should test retrieving list with all p53 analyses

    P53AnalyseFactory(
        user=user, id=sequence.id, tags=["test", "sequence"], threshold=20
    )

    time.sleep(2)

    p53_lst = [p53 for p53 in p53_load_all(user=user, filter_tag=[])]
    assert len(p53_lst) == 1

    p53_by_id = p53_load_by_id(user, id=p53_lst[0].id)

    assert p53_lst[0].id == p53_by_id.id

    res = p53_delete_analyse(user=user, id=p53_lst[0].id)
    assert res is True
"""
