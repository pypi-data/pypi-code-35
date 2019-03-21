from fortnite_easy_api import user_search, weapon_search

matches = user_search.get_matches('98be824f0bc644f798643f3d2ee23980')
for match in matches:
    print(match['playlist'])