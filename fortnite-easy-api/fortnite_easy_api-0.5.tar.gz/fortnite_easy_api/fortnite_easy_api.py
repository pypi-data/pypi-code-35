import requests
import json

class shop():
    def get(language):
        if not language:
            return False
        response = requests.get("https://fortnite-public-api.theapinetwork.com/prod09/store/get?language=" + language)
        rawdata = response.content.decode()
        data = json.loads(rawdata)
        items = data['items']
        final_result = []
        for item in items:
            identifier = item['itemid']
            inner_item = item['item']
            if '(BUNDLE)' in item['name']:
                name = item['name'].replace(' (BUNDLE)','')
            else:
                name = item['name']
            if inner_item['type'] == 'bundle' or inner_item['type'] == 'outfit':
                kind = 'outfit'
            else:
                kind = inner_item['type']
            if item['featured'] == 1:
                featured = True
            else:
                featured = False
            cost = item['cost']
            rarity = inner_item['rarity']
            images = inner_item['images']
            image_transparent = images['transparent']
            image_background = images['background']
            image_info = images['information']
            found = True
            result = {
                'identifier': identifier,
                'name': name,
                'type': kind,
                'rarity': rarity,
                'cost': cost,
                'featured': featured,
                'image_transparent': image_transparent,
                'image_background': image_background,
                'image_info': image_info
            }
            final_result.append(result)
        return final_result

class user_search():
    def getid(username):
        if not username:
            return False
        response = requests.get("https://fortnite-public-api.theapinetwork.com/prod09/users/id?username=" + username.lower())
        rawdata = response.content.decode()
        data = json.loads(rawdata)
        id = data['uid']
        return id
    def getstats(username, platform):
        platform = platform.lower()
        if not username:
            return False
        url = 'https://api.fortnitetracker.com/v1/profile/' + platform.lower() + '/' + username.lower()
        response = requests.get(url, headers={'TRN-Api-Key': '8987093d-e29d-40cf-b77b-1d518b6858d5'})
        rawdata = response.content.decode()
        data = json.loads(rawdata)
        stats = data['stats']
        solo = stats['p2']
        solo_wins_raw = solo['top1']
        solo_wins = solo_wins_raw['displayValue']
        solo_kills_raw = solo['kills']
        solo_kills = solo_kills_raw['displayValue']
        solo_win_percentage_raw = solo['winRatio']
        solo_win_percentage = solo_win_percentage_raw['displayValue']
        solo_kd_raw = solo['kd']
        solo_kd = solo_kd_raw['displayValue']
        solo_top10_raw = solo['top10']
        solo_top10 = solo_top10_raw['displayValue']
        solo_kills_per_match_raw = solo['kpg']
        solo_kills_per_match = solo_kills_per_match_raw['displayValue']
        solo_top25_raw = solo['top25']
        solo_top25 = solo_top25_raw['displayValue']
        duo = stats['p10']
        duo_wins_raw = duo['top1']
        duo_wins = duo_wins_raw['displayValue']
        duo_kills_raw = duo['kills']
        duo_kills = duo_kills_raw['displayValue']
        duo_win_percentage_raw = duo['winRatio']
        duo_win_percentage = duo_win_percentage_raw['displayValue']
        duo_kd_raw = duo['kd']
        duo_kd = duo_kd_raw['displayValue']
        duo_top5_raw = duo['top5']
        duo_top5 = duo_top5_raw['displayValue']
        duo_kills_per_match_raw = duo['kpg']
        duo_kills_per_match = duo_kills_per_match_raw['displayValue']
        duo_top12_raw = duo['top12']
        duo_top12 = duo_top12_raw['displayValue']
        squad = stats['p9']
        squad_wins_raw = squad['top1']
        squad_wins = squad_wins_raw['displayValue']
        squad_kills_raw = squad['kills']
        squad_kills = squad_kills_raw['displayValue']
        squad_win_percentage_raw = squad['winRatio']
        squad_win_percentage = squad_win_percentage_raw['displayValue']
        squad_kd_raw = squad['kd']
        squad_kd = squad_kd_raw['displayValue']
        squad_top3_raw = squad['top3']
        squad_top3 = squad_top3_raw['displayValue']
        squad_kills_per_match_raw = squad['kpg']
        squad_kills_per_match = squad_kills_per_match_raw['displayValue']
        squad_top6_raw = squad['top6']
        squad_top6 = squad_top6_raw['displayValue']
        result = {
            'solo': {
                'wins': solo_wins,
                'kills': solo_kills,
                'winratio': solo_win_percentage,
                'kd': solo_kd,
                'kpm': solo_kills_per_match,
                'top10': solo_top10,
                'top25': solo_top25
            },
            'duo': {
                'wins': duo_wins,
                'kills': duo_kills,
                'winratio': duo_win_percentage,
                'kd': duo_kd,
                'kpm': duo_kills_per_match,
                'top5': duo_top5,
                'top12': duo_top12
            },
            'squad': {
                'wins': squad_wins,
                'kills': squad_kills,
                'winratio': squad_win_percentage,
                'kd': squad_kd,
                'kpm': squad_kills_per_match,
                'top3': squad_top3,
                'top6': squad_top6
            }
        }
        return result

