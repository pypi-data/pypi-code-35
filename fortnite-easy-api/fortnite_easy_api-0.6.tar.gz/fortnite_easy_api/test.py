from fortnite_easy_api import user_search

gwet_solo = user_search.getstats('xd gwet', 'pc')['duo']
print(gwet_solo['wins'])
