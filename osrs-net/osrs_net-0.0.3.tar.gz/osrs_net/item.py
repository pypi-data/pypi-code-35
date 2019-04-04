import json
import os
import osrs_net

from osrs_net.util.file_io import read


class Item:
    def __init__(self, item_id, item_name, price_data):
        self.id = item_id
        self.name = item_name
        self.price_data = price_data

    @staticmethod
    def _get_item_data():
        base_dir = os.path.dirname(osrs_net.__file__)
        filepath = os.path.join(base_dir, 'resources', 'items.json')
        text = read(filepath)
        return json.loads(text)

    @staticmethod
    def get_ids(name):
        item_data = Item._get_item_data()
        try:
            return item_data[name.lower()]['id']
        except KeyError:
            matches = []
            for item in item_data:
                if name in item:
                    matches.append(item_data[item]['id'])
            return matches

    @staticmethod
    def id_to_name(id_num):
        data = Item._get_item_data()
        for item in data:
            if data[item]['id'] == id_num:
                return data[item]['name']
        return None
