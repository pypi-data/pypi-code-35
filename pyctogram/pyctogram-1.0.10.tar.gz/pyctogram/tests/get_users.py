from pyctogram.instagram_client.relations import base
from pyctogram.tests import account

if __name__ == '__main__':
    victim = 'sova_timofei'
    proxies = [
        {'http': 'http://proxy_user:proxy_password@185.252.147.201:4128',
         'https': 'https://proxy_user:proxy_password@185.252.147.201:4128'},

        {'http': 'http://proxy_user:proxy_password@185.252.147.193:4128',
         'https': 'https://proxy_user:proxy_password@185.252.147.193:4128'},

        {'http': 'http://proxy_user:proxy_password@185.252.147.192:4128',
         'https': 'https://proxy_user:proxy_password@185.252.147.192:4128'},

        {'http': 'http://proxy_user:proxy_password@185.252.147.185:4128',
         'https': 'https://proxy_user:proxy_password@185.252.147.185:4128'},

        {'http': 'http://proxy_user:proxy_password@185.252.147.182:4128',
         'https': 'https://proxy_user:proxy_password@185.252.147.182:4128'},

        {'http': 'http://proxy_user:proxy_password@185.252.147.181:4128',
         'https': 'https://proxy_user:proxy_password@185.252.147.181:4128'},

        {'http': 'http://proxy_user:proxy_password@185.252.147.180:4128',
         'https': 'https://proxy_user:proxy_password@185.252.147.180:4128'},

        {'http': 'http://proxy_user:proxy_password@185.252.147.179:4128',
         'https': 'https://proxy_user:proxy_password@185.252.147.179:4128'},

        {'http': 'http://proxy_user:proxy_password@185.252.147.171:4128',
         'https': 'https://proxy_user:proxy_password@185.252.147.171:4128'},
    ]
    counter = 0
    for user in base.get_users(account.username, account.password, victim, proxies=proxies):
        counter += 1
        print(counter)
        print(user)
