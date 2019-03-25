from links_pydriver.connection import db_utils
from links_pydriver.model.Experiment import Experiment
from links_pydriver.model.Relation import Relation
from links_pydriver.model.Snapshot import Snapshot
from links_pydriver.model.Entity import Entity
from links_pydriver.marshaler.DriverMarshaler import marshalling


def create_experience():
    name = "exp_example"
    attribute_map = {'Description': 'Example links data structure',
                     'Configuration': {'confName': 'MyConf1',
                                       'confProfile': 'DEBUG'},
                     'Version': '0.1'}

    exp = Experiment(name, attribute_map, None)
    return exp


def create_entities():
    e1 = Entity("Agent 1", "Ant", {'role': 'Furrowmaker', 'name': 'Maholise', 'health': 30})
    e2 = Entity("Agent 2", "Ant", {'role': 'Furrowmaker', 'name': 'Tuoi', 'health': 90})
    e3 = Entity("Agent 3", "Ant", {'role': 'Sheperdess', 'name': 'Loumwe', 'health': 50})
    e4 = Entity("Agent 4", "Ant", {'role': 'Warrior', 'name': 'Ereat', 'health': 15})
    e5 = Entity("Agent 5", "Termite", {'role': 'Warrior', 'name': 'Yherzok', 'health': 2})
    l_entities = [e1, e2, e3, e4, e5]

    return l_entities


def create_relations():
    r1 = Relation('helping1', 'Agent 2', 'Agent 1', True, 'Help')
    r2 = Relation('helping1', 'Agent 3', 'Agent 1', True, 'Help')
    r3 = Relation('fight1', 'Agent 4', 'Agent 5', False, 'Fight')
    l_relations = [r1, r2, r3]

    return l_relations


if __name__ == '__main__':
    db = db_utils.connect()
    exp = create_experience()
    list_entities = create_entities()
    list_relations = create_relations()

    s1 = Snapshot(0, list_entities[:4], list_relations[:2], {'Encontred exception': 'Unhandle NCS !'})
    s2 = Snapshot(1, list_entities, list_relations, {'Encontred exception': 'Unhandle NCS !'})

    list_snapshots = [s1, s2]

    exp.snapshots = list_snapshots

    marshalling(db, exp)