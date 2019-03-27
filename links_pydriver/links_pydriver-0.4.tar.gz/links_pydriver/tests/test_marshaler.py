from links_pydriver.model.Experiment import Experiment
from links_pydriver.model.Relation import Relation
from links_pydriver.model.Snapshot import Snapshot
from links_pydriver.model.Entity import Entity
from links_pydriver.marshaler.DriverMarshaler import marshalling

from bson.objectid import ObjectId
import mongomock
import json
import os

TEST_FOLDER = os.path.join('links_pydriver', 'tests')


def __process(obj):
    """
    Processing before comparing object
    Remove $oid, $numberInt and sort dictionary
    """
    if isinstance(obj, dict):
        if list(obj.keys()) == ['$oid']:
            return 'OBJECT_ID'
        if list(obj.keys()) == ['$numberInt']:
            return int(obj['$numberInt'])
        return sorted((k, __process(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(__process(x) for x in obj)
    if isinstance(obj, ObjectId):
        return 'OBJECT_ID'
    else:
        return obj


def __create_experiment():
    # Creating entities
    e1 = Entity("Agent 1", "Type A", {'name': 'A'})
    e2 = Entity("Agent 2", "Type B", {'name': 'B'})
    e3 = Entity("Agent 3", "Type C", {})

    # Creating relations
    r1 = Relation('relation1', 'Agent 1', 'Agent 2', True, 'Relation1')
    r2 = Relation('relation2', 'Agent 3', 'Agent 1', False, 'Relation2')

    # Creating snapshot
    s1 = Snapshot(0, [e1], [], {'Encountered exception': 'Unhandled NCS !'})
    s2 = Snapshot(1, [e1, e2, e3], [r1, r2], {})
    s3 = Snapshot(2, [], [], {})

    # Creating experiment
    exp = Experiment('exp_ref', {'Description': 'Example links data structure'}, [s1, s2, s3])

    return exp


def test_marshaler():
    # Create an experiment and fill a mocked database
    db = mongomock.MongoClient().db['links']
    exp = __create_experiment()
    marshalling(db, exp)

    # Get the data from mocked database
    data_test = list(db['exp_ref'].find())

    # Get reference data
    filename = "data/ref.json"
    with open(os.path.join(TEST_FOLDER, filename), 'r') as f:
        data_ref = json.load(f)

    # Comparison
    assert __process(data_test) == __process(data_ref)
