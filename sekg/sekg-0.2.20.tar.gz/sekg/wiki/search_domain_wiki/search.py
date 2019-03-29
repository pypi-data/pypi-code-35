import re

import requests
from bs4 import BeautifulSoup


def get_wiki_id(wd_url):
    return (str(wd_url).split('/'))[-1]


# re connect
def conn_try_again(function):
    retries = 5
    # retry time
    count = {"num": retries}

    def wrapped(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as err:
            if count['num'] < 2:
                count['num'] += 1
                return wrapped(*args, **kwargs)
            else:
                raise Exception(err)

    return wrapped


@conn_try_again
def get_wd_by_title(title, use_proxies=False, max_candidate_num=1):
    if use_proxies:
        proxies = {"http": "127.0.0.1:1080", "https": "127.0.0.1:1080"}
    else:
        proxies = None
    try:
        base_url = "https://en.wikipedia.org"
        url = base_url + "/wiki/" + title
        m = requests.get(url, proxies=proxies)
        if m.status_code == 200:
            soup = BeautifulSoup(m.content, "lxml")
            wikidata_node_list = soup.select('#t-wikibase')
            if wikidata_node_list:
                wikidata_node = wikidata_node_list[0]
                for link in wikidata_node.findAll('a', attrs={'href': re.compile("^https://")}):
                    wd_href = link.get('href')
                    return get_wiki_id(wd_href)
            else:
                print("wikidata_node_list is empty")
        else:
            new_title = title.replace(" ", "+")
            url = "https://en.wikipedia.org/w/index.php?search=" + new_title + "&title=Special%3ASearch&go=Go"
            m = requests.get(url, proxies=proxies)
            if m.status_code == 200:
                soup = BeautifulSoup(m.content, "lxml")
                candidate_list = soup.select('.mw-search-result-heading')
                for i, candidate in enumerate(candidate_list):
                    if i == max_candidate_num:
                        break
                    for link in candidate.findAll('a', attrs={'href': re.compile("^/wiki/")}):
                        wd_href = link.get('href')
                        redirect_url = base_url + wd_href
                        redirect_m = requests.get(redirect_url, proxies=proxies)
                        if redirect_m.status_code == 200:
                            soup = BeautifulSoup(redirect_m.content, "lxml")
                            wikidata_node_list = soup.select('#t-wikibase')
                            if wikidata_node_list:
                                wikidata_node = wikidata_node_list[0]
                                for link in wikidata_node.findAll('a', attrs={'href': re.compile("^https://")}):
                                    wd_href = link.get('href')
                                    return get_wiki_id(wd_href)
            else:
                print("fail to find")
    except Exception as e:
        print(e)