class item_search():
    def name(name):
        response = requests.get("https://fortnite-public-api.theapinetwork.com/prod09/items/list")
        rawdata = response.content.decode()
        items = json.loads(rawdata)
        if not name:
            return False
        found = False
        for item in items:
            if name.lower() == item['name'].lower() or name.lower() + ' (bundle)' == item['name'].lower():
                identifier = item['identifier']
                if '(BUNDLE)' in item['name']:
                    name = item['name'].replace(' (BUNDLE)','')
                else:
                    name = item['name']
                if item['type'] == 'bundle' or item['type'] == 'outfit':
                    kind = 'outfit'
                else:
                    kind = item['type']
                cost = item['cost']
                description = item['description']
                rarity = item['rarity']
                images = item['images']
                image_transparent = images['transparent']
                image_background = images['background']
                image_info = images['info']
                found = True
                result = {
                    'identifier': identifier,
                    'name': name,
                    'type': kind,
                    'rarity': rarity,
                    'cost': cost,
                    'description': description,
                    'image_transparent': image_transparent,
                    'image_background': image_background,
                    'image_info': image_info
                }
                return result
                break
            else:
                continue
        if found == True:
            pass
        else:
            return False
    def identefier(identefier):
        response = requests.get("https://fortnite-public-api.theapinetwork.com/prod09/items/list")
        rawdata = response.content.decode()
        items = json.loads(rawdata)
        if not identefier:
            return False
        else:
            pass
        for item in items:
            found = False
            if identefier == item['identifier']:
                identifier = item['identifier']
                if '(BUNDLE)' in item['name']:
                    name = item['name'].replace(' (BUNDLE)','')
                else:
                    name = item['name']
                if item['type'] == 'bundle' or item['type'] == 'outfit':
                    kind = 'outfit'
                else:
                    kind = item['type']
                cost = item['cost']
                description = item['description']
                rarity = item['rarity']
                images = item['images']
                image_transparent = images['transparent']
                image_background = images['background']
                image_info = images['info']
                found = True
                result = {
                    'identifier': identifier,
                    'name': name,
                    'type': kind,
                    'rarity': rarity,
                    'cost': cost,
                    'description': description,
                    'image_transparent': image_transparent,
                    'image_background': image_background,
                    'image_info': image_info
                }
                return result
                break
            else:
                continue
        if found == True:
            pass
        else:
            return False
    def rarity(rarity):
        response = requests.get("https://fortnite-public-api.theapinetwork.com/prod09/items/list")
        rawdata = response.content.decode()
        items = json.loads(rawdata)
        if not rarity:
            return False
        else:
            pass
        if 'legendary' not in rarity and 'epic' not in rarity and 'rare' not in rarity and 'uncommon' not in rarity and 'common' not in rarity:
            return False
        else:
            pass
        final_result = []
        found = False
        for item in items:
            if rarity == item['rarity']:
                identifier = item['identifier']
                if '(BUNDLE)' in item['name']:
                    name = item['name'].replace(' (BUNDLE)','')
                else:
                    name = item['name']
                if item['type'] == 'bundle' or item['type'] == 'outfit':
                    kind = 'outfit'
                else:
                    kind = item['type']
                cost = item['cost']
                description = item['description']
                rarity = item['rarity']
                images = item['images']
                image_transparent = images['transparent']
                image_background = images['background']
                image_info = images['info']
                found = True
                result = {
                    'identifier': identifier,
                    'name': name,
                    'type': kind,
                    'rarity': rarity,
                    'cost': cost,
                    'description': description,
                    'image_transparent': image_transparent,
                    'image_background': image_background,
                    'image_info': image_info
                }
                final_result.append(result)
            else:
                continue
        return final_result
        if found == True:
            pass
        else:
            return False
    def cost(cost):
        response = requests.get("https://fortnite-public-api.theapinetwork.com/prod09/items/list")
        rawdata = response.content.decode()
        items = json.loads(rawdata)
        if not cost:
            return False
        else:
            pass
        final_result = []
        found = False
        for item in items:
            if cost == item['cost']:
                identifier = item['identifier']
                if '(BUNDLE)' in item['name']:
                    name = item['name'].replace(' (BUNDLE)','')
                else:
                    name = item['name']
                if item['type'] == 'bundle' or item['type'] == 'outfit':
                    kind = 'outfit'
                else:
                    kind = item['type']
                cost = item['cost']
                description = item['description']
                rarity = item['rarity']
                images = item['images']
                image_transparent = images['transparent']
                image_background = images['background']
                image_info = images['info']
                found = True
                result = {
                    'identifier': identifier,
                    'name': name,
                    'type': kind,
                    'rarity': rarity,
                    'cost': cost,
                    'description': description,
                    'image_transparent': image_transparent,
                    'image_background': image_background,
                    'image_info': image_info
                }
                final_result.append(result)
            else:
                continue
        return final_result
        if found == True:
            pass
        else:
            return False