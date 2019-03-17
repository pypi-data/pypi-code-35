import json
import os
import html

from .models import Item
from .models import Weapon
from .models import Armour
from .models import Prophecy
from .models import Gem
from .models import DivCard
from .models import ItemDrop
from .models import Requirements
from .utils import reg
from bs4 import BeautifulSoup as BS


class ClientBase:
    _dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'valid_filters.json')
    with open(_dir) as f:
        filters = json.load(f)

    valid_item_filters = filters['item']

    valid_gem_filters = filters['gem']

    valid_gem_level_filters = filters['gem_levels']

    valid_weapon_filters = filters['weapon']

    valid_armour_filters = filters['armour']

    #No other way to tell if an item is an elder or shaper unique other than locally storing it at the moment
    shaper_items = filters['shaper']

    elder_items = filters['elder']

    operators = ['>', '<', '=']

    @staticmethod
    def extract_cargoquery(data):
        extracted = []
        #if 'cargoquery' not in data:
        #    print(data)
        for item in data['cargoquery']:
            extracted.append(item['title'])
        return extracted

    @staticmethod
    def bool_(val):
        return bool(int(val))

    def _param_gen(self, where, filters):
        where_params = []
        for key, val in where.items():
            #if key.lower() not in filters:
             #  print(f"WARNING: {key} is not a valid filter, continuing without it.")
              # continue
            if 'skill_id' in filters and key == 'name':
                key = 'skill_levels._pageName'
            if val[0] in self.operators:
                where_params.append(f'{key}{val}')
            else:
                where_params.append(f'{key} LIKE "{val}"')
        where_str = " AND ".join(where_params)
        return where_str

    def gem_param_gen(self, where):

        where_str = self._param_gen(where, self.valid_gem_filters)
        params = {
            'tables': "skill_levels,skill,items,skill_gems",
            'join_on': "skill_levels._pageName=skill._pageName,skill_levels._pageName=items._pageName,skill_levels._pageName=skill_gems._pageName",
            'fields': f"{','.join(self.valid_gem_filters)},skill_levels._pageName=name,items.inventory_icon, skill_gems.gem_tags, items.tags",
            'where': where_str,
            'group_by': 'name'
        }
        return params

    def item_param_gen(self, where, limit):
        where_str = self._param_gen(where, self.valid_item_filters)
        params = {
            'tables': "items",
            'fields': f"{','.join(self.valid_item_filters)},_pageName=name",
            'where': where_str
        }
        if limit:
            params['limit'] = str(limit)
        return params
    @staticmethod
    def get_image_url(filename, req):
        query_url = "https://pathofexile.gamepedia.com/api.php?action=query"
        param = {
                'titles': filename,
                'prop': 'imageinfo&',
                'iiprop': 'url'
            }
        dat = req(query_url, param)
        ic = dat['query']['pages'][list(dat['query']['pages'].keys())[0]].get('imageinfo', None)
        return ic[0]['url'] if ic else ic

    def get_gems(self, where: dict, req, url):
        params = self.gem_param_gen(where)
        data = req(url, params=params)
        result_list = self.extract_cargoquery(data)
        final_list = []
        for gem in result_list:
            vendor_params = {
                'tables': "vendor_rewards",
                'fields': "act,classes",
                'where': f'''reward="{gem['name']}"'''
            }
            vendors_raw = req(url, params=vendor_params)
            vendors = self.extract_cargoquery(vendors_raw)
            for act in vendors:
                act['classes'] = act['classes'].replace('�', ', ')
            stats_params = {
                'tables': "skill_levels",
                'fields': ','.join(self.valid_gem_level_filters),
                'where': f'''_pageName="{gem['name']}"'''
            }
            stats_raw = req(url, params=stats_params)
            stats_list = self.extract_cargoquery(stats_raw)
            stats = {}
            #print(gem['has percentage mana cost'], gem['has reservation mana cost'])
            if int(gem['has percentage mana cost']) or int(gem['has reservation mana cost']):
                aura = True
            else:
                aura = False
            for stats_dict in stats_list:
                stats[int(stats_dict['level'])] = stats_dict
            requirements = Requirements(stats[1]['dexterity requirement'], stats[1]['strength requirement'],
                                        stats[1]['intelligence requirement'], stats[1]['level requirement'])
            inv_icon = self.get_image_url(gem['inventory icon'], req)
            if gem['skill icon']:
                skill_icon = self.get_image_url(gem['skill icon'], req)
            else:
                skill_icon = None
            gem = Gem(gem["skill id"], gem["cast time"], gem["description"],
                      gem["name"], gem["item class restriction"], gem["stat text"],
                      gem["quality stat text"], gem["radius"],
                      gem["radius description"], gem["radius secondary"],
                      gem["radius secondary description"], gem["radius tertiary"],
                      gem["radius tertiary description"], skill_icon,
                      gem["skill screenshot"], inv_icon, gem['gem tags'], gem['tags'], stats,
                      aura, vendors, requirements)
            final_list.append(gem)
        return final_list
    def item_list_gen(self, data, req=None, url=None, where=None):
        result_list = self.extract_cargoquery(data)
        final_list = []
        for item in result_list:
            shaper = False
            elder = False
            if item['name'] in self.shaper_items:
                shaper = True
            if item['name'] in self.elder_items:
                elder = True
            if 'weapon' in item['tags'].split(','):
                params = {
                    'tables': 'weapons',
                    'fields': ','.join(self.valid_weapon_filters),
                    'where': f'_pageName="{item["name"]}"'
                }
                data = req(url, params)
                stats = self.extract_cargoquery(data)[0]
                i = Weapon
            elif 'armour' in item['tags'].split(','):
                if 'shield' in item['tags'].split(','):
                    params = {
                        'tables': 'armours, shields',
                        'join_on': 'armours._pageName=shields._pageName',
                        'fields': f"{','.join(self.valid_armour_filters)},block_range_average",
                        'where': f'shields._pageName="{item["name"]}"'
                    }
                else:
                    params = {
                        'tables': 'armours',
                        'fields': ','.join(self.valid_armour_filters),
                        'where': f'_pageName="{item["name"]}"'
                    }
                #Only extra stat a shield has from other armours is the block chance
                #So I didn't add it to a filter key and blah blah
                data = req(url, params)
                #print(data)
                stats = self.extract_cargoquery(data)[0]
                i = Armour
            elif 'gem' in item['tags'].split(','):
                current_item = self.get_gems({'name': item['name']}, req, url)[0]
            elif 'divination_card' in item['tags'].split(','):
                params ={
                    'tables': 'divination_cards, stackables',
                    'join_on': 'divination_cards._pageName=stackables._pageName',
                    'fields': 'card_art, stack_size',
                    'where': f'divination_cards._pageName="{item["name"]}"'
                }
                data = self.extract_cargoquery(req(url, params))[0]
                card_art = self.get_image_url(data['card art'], req)
                soup = BS(html.unescape(item['html']))
                div_data = soup.select_one('span.divicard-reward span span')
                reward_flavour = div_data.attrs['class'][1][1:]
                if reward_flavour == 'currency':
                    reward_flavour = 'normal'
                matches = reg.findall(div_data.text)
                if len(matches)>1:
                    reward = matches[1].split('|')[1].strip(']]')
                elif len(matches) == 1:
                    reward = matches[0].split('|')[1].strip(']]')
                else:
                    reward = div_data.text
                stats = {'card_art': card_art,
                         'stack_size': data['stack size'],
                         'reward_flavor': reward_flavour,
                         'reward': reward}
                i = DivCard
            elif item['base item'] == "Prophecy":
                params = {
                    'tables': 'prophecies',
                    'fields': 'objective, prediction_text, seal_cost',
                    'where': f'_pageName="{item["name"]}"'
                }
                data = req(url, params)
                stats = self.extract_cargoquery(data)[0]
                i = Prophecy
            else:
                stats = None
                i = Item
            #print(item['inventory icon'])
            if 'gem' not in item['tags'].split(','):
                print(item['inventory icon'])
                image_url = self.get_image_url(item['inventory icon'], req)
                drops = ItemDrop(item['drop enabled'], item['drop level'],
                                 item['drop level maximum'], item['drop leagues'],
                                 item['drop areas'], item['drop text'])
                requirements = Requirements(item['required dexterity'], item['required strength'],
                                   item['required intelligence'], item['required level'])

                current_item = i(item['base item'], item['class'], item['name'],
                                 item['rarity'], (item['size x'], item['size y']), drops, requirements,
                                 item['flavour text'], item['help text'], self.bool_(item['is corrupted']),
                                 self.bool_(item['is relic']), item['alternate art inventory icons'],
                                 item['quality'], item['implicit stat text'], item['explicit stat text'],
                                 item['tags'], image_url,shaper, elder, stats)

            final_list.append(current_item)
        return final_list