import requests
import json
import os
import osrs_net

from osrs_net.util.file_io import write, create_directory


API_URL = 'https://storage.googleapis.com/osbuddy-exchange/summary.json'


def get_item_data():
    response = requests.get(API_URL)
    return response.json()


def create_item_database(item_data):
    database = dict()
    for key in list(item_data):
        name = item_data[key]['name']
        item_id = item_data[key]['id']
        members = item_data[key]['members']
        item_dict = {'name': name, 'id': item_id, 'members': members}
        database[name.lower()] = item_dict

    return database


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    default_path = os.path.join(os.path.dirname(osrs_net.__file__), 'resources', 'items.json')
    parser.add_argument('-o', '--output_file', default=default_path, help='Path to output file')
    args = parser.parse_args()

    out_file = args.output_file

    data = get_item_data()
    database = create_item_database(data)

    create_directory(out_file)
    write(json.dumps(database, indent=4), out_file)




