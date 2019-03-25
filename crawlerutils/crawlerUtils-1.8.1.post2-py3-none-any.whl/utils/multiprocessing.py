import asyncio
from multiprocessing import Process, cpu_count
import os
import requests
from bs4 import BeautifulSoup
import numpy
import csv


class MultiProcessAsync():
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    session = requests.session()

    @classmethod
    async def getSoup(self, url):
        r = requests.get(url, headers=self.headers)
        r.encoding = "gb18030"
        soup = BeautifulSoup(r.text, "html.parser")
        return soup

    @classmethod
    async def hello(self, url):
        item = {}
        print('start:{}  pid:{}'.format(url, os.getpid()))
        soup = await getSoup(url)
        ul = soup.find('ul', {"class": "bang_list"})
        if ul:
            elements = ul.find_all('li')
            for element in elements:
                item['name'] = element.find(
                    'div', class_="name").find('a')['title']
                item['author'] = element.find('div', class_="publisher_info").text
                item['price'] = element.find('div', class_="price").find(
                    'span', class_="price_n").text

                with open("123.csv", "a", newline="", encoding="utf-8-sig") as f:
                    writer = csv.writer(f)
                    writer.writerow([item["name"], item["author"], item["price"]])

                print(item)
            print('end:{}  pid:{}'.format(url, os.getpid()))

    @classmethod
    def process_start(self, coroutine_num, url_list):
        tasks = []
        loop = asyncio.get_event_loop()
        for url in url_list:
            if url:
                tasks.append(asyncio.ensure_future(hello(url)))
        loop.run_until_complete(asyncio.wait(tasks))

    @classmethod
    def task_start(self, url_list):
        # 进程池进程数量
        cpu_num = cpu_count()
        if len(url_list) <= cpu_num:
            processes = []
            for i in range(len(url_list)):
                url = url_list[i]
                url_list = [url]
                p = Process(target=process_start, args=(1, url_list,))
                processes.append(p)
            for p in processes:
                p.start()
        else:
            coroutine_num = len(url_list) // cpu_num
            processes = []
            url_list += [""] * (cpu_num * (coroutine_num + 1) - len(url_list))
            data = numpy.array(url_list).reshape(coroutine_num+1, cpu_num)
            for i in range(cpu_num):
                url_list = data[:, i]
                p = Process(target=process_start, args=(coroutine_num, url_list,))
                processes.append(p)
            for p in processes:
                p.start()

    @classmethod
    def multiProcessAsync(self, url_list, title_list, csv_name="crawlerUtils.csv", encoding="utf-8"):
        with open(csv_name, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(title_list)
        task_start(url_list)
