from bs4 import BeautifulSoup
import requests
from .HtmlParser import SearchOptionParser, ProductListParser
import threading
import time

class StructuredProductCrawler:
    headers = {
                'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            }
    def __init__(self):
        self.index_url = "https://structurednotes-announce.tdcc.com.tw/Snoteanc/apps/bas/BAS210.jsp"
        self.product_url = self.index_url + "?fundUuid={fund_id}"
        self.max_pages = {}
        self.products = []
        self.queries = [
            "AGENT_CODE={agent}",
            "ISSUE_ORG_UUID=",
            "SALE_ORG_UUID=",
            "FUND_LINK_TYPE=",
            "FUND_CURR=",
            "FUND_TYPE=",
            "FUND_STOP_DATE=",
            "agentDateStart=",
            "agentDateEnd=",
            "action=Q",
            "LAST_ORDER_BY=FUND_NAME",
            "ORDER_BY=",
            "IS_ASC=",
            "currentPage={page_number}"
        ]
        self.base_query_url = self.index_url + "?" + "&".join(self.queries)

    def _get_master_agents(self):
        response = requests.get(self.index_url, headers=self.headers)
        parser = SearchOptionParser(response)
        return parser.get_master_agents()
    def _get_max_page(self, url, agent):
        print("max_page get {}".format(url))
        response = requests.get(url,headers=self.headers)
        print("max_page rec {}".format(url))
        max_page_number = ProductListParser(response).get_max_list_page()
        self.max_pages[agent]=max_page_number
    def _get_max_pages_for_all_master_agents(self):
        agents = list(self._get_master_agents().keys())
        threads = []
        for agent in agents:
            first_page_url = self.base_query_url.format(agent=agent, page_number =1)
            thread = threading.Thread(target = self._get_max_page, args=(first_page_url, agent,))
            thread.start()
            time.sleep(0.5)
            threads.append(thread)
        for thread in threads:
            thread.join()
        return self.max_pages
    def _get_all_page_urls(self):
        max_pages = self._get_max_pages_for_all_master_agents()
        urls = []
        for agent, max_page in max_pages.items():
            agent_urls = [self.base_query_url.format(agent=agent, page_number =x) for x in range(1,max_page+1)]
            urls += agent_urls
        return urls
    def _get_product_list(self, url):
        print("getting {}".format(url))
        response = requests.get(url, headers=self.headers)
        print("received {}".format(url))
        parser = ProductListParser(response)
        product_list = parser.get_product_list()

        self.products += product_list
    def crawl(self):
        threads =[]
        page_urls = self._get_all_page_urls()
        for index, url in enumerate(page_urls):
            thread = threading.Thread(target = self._get_product_list, args=(url,))
            thread.start()
            time.sleep(0.5)
            threads.append(thread)
            if index%20==0:
                time.sleep(1)
        for thread in threads:
            thread.join()
        return self.products
