import requests
from osrs_net.hiscores.skill import Skill
from osrs_net.hiscores.account import Account

skills = ['total', 'attack', 'defence', 'strength', 'hitpoints', 'ranged', 'prayer', 'magic', 'cooking', 'woodcutting',
          'fletching', 'fishing', 'firemaking', 'crafting', 'smithing', 'mining', 'herblore', 'agility', 'thieving',
          'slayer', 'farming', 'runecraft', 'hunter', 'construction']


def lookup(player_name):
    player_stats = dict()
    url = f'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={player_name}'
    text = requests.get(url).text
    text = text.split('\n')

    for i, skill in enumerate(skills):
        curr_text = text[i].split(',')
        rank, level, exp = curr_text
        curr_skill = Skill(skill, int(level), int(exp), int(rank))
        player_stats[skill] = curr_skill

    return Account(player_name, player_stats)
