from fortnite_easy_api import user_search, weapon_search

pistol = weapon_search.id('87043ca-bdac980-7280920-cbf544a')
print(pistol['name'])
print(pistol['rarity'])
