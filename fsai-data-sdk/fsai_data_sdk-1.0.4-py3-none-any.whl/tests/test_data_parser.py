# coding: utf-8
import json
from fsai.services.data_object.DynamicObjectData import DynamicObjectData
from fsai.services.data_object.Semantic2DData import semantic_2d_data_from_dict, semantic_2d_data_to_dict

def test_dynamic_object_parse_data_ok():
    with open('./data/trajectories.json') as json_file:
        json_file = json.load(json_file)
        dynamic_object_data = DynamicObjectData.from_json(json_file)
        print('\n')
        sample_object = dynamic_object_data.collections[0].objects[0]
        print(sample_object.get_moving_distance())
        assert sample_object.get_moving_distance() == 4.242640687119286
        assert sample_object.states[0].acceleration.x == -4.656612873077392578e-08
        assert sample_object.states[0].acceleration.y == -9.313225746154785156e-08
        assert sample_object.states[0].acceleration.z == 4.656612873077392578e-08

        assert sample_object.states[0].velocity.x == -12.38638929091393948
        assert sample_object.states[0].velocity.y == 5.039367619901895523
        assert sample_object.states[0].velocity.z == -2.845609406940639019
        assert sample_object.states[0].shape == 'cuboid'


def test_semantic_2d_parse_data_ok():
    with open('./data/semantic_2d_data.json') as json_file:
        dict = json.load(json_file)
        semantic_object = semantic_2d_data_from_dict(dict)

        # reverse back to dict
        reversedDict = semantic_2d_data_to_dict(semantic_object);

        diff = {k: reversedDict[k] for k in set(reversedDict) - set(dict)}
        # result the same dictionary when convert back
        assert len(diff) == 0


