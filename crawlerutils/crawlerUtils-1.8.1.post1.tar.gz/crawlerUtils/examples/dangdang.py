from ..utils import Get
import re


__all__ = ["runDangdangBook"]


start_urls = []
for x in range(100):
    url = "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-year-2018-0-1-{}".format(
        x+1)
    start_urls.append(url)


async def DangdangBook():
    ''' 从当当图书获取前3页书籍的信息 '''
    while start_urls:
        url = start_urls.pop(0)
        html = await Get(url, encoding="gb18030").ahtml
        ul = html.find("ul.bang_list", first=True)
        if ul:
            books = ul.find("li")
            for book in books:
                iterm = {}
                iterm["name"] = book.find("div.name", first=True).text
                iterm["author"] = book.find("div.publisher_info", first=True).text
                iterm["price"] = book.find("span.price_n", first=True).text
                print(iterm)


def runDangdangBook(number_asynchronous=3):
    ''' 从当当图书获取前3页书籍的信息 '''
    Get.asyncRun(DangdangBook, number_asynchronous)
