import requests
from osrs_net.item import Item


class GrandExchange:

    @staticmethod
    def item(id_num):
        url = 'https://rsbuddy.com/exchange/graphs/1440/{}.json'.format(id_num)
        data = requests.get(url).json()
        current_item = data[len(data) - 1]
        price_data = {
            'price': current_item['overallPrice'],
            'buyPrice': current_item['buyingPrice'],
            'sellPrice': current_item['sellingPrice']
        }

        result = Item(id_num, Item.id_to_name(id_num), price_data)
        return result
