import re

import requests
from bs4 import BeautifulSoup
from sekg.util.url_util import URLUtil

# re connect
from sekg.wiki.WikiDataItem import WikiDataItem


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


class WikiTool:
    def __init__(self, domain_name_set, use_proxies=False, max_candidate_num=3):
        self.title_2_wiki = dict()
        self.domain_name_set = domain_name_set
        self.use_proxies = use_proxies
        self.max_candidate_num = max_candidate_num

    def get_wiki_id(self, wd_url):
        return (str(wd_url).split('/'))[-1]

    def search(self):
        search_result = []
        for title in self.domain_name_set:
            search_result.append(self.get_wd_by_title(title))
        return search_result

    @conn_try_again
    def get_wd_by_title(self, title):
        wiki_id_list = []
        wikipedia_url_list = []
        wikipedia_title_list = []
        if self.use_proxies:
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
                        wd_id = self.get_wiki_id(wd_href)
                        wiki_id_list.append(wd_id)
                        wikipedia_url_list.append(m.url)
                        wikipedia_title_list.append(URLUtil.parse_url_to_title(m.url))
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
                        if i == self.max_candidate_num - 1:
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
                                        wd_id = self.get_wiki_id(wd_href)
                                        if len(wd_id) > 1 and wd_id[0] == "Q":
                                            wiki_id_list.append(wd_id)
                                            wikipedia_url_list.append(redirect_m.url)
                                            wikipedia_title_list.append(URLUtil.parse_url_to_title(redirect_m.url))
                                            break
                else:
                    print("fail to find")
            wd_item_list = []
            for wiki_id in wiki_id_list:
                wd_item = WikiDataItem(wiki_id)
                if wd_item:
                    wd_item_list.append(wd_item)

            return wiki_id_list, wikipedia_url_list, wikipedia_title_list, wd_item_list
        except Exception as e:
            print(e)


# if __name__ == '__main__':
#     test_set = set()
#     test_set.add("Peer alarm")
#     wiki_tool = WikiTool(domain_name_set=test_set, use_proxies=False, max_candidate_num=5)
#     result = wiki_tool.search()
#     print(result)
