import asyncio
from multiprocessing import Process, cpu_count
import os
import requests
from bs4 import BeautifulSoup
import numpy
import csv

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}


async def getSoup(url):
    r = requests.get(url, headers=headers)
    r.encoding = "gb18030"
    soup = BeautifulSoup(r.text, "html.parser")
    return soup


def process_start(coroutine_num, url_list):
    tasks = []
    loop = asyncio.get_event_loop()
    for url in url_list:
        if url:
            tasks.append(asyncio.ensure_future(hello(url)))
    loop.run_until_complete(asyncio.wait(tasks))


def task_start(url_list):
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
        data = numpy.array(url_list).reshape(coroutine_num + 1, cpu_num)
        for i in range(cpu_num):
            url_list = data[:, i]
            p = Process(target=process_start, args=(coroutine_num, url_list,))
            processes.append(p)
        for p in processes:
            p.start()


async def hello(url):
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


def multiProcessAsync(url_list, csv_name="crawlerUtils.csv"):
    with open(csv_name, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["书名", "作者", "价格"])
    task_start(url_list)


# url_list = []
# for x in range(1, 101):
#     url_ = 'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-year-2018-0-1-' + \
#            str(x)
#     url_list.append(url_)
#
#
# multiProcessAsync(url_list)
