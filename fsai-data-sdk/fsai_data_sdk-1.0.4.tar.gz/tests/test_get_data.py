# coding: utf-8
import os


from fsai import DatasetService
from fsai.services.data_object.DynamicObjectData import DynamicObjectData
from fsai.services.data_object.Semantic2DData import semantic_2d_data_from_dict

try:
    api_key = os.environ['FORESIGHT_API_KEY']
    secret_key = os.environ['FORESIGHT_SECRET_KEY']
except KeyError:
    raise Exception("FORESIGHT_API_KEY and FORESIGHT_SECRET_KEY environment keys are required to run test")


def test_get_data_all_layers_ok():
    portal = DatasetService(api_key, secret_key)
    result = portal.get_data_at(lng=-122.1598309, lat=37.4358347, radius=2000, layers=["SEMANTIC_2D", "DYNAMIC_OBJECTS"])
    print(len(result))
    sample_dataset = result[0]
    print(sample_dataset)
    print(sample_dataset.layers.semantic_2d.get())

    # DYNAMIC OBJECT
    "Get raw JSON data"
    dynamic_object_json_data = sample_dataset.layers.dynamic_objects[0].get()

    "Get parsed data objects"
    dynamic_object_data = DynamicObjectData.from_json(dynamic_object_json_data)
    for object in dynamic_object_data.collections[0].objects:
        print(object.get_moving_distance())

    # SEMANTIC MAP
    "Get semantic map open drive JSON data"
    semantic_2d_data = sample_dataset.layers.semantic_2d.get()
    "Get parsed data objects"
    semantic_object = semantic_2d_data_from_dict(semantic_2d_data)
    # empty to get sum length
    total_length = 0
    # loop through all the roads and compute the total length
    for road in semantic_object.road:
        total_length = total_length + road.attributes.length
    print('\n')
    print(total_length)

